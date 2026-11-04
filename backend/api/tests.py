import io

from django.db import IntegrityError, transaction
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import Member, Supplier, WorkingGroup
from chemicals.models import Component, Compound, Container, Substance, Unit
from locations.models import Building, Room, Storage

from .urls import router

PUBLIC_ACTIONS = {('members', 'register')}


class AuthorizationMatrixTests(APITestCase):
    """Every routed endpoint rejects anonymous requests (deny by default)."""

    def test_every_route_rejects_anonymous_requests(self):
        checked = 0
        for url in router.urls:
            basename = url.name.split('-')[0]
            kwargs = {'pk': 1} if 'pk' in url.pattern.regex.groupindex else {}
            path = reverse(url.name, kwargs=kwargs)
            # copy: DRF adds 'head' to this shared dict while dispatching
            for method, view_action in list(url.callback.actions.items()):
                if (basename, view_action) in PUBLIC_ACTIONS:
                    continue
                with self.subTest(path=path, method=method):
                    response = getattr(self.client, method)(path)
                    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
                    checked += 1
        self.assertGreater(checked, 50)  # guard against the loop silently checking nothing

    def test_regular_user_cannot_write_reference_data(self):
        user = Member.objects.create_user(email='user@example.org', password='x')
        self.client.force_authenticate(user)
        for path in ('/api/units/', '/api/substances/', '/api/components/', '/api/compounds/',
                     '/api/groups/', '/api/roles/', '/api/buildings/', '/api/containers/'):
            with self.subTest(path=path):
                self.assertEqual(self.client.post(path, {}, format='json').status_code, status.HTTP_403_FORBIDDEN)


