from rest_framework import viewsets
from rest_framework.response import Response

from .models import Bb, Rubric
from .serializers import BbSerializer, RubricSerializer
from django.db.models import Q, F


class BbViewSet(viewsets.ModelViewSet):
    serializer_class = BbSerializer
    queryset = Bb.objects.all()
    http_method_names = ['get']  # Только метод GET разрешен

    def get_queryset(self):
        query = self.request.GET.get('query', '').strip()  # Убираем пробелы
        rubric_id = self.request.GET.get('rubric', None)
        author_id = self.request.GET.get('author', None)  # Новый параметр для фильтрации по автору

        queryset = Bb.objects.all()

        # Поиск по каждому слову в запросе (регистр не учитывается)
        if query:
            words = query.split()  # Разбиваем строку на слова
            query_filter = Q()
            for word in words:
                query_filter |= Q(title__icontains=word)  # Ищем любое слово в title
            queryset = queryset.filter(query_filter)

        # Фильтрация по рубрике
        if rubric_id and rubric_id.isdigit():  # Проверяем, что rubric_id — число
            queryset = queryset.filter(rubric_id=int(rubric_id))

        # Фильтрация по автору
        if author_id and author_id.isdigit():  # Проверяем, что author_id — число
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

