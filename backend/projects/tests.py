import hashlib
import shutil
import tempfile

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import Member, Supplier, WorkingGroup
from chemicals.models import Container, Unit

from .models import AccessLevel, Attachment, Entry, Experiment, ExperimentShare, MaterialUsage, Project, ProjectShare


class NotebookFixture(APITestCase):
    """
    lead (group A) owns the project; author (group A) writes the experiment in it.

    groupmate   group A, no shares              -> read
    outsider    group B, no shares              -> nothing
    admin       staff, no group                 -> read, never edit
    reader      group B, experiment share read  -> read
    editor      group B, experiment share edit  -> read + edit
    p_reader    group B, project share read     -> read
    p_editor    group B, project share edit     -> read + edit (+ create experiments)
    """

    def setUp(self):
        self.group_a = WorkingGroup.objects.create(name='A')
        self.group_b = WorkingGroup.objects.create(name='B')

        def member(name, group=None, **extra):
            return Member.objects.create_user(
                email=f'{name}@example.org', password='x', first_name=name, last_name=name.upper(),
                working_group=group, **extra
            )

        self.lead = member('lead', self.group_a)
        self.author = member('author', self.group_a)
        self.groupmate = member('groupmate', self.group_a)
        self.outsider = member('outsider', self.group_b)
        self.admin = member('admin', is_staff=True, is_superuser=True)
        self.reader = member('reader', self.group_b)
        self.editor = member('editor', self.group_b)
        self.p_reader = member('preader', self.group_b)
        self.p_editor = member('peditor', self.group_b)

        self.project = Project.objects.create(title='Catalysis', owner=self.lead, working_group=self.group_a)
        self.experiment = Experiment.objects.create(
            project=self.project, title='Suzuki coupling', owner=self.author, working_group=self.group_a
        )
        ExperimentShare.objects.create(experiment=self.experiment, member=self.reader, level=AccessLevel.READ)
        ExperimentShare.objects.create(experiment=self.experiment, member=self.editor, level=AccessLevel.EDIT)
        ProjectShare.objects.create(project=self.project, member=self.p_reader, level=AccessLevel.READ)
        ProjectShare.objects.create(project=self.project, member=self.p_editor, level=AccessLevel.EDIT)

        self.url = f'/api/experiments/{self.experiment.id}/'

    def as_user(self, user):
        self.client.force_authenticate(user)
        return self.client

    def complete(self):
        response = self.as_user(self.author).post(f'{self.url}complete/')
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.experiment.refresh_from_db()


