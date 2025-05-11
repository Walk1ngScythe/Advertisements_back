from rest_framework.routers import DefaultRouter
from .views import ComplaintViewSet, ComplaintStatusViewSet

router = DefaultRouter()
router.register(r'complaints', ComplaintViewSet, basename='complaint')
router.register(r'complaint-statuses', ComplaintStatusViewSet, basename='complaint-status')

urlpatterns = router.urls
