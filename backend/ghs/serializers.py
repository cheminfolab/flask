from rest_framework.serializers import ModelSerializer
from .models import *


class PictogramSerializer(ModelSerializer):
    class Meta:
        model = Pictogram
        exclude = ['id']


class HazardClassSerializer(ModelSerializer):
    pictogram = PictogramSerializer(many=False)

    class Meta:
        model = HazardClass
        exclude = ['id']


class HazardStatementSerializer(ModelSerializer):
    class Meta:
        model = HazardStatement
        exclude = ['id']


class PrecautionaryStatementSerializer(ModelSerializer):
    class Meta:
        model = PrecautionaryStatement
        exclude = ['id']


class GHSSerializer(ModelSerializer):
    hazard_classes = HazardClassSerializer(many=True)
    H = HazardStatementSerializer(many=True)
    P = PrecautionaryStatementSerializer(many=True)

    class Meta:
        model = GHS
        exclude = ['id']
