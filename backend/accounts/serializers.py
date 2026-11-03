from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.serializers import ModelSerializer, ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import *


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims:
        token['email'] = user.email

        return token


class WorkingGroupSerializer(ModelSerializer):
    class Meta:
        model = WorkingGroup
        fields = ('id', 'name')


class RoleSerializer(ModelSerializer):
    class Meta:
        model = Role
        fields = ('id', 'name')


class MemberSerializer(ModelSerializer):
    class Meta:
        model = Member
        fields = ['id', 'first_name', 'last_name', 'email', 'password', 'working_group', 'roles']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_password(self, value):
        try:
            validate_password(value, user=self.instance)
        except DjangoValidationError as error:
            raise ValidationError(list(error.messages))
        return value

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        roles = validated_data.pop('roles', [])
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        else:
            instance.set_unusable_password()
        instance.save()
        instance.roles.set(roles)
        return instance

    def update(self, instance, validated_data):
        # never store the raw value: hash it
        password = validated_data.pop('password', None)
        instance = super().update(instance, validated_data)
        if password is not None:
            instance.set_password(password)
            instance.save(update_fields=['password'])
        return instance


class MemberDirectorySerializer(ModelSerializer):
    """Public-within-the-app member listing: names and group only, no contact data."""
    class Meta:
        model = Member
        fields = ['id', 'first_name', 'last_name', 'working_group']
        read_only_fields = fields


class RegistrationSerializer(ModelSerializer):
    """
    Public self-registration. Only personal fields are accepted: working group,
    roles and staff flags are assigned by an admin. Accounts are created
    inactive and must be activated by an admin before they can log in.
    """
    class Meta:
        model = Member
        fields = ['id', 'first_name', 'last_name', 'email', 'password', 'is_active']
        read_only_fields = ['id', 'is_active']
        extra_kwargs = {
            'password': {'write_only': True, 'style': {'input_type': 'password'}},
            'first_name': {'required': True, 'allow_blank': False},
            'last_name': {'required': True, 'allow_blank': False},
        }

    def validate(self, attrs):
        # Run Django's AUTH_PASSWORD_VALIDATORS, including the similarity check
        # against the user's own name and email.
        candidate = Member(**{k: v for k, v in attrs.items() if k != 'password'})
        try:
            validate_password(attrs['password'], user=candidate)
        except DjangoValidationError as error:
            raise ValidationError({'password': list(error.messages)})
        return attrs

    def create(self, validated_data):
        return Member.objects.create_user(is_active=False, **validated_data)

