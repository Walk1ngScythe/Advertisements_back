from rest_framework import viewsets
from rest_framework.response import Response
from .filtres import AdvFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import Bb, Rubric
from .serializers import BbSerializer, RubricSerializer
from django.db.models import Q, F


class BbViewSet(viewsets.ModelViewSet):
    serializer_class = BbSerializer
    queryset = Bb.objects.all()
    http_method_names = ['get']  # Только метод GET разрешен
    filter_backends = [DjangoFilterBackend]
    filterset_class = AdvFilter
    pagination_class = None

    def get_queryset(self):
        queryset = Bb.objects.all()
        author_id = self.request.GET.get('author', None)
        if author_id and author_id.isdigit():
            queryset = queryset.filter(author_id=int(author_id))
        return queryset



    def retrieve(self, request, *args, **kwargs):
        """Переопределяем метод retrieve, чтобы увеличивать просмотры"""
        instance = self.get_object()
        Bb.objects.filter(id=instance.id).update(views=F('views') + 1)  # Увеличиваем просмотры
        instance.refresh_from_db()  # Обновляем объект из БД
        serializer = self.get_serializer(instance)
        return Response(serializer.data)



class RubricViewSet(viewsets.ModelViewSet):
    serializer_class = RubricSerializer
    queryset = Rubric.objects.all()
    http_method_names = ['get']

