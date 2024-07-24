from django.contrib import admin
from django.urls import path, include

from oauth2_provider import urls as oauth2_urls

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include('task_manager.urls')),
    path(
        'api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path(
        'api/token-refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'
    ),
]
