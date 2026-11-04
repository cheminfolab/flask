"""
Notebook API. Access rules live in projects/access.py; the record-lock rules
are enforced here:

- draft experiment: editors may change it, its entries, materials and attachments
- completed experiment: read-only; editors may only add correction entries
- experiments are never deleted through the API
"""
import mimetypes

from django.conf import settings
from django.db import transaction
from django.http import FileResponse, HttpResponse
from django.utils import timezone
from django.utils.http import content_disposition_header
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import APIException, NotFound, PermissionDenied, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.views import ProvenanceMixin
from chemicals.models import Container

from . import access
from .models import Attachment, Entry, Experiment, ExperimentShare, MaterialUsage, Project, ProjectShare
from .serializers import (
    AttachmentSerializer, EntrySerializer, ExperimentSerializer, ExperimentShareSerializer,
    MaterialUsageSerializer, ProjectSerializer, ProjectShareSerializer,
)


class RecordLocked(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = 'The experiment is completed and locked. Record changes as correction entries.'
    default_code = 'locked'


def _require_edit(user, experiment):
    if not access.can_edit_experiment(user, experiment):
        raise PermissionDenied('You do not have edit access to this experiment.')


def _require_draft(experiment):
    if experiment.is_locked:
        raise RecordLocked()


def _readable_experiment_or_400(user, experiment, field='experiment'):
    # unreadable experiments are reported like unknown ids, so ids cannot be probed
    if not access.can_read_experiment(user, experiment):
        raise ValidationError({field: [f'Invalid pk "{experiment.pk}" - object does not exist.']})


class ProjectViewSet(ProvenanceMixin, viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):  # OpenAPI generation has no real user
            return Project.objects.none()
        return access.readable_projects(Project.objects.all(), self.request.user)

    def perform_create(self, serializer):
        user = self.request.user
        super().perform_create(serializer, owner=user, working_group=user.working_group)

    def perform_update(self, serializer):
        if not access.can_edit_project(self.request.user, serializer.instance):
            raise PermissionDenied('You do not have edit access to this project.')
        super().perform_update(serializer)

    def perform_destroy(self, instance):
        if instance.owner_id != self.request.user.id:
            raise PermissionDenied('Only the project owner can delete a project.')
        instance.delete()  # PROTECT: projects with experiments answer 409


class ExperimentViewSet(ProvenanceMixin, viewsets.ModelViewSet):
    serializer_class = ExperimentSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'put', 'patch', 'head', 'options']  # no DELETE: records are kept

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Experiment.objects.none()
        queryset = access.readable_experiments(Experiment.objects.all(), self.request.user)
        project = self.request.query_params.get('project')
        if project:
            queryset = queryset.filter(project_id=project)
        return queryset

    def perform_create(self, serializer):
        user = self.request.user
        project = serializer.validated_data['project']
        if not access.readable_projects(Project.objects.filter(pk=project.pk), user).exists():
            raise ValidationError({'project': [f'Invalid pk "{project.pk}" - object does not exist.']})
        if not access.can_edit_project(user, project):
            raise PermissionDenied('You do not have edit access to this project.')
        super().perform_create(serializer, owner=user, working_group=user.working_group)

    def perform_update(self, serializer):
        _require_edit(self.request.user, serializer.instance)
        _require_draft(serializer.instance)
        super().perform_update(serializer)

    @extend_schema(request=None)
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """Lock the experiment. Only the author can do this; it cannot be undone."""
        experiment = self.get_object()
        if experiment.owner_id != request.user.id:
            raise PermissionDenied('Only the author can complete an experiment.')
        _require_draft(experiment)
        experiment.status = Experiment.Status.COMPLETED
        experiment.completed_at = timezone.now()
        experiment.completed_by = request.user
        experiment.updated_by = request.user
        experiment.save()
        return Response(self.get_serializer(self.get_queryset().get(pk=experiment.pk)).data)


class _ShareViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """Shares are visible to everyone who can read the target; only its owner manages them."""
    permission_classes = [IsAuthenticated]
    target_field = None  # 'project' or 'experiment'

    def readable_targets(self):
        raise NotImplementedError

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return self.serializer_class.Meta.model.objects.none()
        queryset = self.serializer_class.Meta.model.objects.filter(
            **{f'{self.target_field}__in': self.readable_targets().values('pk')}
        ).order_by('pk')
        target = self.request.query_params.get(self.target_field)
        if target:
            queryset = queryset.filter(**{f'{self.target_field}_id': target})
        return queryset

    def _require_owner(self, target):
        if not self.readable_targets().filter(pk=target.pk).exists():
            raise ValidationError({self.target_field: [f'Invalid pk "{target.pk}" - object does not exist.']})
        if target.owner_id != self.request.user.id:
            raise PermissionDenied(f'Only the {self.target_field} owner can manage shares.')

    def perform_create(self, serializer):
        target = serializer.validated_data[self.target_field]
        self._require_owner(target)
        if serializer.validated_data['member'].id == target.owner_id:
            raise ValidationError({'member': ['The owner already has full access.']})
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        self._require_owner(getattr(serializer.instance, self.target_field))
        new_target = serializer.validated_data.get(self.target_field)
        if new_target is not None and new_target != getattr(serializer.instance, self.target_field):
            raise ValidationError({self.target_field: ['A share cannot be moved.']})
        serializer.save()

    def perform_destroy(self, instance):
        self._require_owner(getattr(instance, self.target_field))
        instance.delete()


class ProjectShareViewSet(_ShareViewSet):
    serializer_class = ProjectShareSerializer
    target_field = 'project'

    def readable_targets(self):
        return access.readable_projects(Project.objects.all(), self.request.user)


