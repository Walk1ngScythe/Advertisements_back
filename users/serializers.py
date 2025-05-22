from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import CustomUser, Role, Company, Review
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

class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)  # Показываем имя автора
    seller = serializers.StringRelatedField(read_only=True)  # Показываем имя продавца

    class Meta:
        model = Review
        fields = ['id', 'seller', 'author', 'ad', 'rating', 'comment', 'created_at']

class PublicUserSerializer(serializers.ModelSerializer):
    company = CompanySerializer(many=False, read_only=True)

    class Meta:
        model = CustomUser
        fields = [
            'first_name', 'last_name', 'phone_number', 'email',
            'registration_date', 'rating', 'avatar', 'company'
        ]


class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)

    def validate(self, data):
        phone_number = data.get('phone_number')
        password = data.get('password')

        if not phone_number:
            raise serializers.ValidationError({'phone_number': 'Для входа необходим номер телефона.'})

        if not password:
            raise serializers.ValidationError({'password': 'Для входа необходим пароль.'})

        # Проверка наличия пользователя
        user = authenticate(phone_number=phone_number, password=password)

        if user is None:
            # Если почта не найдена
            if not CustomUser.objects.filter(phone_number=phone_number).exists():
                raise serializers.ValidationError({'phone_number': 'Пользователь с таким адресом номером телефона не найден.'})
            # Если неправильный пароль
            raise serializers.ValidationError({'password': 'Неправильный пароль.'})

        if not user.is_active:
            raise serializers.ValidationError({'phone_number': 'Этот пользователь был деактивирован.'})

        return {'user': user}

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    avatar = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'password', 'avatar']

    def create(self, validated_data):
        from .models import Role  # Импортируем здесь, чтобы избежать проблем с зависимостями
        role = Role.objects.get_or_create(name="Покупатель")[0]

        avatar = validated_data.pop('avatar', None)  # достаём аватар, если есть

        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            phone_number=validated_data['phone_number'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            role=role,
            avatar=avatar
        )
        return user


