from django.urls import path
from .views import RegistrationAPIView, LoginAPIView, CheckAuthAPIView, TokenRefreshView

urlpatterns = [

    path('users/register/', RegistrationAPIView.as_view()),
    path('users/login/', LoginAPIView.as_view()),
    path('users/check/', CheckAuthAPIView.as_view(), name='check-auth'),
    path('users/refresh/', TokenRefreshView.as_view(), name='check-auth'),

]