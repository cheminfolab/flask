from rest_framework.serializers import ModelSerializer
from .models import *


class StorageSerializer(ModelSerializer):
    class Meta:
        model = Storage
        exclude = ['id']
