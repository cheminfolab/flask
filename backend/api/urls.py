"""api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static

from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    MyTokenObtainPairView, SubstanceList, SubstanceDetail, CompoundList, CompoundDetail,
    GroupList, UserList, RegisterUser
)

urlpatterns = [
    path('admin/', admin.site.urls),
    # API
    path('api/group/', GroupList, name='get_groups'),
    path('api/user/', UserList, name='get_users'),
    path('api/user/register/', RegisterUser, name='register_user'),
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/substance/', SubstanceList, name='get_substances'),
    path('api/substance/<int:pk>/', SubstanceDetail, name='get_substance_detail'),
    path('api/compound/', CompoundList, name='get_compounds'),
    path('api/compound/<int:pk>/', CompoundDetail, name='get_compound_detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
