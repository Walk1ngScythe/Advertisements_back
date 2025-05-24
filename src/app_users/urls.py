from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import MyAccount, UserList, UserProfile

router = DefaultRouter()

router.register(r'users/my-profile', MyAccount, basename='user')
router.register(r'users/list', UserList, basename='list')

urlpatterns = router.urls + [
    path('users/profile/<int:id>/', UserProfile.as_view({'get': 'list'}), name='user-profile'),
]