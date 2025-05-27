from django.http import JsonResponse
from django.conf import settings
from datetime import timedelta
from django.utils import timezone

from rest_framework import generics, status, viewsets, serializers
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action, api_view
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from app_auth.serializers import LoginSerializer, RegistrationSerializer
from app_auth.base_auth import CookieJWTAuthentication

from .models import CustomUser, SellerApplication
from .serializers import UserSerializer, PublicUserSerializer, SellerApplicationSerializer


class UserList(viewsets.ReadOnlyModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


class UserProfile(viewsets.ReadOnlyModelViewSet):  # Только для чтения (GET-запросы)
    serializer_class = PublicUserSerializer
    queryset = CustomUser.objects.all()
    lookup_field = 'id'  # Будем искать по `id`

    def get_queryset(self):
        user_id = self.kwargs.get('id')  # Получаем ID из URL
        if user_id:
            return CustomUser.objects.filter(id=user_id)  # Возвращаем конкретного пользователя
        return CustomUser.objects.none()  # Если ID нет, вернём пустой QuerySet


class GetUserRoleView(APIView):
    permission_classes = [IsAuthenticated]  # Только для аутентифицированных пользователей
    authentication_classes = [CookieJWTAuthentication]  # Используем JWT для аутентификации

    def get(self, request):
        user = request.user  # Получаем аутентифицированного пользователя

        # Если поле role - это объект, то возвращаем его строковое представление
        role = str(user.role) if user.role else "No Role"

        return Response({"role": role})  # Возвращаем роль как строку


class MyAccount(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [CookieJWTAuthentication]  # Используем кастомную аутентификацию

    def get_queryset(self):
        return CustomUser.objects.filter(id=self.request.user.id)

    @action(detail=False, methods=['GET'], url_path='profile')
    def profile(self, request):
        user = self.request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data)


@api_view(['POST'])
def logout(request):
    # Создаем ответ
    response = JsonResponse({'message': 'Logged out successfully'})

    # Удаляем все cookies, установленные для текущего домена
    for cookie in request.COOKIES:
        response.delete_cookie(cookie, path='/')  # Удаляем куку по имени

    return response

class SellerApplicationCreateView(generics.CreateAPIView):
    queryset = SellerApplication.objects.all()
    serializer_class = SellerApplicationSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [CookieJWTAuthentication]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class SellerApplicationDetailView(generics.RetrieveAPIView):
    queryset = SellerApplication.objects.all()
    serializer_class = SellerApplicationSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [CookieJWTAuthentication]

    def get_queryset(self):
        # Ограничим просмотр: пользователь видит только свою заявку
        return self.queryset.filter(user=self.request.user)