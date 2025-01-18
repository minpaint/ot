from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'employees'

router = DefaultRouter()
router.register(r'', views.EmployeeViewSet, basename='employee')

urlpatterns = [
    path('', include(router.urls)),
]