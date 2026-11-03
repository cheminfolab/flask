from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import Member
from .models import Building, Room


class BuildingPermissionTests(APITestCase):
    def setUp(self):
        self.building = Building.objects.create(name='NC', street='Universitätsstr. 150', city='Bochum', zipcode='44801')
        Room.objects.create(number=159, floor=4, building=self.building)
        self.user = Member.objects.create_user(email='user@example.org', password='x')
        self.admin = Member.objects.create_superuser(email='admin@example.org', password='x')
        self.new_building = {'name': 'NB', 'street': 'Universitätsstr. 150', 'city': 'Bochum', 'zipcode': '44801'}
        self.detail = f'/api/buildings/{self.building.id}/'

    def test_anonymous_has_no_access(self):
        self.assertEqual(self.client.get('/api/buildings/').status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(self.client.get(self.detail).status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            self.client.post('/api/buildings/', self.new_building, format='json').status_code,
            status.HTTP_401_UNAUTHORIZED,
        )
        self.assertEqual(
            self.client.patch(self.detail, {'city': 'X'}, format='json').status_code,
            status.HTTP_401_UNAUTHORIZED,
        )
        self.assertEqual(self.client.delete(self.detail).status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue(Building.objects.filter(pk=self.building.pk).exists())
        self.assertEqual(Room.objects.count(), 1)

    def test_user_can_read_but_not_write(self):
        self.client.force_authenticate(self.user)

        self.assertEqual(self.client.get('/api/buildings/').status_code, status.HTTP_200_OK)
        self.assertEqual(self.client.get(self.detail).status_code, status.HTTP_200_OK)
        self.assertEqual(
            self.client.post('/api/buildings/', self.new_building, format='json').status_code,
            status.HTTP_403_FORBIDDEN,
        )
        self.assertEqual(
            self.client.patch(self.detail, {'city': 'X'}, format='json').status_code,
            status.HTTP_403_FORBIDDEN,
        )
        self.assertEqual(self.client.delete(self.detail).status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Room.objects.count(), 1)

    def test_admin_can_write(self):
        self.client.force_authenticate(self.admin)

        self.assertEqual(
            self.client.post('/api/buildings/', self.new_building, format='json').status_code,
            status.HTTP_201_CREATED,
        )
        self.assertEqual(
            self.client.patch(self.detail, {'city': 'Essen'}, format='json').status_code,
            status.HTTP_200_OK,
        )
        # buildings that still have rooms are protected (409); an empty one can be deleted
        self.assertEqual(self.client.delete(self.detail).status_code, status.HTTP_409_CONFLICT)
        empty = Building.objects.get(name='NB')
        self.assertEqual(
            self.client.delete(f'/api/buildings/{empty.id}/').status_code, status.HTTP_204_NO_CONTENT
        )

    def test_csv_export_is_admin_only(self):
        self.client.force_authenticate(self.user)
        self.assertEqual(
            self.client.get('/api/buildings/download_csv/').status_code, status.HTTP_403_FORBIDDEN
        )
