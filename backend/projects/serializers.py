from django.conf import settings
from django.urls import reverse
from rest_framework import serializers

from .models import Attachment, Entry, Experiment, ExperimentShare, MaterialUsage, Project, ProjectShare


class ProjectSerializer(serializers.ModelSerializer):
    can_edit = serializers.BooleanField(read_only=True)

    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ['owner', 'working_group']


class ProjectShareSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectShare
        fields = '__all__'


class ExperimentSerializer(serializers.ModelSerializer):
    can_edit = serializers.BooleanField(read_only=True)

    class Meta:
        model = Experiment
        fields = '__all__'
        read_only_fields = ['owner', 'working_group', 'status', 'completed_at', 'completed_by']

    def validate_project(self, project):
        if self.instance is not None and project != self.instance.project:
            raise serializers.ValidationError('An experiment cannot be moved to another project.')
        return project


class ExperimentShareSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExperimentShare
        fields = '__all__'


class EntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entry
        fields = '__all__'

    def validate(self, attrs):
        experiment = attrs.get('experiment', getattr(self.instance, 'experiment', None))
        if self.instance is not None:
            if 'experiment' in attrs and attrs['experiment'] != self.instance.experiment:
                raise serializers.ValidationError({'experiment': 'An entry cannot be moved to another experiment.'})
            if attrs.get('kind', self.instance.kind) != self.instance.kind and Entry.Kind.CORRECTION in (
                attrs.get('kind'), self.instance.kind
            ):
                raise serializers.ValidationError({'kind': 'Corrections cannot be converted.'})

        kind = attrs.get('kind', getattr(self.instance, 'kind', None))
        corrects = attrs.get('corrects', getattr(self.instance, 'corrects', None))
        reason = attrs.get('reason', getattr(self.instance, 'reason', ''))
        if kind == Entry.Kind.CORRECTION:
            if corrects is None:
                raise serializers.ValidationError({'corrects': 'A correction must reference the corrected entry.'})
            if not reason.strip():
                raise serializers.ValidationError({'reason': 'A correction must state a reason.'})
            if corrects.experiment_id != experiment.id:
                raise serializers.ValidationError({'corrects': 'The corrected entry belongs to another experiment.'})
        elif corrects is not None:
            raise serializers.ValidationError({'corrects': 'Only corrections reference another entry.'})
        return attrs


class MaterialUsageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialUsage
        fields = '__all__'

    def validate(self, attrs):
        container, unit, amount = attrs['container'], attrs['unit'], attrs['amount']
        if amount <= 0:
            raise serializers.ValidationError({'amount': 'Must be positive.'})
        if container.amount_unit_id is None or container.amount_unit_id != unit.id:
            # no unit conversion: the usage must be recorded in the container's unit
            raise serializers.ValidationError({'unit': 'Must match the container unit.'})
        return attrs


class AttachmentSerializer(serializers.ModelSerializer):
    file = serializers.FileField(write_only=True)
    download_url = serializers.SerializerMethodField()

    class Meta:
        model = Attachment
        fields = [
            'id', 'experiment', 'entry', 'file', 'original_name', 'content_type', 'size', 'sha256',
            'description', 'uploaded_at', 'uploaded_by', 'download_url',
        ]
        read_only_fields = ['original_name', 'content_type', 'size', 'sha256', 'uploaded_at', 'uploaded_by']

    def get_download_url(self, obj) -> str:
        return reverse('attachments-download', kwargs={'pk': obj.pk})

    def validate_file(self, file):
        if file.size > settings.ATTACHMENT_MAX_SIZE:
            limit = settings.ATTACHMENT_MAX_SIZE // (1024 * 1024)
            raise serializers.ValidationError(f'Files larger than {limit} MB are not accepted.')
        return file

    def validate(self, attrs):
        entry = attrs.get('entry')
        if entry is not None and entry.experiment_id != attrs['experiment'].id:
            raise serializers.ValidationError({'entry': 'The entry belongs to another experiment.'})
        return attrs
