from api.views import CustomViewSet
from .models import *
from .serializers import *


class BuildingViewSet(CustomViewSet):

    model = Building
    serializer_class = BuildingSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'list':
            permission_classes = []
        else:
            permission_classes = []  # IsAdminUser
        return [permission() for permission in permission_classes]

