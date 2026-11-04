from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework import routers
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from accounts.views import (
    CustomTokenObtainPairView, LogoutView, MemberViewSet, RoleViewSet, ThrottledTokenRefreshView,
    WorkingGroupViewSet,
)
from .health import health
from locations.views import BuildingViewSet, StorageViewSet
from chemicals.views import UnitViewSet, SubstanceViewSet, ComponentViewSet, CompoundViewSet, ContainerViewSet
from projects.views import (
    AttachmentViewSet, EntryViewSet, ExperimentShareViewSet, ExperimentViewSet, MaterialUsageViewSet,
    ProjectShareViewSet, ProjectViewSet,
)

router = routers.SimpleRouter()
router.register("members", MemberViewSet, basename="members")
router.register("roles", RoleViewSet, basename="roles")
router.register("groups", WorkingGroupViewSet, basename="groups")
router.register("buildings", BuildingViewSet, basename="buildings")
router.register("storages", StorageViewSet, basename="storages")
router.register("units", UnitViewSet, basename="units")
router.register("substances", SubstanceViewSet, basename="substances")
router.register("components", ComponentViewSet, basename="components")
router.register("compounds", CompoundViewSet, basename="compounds")
router.register("containers", ContainerViewSet, basename="containers")
# notebook
router.register("projects", ProjectViewSet, basename="projects")
router.register("project-shares", ProjectShareViewSet, basename="project-shares")
router.register("experiments", ExperimentViewSet, basename="experiments")
router.register("experiment-shares", ExperimentShareViewSet, basename="experiment-shares")
router.register("entries", EntryViewSet, basename="entries")
router.register("materials", MaterialUsageViewSet, basename="materials")
router.register("attachments", AttachmentViewSet, basename="attachments")

# OpenAPI schema and interactive docs: admins only, via the Django admin session login
_docs = dict(authentication_classes=[SessionAuthentication, JWTAuthentication], permission_classes=[IsAdminUser])

urlpatterns = [
    # ADMIN
    path("admin/", admin.site.urls),
    # API
    path("api/token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", ThrottledTokenRefreshView.as_view(), name="token_refresh"),
    path("api/token/blacklist/", LogoutView.as_view(), name="token_blacklist"),
    path("api/health/", health, name="health"),
    path("api/schema/", SpectacularAPIView.as_view(**_docs), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema", **_docs), name="docs"),
    path("api/", include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
