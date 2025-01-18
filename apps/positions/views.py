from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from .models import Position
from .serializers import PositionSerializer
from apps.core.permissions import HasOrganizationPermission

class PositionViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с должностями"""
    serializer_class = PositionSerializer
    permission_classes = [IsAuthenticated, HasOrganizationPermission]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_fields = [
        'organization',
        'department',
        'electrical_safety_group',
        'is_safety_responsible',
        'is_electrical_personnel'
    ]
    search_fields = ['name', 'division', 'safety_instructions']
    ordering_fields = ['name', 'department__name', 'division']
    ordering = ['organization', 'department', 'name']

    def get_queryset(self):
        """
        Возвращает queryset должностей в зависимости от прав пользователя
        """
        user = self.request.user
        if user.is_superuser:
            return Position.objects.all()
        return Position.objects.filter(organization__in=user.organizations.all())