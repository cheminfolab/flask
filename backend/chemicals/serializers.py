from rest_framework.serializers import ModelSerializer

from accounts.serializers import WorkingGroupSerializer
from locations.serializers import StorageSerializer
from .models import *


class CurrencySerializer(ModelSerializer):
    class Meta:
        model = Currency
        exclude = ['id']


class UnitSerializer(ModelSerializer):
    class Meta:
        model = Unit
        exclude = ['id', 'type']


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
