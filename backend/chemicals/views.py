from api.views import CustomViewSet

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .serializers import *
from .permissions import *


class UnitViewSet(CustomViewSet):
    model = Unit
    serializer_class = UnitSerializer


class SubstanceViewSet(CustomViewSet):
    model = Substance
    serializer_class = SubstanceSerializer


class ComponentViewSet(CustomViewSet):
    model = Component
    serializer_class = ComponentSerializer


class CompoundViewSet(CustomViewSet):
    model = Compound
    serializer_class = CompoundSerializer


class ContainerViewSet(CustomViewSet):
    model = Container
    serializer_class = ContainerSerializer

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAuthenticated]
        elif self.action == 'retrieve':
            permission_classes = []
        # todo: add permissions for create method (based on role)
        elif self.action == 'partial_update' or self.action == 'update':
            permission_classes = [IsAuthenticated, IsOwnerOrEditFieldOnly]
        elif self.action == 'download_csv_template':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
