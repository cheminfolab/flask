"""Phase 4: pagination, query counts, health, throttling, logout, request ids, logging."""
import json
import logging
from io import StringIO
from unittest import mock

from django.db import connection
from django.test import override_settings
from django.test.utils import CaptureQueriesContext
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.throttling import ScopedRateThrottle

from accounts.models import Member, Role, Supplier, WorkingGroup
from chemicals.models import Component, Compound, Container, Substance, Unit
from projects.models import Experiment, ExperimentShare, Project

from .log import JsonFormatter, RequestIdFilter


class PaginationTests(APITestCase):
    def setUp(self):
        self.user = Member.objects.create_user(email='user@example.org', password='x')
        self.client.force_authenticate(self.user)
        Unit.objects.bulk_create(Unit(name=f'unit {i}', symbol=f'u{i:03}') for i in range(120))

    def test_lists_are_paginated_with_stable_order(self):
        first = self.client.get('/api/units/').data
        second = self.client.get('/api/units/?page=2').data

        self.assertEqual(first['count'], 120)
        self.assertEqual(len(first['results']), 50)
        self.assertIsNotNone(first['next'])
        ids = [u['id'] for u in first['results']] + [u['id'] for u in second['results']]
        self.assertEqual(ids, sorted(ids))
        self.assertEqual(len(set(ids)), 100)  # no overlap between pages

    def test_page_size_is_capped(self):
        Unit.objects.bulk_create(Unit(name=f'more {i}', symbol=f'm{i:03}') for i in range(450))
        response = self.client.get('/api/units/?page_size=10000')
        self.assertEqual(len(response.data['results']), 500)

    def test_page_out_of_range_is_404(self):
        self.assertEqual(self.client.get('/api/units/?page=99').status_code, status.HTTP_404_NOT_FOUND)


class QueryCountTests(APITestCase):
    """List endpoints must not issue one query per row (N+1)."""

    def setUp(self):
        self.admin = Member.objects.create_superuser(email='admin@example.org', password='x')
        self.client.force_authenticate(self.admin)

    def queries_for(self, url):
        with CaptureQueriesContext(connection) as context:
            response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return len(context.captured_queries)

    def assert_constant(self, url, add_rows):
        add_rows(3)
        few = self.queries_for(url)
        add_rows(30)
        many = self.queries_for(url)
        self.assertEqual(few, many, f'{url}: {few} queries for 3 rows, {many} for 33')

    def test_compounds(self):
        substance = Substance.objects.create(name='water')

        def add(n):
            for _ in range(n):
                compound = Compound.objects.create(name='c')
                compound.substances.add(Component.objects.create(substance=substance))
        self.assert_constant('/api/compounds/', add)

    def test_members(self):
        role = Role.objects.create(name='r')

        def add(n):
            for i in range(n):
                Member.objects.create_user(email=f'm{Member.objects.count()}@x.org', password='x').roles.add(role)
        self.assert_constant('/api/members/', add)

    def test_containers(self):
        supplier = Supplier.objects.create(name='s')
        self.assert_constant(
            '/api/containers/', lambda n: Container.objects.bulk_create(Container(supplier=supplier, amount=1) for _ in range(n))
        )

    def test_experiments_with_access_annotations(self):
        user = Member.objects.create_user(email='u@x.org', password='x', working_group=WorkingGroup.objects.create(name='g'))
        project = Project.objects.create(title='p', owner=user)

        def add(n):
            for _ in range(n):
                experiment = Experiment.objects.create(project=project, title='e', owner=self.admin)
                ExperimentShare.objects.create(experiment=experiment, member=user)
        self.client.force_authenticate(user)
        self.assert_constant('/api/experiments/', add)


