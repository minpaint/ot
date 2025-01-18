from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from .models import Department
from .serializers import DepartmentSerializer
from apps.core.permissions import HasOrganizationPermission

class DepartmentViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с подразделениями"""
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated, HasOrganizationPermission]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_fields = ['organization']
    search_fields = ['name']
    ordering_fields = ['name']
    ordering = ['name']

    def get_queryset(self):
        """
        Возвращает queryset подразделений в зависимости от прав пользователя
        """
        user = self.request.user
        if user.is_superuser:
            return Department.objects.all()
        return Department.objects.filter(organization__in=user.organizations.all())