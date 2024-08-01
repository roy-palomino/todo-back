from django.contrib import admin
from django.urls import path, include

from task_manager.views import (
    SelfView,
    CustomTokenRefreshView,
    CustomTokenObtainPairView,
    LogoutView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include('task_manager.urls')),
    path(
        'api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path(
        'api/token/refresh/',
        CustomTokenRefreshView.as_view(),
        name='token_refresh'
    ),
    path('api/token/logout/', LogoutView.as_view(), name='logout'),
    path('api/self/', SelfView.as_view(), name='self')
]
