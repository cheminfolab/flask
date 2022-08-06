from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    TokenObtainPairView, SubstanceList, SubstanceDetail, CompoundList, CompoundDetail,
    GroupList, UserList, RegisterUser
)
from locations.views import BuildingViewSet

router = routers.SimpleRouter()
router.register(r'building', BuildingViewSet, basename='buildings')

urlpatterns = [
    path('admin/', admin.site.urls),
    # API
    path('api/group/', GroupList, name='get_groups'),
    path('api/user/', UserList, name='get_users'),
    path('api/user/register/', RegisterUser, name='register_user'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/substance/', SubstanceList, name='get_substances'),
    path('api/substance/<int:pk>/', SubstanceDetail, name='get_substance_detail'),
    path('api/compound/', CompoundList, name='get_compounds'),
    path('api/compound/<int:pk>/', CompoundDetail, name='get_compound_detail'),
    path('api/', include(router.urls))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
