from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import SubstanceSerializer, CompoundSerializer, RegisterUserSerializer, UserSerializer, MyTokenObtainPairSerializer
from chemicals.models import Substance, Compound
from accounts.models import User


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


# ViewSets define the view behavior.
@permission_classes([])
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getCompounds(request):
    compounds = Compound.objects.all()
    serializer = CompoundSerializer(compounds, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getSubstances(request):
    substances = Substance.objects.all()
    serializer = SubstanceSerializer(substances, many=True)
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



