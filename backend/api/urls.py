from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView

from accounts.views import CustomTokenObtainPairView, MemberViewSet, RoleViewSet, WorkingGroupViewSet
from locations.views import BuildingViewSet
from chemicals.views import UnitViewSet, SubstanceViewSet, ComponentViewSet, CompoundViewSet, ContainerViewSet

router = routers.SimpleRouter()
router.register("members", MemberViewSet, basename="members")
router.register("roles", RoleViewSet, basename="roles")
router.register("group", WorkingGroupViewSet, basename="groups")
router.register("building", BuildingViewSet, basename="buildings")
router.register("unit", UnitViewSet, basename="units")
router.register("substance", SubstanceViewSet, basename="substances")
router.register("component", ComponentViewSet, basename="components")
router.register("compound", CompoundViewSet, basename="compounds")
router.register("container", ContainerViewSet, basename="containers")

urlpatterns = [
    # ADMIN
    path("admin/", admin.site.urls),
    # API
    path("api/token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/", include(router.urls))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
