from rest_framework import viewsets
from app_auth.base_auth import CookieJWTAuthentication
from .models import Complaint, ComplaintStatus
from .permissions import IsSenderOrAdminModerator
from .serializers import ComplaintSerializer, ComplaintStatusSerializer


class ComplaintViewSet(viewsets.ModelViewSet):
    queryset = Complaint.objects.all()
    serializer_class = ComplaintSerializer
    authentication_classes = [CookieJWTAuthentication]
    #permission_classes = [IsSenderOrAdminModerator]

    def perform_create(self, serializer):
        from django.shortcuts import get_object_or_404
        status_in_progress = get_object_or_404(ComplaintStatus, name="Отправлена")
        serializer.save(sender=self.request.user, status=status_in_progress)

    def get_queryset(self):
        user = self.request.user

        # Возвращаем только жалобы, где пользователь — отправитель или он админ/модератор
        qs = Complaint.objects.all()
        if user.role and user.role.name in ["Администратор", "Модератор"]:
            return qs
        return qs.filter(sender=user)


class ComplaintStatusViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ComplaintStatus.objects.all()
    serializer_class = ComplaintStatusSerializer
    authentication_classes = [CookieJWTAuthentication]  # Используем JWT для аутентификации
