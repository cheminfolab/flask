from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import CustomTokenObtainPairSerializer
from accounts.serializers import MemberSerializer, RegisterMemberSerializer, WorkingGroupSerializer
from accounts.models import Member, WorkingGroup
from accounts.permissions import CompoundUserWritePermission

from chemicals.serializers import SubstanceSerializer, CompoundSerializer, ContainerSerializer
from chemicals.models import Substance, Compound, Container


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def CompoundList(request):
    queryset = Container.objects.all()
    serializer = ContainerSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(['GET', 'PUT', 'PATCH', 'POST', 'DELETE', 'HEAD', 'OPTIONS'])
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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def SubstanceDetail(request, pk):
    queryset = Substance.objects.get(pk=pk)
    serializer = SubstanceSerializer(queryset)
    return Response(serializer.data)


# AUTHENTICATION
# todo: use function based views
@permission_classes([])
class TokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


@api_view(['GET'])
@permission_classes([])
def GroupList(request):
    queryset = WorkingGroup.objects.all()
    serializer = WorkingGroupSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def UserList(request):
    queryset = Member.objects.all()
    serializer = MemberSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([])
def RegisterUser(request):
    serializer = RegisterMemberSerializer(data=request.data)
    if serializer.is_valid():
        newuser = serializer.save()
        if newuser:
            # todo: something missing?
            pass
    return Response(serializer.data)
