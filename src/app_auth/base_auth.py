from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import AccessToken


class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        # Извлекаем токен из cookies
        token = request.COOKIES.get('access_token')
        if not token:
            raise AuthenticationFailed({
                "message": "401: Unauthorized",
                "code": 0
            })

        try:
            # Проверка токена с помощью стандартного механизма JWT
            access_token = AccessToken(token)
        except Exception:
            raise AuthenticationFailed({
                "message": "Токен просрочен",
                "code": 0
            })

        # делаем возврат пользователя
        return self.getUser_from_token(access_token)

    def getUser_from_token(self, access_token):
        try:
            user = self.get_user(access_token)
            return user, access_token
        except Exception as e:
            raise AuthenticationFailed({
                "message": f'Невозможно извлечь пользователя из токена: {str(e)}',
                "code": 0
            })