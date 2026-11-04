from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import *


class BuildingSerializer(ModelSerializer):
    class Meta:
        model = Building
        fields = '__all__'


class StorageSerializer(ModelSerializer):
    label = SerializerMethodField()

    class Meta:
        model = Storage
        fields = '__all__'

    def get_label(self, obj) -> str:
        return str(obj)
