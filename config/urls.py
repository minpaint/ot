from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.core.urls')),
    path('organizations/', include('apps.organizations.urls')),
    path('departments/', include('apps.departments.urls')),
    path('positions/', include('apps.positions.urls')),
    path('employees/', include('apps.employees.urls')),
    path('documents/', include('apps.documents.urls')),
    path('api/', include('apps.api.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
