from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import Member, Supplier, WorkingGroup
from .models import Container, Substance, Unit


class ReadAccessTests(APITestCase):
    def setUp(self):
        self.user = Member.objects.create_user(email='user@example.org', password='x')
        Substance.objects.create(name='sulfuric acid', formula='H2SO4')

    def test_collections_require_authentication(self):
        for url in ('/api/units/', '/api/substances/', '/api/components/', '/api/compounds/', '/api/containers/'):
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, status.HTTP_401_UNAUTHORIZED)

    def test_substance_list_serializes(self):
        # regression: the serializer declared a removed `structure` field and returned 500
        self.client.force_authenticate(self.user)

        response = self.client.get('/api/substances/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['name'], 'sulfuric acid')
        self.assertNotIn('structure', response.data['results'][0])


class ContainerPermissionTests(APITestCase):
    def setUp(self):
        self.group_a = WorkingGroup.objects.create(name='A')
        self.group_b = WorkingGroup.objects.create(name='B')
        self.supplier = Supplier.objects.create(name='Supplier')
        self.unit = Unit.objects.create(name='gram', symbol='g')

    def make_user(self, group=None, email='user@example.org', **extra):
        return Member.objects.create_user(email=email, password='x', working_group=group, **extra)

    def make_container(self, owner=None):
        return Container.objects.create(
            supplier=self.supplier, amount=100, amount_left=100, amount_unit=self.unit, owner=owner
        )

    def patch(self, user, container, data):
        self.client.force_authenticate(user)
        return self.client.patch(f'/api/containers/{container.id}/', data, format='json')

    def test_anonymous_cannot_retrieve(self):
        container = self.make_container()
        response = self.client.get(f'/api/containers/{container.id}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_full_edit_matrix(self):
        cases = [
            # (user's group, container owner, expected status)
            (None, None, status.HTTP_403_FORBIDDEN),  # regression: None == None used to pass
            (None, 'a', status.HTTP_403_FORBIDDEN),
            ('a', None, status.HTTP_403_FORBIDDEN),
            ('a', 'b', status.HTTP_403_FORBIDDEN),
            ('a', 'a', status.HTTP_200_OK),
        ]
        groups = {None: None, 'a': self.group_a, 'b': self.group_b}
        for index, (user_group, owner, expected) in enumerate(cases):
            with self.subTest(user_group=user_group, owner=owner):
                user = self.make_user(groups[user_group], email=f'u{index}@example.org')
                container = self.make_container(groups[owner])

                response = self.patch(user, container, {'description': 'relabelled'})

                self.assertEqual(response.status_code, expected)
                container.refresh_from_db()
                self.assertEqual(container.description == 'relabelled', expected == status.HTTP_200_OK)

    def test_full_put_by_non_member_is_forbidden(self):
        user = self.make_user()
        container = self.make_container(self.group_a)
        self.client.force_authenticate(user)

        response = self.client.put(
            f'/api/containers/{container.id}/',
            {'supplier': self.supplier.id, 'amount': 1, 'amount_left': 1, 'owner': self.group_b.id},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_non_member_can_record_usage_and_server_assigns_provenance(self):
        user = self.make_user()
        container = self.make_container(self.group_a)

        response = self.patch(user, container, {'amount_left': 60})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        container.refresh_from_db()
        self.assertEqual(container.amount_left, 60)
        self.assertEqual(container.last_user, user)
        self.assertEqual(container.last_used, timezone.localdate())

    def test_non_member_cannot_set_last_user(self):
        user = self.make_user()
        other = self.make_user(email='other@example.org')
        container = self.make_container(self.group_a)

        response = self.patch(user, container, {'amount_left': 60, 'last_user': other.id})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_provenance_fields_are_read_only_for_members(self):
        member = self.make_user(self.group_a)
        other = self.make_user(email='other@example.org')
        container = self.make_container(self.group_a)

        response = self.patch(
            member, container, {'last_user': other.id, 'created_by': other.id, 'last_used': '2000-01-01'}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        container.refresh_from_db()
        self.assertIsNone(container.last_user)
        self.assertIsNone(container.created_by)
        self.assertIsNone(container.last_used)

    def test_same_user_can_be_last_user_of_several_containers(self):
        # regression: last_user was a OneToOneField, so the second update raised IntegrityError
        user = self.make_user()
        first, second = self.make_container(), self.make_container()

        self.assertEqual(self.patch(user, first, {'amount_left': 50}).status_code, status.HTTP_200_OK)
        self.assertEqual(self.patch(user, second, {'amount_left': 50}).status_code, status.HTTP_200_OK)

    def test_staff_can_edit_everything(self):
        admin = self.make_user(email='admin@example.org', is_staff=True)
        container = self.make_container(self.group_a)

        response = self.patch(admin, container, {'description': 'checked'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
