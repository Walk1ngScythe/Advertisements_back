from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import F
from app_auth.base_auth import CookieJWTAuthentication
from .models import Bb, Rubric, BbImage
from .serializers import BbSerializer, RubricSerializer, BbImageSerializer
from .filtres import AdvFilter
from rest_framework.exceptions import PermissionDenied, NotFound, ValidationError


class BbViewSet(viewsets.ModelViewSet):
    serializer_class = BbSerializer
    queryset = Bb.objects.all()
    http_method_names = ['get', 'post', 'delete']  # Разрешаем GET и POST
    filter_backends = [DjangoFilterBackend]
    filterset_class = AdvFilter
    pagination_class = None
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Bb.objects.all()
        author_id = self.request.GET.get('author', None)
        if author_id and author_id.isdigit():
            queryset = queryset.filter(author_id=int(author_id))

        return queryset

    def retrieve(self, request, *args, **kwargs):
        """Увеличиваем просмотры при получении объекта"""
        instance = self.get_object()
        Bb.objects.filter(id=instance.id).update(views=F('views') + 1)
        instance.refresh_from_db()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        user = request.user
        if not user or not user.is_authenticated:
            raise ValidationError("Вы не авторизованы")

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=user)  # ← вот здесь передаём автора
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        try:
            bb = self.get_object()
        except Bb.DoesNotExist:
            raise NotFound("Объявление не найдено")

        user = request.user
        is_admin = user.role and user.role.name.lower() == 'администратор'

        if bb.author != user and not is_admin:
            raise PermissionDenied("Вы не можете удалить это объявление")

        bb.is_deleted = True
        bb.save()

        return Response({'detail': 'Объявление логически удалено'}, status=status.HTTP_200_OK)

class RubricViewSet(viewsets.ModelViewSet):
    serializer_class = RubricSerializer
    queryset = Rubric.objects.all()
    http_method_names = ['get']

class BbImageViewSet(viewsets.ModelViewSet):
    serializer_class = BbImageSerializer
    queryset = BbImage.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [CookieJWTAuthentication]

    def perform_create(self, serializer):
        bb_id = self.request.data.get('bb')
        print("DATA:", self.request.data)  # DEBUG!
        if not Bb.objects.filter(id=bb_id).exists():
            raise ValidationError("Объявление не найдено")
        serializer.save()

