from django.utils import timezone
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from api.views import BaseModelViewSet

from .models import Component, Compound, Container, Substance, Unit
from .permissions import IsOwnerOrEditFieldOnly
from .serializers import (
    ComponentSerializer, CompoundDetailSerializer, CompoundListSerializer, CompoundSerializer,
    ContainerSerializer, SubstanceSerializer, UnitSerializer,
)


class UnitViewSet(BaseModelViewSet):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer


class SubstanceViewSet(BaseModelViewSet):
    queryset = Substance.objects.all()
    serializer_class = SubstanceSerializer


class ComponentViewSet(BaseModelViewSet):
    queryset = Component.objects.select_related('substance')
    serializer_class = ComponentSerializer


class CompoundViewSet(BaseModelViewSet):
    queryset = Compound.objects.all()
    serializer_class = CompoundSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action == 'list':
            return queryset.prefetch_related('substances', 'categories')
        if self.action == 'retrieve':
            return queryset.prefetch_related(
                'substances', 'categories', 'containers',
                'ghs__hazard_classes__pictogram', 'ghs__H', 'ghs__P',
            )
        return queryset

    def get_serializer_class(self):
        if self.action == 'list':
            return CompoundListSerializer
        if self.action == 'retrieve':
            return CompoundDetailSerializer
        return CompoundSerializer


class ContainerViewSet(BaseModelViewSet):
    queryset = Container.objects.all()
    serializer_class = ContainerSerializer

    def get_permissions(self):
        if self.action in ('list', 'retrieve', 'download_csv_template'):
            permission_classes = [IsAuthenticated]
        # todo: add permissions for create method (based on role)
        elif self.action in ('update', 'partial_update'):
            permission_classes = [IsAuthenticated, IsOwnerOrEditFieldOnly]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def perform_update(self, serializer):
        # Usage is recorded by the server, never taken from the client.
        if 'amount_left' in serializer.validated_data:
            super().perform_update(serializer, last_user=self.request.user, last_used=timezone.localdate())
        else:
            super().perform_update(serializer)
