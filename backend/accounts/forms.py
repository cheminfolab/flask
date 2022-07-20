from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.admin.widgets import FilteredSelectMultiple
from locations.models import Room
from .models import *


class CustomUserCreationForm(UserCreationForm):
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
        model = User
        fields = '__all__'


class CustomUserChangeForm(UserChangeForm):
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
        model = User
        fields = '__all__'