class CreateSemanticsTests(APITestCase):
    def setUp(self):
        self.admin = Member.objects.create_superuser(email='admin@example.org', password='x')
        self.other = Member.objects.create_user(email='other@example.org', password='x')
        self.supplier = Supplier.objects.create(name='Supplier')
        self.unit = Unit.objects.create(name='gram', symbol='g')
        self.client.force_authenticate(self.admin)

    def test_create_returns_201_with_id_and_server_assigned_author(self):
        response = self.client.post('/api/containers/', {
            'supplier': self.supplier.id, 'amount': 100, 'amount_left': 100, 'amount_unit': self.unit.id,
            'created_by': self.other.id, 'updated_by': self.other.id,
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        container = Container.objects.get(pk=response.data['id'])
        self.assertEqual(container.created_by, self.admin)
        self.assertEqual(container.updated_by, self.admin)
        self.assertEqual(response.data['created_by'], self.admin.id)
        self.assertIsNotNone(container.created_at)

    def test_update_records_updating_user(self):
        container = Container.objects.create(supplier=self.supplier, amount=10, amount_left=10, created_by=self.other)

        self.client.patch(f'/api/containers/{container.id}/', {'description': 'checked'}, format='json')

        container.refresh_from_db()
        self.assertEqual(container.created_by, self.other)
        self.assertEqual(container.updated_by, self.admin)

    def test_create_with_many_to_many(self):
        # regression: objects.create(**validated_data) raised TypeError for M2M fields
        substance = Substance.objects.create(name='water')
        component = Component.objects.create(substance=substance, fraction=1)

        response = self.client.post(
            '/api/compounds/', {'name': 'water', 'substances': [component.id]}, format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        compound = Compound.objects.get(pk=response.data['id'])
        self.assertEqual(list(compound.substances.all()), [component])
        self.assertEqual(compound.created_by, self.admin)

    def test_compound_update_and_detail(self):
        # regression: CompoundViewSet had no serializer_class, so writes raised TypeError
        component = Component.objects.create(substance=Substance.objects.create(name='water'), fraction=1)
        compound = Compound.objects.create(name='water')
        compound.substances.add(component)

        patch = self.client.patch(f'/api/compounds/{compound.id}/', {'label': 'H2O'}, format='json')
        detail = self.client.get(f'/api/compounds/{compound.id}/')

        self.assertEqual(patch.status_code, status.HTTP_200_OK)
        self.assertEqual(detail.data['label'], 'H2O')
        self.assertEqual(detail.data['substances'][0]['substance'], component.substance_id)

    def test_invalid_amount_is_rejected_and_nothing_is_written(self):
        response = self.client.post('/api/containers/', {
            'supplier': self.supplier.id, 'amount': 10, 'amount_left': 20,
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('amount_left', response.data)
        self.assertFalse(Container.objects.exists())

    def test_admin_password_update_is_hashed(self):
        response = self.client.patch(
            f'/api/members/{self.other.id}/', {'password': 'New-Secret-Passphrase-9'}, format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.other.refresh_from_db()
        self.assertNotEqual(self.other.password, 'New-Secret-Passphrase-9')
        self.assertTrue(self.other.check_password('New-Secret-Passphrase-9'))


class ProtectedDeleteTests(APITestCase):
    def test_deleting_referenced_building_returns_409(self):
        admin = Member.objects.create_superuser(email='admin@example.org', password='x')
        building = Building.objects.create(name='NC', street='s', city='c', zipcode='44801')
        Room.objects.create(number=101, building=building)
        self.client.force_authenticate(admin)

        response = self.client.delete(f'/api/buildings/{building.id}/')

        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertTrue(Building.objects.filter(pk=building.pk).exists())
        self.assertEqual(Room.objects.count(), 1)

    def test_deleting_author_of_records_returns_409(self):
        admin = Member.objects.create_superuser(email='admin@example.org', password='x')
        author = Member.objects.create_user(email='author@example.org', password='x')
        Container.objects.create(supplier=Supplier.objects.create(name='S'), amount=1, created_by=author)
        self.client.force_authenticate(admin)

        response = self.client.delete(f'/api/members/{author.id}/')

        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertTrue(Member.objects.filter(pk=author.pk).exists())


class DatabaseConstraintTests(APITestCase):
    """Invariants hold even for writes that bypass serializers."""

    def setUp(self):
        self.supplier = Supplier.objects.create(name='Supplier')

    def assertRejected(self, create):
        with self.assertRaises(IntegrityError), transaction.atomic():
            create()

    def test_container_amount_constraints(self):
        self.assertRejected(lambda: Container.objects.create(supplier=self.supplier, amount=10, amount_left=11))
        self.assertRejected(lambda: Container.objects.create(supplier=self.supplier, amount=-1))
        self.assertRejected(lambda: Container.objects.create(supplier=self.supplier, amount=1, amount_left=-1))
        self.assertRejected(lambda: Container.objects.create(supplier=self.supplier, amount=1, price=-5))
        Container.objects.create(supplier=self.supplier, amount=10, amount_left=10)
        Container.objects.create(supplier=self.supplier, amount=None, amount_left=None)

    def test_fraction_and_purity_constraints(self):
        substance = Substance.objects.create(name='x')
        self.assertRejected(lambda: Component.objects.create(substance=substance, fraction=1.5))
        self.assertRejected(lambda: Compound.objects.create(name='x', purity=-0.1))

    def test_room_numbers_unique_per_building_only(self):
        first = Building.objects.create(name='NA', street='s', city='c', zipcode='1')
        second = Building.objects.create(name='NB', street='s', city='c', zipcode='1')
        Room.objects.create(number=101, building=first)
        Room.objects.create(number=101, building=second)  # regression: number used to be the primary key
        self.assertRejected(lambda: Room.objects.create(number=101, building=first))

    def test_storage_without_room_is_not_duplicated(self):
        Storage.objects.create(room=None, name='cabinet', compartment='')
        self.assertRejected(lambda: Storage.objects.create(room=None, name='cabinet', compartment=''))
        self.assertEqual(str(Storage.objects.get()), 'cabinet')  # regression: __str__ crashed without a room

    def test_long_identifiers_are_stored(self):
        inchi = 'InChI=1S/' + 'C' * 500
        substance = Substance.objects.create(name='large molecule', inchi=inchi, smiles='C' * 500)
        substance.refresh_from_db()
        self.assertEqual(substance.inchi, inchi)

    def test_compounds_can_share_ghs_classification(self):
        from ghs.models import GHS
        ghs = GHS.objects.create()
        Compound.objects.create(name='a', ghs=ghs)
        Compound.objects.create(name='b', ghs=ghs)  # regression: was a OneToOneField
        self.assertEqual(ghs.hazardous_compounds.count(), 2)


class HistoryTests(APITestCase):
    def setUp(self):
        self.group = WorkingGroup.objects.create(name='A')
        self.user = Member.objects.create_user(email='user@example.org', password='x', working_group=self.group)
        self.admin = Member.objects.create_superuser(email='admin@example.org', password='x')
        self.container = Container.objects.create(
            supplier=Supplier.objects.create(name='S'), amount=100, amount_left=100, owner=self.group
        )

    def test_update_keeps_previous_state_and_acting_user(self):
        self.client.force_authenticate(self.user)

        self.client.patch(f'/api/containers/{self.container.id}/', {'amount_left': 40}, format='json')

        records = self.container.history.order_by('history_date')
        self.assertEqual([record.history_type for record in records], ['+', '~'])
        self.assertEqual(records[0].amount_left, 100)
        self.assertEqual(records[1].amount_left, 40)
        self.assertEqual(records[1].history_user, self.user)  # JWT/DRF user reaches the history middleware

    def test_delete_leaves_a_record_of_the_deleted_state(self):
        self.client.force_authenticate(self.admin)
        container_id = self.container.id

        response = self.client.delete(f'/api/containers/{container_id}/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        deleted = Container.history.filter(id=container_id, history_type='-').get()
        self.assertEqual(deleted.amount_left, 100)
        self.assertEqual(deleted.history_user, self.admin)


class CsvTests(APITestCase):
    def setUp(self):
        self.admin = Member.objects.create_superuser(email='admin@example.org', password='x')
        self.client.force_authenticate(self.admin)

    def upload(self, content):
        file = io.BytesIO(content.encode('utf-8'))
        file.name = 'units.csv'
        return self.client.post('/api/units/upload_csv/', {'file': file}, format='multipart')

    def test_template_upload_round_trip(self):
        template = self.client.get('/api/units/download_csv_template/').content.decode()
        self.assertEqual(template.strip(), 'name;symbol')

        response = self.upload('name;symbol\nmetre;m\nkelvin;K\n')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertEqual(set(Unit.objects.values_list('symbol', flat=True)), {'m', 'K'})

    def test_invalid_row_writes_nothing(self):
        Unit.objects.create(name='metre', symbol='m')

        response = self.upload('name;symbol\nkelvin;K\nmetre again;m\n')  # duplicate symbol

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(Unit.objects.filter(symbol='K').exists())

    def test_missing_file_and_unknown_columns_return_400(self):
        self.assertEqual(
            self.client.post('/api/units/upload_csv/', {}, format='multipart').status_code,
            status.HTTP_400_BAD_REQUEST,
        )
        self.assertEqual(self.upload('name;symbol;id\nmetre;m;5\n').status_code, status.HTTP_400_BAD_REQUEST)

    def test_export_escapes_formulas(self):
        Unit.objects.create(name='=HYPERLINK("http://evil")', symbol='x')

        content = self.client.get('/api/units/download_csv/').content.decode()

        self.assertIn("'=HYPERLINK", content)
        self.assertNotIn(';=HYPERLINK', content)
