from django.db import models
from app_users.models import CustomUser
from app_board.models import Bb


class Review(models.Model):
    seller = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="reviews_received", verbose_name="Продавец")
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="reviews_written", verbose_name="Автор отзыва")
    ad = models.ForeignKey(Bb, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Объявление")
    rating = models.PositiveSmallIntegerField(verbose_name="Оценка", choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField(verbose_name="Комментарий")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата отзыва")
    is_deleted = models.BooleanField(default=False, verbose_name='Удалено')  # Новое поле

    def __str__(self):
        return f"Отзыв от {self.author} для {self.seller} - {self.rating}⭐"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ['-created_at']