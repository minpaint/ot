from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

urlpatterns = [
    # Админка
    path('admin/', admin.site.urls),

    # Приложения
    path('organizations/', include('apps.organizations.urls')),
    path('departments/', include('apps.departments.urls')),
    path('positions/', include('apps.positions.urls')),
    path('employees/', include('apps.employees.urls')),
    path('documents/', include('apps.documents.urls')),
    path('api/', include('apps.api.urls')),

    # Медиа и статические файлы
    path('media/<path:path>/', serve, {'document_root': settings.MEDIA_ROOT}),
    path('static/<path:path>/', serve, {'document_root': settings.STATIC_ROOT}),
]

# Добавляем обработку медиа и статических файлов в режиме разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)