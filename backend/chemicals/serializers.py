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
        exclude = ['id']


class SubstanceSerializer(ModelSerializer):
    mol_weight_unit = UnitSerializer(many=False)

    class Meta:
        model = Substance
        fields = '__all__'


class QuantitySerializer(ModelSerializer):
    substance = SubstanceSerializer(many=False)
    unit = UnitSerializer(many=False)

    class Meta:
        model = Quantity
        fields = '__all__'


class CompoundSerializer(ModelSerializer):
    substances = QuantitySerializer(many=False)
    density_unit = UnitSerializer(many=False)
    ghs = GHSSerializer(many=False)

    class Meta:
        model = Compound
        fields = '__all__'


class ContainerSerializer(ModelSerializer):
    compound = CompoundSerializer(many=False)
    amount_unit = UnitSerializer(many=False)
    tara_unit = UnitSerializer(many=False)
    currency = CurrencySerializer(many=False)
    location = StorageSerializer(many=False)
    owner = WorkingGroupSerializer(many=False)

    class Meta:
        model = Container
        fields = '__all__'
