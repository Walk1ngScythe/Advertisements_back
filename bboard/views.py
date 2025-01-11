from rest_framework import viewsets
from rest_framework.response import Response
from .models import Bb, Rubric
from .serializers import BbSerializer, RubricSerializer


class BbViewSet(viewsets.ModelViewSet):
    serializer_class = BbSerializer
    queryset = Bb.objects.all()
    http_method_names = ['get']  # Только метод GET разрешен для этого ViewSet

    def get_queryset(self):
        query = self.request.GET.get('query', '')
        if query:
            return Bb.objects.filter(title__icontains=query)
        return Bb.objects.all()


class RubricViewSet(viewsets.ModelViewSet):
    serializer_class = RubricSerializer
    queryset = Rubric.objects.all()
    http_method_names = ['get']  # Только метод GET разрешен для этого ViewSet

