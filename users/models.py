from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)


class CustomUserManager(BaseUserManager):
    def create_user(self, email, phone_number, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        if not phone_number:
            raise ValueError('Users must have a phone number')

        user = self.model(
            email=self.normalize_email(email),
            phone_number=phone_number,
            **extra_fields
        )
        user.set_password(password)  # Хешируем пароль
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, phone_number, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    phone_number = models.CharField(max_length=15, unique=True, verbose_name="Телефон")
    email = models.EmailField(unique=True, verbose_name="Электронная почта")
    registration_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата регистрации")
    rating = models.FloatField(verbose_name='Рейтинг', default=0)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name="Аватар")
    role = models.ForeignKey('Role', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Роль")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    company = models.ForeignKey('Company', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Компания")

    USERNAME_FIELD = 'phone_number'  # Используем номер телефона в качестве имени пользователя
    REQUIRED_FIELDS = ['email']  # Остальные обязательные поля при создании суперпользователя

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.phone_number})"

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Role(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Роль")
    description = models.TextField(blank=True, verbose_name="Описание роли")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Роль"
        verbose_name_plural = "Роли"


class Company(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Компания")
    description = models.TextField(blank=True, verbose_name="Описание компании")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Компания"
        verbose_name_plural = "Компании"

class Review(models.Model):
    seller = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="reviews_received", verbose_name="Продавец")
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="reviews_written", verbose_name="Автор отзыва")
    ad = models.ForeignKey('bboard.Bb', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Объявление")  # Строка вместо прямого импорта
    rating = models.PositiveSmallIntegerField(verbose_name="Оценка", choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField(verbose_name="Комментарий")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата отзыва")

    def __str__(self):
        return f"Отзыв от {self.author} для {self.seller} - {self.rating}⭐"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ['-created_at']
