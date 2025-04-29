from django.http import JsonResponse
from rest_framework import generics, status, viewsets, serializers
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.utils import timezone
from rest_framework.views import APIView
from django.utils import timezone
from datetime import timedelta
from .models import CustomUser, Review
from .serializers import UserSerializer, PublicUserSerializer, LoginSerializer, ReviewSerializer
from rest_framework.decorators import action, api_view
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from .renders import UserJSONRenderer
from .authentication import CookieJWTAuthentication  # Импорт кастомной аутентификации


class UserList(viewsets.ReadOnlyModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        seller_id = self.kwargs.get('seller_id')  # Достаем ID продавца из URL
        if seller_id:
            return Review.objects.filter(seller_id=seller_id)
        return Review.objects.all()  # Если ID не указан, отдаем все отзывы

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
    serializer_class = PublicUserSerializer
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


class TokenRefreshView(APIView):
    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')
        if not refresh_token:
            return Response({'detail': 'Refresh token not provided'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            refresh = RefreshToken(refresh_token)
            access_token = refresh.access_token
            access_token_exp = (timezone.now() + timedelta(hours=1)).isoformat()

            response = Response({
                'access_token': str(access_token),
                'access_token_exp': access_token_exp
            }, status=status.HTTP_200_OK)

            response.set_cookie(
                key='access_token',
                value=str(access_token),
                expires=timezone.now() + timedelta(hours=1),
                httponly=False,
                secure=False,  # Для разработки без HTTPS
                samesite='None',
                path='/'
            )

            response.set_cookie(
                key='refresh_token',
                value=str(refresh),
                expires=timezone.now() + timedelta(days=7),
                httponly=False,
                secure=True,
                samesite='None'
            )

            return response
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class auth(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data.get('user', {}))
        try:
            serializer.is_valid(raise_exception=True)
        except serializers.ValidationError as e:
            return Response({'error': e.detail}, status=status.HTTP_400_BAD_REQUEST)

        # Получаем пользователя из сериализатора
        user = serializer.validated_data.get('user')

        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token
        access_token_exp = (timezone.now() + timedelta(days=5)).isoformat()

        # Сохранение токенов в httpOnly cookies
        response = Response({
            'email': user.email,
            'user_id': user.id,
            'access_token_exp': access_token_exp
        }, status=status.HTTP_200_OK)

        response.set_cookie(
            key='access_token',
            value=str(access_token),
            expires=timezone.now() + timedelta(days=5),
            httponly=True,
            secure=True,
            samesite='None',
            path='/'
        )

        response.set_cookie(
            key='exp',
            value=str(access_token_exp),
            expires=timezone.now() + timedelta(days=5),
            httponly=True,
            secure=True,
            samesite='None',
            path='/'
        )

        response.set_cookie(
            key='refresh_token',
            value=str(refresh),
            expires=timezone.now() + timedelta(days=7),
            httponly=True,
            secure=True,
            samesite='None'
        )

        return response

