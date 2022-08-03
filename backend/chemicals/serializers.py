from rest_framework.serializers import ModelSerializer

from accounts.serializers import WorkingGroupSerializer
from locations.serializers import StorageSerializer
from ghs.serializers import GHSSerializer
from .models import *


class CurrencySerializer(ModelSerializer):
    class Meta:
        model = Currency
        exclude = ['id']


class UnitSerializer(ModelSerializer):
    class Meta:
        model = Unit
        exclude = ['id', 'type']


class SubstanceSerializer(ModelSerializer):
    mol_weight_unit = UnitSerializer(many=False)

    class Meta:
        model = Substance
        fields = '__all__'


class CompoundSerializer(ModelSerializer):
    substance = SubstanceSerializer(many=False)
    density_unit = UnitSerializer(many=False)
    ghs = GHSSerializer(many=False)

    class Meta:
        model = Compound
        fields = '__all__'


class ContainerSerializer(ModelSerializer):
    compound = CompoundSerializer(many=False)
    amount_unit = UnitSerializer(many=False)
    tara_unit = UnitSerializer(many=False)
    location = StorageSerializer(many=False)
    currency = CurrencySerializer(many=False)
    owner = WorkingGroupSerializer(many=False)

    class Meta:
        model = Container
        exclude = ['id']
