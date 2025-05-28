from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import ReviewViewSet

router = DefaultRouter()


urlpatterns = router.urls + [
    path('users/<int:seller_id>/reviews/', ReviewViewSet.as_view({'get': 'list'}), name='user-reviews'),
]