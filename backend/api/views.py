from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import MyTokenObtainPairSerializer
from chemicals.serializers import SubstanceSerializer, CompoundSerializer
from chemicals.models import Substance, Compound

from accounts.serializers import RegisterUserSerializer, UserSerializer
from accounts.models import Member
from accounts.permissions import CompoundUserWritePermission




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def CompoundList(request):
    queryset = Compound.objects.all()
    serializer = CompoundSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE', 'HEAD', 'OPTIONS'])
@permission_classes([CompoundUserWritePermission])
def CompoundDetail(request, pk):
    queryset = Compound.objects.get(pk=pk)
    serializer = CompoundSerializer(queryset)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def SubstanceList(request):
    queryset = Substance.objects.all()
    serializer = SubstanceSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE', 'HEAD', 'OPTIONS'])
@permission_classes([])
def SubstanceDetail(request, pk):
    queryset = Substance.objects.get(pk=pk)
    serializer = SubstanceSerializer(queryset)
    return Response(serializer.data)


# AUTHENTICATION

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

@api_view(['GET'])
@permission_classes([])
def UserList(request):
    queryset = Member.objects.all()
    serializer = UserSerializer(queryset, many=True)
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
