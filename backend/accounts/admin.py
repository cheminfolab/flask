from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import Group
from .forms import MemberCreationForm, MemberChangeForm
from .models import *


class CustomUserAdmin(UserAdmin):
    model = Member
    add_form = MemberCreationForm
    form = MemberChangeForm

    fieldsets = (
        ('Personal Info', {
            'fields': (
                'email',
                'username',
                'password',
                'first_name',
                'last_name',
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
                'groups',
                'user_permissions',
            )
        }),
        ('Important Dates', {
            'fields': (
                'last_login',
                'date_joined',
            )
        }),
    )


admin.site.register(PhoneNumber)
admin.site.register(WorkingGroup)

admin.site.unregister(Group)
admin.site.register(Role, GroupAdmin)
admin.site.register(Member, CustomUserAdmin)
