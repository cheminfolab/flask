from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import *


# Register your models here.

class CustomUserAdmin(UserAdmin):
    model = User
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm

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
admin.site.register(User, CustomUserAdmin)
