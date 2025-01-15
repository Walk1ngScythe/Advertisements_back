# models.py для объявлений
from django.db import models
from persons.models import CustomUser  # Импортируем модель пользователя

class Bb(models.Model):
    title = models.CharField(max_length=50, verbose_name='Название')
    content = models.TextField(verbose_name='Описание')
    price = models.FloatField(verbose_name='Цена')
    published = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Опубликовано')
    rubric = models.ForeignKey('Rubric', null=True, on_delete=models.PROTECT, verbose_name='Рубрика')
    main_image = models.ImageField(upload_to='Bb_images/', null=True, blank=True, verbose_name='Изображение')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Автор')  # Добавляем автора

    class Meta:
        verbose_name_plural = 'Объявления'
        verbose_name = 'Объявление'
        ordering = ['-published']


class Rubric(models.Model):
    name = models.CharField(max_length=20, db_index=True, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Рубрики'
        verbose_name = 'Рубрика'
        ordering = ['name']

# Модель для нескольких изображений
class BbImage(models.Model):
    bb = models.ForeignKey(Bb, on_delete=models.CASCADE, verbose_name='Объявление')  # Связь с Bb
    image = models.ImageField(upload_to='Bb_images/', verbose_name='Изображение')

    class Meta:
        verbose_name_plural = 'Изображения'
        verbose_name = 'Изображение'


