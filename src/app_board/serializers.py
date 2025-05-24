from rest_framework import serializers
from app_users.models import CustomUser
from app_users.serializers import CompanySerializer
from .models import Bb, Rubric, BbImage


class RubricSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rubric
        fields = '__all__'  # Все поля рубрики


class BbImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BbImage
        fields = ['id', 'bb', 'image']  # ← Должно быть 'bb' тоже


class BbAuthorSerializer(serializers.ModelSerializer):
    company = CompanySerializer(many=False, read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'rating', 'company', 'avatar',
                  'phone_number']  # Информация о пользователе-авторе


class BbSerializer(serializers.ModelSerializer):
    rubric = serializers.PrimaryKeyRelatedField(
        queryset=Rubric.objects.all(), write_only=True
    )
    rubric_info = RubricSerializer(source='rubric', read_only=True)

    images = BbImageSerializer(many=True, read_only=True)
    author = BbAuthorSerializer(read_only=True)

    class Meta:
        model = Bb
        fields = [
            'id', 'title', 'content', 'price', 'published',
            'rubric', 'rubric_info', 'main_image', 'images',
            'author', 'views', 'is_deleted'  # добавлено
        ]
        read_only_fields = ['views', 'author', 'is_deleted']  # если нельзя редактировать
