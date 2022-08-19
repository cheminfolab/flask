from rest_framework.serializers import ModelSerializer
from .models import *


class BuildingSerializer(ModelSerializer):
    class Meta:
        model = Building
        fields = '__all__'


class StorageSerializer(ModelSerializer):
    class Meta:
        model = Storage
        exclude = ['id']
