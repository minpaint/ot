
from django.contrib import admin
from django.urls import path, include
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.employees.urls')),
    path('', include('apps.organizations.urls')),
    path('', include('apps.positions.urls')),
    path('', include('apps.documents.urls')),
]
