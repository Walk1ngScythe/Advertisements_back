from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('bboard.urls')),
    path('api/v1/', include('users.urls')),
    path('api/v1/', include('сomplaints.urls')),

    # Используем кастомный View для получения токенов
    path('api/v1/token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token', TokenRefreshView.as_view(), name='token_refresh'),
]

# Добавляем пути для медиафайлов при отладке
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
