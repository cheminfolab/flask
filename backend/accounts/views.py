from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
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

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAuthenticated]
        elif self.action == 'register':
            permission_classes = []
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['POST'])
    def register(self, request):
        serializer = MemberSerializer(data=request.data)
        if serializer.is_valid():
            newuser = serializer.save()
            if newuser:
                # do stuff
                pass
        return Response(serializer.data)

