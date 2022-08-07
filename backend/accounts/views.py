from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model


from api.views import CustomViewSet
from .serializers import *


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = []


class WorkingGroupViewSet(CustomViewSet):
    model = WorkingGroup
    serializer_class = WorkingGroupSerializer


class MemberViewSet(CustomViewSet):
    model = Member
    serializer_class = MemberSerializer

    def get_queryset(self):
        return get_user_model().objects.all()

    # @action(detail=True, methods=['POST'])
    # def register(self, request):
    #     pass
    #
    # @action(detail=False, methods=['POST'])
    # def RegisterUser(request):
    #     serializer = RegisterMemberSerializer(data=request.data)
    #     if serializer.is_valid():
    #         newuser = serializer.save()
    #         if newuser:
    #             # do stuff
    #             pass
    #     return Response(serializer.data)
