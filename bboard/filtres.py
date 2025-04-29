import django_filters
from .models import Bb

class AdvFilter(django_filters.FilterSet):
    author = django_filters.NumberFilter()

    class Meta:
        model = Bb
        fields = ['author']