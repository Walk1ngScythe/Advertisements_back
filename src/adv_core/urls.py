from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('app_board.urls')),
    path('api/v1/', include('app_users.urls')),
    path('api/v1/', include('app_complaints.urls')),
    path('api/v1/', include('app_reviews.urls')),
    path('api/v1/', include('app_auth.urls')),
]

# Добавляем пути для медиафайлов при отладке
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
