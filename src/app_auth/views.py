from django.conf import settings
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .base_auth import CookieJWTAuthentication
from .serializers import RegistrationSerializer, LoginSerializer
from adv_core.utils import build_absolute_uri


class CheckAuthAPIView(APIView):
    authentication_classes = [CookieJWTAuthentication]

    def get(self, request):
        user = request.user
        return Response({
            "user_id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "phone_number": user.phone_number,
            "role": user.role.name if user.role else None,
            "registration_date": user.registration_date,
            "rating": user.rating,
            "company": {
                "id": user.company.id,
                "name": user.company.name,
            } if user.company else None,
            "avatar": request.build_absolute_uri(user.avatar.url) if user and user.avatar else None,
        })


class TokenRefreshView(APIView):
    def post(self, request):
        refresh_token = request.COOKIES.get(settings.SIMPLE_JWT["COOKIE_SETTINGS"]["REFRESH_TOKEN"]["key"])
        if not refresh_token:
            return Response({'detail': 'Refresh token not provided'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            refresh = RefreshToken(refresh_token)
            access_token = refresh.access_token

            response = Response({"detail": "Token refreshed"}, status=status.HTTP_200_OK)
            cookie_settings = settings.SIMPLE_JWT["COOKIE_SETTINGS"]["ACCESS_TOKEN"]

            response.set_cookie(
                key=cookie_settings["key"],
                value=str(access_token),
                expires=timezone.now() + settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"],
                httponly=cookie_settings["httponly"],
                secure=cookie_settings["secure"],
                samesite=cookie_settings["samesite"],
            )

            return response
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tokens = serializer.validated_data

        response = Response(tokens, status=status.HTTP_200_OK)

        for token_type in ["ACCESS_TOKEN", "REFRESH_TOKEN"]:
            cookie_settings = settings.SIMPLE_JWT["COOKIE_SETTINGS"][token_type]
            response.set_cookie(
                key=cookie_settings["key"],
                value=tokens[cookie_settings["key"]],
                expires=timezone.now() + settings.SIMPLE_JWT[f"{token_type}_LIFETIME"],
                httponly=cookie_settings["httponly"],
                secure=cookie_settings["secure"],
                samesite=cookie_settings["samesite"],
            )

        return response


class RegistrationAPIView(APIView):
    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)