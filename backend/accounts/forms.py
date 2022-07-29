from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django.contrib.admin.widgets import FilteredSelectMultiple

from locations.models import Room, PhoneNumber
from .models import *


class MemberCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    role = forms.ModelMultipleChoiceField(
        queryset=Role.objects.all(),
        required=False,
        widget=FilteredSelectMultiple(
            verbose_name='Roles',
            is_stacked=False
        )
    )
    rooms = forms.ModelMultipleChoiceField(
          queryset=Room.objects.all(),
          required=False,
          widget=FilteredSelectMultiple(
              verbose_name='Rooms',
              is_stacked=False
          )
    )
    phones = forms.ModelMultipleChoiceField(
          queryset=PhoneNumber.objects.all(),
          required=False,
          widget=FilteredSelectMultiple(
              verbose_name='Phone numbers',
              is_stacked=False
          )
    )

    class Meta:
        model = Member
        fields = '__all__'

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class MemberChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    role = forms.ModelMultipleChoiceField(
        queryset=Role.objects.all(),
        required=False,
        widget=FilteredSelectMultiple(
            verbose_name='Roles',
            is_stacked=False
        )
    )
    rooms = forms.ModelMultipleChoiceField(
          queryset=Room.objects.all(),
          required=False,
          widget=FilteredSelectMultiple(
              verbose_name='Rooms',
              is_stacked=False
          )
    )
    phones = forms.ModelMultipleChoiceField(
          queryset=PhoneNumber.objects.all(),
          required=False,
          widget=FilteredSelectMultiple(
              verbose_name='Phone numbers',
              is_stacked=False
          )
    )

    class Meta:
        model = Member
        fields = '__all__'
