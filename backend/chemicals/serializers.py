from rest_framework.serializers import ModelSerializer, ValidationError

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
        fields = '__all__'


class ContainerSerializer(ModelSerializer):
    # compound = CompoundSerializer(many=False)
    # location = StorageSerializer(many=False)
    # owner = WorkingGroupSerializer(many=False)

    class Meta:
        model = Container
        fields = '__all__'
        # usage fields are assigned by the server (see ContainerViewSet.perform_update);
        # created_*/updated_* are non-editable model fields and therefore read-only too
        read_only_fields = ['last_user', 'last_used']

    def validate(self, attrs):
        # mirrors the database CheckConstraints so clients get a 400 instead of an IntegrityError
        def current(name):
            if name in attrs:
                return attrs[name]
            return getattr(self.instance, name, None)

        amount, amount_left = current('amount'), current('amount_left')
        if amount is not None and amount_left is not None and amount_left > amount:
            raise ValidationError({'amount_left': 'Cannot exceed the container amount.'})
        for name in ('amount', 'amount_left', 'tara', 'price'):
            if attrs.get(name) is not None and attrs[name] < 0:
                raise ValidationError({name: 'Must not be negative.'})
        return attrs


class StructureSerializer(ModelSerializer):
    class Meta:
        model = Structure
        fields = '__all__'


class SubstanceSerializer(ModelSerializer):
    class Meta:
        model = Substance
        fields = '__all__'


class ComponentSerializer(ModelSerializer):
    class Meta:
        model = Component
        fields = '__all__'


class CompoundSerializer(ModelSerializer):
    """Write serializer: components and categories as primary-key lists."""
    class Meta:
        model = Compound
        fields = '__all__'


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
