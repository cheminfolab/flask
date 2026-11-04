"""
Electronic lab notebook records: Project -> Experiment -> Entries, plus the
materials taken from inventory and attached files.

Record integrity rules (enforced in the API, see projects/views.py, and where
possible in the database):

- Authorship and timestamps are assigned by the server (TrackedModel).
- Every change is kept in history tables (django-simple-history).
- Experiments are never deleted through the API.
- A completed experiment is locked: its fields, entries, materials and
  attachments can no longer change. Later changes are recorded as correction
  entries that reference the corrected entry and state a reason.
"""
import hashlib
import uuid

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.db.models import Q
from django.utils.functional import LazyObject
from simple_history.models import HistoricalRecords

from accounts.models import WorkingGroup
from api.models import TrackedModel
from chemicals.models import Container, Unit


class AccessLevel(models.TextChoices):
    READ = 'read', 'read'
    EDIT = 'edit', 'edit'


class Project(TrackedModel):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='owned_projects')
    # copied from the owner at creation, so visibility does not change when the owner changes groups
    working_group = models.ForeignKey(
        WorkingGroup, null=True, blank=True, on_delete=models.PROTECT, related_name='projects'
    )

    history = HistoricalRecords()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class ProjectShare(models.Model):
    """Grants a member read or edit access to every experiment in a project."""
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='shares')
    member = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='project_shares')
    level = models.CharField(max_length=4, choices=AccessLevel.choices, default=AccessLevel.READ)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, editable=False, on_delete=models.PROTECT, related_name='+'
    )

    history = HistoricalRecords()

    class Meta:
        constraints = [models.UniqueConstraint(fields=['project', 'member'], name='project_share_unique_member')]

    def __str__(self):
        return f"{self.project} -> {self.member} ({self.level})"


class Experiment(TrackedModel):
    class Status(models.TextChoices):
        DRAFT = 'draft', 'draft'
        COMPLETED = 'completed', 'completed'

    project = models.ForeignKey(Project, on_delete=models.PROTECT, related_name='experiments')
    title = models.CharField(max_length=200)
    objective = models.TextField(blank=True)
    started_on = models.DateField(null=True, blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='owned_experiments')
    # copied from the owner at creation (see Project.working_group)
    working_group = models.ForeignKey(
        WorkingGroup, null=True, blank=True, on_delete=models.PROTECT, related_name='experiments'
    )
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.DRAFT)
    completed_at = models.DateTimeField(null=True, blank=True)
    completed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.PROTECT, related_name='+'
    )

    history = HistoricalRecords()

    class Meta:
        ordering = ['-created_at']
        constraints = [
            models.CheckConstraint(
                condition=(
                    Q(status='draft', completed_at__isnull=True, completed_by__isnull=True)
                    | Q(status='completed', completed_at__isnull=False, completed_by__isnull=False)
                ),
                name='experiment_completion_consistent',
            ),
        ]

    @property
    def is_locked(self):
        return self.status == self.Status.COMPLETED

    def __str__(self):
        return self.title


class ExperimentShare(models.Model):
    """Grants a member (also outside the working group) read or edit access to one experiment."""
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE, related_name='shares')
    member = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='experiment_shares')
    level = models.CharField(max_length=4, choices=AccessLevel.choices, default=AccessLevel.READ)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, editable=False, on_delete=models.PROTECT, related_name='+'
    )

    history = HistoricalRecords()

    class Meta:
        constraints = [models.UniqueConstraint(fields=['experiment', 'member'], name='experiment_share_unique_member')]

    def __str__(self):
        return f"{self.experiment} -> {self.member} ({self.level})"


class Entry(TrackedModel):
    class Kind(models.TextChoices):
        PROCEDURE = 'procedure', 'procedure'
        OBSERVATION = 'observation', 'observation'
        RESULT = 'result', 'result'
        NOTE = 'note', 'note'
        CORRECTION = 'correction', 'correction'

    experiment = models.ForeignKey(Experiment, on_delete=models.PROTECT, related_name='entries')
    kind = models.CharField(max_length=12, choices=Kind.choices)
    content = models.TextField()
    # corrections reference the entry they correct and must state why
    corrects = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.PROTECT, related_name='corrections'
    )
    reason = models.TextField(blank=True)

    history = HistoricalRecords()

    class Meta:
        ordering = ['created_at', 'id']
        verbose_name_plural = 'entries'
        constraints = [
            models.CheckConstraint(
                condition=(
                    (Q(kind='correction') & Q(corrects__isnull=False) & ~Q(reason=''))
                    | (~Q(kind='correction') & Q(corrects__isnull=True))
                ),
                name='entry_correction_has_target_and_reason',
            ),
        ]

    def __str__(self):
        return f"{self.experiment}: {self.kind} #{self.pk}"


class MaterialUsage(TrackedModel):
    """
    Ledger of material taken from an inventory container for an experiment.
    Creating a usage decrements Container.amount_left; deleting one (only while
    the experiment is a draft) restores it.
    """
    experiment = models.ForeignKey(Experiment, on_delete=models.PROTECT, related_name='materials')
    container = models.ForeignKey(Container, on_delete=models.PROTECT, related_name='usages')
    amount = models.FloatField()
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT, related_name='+')
    note = models.CharField(max_length=500, blank=True)

    history = HistoricalRecords()

    class Meta:
        ordering = ['created_at', 'id']
        constraints = [models.CheckConstraint(condition=Q(amount__gt=0), name='material_usage_amount_positive')]

    def __str__(self):
        return f"{self.amount} {self.unit.symbol} of {self.container} for {self.experiment}"


class PrivateMediaStorage(LazyObject):
    """
    File storage outside MEDIA_ROOT: nginx never serves these files directly.
    Downloads go through the permission-checked API view (projects.views).
    """
    def _setup(self):
        self._wrapped = FileSystemStorage(location=settings.PRIVATE_MEDIA_ROOT, base_url=None)


private_storage = PrivateMediaStorage()


def attachment_path(instance, filename):
    # server-generated name: user-supplied names never become paths
    return f"attachments/{instance.experiment_id}/{instance.id}"


class Attachment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    experiment = models.ForeignKey(Experiment, on_delete=models.PROTECT, related_name='attachments')
    entry = models.ForeignKey(Entry, null=True, blank=True, on_delete=models.PROTECT, related_name='attachments')
    file = models.FileField(storage=private_storage, upload_to=attachment_path, max_length=255)
    original_name = models.CharField(max_length=255)
    content_type = models.CharField(max_length=100)
    size = models.BigIntegerField()
    sha256 = models.CharField(max_length=64)
    description = models.CharField(max_length=500, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='+')

    history = HistoricalRecords()

    class Meta:
        ordering = ['uploaded_at']
        constraints = [models.CheckConstraint(condition=Q(size__gte=0), name='attachment_size_non_negative')]

    @staticmethod
    def checksum(uploaded_file):
        digest = hashlib.sha256()
        for chunk in uploaded_file.chunks():
            digest.update(chunk)
        uploaded_file.seek(0)
        return digest.hexdigest()

    def __str__(self):
        return self.original_name
