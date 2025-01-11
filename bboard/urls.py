from rest_framework.routers import DefaultRouter
from .views import BbViewSet, RubricViewSet

router = DefaultRouter()
router.register(r'bbs', BbViewSet, basename='bb')
router.register(r'rubrics', RubricViewSet, basename='rubric')

urlpatterns = router.urls
