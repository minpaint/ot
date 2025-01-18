from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.organizations.views import OrganizationViewSet
from apps.employees.views import EmployeeViewSet
from apps.documents.views import DocumentViewSet
from apps.importer.views import ImportSessionViewSet

router = DefaultRouter()
router.register(r'organizations', OrganizationViewSet)
router.register(r'employees', EmployeeViewSet)
router.register(r'documents', DocumentViewSet)
router.register(r'import', ImportSessionViewSet)

app_name = 'api'

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls')),
]