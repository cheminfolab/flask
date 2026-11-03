from api.views import BaseModelViewSet

from .models import Building, Storage
from .serializers import BuildingSerializer, StorageSerializer


class BuildingViewSet(BaseModelViewSet):
    # Permissions: inherited ReadOnlyOrAdmin (authenticated read, staff write).
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer


class StorageViewSet(BaseModelViewSet):
    queryset = Storage.objects.select_related('room__building')
    serializer_class = StorageSerializer
