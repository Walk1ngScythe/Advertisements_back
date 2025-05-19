import django_filters
from .models import Bb

class AdvFilter(django_filters.FilterSet):
    author = django_filters.NumberFilter()
    title = django_filters.CharFilter(lookup_expr='icontains')
    is_deleted = django_filters.BooleanFilter()  # ← ЯВНО УКАЗАННОЕ ПОЛЕ

    class Meta:
        model = Bb
        fields = ['author', 'title', 'is_deleted']
