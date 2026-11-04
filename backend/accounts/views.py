from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model


from api.views import BaseModelViewSet
from .serializers import *


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = []


class WorkingGroupViewSet(BaseModelViewSet):
    queryset = WorkingGroup.objects.all()
    serializer_class = WorkingGroupSerializer


class RoleViewSet(BaseModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


class MemberViewSet(BaseModelViewSet):
    queryset = get_user_model().objects.prefetch_related('roles')
    serializer_class = MemberSerializer

    def get_permissions(self):
        if self.action == 'register':
            permission_classes = [AllowAny]
        elif self.action in ('me', 'directory'):
            permission_classes = [IsAuthenticated]
        else:
            # listing members exposes personal data (emails), so admins only
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['POST'], serializer_class=RegistrationSerializer)
    def register(self, request):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['GET'])
    def me(self, request):
        return Response(MemberSerializer(request.user).data)

    @action(detail=False, methods=['GET'], serializer_class=MemberDirectorySerializer)
    def directory(self, request):
        """Active members by name, for choosing whom to share a record with. No emails."""
        members = get_user_model().objects.filter(is_active=True).order_by('last_name', 'first_name')
        return Response(MemberDirectorySerializer(members, many=True).data)
