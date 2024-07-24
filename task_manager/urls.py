from .views import (
    UserViewset,
    UserRegistrationView,
    TaskViewset,
    TagViewset,
    CategoryViewset,
)

from django.urls import include, path

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'users', UserViewset, basename='user')
router.register(r'tasks', TaskViewset, basename='task')
router.register(r'categories', CategoryViewset, basename='category')
router.register(r'tags', TagViewset, basename='tag'),

urlpatterns = [
    path('', include(router.urls)),
    path('register/', UserRegistrationView.as_view(), name='user-register')
]
