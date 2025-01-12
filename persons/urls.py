# persons/urls.py
from rest_framework.routers import DefaultRouter
from .views import UserList, UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')


urlpatterns = router.urls
