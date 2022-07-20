from django.conf import settings
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from chemicals.models import *
from accounts.models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class WorkingGroupSerializer(ModelSerializer):
    class Meta:
        model = WorkingGroup
        fields = ('name',)


class CurrencySerializer(ModelSerializer):
    class Meta:
        model = Currency
        exclude = ['id']


class UnitSerializer(ModelSerializer):
    class Meta:
        model = Unit
        exclude = ['id', 'type']


class StorageSerializer(ModelSerializer):
    class Meta:
        model = Storage
        exclude = ['id']


class ContainerSerializer(ModelSerializer):
    amount_unit = UnitSerializer(many=False)
    tara_unit = UnitSerializer(many=False)
    location = StorageSerializer(many=False)
    class Meta:
        model = Container
        exclude = ['id']


class SubstanceSerializer(ModelSerializer):
    mol_weight_unit = UnitSerializer(many=False)

    class Meta:
        model = Substance
        fields = '__all__'


class CompoundSerializer(ModelSerializer):
    substance = SubstanceSerializer(many=False)
    container = ContainerSerializer(many=False)
    density_unit = UnitSerializer(many=False)
    currency = CurrencySerializer(many=False)
    owner = WorkingGroupSerializer(many=False)

    class Meta:
        model = Compound
        fields = '__all__'


# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username

        return token
