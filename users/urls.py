# users/urls.py
from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import UserList, auth, MyAccount, logout

router = DefaultRouter()

# Регистрация MyAccount через DefaultRouter
router.register(r'users/profile', MyAccount, basename='user')

urlpatterns = router.urls + [
    path('auth/', auth.as_view(), name='login'),
    path('auth/logout/', logout, name='logout'),
]
