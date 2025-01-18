from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.employees.views import EmployeeViewSet
from apps.organizations.views import OrganizationViewSet
from apps.departments.views import DepartmentViewSet
from apps.positions.views import PositionViewSet
from apps.documents.views import DocumentViewSet

router = DefaultRouter()
router.register('employees', EmployeeViewSet, basename='employees')
router.register('organizations', OrganizationViewSet, basename='organizations')
router.register('departments', DepartmentViewSet, basename='departments')
router.register('positions', PositionViewSet, basename='positions')
router.register('documents', DocumentViewSet, basename='documents')

urlpatterns = [
    path('', include(router.urls)),
]