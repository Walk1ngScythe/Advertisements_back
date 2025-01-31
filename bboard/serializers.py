from rest_framework import serializers
from users.models import CustomUser
from users.serializers import CompanySerializer
from .models import Bb, Rubric, BbImage

class RubricSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rubric
        fields = '__all__'  # Все поля рубрики

class BbImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BbImage
        fields = ['id', 'image']  # Поля изображения

class BbAuthorSerializer(serializers.ModelSerializer):
    company = CompanySerializer(many=False, read_only=True)
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'rating','company']  # Информация о пользователе-авторе

class BbSerializer(serializers.ModelSerializer):
    rubric = RubricSerializer(many=False, read_only=True)
    images = BbImageSerializer(many=True, read_only=True)
    author = BbAuthorSerializer(many=False, read_only=True)  # Замените на правильное имя поля

    class Meta:
        model = Bb
        fields = ['id', 'title', 'content', 'price', 'published', 'rubric', 'main_image', 'images', 'author']  # Используем правильное имя поля
