from django.contrib import admin
from django.core.exceptions import PermissionDenied
from simple_history.admin import SimpleHistoryAdmin

from .models import Attachment, Entry, Experiment, ExperimentShare, MaterialUsage, Project, ProjectShare


class ReadOnlyHistoryAdmin(SimpleHistoryAdmin):
    """
    Notebook records are read-only in the admin: admins may inspect records and
    their history but not change them (changes go through the API, which
    enforces authorship, sharing and the completion lock).
    """
    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def history_form_view(self, request, object_id, version_id, extra_context=None):
        # Viewing old versions is fine; reverting is a change. simple-history saves a
        # POST to this view after checking only *view* permission, so refuse it here.
        if request.method == 'POST':
            raise PermissionDenied
        return super().history_form_view(request, object_id, version_id, extra_context)


@admin.register(Project)
class ProjectAdmin(ReadOnlyHistoryAdmin):
    list_display = ('title', 'owner', 'working_group', 'created_at')
    search_fields = ('title',)


@admin.register(Experiment)
class ExperimentAdmin(ReadOnlyHistoryAdmin):
    list_display = ('title', 'project', 'owner', 'status', 'created_at', 'completed_at')
    list_filter = ('status',)
    search_fields = ('title',)


@admin.register(Entry)
class EntryAdmin(ReadOnlyHistoryAdmin):
    list_display = ('experiment', 'kind', 'created_by', 'created_at')
    list_filter = ('kind',)


@admin.register(MaterialUsage)
class MaterialUsageAdmin(ReadOnlyHistoryAdmin):
    list_display = ('experiment', 'container', 'amount', 'unit', 'created_by', 'created_at')


@admin.register(Attachment)
class AttachmentAdmin(ReadOnlyHistoryAdmin):
    list_display = ('original_name', 'experiment', 'size', 'sha256', 'uploaded_by', 'uploaded_at')
    exclude = ('file',)  # never link the stored path; download through the API


admin.site.register(ProjectShare, ReadOnlyHistoryAdmin)
admin.site.register(ExperimentShare, ReadOnlyHistoryAdmin)
