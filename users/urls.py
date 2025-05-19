# users/urls.py
from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import auth, MyAccount, logout, GetUserRoleView, ReviewViewSet, UserList, UserProfile, TokenRefreshView

router = DefaultRouter()

router.register(r'users/my-profile', MyAccount, basename='user')
router.register(r'users/list', UserList, basename='list')

urlpatterns = router.urls + [
    path('users/profile/<int:id>/', UserProfile.as_view({'get': 'list'}), name='user-profile'),
    path('users/<int:seller_id>/reviews/', ReviewViewSet.as_view({'get': 'list'}), name='user-reviews'),
    path('auth/', auth.as_view(), name='login'),
    path('token-refresh/', TokenRefreshView.as_view(), name='refresh-token'),
    path('auth/logout/', logout, name='logout'),
    path('get-role/', GetUserRoleView.as_view(), name='user-role'),

]
