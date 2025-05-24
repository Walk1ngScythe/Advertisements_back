from rest_framework import generics, status, viewsets, serializers
from .serializers import ReviewSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        seller_id = self.kwargs.get('seller_id')  # Достаем ID продавца из URL
        if seller_id:
            return Review.objects.filter(seller_id=seller_id)
        return Review.objects.all()  # Если ID не указан, отдаем все отзывы
