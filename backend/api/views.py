from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import SubstanceSerializer, CompoundSerializer, RegisterUserSerializer, MyTokenObtainPairSerializer
from chemicals.models import Substance, Compound


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def CompoundList(request):
    queryset = Compound.objects.all()
    serializer = CompoundSerializer(queryset, many=True)
    return Response(serializer.data)

# todo: add detailed view


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def SubstanceList(request):
    queryset = Substance.objects.all()
    serializer = SubstanceSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([])
def RegisterUser(request):
    serializer = RegisterUserSerializer(data=request.data)
    if serializer.is_valid():
        newuser = serializer.save()
        if newuser:
            pass
    return Response(serializer.data)



