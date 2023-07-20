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


class ContainerSerializer(ModelSerializer):
    # compound = CompoundSerializer(many=False)
    # location = StorageSerializer(many=False)
    # owner = WorkingGroupSerializer(many=False)

    class Meta:
        model = Container
        fields = '__all__'


class SubstanceSerializer(ModelSerializer):
    class Meta:
        model = Substance
        fields = '__all__'


class ComponentSerializer(ModelSerializer):
    class Meta:
        model = Component
        exclude = ['id']


class CompoundListSerializer(ModelSerializer):
    substances = ComponentSerializer(many=True)

    class Meta:
        model = Compound
        fields = '__all__'


class CompoundDetailSerializer(ModelSerializer):
    substances = ComponentSerializer(many=True)
    containers = ContainerSerializer(many=True)
    ghs = GHSSerializer(many=False)

    class Meta:
        model = Compound
        fields = '__all__'
