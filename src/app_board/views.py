from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import F

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied, NotFound, ValidationError

from app_auth.base_permissions import BaseEditViewSet
from app_auth.base_auth import CookieJWTAuthentication
from app_users.models import CustomUser

from .models import Bb, Rubric, BbImage
from .serializers import BbSerializer, RubricSerializer, BbImageSerializer
from .filtres import AdvFilter


class BbViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = BbSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AdvFilter
    pagination_class = None
    queryset = Bb.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        author_id = self.request.GET.get('author')
        if author_id and author_id.isdigit():
            queryset = queryset.filter(author_id=int(author_id))
        return queryset

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        Bb.objects.filter(id=instance.id).update(views=F('views') + 1)
        instance.refresh_from_db()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class BbEditViewSet(BaseEditViewSet):
    authentication_classes = [CookieJWTAuthentication]
    queryset = Bb.objects.all()
    serializer_class = BbSerializer

    def perform_create(self, serializer):
        user = self.request.user
        if not user or not user.is_authenticated:
            raise ValidationError("Вы не авторизованы")
        serializer.save(author=user)

    def perform_destroy(self, instance):
        # Проверка прав делегируется AuthorOrAdminPermission
        instance.is_deleted = True
        instance.save()


class RubricViewSet(viewsets.ModelViewSet):
    serializer_class = RubricSerializer
    queryset = Rubric.objects.all()
    http_method_names = ['get']


class BbImageViewSet(viewsets.ModelViewSet):
    serializer_class = BbImageSerializer
    queryset = BbImage.objects.all()

    def perform_create(self, serializer):
        bb_id = self.request.data.get('bb')
        print("DATA:", self.request.data)  # DEBUG!
        if not Bb.objects.filter(id=bb_id).exists():
            raise ValidationError("Объявление не найдено")
        serializer.save()
