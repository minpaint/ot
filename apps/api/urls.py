from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.departments.views import DepartmentViewSet

router = DefaultRouter()
router.register('departments', DepartmentViewSet, basename='api-department')

urlpatterns = [
    path('', include(router.urls)),
]
