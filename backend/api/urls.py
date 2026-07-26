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
router.register("groups", WorkingGroupViewSet, basename="groups")
router.register("buildings", BuildingViewSet, basename="buildings")
router.register("units", UnitViewSet, basename="units")
router.register("substances", SubstanceViewSet, basename="substances")
router.register("components", ComponentViewSet, basename="components")
router.register("compounds", CompoundViewSet, basename="compounds")
router.register("containers", ContainerViewSet, basename="containers")

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