class ExperimentAccessTests(NotebookFixture):
    def test_read_access(self):
        expected = {
            'author': True, 'lead': True, 'groupmate': True, 'outsider': False, 'admin': True,
            'reader': True, 'editor': True, 'p_reader': True, 'p_editor': True,
        }
        for name, can_read in expected.items():
            with self.subTest(user=name):
                client = self.as_user(getattr(self, name))
                listed = [e['id'] for e in client.get('/api/experiments/').data]
                detail = client.get(self.url)
                self.assertEqual(self.experiment.id in listed, can_read)
                self.assertEqual(detail.status_code, status.HTTP_200_OK if can_read else status.HTTP_404_NOT_FOUND)

    def test_edit_access(self):
        expected = {
            'author': 200, 'editor': 200, 'p_editor': 200,
            'lead': 403, 'groupmate': 403, 'admin': 403, 'reader': 403, 'p_reader': 403,
            'outsider': 404,
        }
        for name, code in expected.items():
            with self.subTest(user=name):
                client = self.as_user(getattr(self, name))
                response = client.patch(self.url, {'title': f'edited by {name}'}, format='json')
                self.assertEqual(response.status_code, code)
                if code == 200:
                    self.assertTrue(response.data['can_edit'])
                elif code == 403:
                    self.assertFalse(client.get(self.url).data['can_edit'])

    def test_outsider_gets_access_once_shared(self):
        self.as_user(self.author).post(
            '/api/experiment-shares/', {'experiment': self.experiment.id, 'member': self.outsider.id}, format='json'
        )
        self.assertEqual(self.as_user(self.outsider).get(self.url).status_code, status.HTTP_200_OK)

    def test_project_filter(self):
        other = Project.objects.create(title='Other', owner=self.author)
        Experiment.objects.create(project=other, title='Elsewhere', owner=self.author)

        listed = self.as_user(self.author).get(f'/api/experiments/?project={self.project.id}').data

        self.assertEqual([e['title'] for e in listed], ['Suzuki coupling'])

    def test_experiments_cannot_be_deleted(self):
        for user in (self.author, self.admin):
            with self.subTest(user=user.email):
                response = self.as_user(user).delete(self.url)
                self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertTrue(Experiment.objects.filter(pk=self.experiment.pk).exists())

    def test_experiment_cannot_be_moved_to_another_project(self):
        other = Project.objects.create(title='Other', owner=self.author)
        response = self.as_user(self.author).patch(self.url, {'project': other.id}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ExperimentCreateTests(NotebookFixture):
    def create(self, user, project=None):
        return self.as_user(user).post('/api/experiments/', {
            'project': (project or self.project).id, 'title': 'New', 'owner': self.outsider.id,
            'status': 'completed',
        }, format='json')

    def test_project_editors_can_create_and_become_owner(self):
        for user in (self.lead, self.p_editor):
            with self.subTest(user=user.email):
                response = self.create(user)
                self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
                experiment = Experiment.objects.get(pk=response.data['id'])
                self.assertEqual(experiment.owner, user)               # client-supplied owner ignored
                self.assertEqual(experiment.working_group, user.working_group)
                self.assertEqual(experiment.status, 'draft')           # client-supplied status ignored
                self.assertEqual(experiment.created_by, user)

    def test_project_readers_cannot_create(self):
        for user in (self.groupmate, self.p_reader, self.admin):
            with self.subTest(user=user.email):
                self.assertEqual(self.create(user).status_code, status.HTTP_403_FORBIDDEN)

    def test_unreadable_project_looks_like_unknown_id(self):
        response = self.create(self.outsider)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('project', response.data)


class ProjectAccessTests(NotebookFixture):
    def test_read_access(self):
        expected = {'lead': True, 'author': True, 'groupmate': True, 'admin': True, 'p_reader': True,
                    'outsider': False, 'reader': False}
        for name, can_read in expected.items():
            with self.subTest(user=name):
                listed = [p['id'] for p in self.as_user(getattr(self, name)).get('/api/projects/').data]
                self.assertEqual(self.project.id in listed, can_read)

    def test_edit_access(self):
        expected = {'lead': 200, 'p_editor': 200, 'groupmate': 403, 'admin': 403, 'p_reader': 403, 'outsider': 404}
        for name, code in expected.items():
            with self.subTest(user=name):
                response = self.as_user(getattr(self, name)).patch(
                    f'/api/projects/{self.project.id}/', {'description': name}, format='json'
                )
                self.assertEqual(response.status_code, code)

    def test_create_sets_owner_and_group(self):
        response = self.as_user(self.outsider).post('/api/projects/', {'title': 'Mine', 'owner': self.lead.id}, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        project = Project.objects.get(pk=response.data['id'])
        self.assertEqual((project.owner, project.working_group), (self.outsider, self.group_b))

    def test_project_with_experiments_cannot_be_deleted(self):
        self.assertEqual(
            self.as_user(self.p_editor).delete(f'/api/projects/{self.project.id}/').status_code,
            status.HTTP_403_FORBIDDEN,
        )
        self.assertEqual(
            self.as_user(self.lead).delete(f'/api/projects/{self.project.id}/').status_code,
            status.HTTP_409_CONFLICT,
        )


class ShareManagementTests(NotebookFixture):
    def test_only_owner_manages_experiment_shares(self):
        payload = {'experiment': self.experiment.id, 'member': self.outsider.id}
        for user in (self.editor, self.lead, self.admin):
            with self.subTest(user=user.email):
                self.assertEqual(
                    self.as_user(user).post('/api/experiment-shares/', payload, format='json').status_code,
                    status.HTTP_403_FORBIDDEN,
                )
        share = ExperimentShare.objects.get(member=self.reader)
        self.assertEqual(
            self.as_user(self.editor).delete(f'/api/experiment-shares/{share.id}/').status_code,
            status.HTTP_403_FORBIDDEN,
        )
        self.assertEqual(
            self.as_user(self.author).delete(f'/api/experiment-shares/{share.id}/').status_code,
            status.HTTP_204_NO_CONTENT,
        )
        self.assertEqual(self.as_user(self.reader).get(self.url).status_code, status.HTTP_404_NOT_FOUND)

    def test_upgrade_share_level(self):
        share = ExperimentShare.objects.get(member=self.reader)
        response = self.as_user(self.author).patch(f'/api/experiment-shares/{share.id}/', {'level': 'edit'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            self.as_user(self.reader).patch(self.url, {'title': 'x'}, format='json').status_code, status.HTTP_200_OK
        )

    def test_cannot_share_with_owner(self):
        response = self.as_user(self.author).post(
            '/api/experiment-shares/', {'experiment': self.experiment.id, 'member': self.author.id}, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_only_project_owner_manages_project_shares(self):
        payload = {'project': self.project.id, 'member': self.outsider.id, 'level': 'edit'}
        self.assertEqual(
            self.as_user(self.p_editor).post('/api/project-shares/', payload, format='json').status_code,
            status.HTTP_403_FORBIDDEN,
        )
        self.assertEqual(
            self.as_user(self.lead).post('/api/project-shares/', payload, format='json').status_code,
            status.HTTP_201_CREATED,
        )
        self.assertEqual(
            self.as_user(self.outsider).patch(self.url, {'title': 'via project share'}, format='json').status_code,
            status.HTTP_200_OK,
        )


class LockAndCorrectionTests(NotebookFixture):
    def setUp(self):
        super().setUp()
        self.entry = Entry.objects.create(experiment=self.experiment, kind='result', content='yield 81 %')

    def post_entry(self, user, **data):
        return self.as_user(user).post('/api/entries/', {'experiment': self.experiment.id, **data}, format='json')

    def test_only_author_can_complete(self):
        for user in (self.editor, self.p_editor, self.admin):
            with self.subTest(user=user.email):
                self.assertEqual(
                    self.as_user(user).post(f'{self.url}complete/').status_code, status.HTTP_403_FORBIDDEN
                )

        self.complete()

        self.assertEqual(self.experiment.status, 'completed')
        self.assertEqual(self.experiment.completed_by, self.author)
        self.assertIsNotNone(self.experiment.completed_at)
        self.assertEqual(
            self.as_user(self.author).post(f'{self.url}complete/').status_code, status.HTTP_409_CONFLICT
        )

    def test_completed_experiment_is_read_only(self):
        self.complete()

        self.assertEqual(
            self.as_user(self.author).patch(self.url, {'title': 'changed'}, format='json').status_code,
            status.HTTP_409_CONFLICT,
        )
        self.assertEqual(self.post_entry(self.author, kind='note', content='late').status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(
            self.as_user(self.author).patch(f'/api/entries/{self.entry.id}/', {'content': 'yield 95 %'}, format='json').status_code,
            status.HTTP_409_CONFLICT,
        )
        self.assertEqual(
            self.as_user(self.author).delete(f'/api/entries/{self.entry.id}/').status_code, status.HTTP_409_CONFLICT
        )
        self.entry.refresh_from_db()
        self.assertEqual(self.entry.content, 'yield 81 %')

    def test_corrections_after_completion(self):
        self.complete()

        missing_reason = self.post_entry(self.author, kind='correction', content='yield 78 %', corrects=self.entry.id)
        self.assertEqual(missing_reason.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('reason', missing_reason.data)

        by_reader = self.post_entry(self.reader, kind='correction', content='x', corrects=self.entry.id, reason='r')
        self.assertEqual(by_reader.status_code, status.HTTP_403_FORBIDDEN)

        response = self.post_entry(
            self.editor, kind='correction', content='yield 78 %', corrects=self.entry.id,
            reason='Balance was not tared; re-weighed product.',
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        correction = Entry.objects.get(pk=response.data['id'])
        self.assertEqual((correction.corrects, correction.created_by), (self.entry, self.editor))
        self.assertEqual(list(self.entry.corrections.all()), [correction])

        # corrections are themselves immutable
        self.assertEqual(
            self.as_user(self.editor).patch(f'/api/entries/{correction.id}/', {'content': 'y'}, format='json').status_code,
            status.HTTP_409_CONFLICT,
        )

    def test_no_corrections_in_drafts(self):
        response = self.post_entry(self.author, kind='correction', content='x', corrects=self.entry.id, reason='r')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_correction_must_target_same_experiment(self):
        other = Experiment.objects.create(project=self.project, title='Other', owner=self.author)
        foreign = Entry.objects.create(experiment=other, kind='note', content='x')
        self.complete()

        response = self.post_entry(self.author, kind='correction', content='x', corrects=foreign.id, reason='r')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_draft_entries_are_editable_with_history(self):
        response = self.as_user(self.editor).patch(
            f'/api/entries/{self.entry.id}/', {'content': 'yield 83 %'}, format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        versions = list(self.entry.history.order_by('history_date').values_list('content', 'history_user'))
        self.assertEqual(versions, [('yield 81 %', None), ('yield 83 %', self.editor.id)])

    def test_shares_remain_manageable_after_completion(self):
        self.complete()
        response = self.as_user(self.author).post(
            '/api/experiment-shares/', {'experiment': self.experiment.id, 'member': self.outsider.id}, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_entries_of_unreadable_experiments_are_hidden(self):
        self.assertEqual(self.as_user(self.outsider).get('/api/entries/').data, [])
        self.assertEqual(
            self.as_user(self.outsider).get(f'/api/entries/{self.entry.id}/').status_code, status.HTTP_404_NOT_FOUND
        )
        response = self.post_entry(self.outsider, kind='note', content='x')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class MaterialLedgerTests(NotebookFixture):
    def setUp(self):
        super().setUp()
        self.gram = Unit.objects.create(name='gram', symbol='g')
        self.litre = Unit.objects.create(name='litre', symbol='L')
        self.container = Container.objects.create(
            supplier=Supplier.objects.create(name='S'), amount=100, amount_left=100, amount_unit=self.gram
        )

    def use(self, user, amount, unit=None):
        return self.as_user(user).post('/api/materials/', {
            'experiment': self.experiment.id, 'container': self.container.id,
            'amount': amount, 'unit': (unit or self.gram).id,
        }, format='json')

    def test_usage_decrements_container(self):
        response = self.use(self.author, 12.5)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        self.container.refresh_from_db()
        self.assertEqual(self.container.amount_left, 87.5)
        self.assertEqual(self.container.last_user, self.author)
        self.assertEqual(self.container.history.latest().history_user, self.author)

    def test_overdraw_and_unit_mismatch_are_rejected(self):
        self.assertEqual(self.use(self.author, 150).status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(self.use(self.author, 1, unit=self.litre).status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(self.use(self.author, 0).status_code, status.HTTP_400_BAD_REQUEST)
        self.container.refresh_from_db()
        self.assertEqual(self.container.amount_left, 100)

    def test_readers_cannot_record_usage(self):
        self.assertEqual(self.use(self.reader, 1).status_code, status.HTTP_403_FORBIDDEN)

    def test_deleting_draft_usage_restores_amount(self):
        usage_id = self.use(self.author, 40).data['id']

        response = self.as_user(self.author).delete(f'/api/materials/{usage_id}/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.container.refresh_from_db()
        self.assertEqual(self.container.amount_left, 100)
        self.assertTrue(MaterialUsage.history.filter(id=usage_id, history_type='-').exists())

    def test_ledger_is_locked_after_completion(self):
        usage_id = self.use(self.author, 40).data['id']
        self.complete()

        self.assertEqual(self.use(self.author, 1).status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(
            self.as_user(self.author).delete(f'/api/materials/{usage_id}/').status_code, status.HTTP_409_CONFLICT
        )
        self.container.refresh_from_db()
        self.assertEqual(self.container.amount_left, 60)

    def test_no_update_endpoint(self):
        usage_id = self.use(self.author, 40).data['id']
        response = self.as_user(self.author).patch(f'/api/materials/{usage_id}/', {'amount': 1}, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class AttachmentTests(NotebookFixture):
    CONTENT = b'<svg onload="alert(1)"></svg>'

    def setUp(self):
        super().setUp()
        self.storage_dir = tempfile.mkdtemp()
        self.settings_override = override_settings(PRIVATE_MEDIA_ROOT=self.storage_dir)
        self.settings_override.enable()
        # reset the lazy storage so it picks up the temporary directory
        from django.utils.functional import empty
        from .models import private_storage
        private_storage._wrapped = empty

    def tearDown(self):
        self.settings_override.disable()
        from django.utils.functional import empty
        from .models import private_storage
        private_storage._wrapped = empty
        shutil.rmtree(self.storage_dir, ignore_errors=True)
        super().tearDown()

    def upload(self, user, name='spectrum.svg', content=None, content_type='text/plain', **extra):
        file = SimpleUploadedFile(name, content or self.CONTENT, content_type=content_type)
        return self.as_user(user).post(
            '/api/attachments/', {'experiment': self.experiment.id, 'file': file, **extra}, format='multipart'
        )

    def test_upload_records_metadata_and_checksum(self):
        response = self.upload(self.author)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        attachment = Attachment.objects.get(pk=response.data['id'])
        self.assertEqual(attachment.sha256, hashlib.sha256(self.CONTENT).hexdigest())
        self.assertEqual(attachment.size, len(self.CONTENT))
        self.assertEqual(attachment.original_name, 'spectrum.svg')
        self.assertEqual(attachment.content_type, 'image/svg+xml')   # derived from the name, not the client
        self.assertEqual(attachment.uploaded_by, self.author)
        self.assertNotIn('spectrum', attachment.file.name)          # stored under a server-generated name
        self.assertNotIn('file', response.data)

    def test_path_traversal_names_are_neutralized(self):
        response = self.upload(self.author, name='../../etc/passwd')
        attachment = Attachment.objects.get(pk=response.data['id'])
        self.assertEqual(attachment.original_name, 'passwd')
        self.assertTrue(attachment.file.name.startswith(f'attachments/{self.experiment.id}/'))

    def test_download_is_permission_checked_and_never_inline(self):
        attachment_id = self.upload(self.author).data['id']
        url = f'/api/attachments/{attachment_id}/download/'

        response = self.as_user(self.reader).get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(b''.join(response.streaming_content), self.CONTENT)
        self.assertTrue(response['Content-Disposition'].startswith('attachment;'))
        self.assertEqual(response['X-Content-Type-Options'], 'nosniff')
        self.assertIn('sandbox', response['Content-Security-Policy'])
        self.assertEqual(self.as_user(self.outsider).get(url).status_code, status.HTTP_404_NOT_FOUND)
        self.client.force_authenticate(None)
        self.assertEqual(self.client.get(url).status_code, status.HTTP_401_UNAUTHORIZED)

    def test_x_accel_download(self):
        attachment_id = self.upload(self.author).data['id']
        with override_settings(ATTACHMENT_X_ACCEL_PREFIX='/protected-attachments/'):
            response = self.as_user(self.author).get(f'/api/attachments/{attachment_id}/download/')

        attachment = Attachment.objects.get(pk=attachment_id)
        self.assertEqual(response['X-Accel-Redirect'], f'/protected-attachments/{attachment.file.name}')
        self.assertEqual(response.content, b'')

    def test_size_limit(self):
        with override_settings(ATTACHMENT_MAX_SIZE=10):
            response = self.upload(self.author)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(Attachment.objects.exists())

    def test_readers_cannot_upload(self):
        self.assertEqual(self.upload(self.reader).status_code, status.HTTP_403_FORBIDDEN)

    def test_entry_must_belong_to_the_experiment(self):
        other = Experiment.objects.create(project=self.project, title='Other', owner=self.author)
        foreign = Entry.objects.create(experiment=other, kind='note', content='x')
        self.assertEqual(self.upload(self.author, entry=foreign.id).status_code, status.HTTP_400_BAD_REQUEST)

    def test_locked_after_completion(self):
        attachment_id = self.upload(self.author).data['id']
        self.complete()

        self.assertEqual(self.upload(self.author).status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(
            self.as_user(self.author).delete(f'/api/attachments/{attachment_id}/').status_code, status.HTTP_409_CONFLICT
        )

    def test_draft_delete_removes_file_after_commit(self):
        attachment_id = self.upload(self.author).data['id']
        stored = Attachment.objects.get(pk=attachment_id).file
        self.assertTrue(stored.storage.exists(stored.name))

        with self.captureOnCommitCallbacks(execute=True):
            response = self.as_user(self.author).delete(f'/api/attachments/{attachment_id}/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(stored.storage.exists(stored.name))
        deleted = Attachment.history.get(id=attachment_id, history_type='-')
        self.assertEqual(deleted.sha256, hashlib.sha256(self.CONTENT).hexdigest())


class DirectoryAndDocsTests(NotebookFixture):
    def test_member_directory_has_names_but_no_emails(self):
        response = self.as_user(self.outsider).get('/api/members/directory/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('author', {m['first_name'] for m in response.data})
        self.assertNotIn('email', response.data[0])

    def test_schema_is_admin_only(self):
        self.client.force_authenticate(None)
        self.assertIn(self.client.get('/api/schema/').status_code, (401, 403))
        self.assertEqual(self.as_user(self.author).get('/api/schema/').status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.as_user(self.admin).get('/api/schema/').status_code, status.HTTP_200_OK)


class ReadOnlyAdminTests(NotebookFixture):
    def test_admin_can_view_but_not_change_notebook_records(self):
        self.client.force_login(self.admin)
        base = '/admin/projects/experiment/'

        self.assertEqual(self.client.get(base).status_code, 200)
        self.assertEqual(self.client.get(f'{base}{self.experiment.id}/change/').status_code, 200)  # view-only page
        self.assertEqual(self.client.get(f'{base}add/').status_code, 403)
        self.assertEqual(
            self.client.post(f'{base}{self.experiment.id}/change/', {'title': 'admin edit'}).status_code, 403
        )
        self.assertEqual(self.client.post(f'{base}{self.experiment.id}/delete/', {'post': 'yes'}).status_code, 403)

        version = self.experiment.history.first()
        revert = self.client.post(f'{base}{self.experiment.id}/history/{version.history_id}/', {'title': 'reverted'})
        self.assertEqual(revert.status_code, 403)
        self.experiment.refresh_from_db()
        self.assertEqual(self.experiment.title, 'Suzuki coupling')
