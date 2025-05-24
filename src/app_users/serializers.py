from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import CustomUser, Role, Company
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    company = CompanySerializer(many=False, read_only=True)
    role = RoleSerializer(many=False, read_only=True)  # Сериализация роли

    class Meta:
        model = CustomUser
        fields = ['id',
                  'first_name', 'last_name', 'phone_number', 'email', 'registration_date',
                  'rating', 'avatar', 'company', 'role'
                  ]
        read_only_fields = 'token'


class PublicUserSerializer(serializers.ModelSerializer):
    company = CompanySerializer(many=False, read_only=True)

    class Meta:
        model = CustomUser
        fields = [
            'first_name', 'last_name', 'phone_number', 'email',
            'registration_date', 'rating', 'avatar', 'company'
        ]
