from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'employees'

router = DefaultRouter()
router.register(r'employees', views.EmployeeViewSet, basename='employee')

urlpatterns = [
    path('', include(router.urls)),
    path('create/', views.employee_create, name='employee_create'),
    path('ajax/departments/', views.get_departments, name='ajax_departments'),
    path('ajax/positions/', views.get_positions, name='ajax_positions'),
]