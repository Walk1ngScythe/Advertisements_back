from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import F
from users.authentication import CookieJWTAuthentication
from .models import Bb, Rubric
from .serializers import BbSerializer, RubricSerializer
from .filtres import AdvFilter
from rest_framework.exceptions import ValidationError


class BbViewSet(viewsets.ModelViewSet):
    serializer_class = BbSerializer
    queryset = Bb.objects.all()
    http_method_names = ['get', 'post']  # Разрешаем GET и POST
    filter_backends = [DjangoFilterBackend]
    filterset_class = AdvFilter
    pagination_class = None
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

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

class RubricViewSet(viewsets.ModelViewSet):
    serializer_class = RubricSerializer
    queryset = Rubric.objects.all()
    http_method_names = ['get']
