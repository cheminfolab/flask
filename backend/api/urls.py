from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView

from accounts.views import CustomTokenObtainPairView, MemberViewSet, WorkingGroupViewSet
from locations.views import BuildingViewSet
from chemicals.views import SubstanceViewSet, CompoundViewSet, ContainerViewSet

router = routers.SimpleRouter()
router.register(r'member', MemberViewSet, basename='members')
router.register(r'group', WorkingGroupViewSet, basename='groups')
router.register(r'building', BuildingViewSet, basename='buildings')
router.register(r'substance', SubstanceViewSet, basename='substances')
router.register(r'compound', CompoundViewSet, basename='containers')
router.register(r'container', ContainerViewSet, basename='containers')

urlpatterns = [
    path('admin/', admin.site.urls),
    # API
    # path('api/group/', GroupList, name='get_groups'),
    # path('api/user/', UserList, name='get_users'),
    # path('api/user/register/', RegisterUser, name='register_user'),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include(router.urls))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
