from rest_framework import serializers
from .models import Bb, Rubric

class RubricSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rubric
        fields = '__all__'  # Все поля рубрики

class BbSerializer(serializers.ModelSerializer):
    rubric = RubricSerializer(many=False, read_only=True)

    class Meta:
        model = Bb
        fields = ['id', 'title', 'content', 'price', 'published', 'rubric', 'image']  # Все поля объявления
