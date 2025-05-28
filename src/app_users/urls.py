from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import MyAccount, UserList, UserProfile, SellerApplicationCreateView, SellerApplicationDetailView, \
    UserProfileEditViewSet

router = DefaultRouter()

router.register(r'users/my-profile', MyAccount, basename='user')
router.register(r'users/list', UserList, basename='list')
router.register(r'users/edit', UserProfileEditViewSet, basename='user-profile-edit')

urlpatterns = router.urls + [
    path('users/profile/<int:id>/', UserProfile.as_view({'get': 'list'}), name='user-profile'),
    path('applications/create/', SellerApplicationCreateView.as_view(), name='create-application'),
    path('applications/<int:pk>/', SellerApplicationDetailView.as_view(), name='detail-application'),
]