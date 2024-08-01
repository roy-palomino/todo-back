from django.contrib.auth.models import User
from django.conf import settings

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import viewsets, permissions, generics, views
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework import status

from .models import Category, Tag, Task, UserSettings
from .serializers import (
    UserSettingsSerializer,
    UserSerializer,
    UserRegistrationSerializer,
    CategorySerializer,
    TagSerializer,
    TaskReadSerializer,
    TaskWriteSerializer,
)


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        refresh_token = response.data.get('refresh')
        response.set_cookie(
            key=settings.SIMPLE_JWT['AUTH_COOKIE'],
            value=refresh_token,
            httponly=True,
            secure=False,
            samesite='Lax'
        )
        del response.data['refresh']
        return response


class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        request.data['refresh'] = request.COOKIES.get(settings.SIMPLE_JWT['AUTH_COOKIE'])
        response = super().post(request, *args, **kwargs)
        if 'refresh' in response.data:
            response.set_cookie(
                key=settings.SIMPLE_JWT['AUTH_COOKIE'],
                value=response.data['refresh'],
                httponly=True,
                secure=False,
                samesite='Lax'
            )
            del response.data['refresh']
        return response


class LogoutView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        response = Response()
        response.delete_cookie(settings.SIMPLE_JWT['AUTH_COOKIE'])
        response.status_code = 204
        return response


class SettingsViewset(
    viewsets.GenericViewSet,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
):
    serializer_class = UserSettingsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        settings = UserSettings.objects.filter(user=self.request.user)
        return settings

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if queryset.exists():
            serializer = self.get_serializer(queryset.first())
            return Response(serializer.data)
        return Response(
            {'detail': 'Settings not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    # TODO: Configure updated method to allow updates without settings id

    # def update(self, request, *args, **kwargs):
    #     queryset = self.get_queryset()
    #     if queryset.exists():
    #         instance = queryset.first()
    #         serializer = self.get_serializer(instance, data=request.data, partial=True)
    #         serializer.is_valid(raise_exception=True)
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(
    #         {"detail": "No settings found."},
    #         status=status.HTTP_404_NOT_FOUND
    #     )

class UserViewset(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]


class CategoryViewset(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class TagViewset(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class TaskViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(owner=user)

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return TaskWriteSerializer
        return TaskReadSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
