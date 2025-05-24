from django.db import models
from app_users.models import CustomUser


class ComplaintStatus(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Статус")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Статус жалобы"
        verbose_name_plural = "Статусы жалоб"


class Complaint(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='complaints_sent', verbose_name="Отправитель")
    recipient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='complaints_received', verbose_name="Кому подана жалоба")
    description = models.TextField(verbose_name="Описание жалобы")
    status = models.ForeignKey(ComplaintStatus, on_delete=models.SET_NULL, null=True, verbose_name="Статус жалобы")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return f"Жалоба от {self.sender} на {self.recipient} ({self.status})"

    class Meta:
        verbose_name = "Жалоба"
        verbose_name_plural = "Жалобы"
        ordering = ['-created_at']
