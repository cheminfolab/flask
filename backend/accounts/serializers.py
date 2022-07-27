from rest_framework.serializers import ModelSerializer, HyperlinkedModelSerializer
from .models import *


class WorkingGroupSerializer(ModelSerializer):
    class Meta:
        model = WorkingGroup
        fields = ('name',)


class RegisterMemberSerializer(ModelSerializer):
    class Meta:
        model = Member
        fields = ['first_name', 'last_name', 'username', 'email', 'password', 'working_group']  # todo: add user role
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class MemberSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Member
        fields = ['url', 'username', 'email', 'is_staff']
