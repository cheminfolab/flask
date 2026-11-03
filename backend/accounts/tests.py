import os
from io import StringIO
from unittest import mock

from django.core.management import call_command
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Member, Role, WorkingGroup

STRONG_PASSWORD = 'Correct-Horse-7-Battery'


class RegistrationTests(APITestCase):
    url = '/api/members/register/'

    def payload(self, **overrides):
        data = {
            'first_name': 'Ada',
            'last_name': 'Lovelace',
            'email': 'ada@example.org',
            'password': STRONG_PASSWORD,
        }
        data.update(overrides)
        return data

    def test_register_creates_inactive_account_and_ignores_privileged_fields(self):
        group = WorkingGroup.objects.create(name='Target')
        role = Role.objects.create(name='Manager')

        response = self.client.post(
            self.url,
            self.payload(working_group=group.id, roles=[role.id], is_staff=True, is_active=True),
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotIn('password', response.data)
        self.assertFalse(response.data['is_active'])
        member = Member.objects.get(email='ada@example.org')
        self.assertFalse(member.is_active)
        self.assertFalse(member.is_staff)
        self.assertIsNone(member.working_group)
        self.assertEqual(member.roles.count(), 0)
        self.assertTrue(member.check_password(STRONG_PASSWORD))

    def test_weak_password_is_rejected(self):
        response = self.client.post(self.url, self.payload(password='1234'), format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)
        self.assertFalse(Member.objects.exists())

    def test_password_similar_to_email_is_rejected(self):
        response = self.client.post(
            self.url, self.payload(email='quantumchemist@example.org', password='quantumchemist'), format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_duplicate_email_returns_400_without_echoing_password(self):
        Member.objects.create_user(email='ada@example.org', password=STRONG_PASSWORD)

        response = self.client.post(self.url, self.payload(), format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)
        self.assertNotIn(STRONG_PASSWORD, response.content.decode())

    def test_inactive_account_cannot_obtain_token(self):
        self.client.post(self.url, self.payload(), format='json')

        response = self.client.post(
            '/api/token/', {'email': 'ada@example.org', 'password': STRONG_PASSWORD}, format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_activated_account_can_obtain_token(self):
        self.client.post(self.url, self.payload(), format='json')
        Member.objects.filter(email='ada@example.org').update(is_active=True)

        response = self.client.post(
            '/api/token/', {'email': 'ada@example.org', 'password': STRONG_PASSWORD}, format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)


class MemberAccessTests(APITestCase):
    def setUp(self):
        self.user = Member.objects.create_user(email='user@example.org', password=STRONG_PASSWORD)
        self.admin = Member.objects.create_superuser(email='admin@example.org', password=STRONG_PASSWORD)

    def test_member_list_is_admin_only(self):
        self.assertEqual(self.client.get('/api/members/').status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.force_authenticate(self.user)
        self.assertEqual(self.client.get('/api/members/').status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(self.admin)
        self.assertEqual(self.client.get('/api/members/').status_code, status.HTTP_200_OK)

    def test_member_retrieve_is_admin_only(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(f'/api/members/{self.admin.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_me_returns_current_user_only(self):
        self.assertEqual(self.client.get('/api/members/me/').status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.force_authenticate(self.user)
        response = self.client.get('/api/members/me/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'user@example.org')
        self.assertNotIn('password', response.data)

    def test_groups_and_roles_require_authentication(self):
        for url in ('/api/groups/', '/api/roles/'):
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, status.HTTP_401_UNAUTHORIZED)


class EnsureSuperuserCommandTests(APITestCase):
    def run_command(self, env):
        with mock.patch.dict(os.environ, env, clear=False):
            for key in ('DJANGO_SUPERUSER_EMAIL', 'DJANGO_SUPERUSER_PASSWORD'):
                if key not in env:
                    os.environ.pop(key, None)
            call_command('ensure_superuser', stdout=StringIO())

    def test_creates_superuser_from_environment(self):
        self.run_command({'DJANGO_SUPERUSER_EMAIL': 'root@example.org', 'DJANGO_SUPERUSER_PASSWORD': STRONG_PASSWORD})

        admin = Member.objects.get(email='root@example.org')
        self.assertTrue(admin.is_superuser)
        self.assertTrue(admin.check_password(STRONG_PASSWORD))

    def test_does_nothing_without_environment(self):
        self.run_command({})
        self.assertFalse(Member.objects.exists())

    def test_never_modifies_existing_superuser(self):
        Member.objects.create_superuser(email='root@example.org', password='Changed-Later-42!')

        self.run_command({'DJANGO_SUPERUSER_EMAIL': 'root@example.org', 'DJANGO_SUPERUSER_PASSWORD': STRONG_PASSWORD})

        self.assertTrue(Member.objects.get(email='root@example.org').check_password('Changed-Later-42!'))
        self.assertEqual(Member.objects.count(), 1)

    def test_no_default_admin_account_exists(self):
        self.assertFalse(Member.objects.filter(email='admin@admin.com').exists())