class HealthTests(APITestCase):
    def test_health_is_public_and_minimal(self):
        response = self.client.get('/api/health/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'status': 'ok'})

    def test_health_reports_database_failure(self):
        with mock.patch('api.health.connection') as broken:
            broken.cursor.side_effect = Exception('database down')
            response = self.client.get('/api/health/')
        self.assertEqual(response.status_code, status.HTTP_503_SERVICE_UNAVAILABLE)
        self.assertEqual(response.json(), {'status': 'unavailable'})  # no error details leak

    @override_settings(ALLOWED_HOSTS=['eln.example.org', '127.0.0.1'])
    def test_reachable_on_internal_address(self):
        # the container health checks use Host: 127.0.0.1
        self.assertEqual(self.client.get('/api/health/', HTTP_HOST='127.0.0.1').status_code, 200)


class ThrottleTests(APITestCase):
    def setUp(self):
        from django.core.cache import cache
        cache.clear()
        Member.objects.create_user(email='user@example.org', password='Correct-Horse-7')

    def test_login_is_throttled(self):
        with mock.patch.object(ScopedRateThrottle, 'THROTTLE_RATES', {'login': '3/minute'}):
            codes = [
                self.client.post('/api/token/', {'email': 'user@example.org', 'password': 'wrong'}, format='json').status_code
                for _ in range(4)
            ]
        self.assertEqual(codes, [401, 401, 401, 429])

    def test_throttle_uses_proxy_address_not_spoofable_header(self):
        with mock.patch.object(ScopedRateThrottle, 'THROTTLE_RATES', {'login': '2/minute'}):
            for i in range(3):
                # the client rotates its own X-Forwarded-For entry; nginx appends the real address last
                response = self.client.post(
                    '/api/token/', {'email': 'user@example.org', 'password': 'wrong'}, format='json',
                    HTTP_X_FORWARDED_FOR=f'10.0.0.{i}, 203.0.113.7',
                )
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)

    def test_registration_is_throttled(self):
        with mock.patch.object(ScopedRateThrottle, 'THROTTLE_RATES', {'register': '1/hour'}):
            payload = {'first_name': 'A', 'last_name': 'B', 'password': 'Correct-Horse-7-Battery'}
            first = self.client.post('/api/members/register/', {**payload, 'email': 'a@x.org'}, format='json')
            second = self.client.post('/api/members/register/', {**payload, 'email': 'b@x.org'}, format='json')
        self.assertEqual((first.status_code, second.status_code), (201, 429))


class LogoutTests(APITestCase):
    def test_blacklisted_refresh_token_cannot_be_used(self):
        Member.objects.create_user(email='user@example.org', password='Correct-Horse-7')
        tokens = self.client.post('/api/token/', {'email': 'user@example.org', 'password': 'Correct-Horse-7'}, format='json').data

        logout = self.client.post('/api/token/blacklist/', {'refresh': tokens['refresh']}, format='json')
        refresh = self.client.post('/api/token/refresh/', {'refresh': tokens['refresh']}, format='json')

        self.assertEqual(logout.status_code, status.HTTP_200_OK)
        self.assertEqual(refresh.status_code, status.HTTP_401_UNAUTHORIZED)


class RequestIdAndLoggingTests(APITestCase):
    def test_request_id_is_generated_or_propagated(self):
        generated = self.client.get('/api/health/')['X-Request-ID']
        propagated = self.client.get('/api/health/', HTTP_X_REQUEST_ID='abc123')['X-Request-ID']
        injected = self.client.get('/api/health/', HTTP_X_REQUEST_ID='bad\nid "x"')['X-Request-ID']

        self.assertRegex(generated, r'^[0-9a-f]{32}$')
        self.assertEqual(propagated, 'abc123')
        self.assertRegex(injected, r'^[0-9a-f]{32}$')  # malformed ids are replaced

    def test_json_log_lines(self):
        stream = StringIO()
        handler = logging.StreamHandler(stream)
        handler.setFormatter(JsonFormatter())
        handler.addFilter(RequestIdFilter())
        logger = logging.getLogger('flask.test')
        logger.addHandler(handler)
        try:
            logger.warning('something "quoted"\nhappened', extra={'event': 'test'})
        finally:
            logger.removeHandler(handler)

        entry = json.loads(stream.getvalue())  # exactly one valid JSON line
        self.assertEqual(entry['message'], 'something "quoted"\nhappened')
        self.assertEqual((entry['level'], entry['event'], entry['request_id']), ('WARNING', 'test', '-'))

    def test_failed_login_is_logged_without_credentials(self):
        with self.assertLogs('flask.security', level='WARNING') as captured:
            self.client.post('/api/token/', {'email': 'who@example.org', 'password': 'secret-guess'}, format='json')

        record = captured.records[0]
        self.assertEqual(record.event, 'login_failed')
        text = record.getMessage() + str(record.__dict__)
        self.assertNotIn('who@example.org', text)
        self.assertNotIn('secret-guess', text)