class ExperimentShareViewSet(_ShareViewSet):
    serializer_class = ExperimentShareSerializer
    target_field = 'experiment'

    def readable_targets(self):
        return access.readable_experiments(Experiment.objects.all(), self.request.user)


class _ExperimentContentMixin:
    """Common queryset filtering for objects that belong to one experiment."""
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return self.model.objects.none()
        readable = access.readable_experiments(Experiment.objects.all(), self.request.user)
        queryset = self.model.objects.filter(experiment__in=readable.values('pk')).select_related('experiment')
        experiment = self.request.query_params.get('experiment')
        if experiment:
            queryset = queryset.filter(experiment_id=experiment)
        return queryset

    def _check_new(self, experiment):
        _readable_experiment_or_400(self.request.user, experiment)
        _require_edit(self.request.user, experiment)

    def _check_existing(self, instance):
        _require_edit(self.request.user, instance.experiment)
        _require_draft(instance.experiment)


class EntryViewSet(_ExperimentContentMixin, ProvenanceMixin, viewsets.ModelViewSet):
    model = Entry
    serializer_class = EntrySerializer

    def perform_create(self, serializer):
        experiment = serializer.validated_data['experiment']
        self._check_new(experiment)
        is_correction = serializer.validated_data['kind'] == Entry.Kind.CORRECTION
        if experiment.is_locked and not is_correction:
            raise RecordLocked()
        if not experiment.is_locked and is_correction:
            raise ValidationError({'kind': ['While the experiment is a draft, edit the entry instead.']})
        super().perform_create(serializer)

    def perform_update(self, serializer):
        self._check_existing(serializer.instance)
        super().perform_update(serializer)

    def perform_destroy(self, instance):
        self._check_existing(instance)
        instance.delete()  # PROTECT: entries with attachments or corrections answer 409


class MaterialUsageViewSet(_ExperimentContentMixin, ProvenanceMixin, mixins.ListModelMixin,
                           mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin,
                           viewsets.GenericViewSet):
    """No updates: correct a usage by deleting it (draft only) and recording a new one."""
    model = MaterialUsage
    serializer_class = MaterialUsageSerializer

    def perform_create(self, serializer):
        experiment = serializer.validated_data['experiment']
        self._check_new(experiment)
        _require_draft(experiment)
        amount = serializer.validated_data['amount']
        # lock the container row: concurrent usages must not overdraw it
        container = Container.objects.select_for_update().get(pk=serializer.validated_data['container'].pk)
        if container.amount_left is None:
            raise ValidationError({'container': ['The remaining amount of this container is unknown.']})
        if amount > container.amount_left:
            raise ValidationError({'amount': [f'Only {container.amount_left} left in this container.']})
        # plain arithmetic is safe: the row is locked until the transaction ends
        container.amount_left = container.amount_left - amount
        container.last_user = self.request.user
        container.last_used = timezone.localdate()
        container.updated_by = self.request.user
        container.save(update_fields=['amount_left', 'last_user', 'last_used', 'updated_by', 'updated_at'])
        super().perform_create(serializer)

    def perform_destroy(self, instance):
        self._check_existing(instance)
        container = Container.objects.select_for_update().get(pk=instance.container_id)
        container.amount_left = (container.amount_left or 0) + instance.amount
        container.updated_by = self.request.user
        container.save(update_fields=['amount_left', 'updated_by', 'updated_at'])
        instance.delete()


class AttachmentViewSet(_ExperimentContentMixin, mixins.ListModelMixin, mixins.CreateModelMixin,
                        mixins.RetrieveModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """
    Files are stored outside the public media directory and only served by
    `download`, after the same read check as the experiment.
    """
    model = Attachment
    serializer_class = AttachmentSerializer

    def perform_create(self, serializer):
        experiment = serializer.validated_data['experiment']
        self._check_new(experiment)
        _require_draft(experiment)
        upload = serializer.validated_data['file']
        name = upload.name.rsplit('/', 1)[-1][:255]
        serializer.save(
            original_name=name,
            # never trust the client's content type: derive it from the name
            content_type=mimetypes.guess_type(name)[0] or 'application/octet-stream',
            size=upload.size,
            sha256=Attachment.checksum(upload),
            uploaded_by=self.request.user,
        )

    def perform_destroy(self, instance):
        self._check_existing(instance)
        stored = instance.file
        instance.delete()
        # remove the file only once the deletion is committed (history keeps the metadata and checksum)
        transaction.on_commit(lambda: stored.storage.delete(stored.name))

    @extend_schema(responses={(200, 'application/octet-stream'): OpenApiResponse(OpenApiTypes.BINARY, description='The file, always as a download.')})
    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        attachment = self.get_object()  # 404 unless the experiment is readable
        disposition = content_disposition_header(as_attachment=True, filename=attachment.original_name)
        prefix = settings.ATTACHMENT_X_ACCEL_PREFIX
        if prefix:
            # production: nginx streams the file from an `internal` location
            response = HttpResponse(content_type=attachment.content_type)
            response['X-Accel-Redirect'] = prefix.rstrip('/') + '/' + attachment.file.name
        else:
            try:
                handle = attachment.file.open('rb')
            except FileNotFoundError:
                raise NotFound('The stored file is missing.')
            response = FileResponse(handle, content_type=attachment.content_type)
        # always download, never render: uploaded HTML/SVG must not run in the app's origin
        response['Content-Disposition'] = disposition
        response['X-Content-Type-Options'] = 'nosniff'
        response['Content-Security-Policy'] = "default-src 'none'; sandbox"
        response['X-Checksum-SHA256'] = attachment.sha256
        return response
