from rest_framework.authentication import BaseAuthentication
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.exceptions import AuthenticationFailed
from users.models import CustomUser  # Импорт модели пользователя

class CookieJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        access_token = request.COOKIES.get('access_token')  # Достаем токен из куков
        if not access_token:
            return None  # Токен не найден, а значит, пользователь не аутентифицирован

        try:
            payload = AccessToken(access_token)  # Расшифровываем токен
            user = CustomUser.objects.get(id=payload['user_id'])  # Ищем пользователя в базе
        except Exception as e:
            raise AuthenticationFailed('Invalid token')

        return (user, None)  # Возвращаем пользователя (а второе значение — токен, но он не нужен)
