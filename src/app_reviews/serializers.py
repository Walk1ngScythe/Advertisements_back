from rest_framework import serializers
from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)  # Показываем имя автора
    seller = serializers.StringRelatedField(read_only=True)  # Показываем имя продавца

    class Meta:
        model = Review
        fields = ['id', 'seller', 'author', 'ad', 'rating', 'comment', 'created_at']
