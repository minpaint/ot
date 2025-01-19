from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
   #  path('', include('apps.employees.urls')),  удаляем эту строку
    path('', include('apps.organizations.urls')),
    path('', include('apps.positions.urls')),
    path('', include('apps.documents.urls')),
    path('departments/', include('apps.departments.urls')),  # Добавляем этот маршрут
    path('employees/', include('apps.employees.urls')),  # Добавляем этот маршрут
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)