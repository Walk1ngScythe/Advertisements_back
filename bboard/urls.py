from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import BbViewSet, RubricViewSet, BbImageViewSet

router = DefaultRouter()
router.register(r'bbs', BbViewSet, basename='bb')
router.register(r'rubrics', RubricViewSet, basename='rubric')
router.register(r'images', BbImageViewSet)

urlpatterns = router.urls
