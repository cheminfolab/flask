from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from .forms import MemberCreationForm, MemberChangeForm
from .models import *


class MemberInline(admin.TabularInline):
    model = Member
    fields = ('email', 'last_name', 'first_name', 'rooms')
    show_change_link = True
    extra = 0

    def has_change_permission(self, request, obj=None):
        return False


class WorkingGroupAdmin(admin.ModelAdmin):
    inlines = [
        MemberInline
    ]


class MemberAdmin(UserAdmin):
    model = Member
    search_fields = ('email', 'last_name', 'first_name')
    list_display = ('email', 'last_name', 'first_name', 'is_active', 'is_staff')
    ordering = ('email',)
    add_form = MemberCreationForm
    form = MemberChangeForm

    fieldsets = [
        ('Personal Information', {
            'fields': (
                'first_name',
                'last_name',
                'email',
                'password',
                'working_group',
                'rooms',
                'phones',

            )
        }),
        ('Permissions', {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'role',
                'user_permissions',
            )
        }),
        ('Important Dates', {
            'fields': (
                'last_login',
                'date_joined',
            )
        }),
    ]
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'first_name',
                'last_name',
                'email',
                'working_group',
                'password1',
                'password2',
                'is_active',
                'is_staff',
                'is_superuser',
                'role',
                'user_permissions',
            ),
        }),
    )


admin.site.register(WorkingGroup, WorkingGroupAdmin)
# unregister Group model to use custom Role proxy model:
admin.site.unregister(Group)
admin.site.register(Role)  # , GroupAdmin)
admin.site.register(Member, MemberAdmin)
