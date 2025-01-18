from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Employee
from .serializers import EmployeeListSerializer, EmployeeDetailSerializer
from apps.core.permissions import HasOrganizationPermission


class EmployeeViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с сотрудниками.
    """
    permission_classes = [IsAuthenticated, HasOrganizationPermission]

    def get_queryset(self):
        """
        Возвращает queryset сотрудников в зависимости от прав пользователя
        """
        user = self.request.user
        if user.is_superuser:
            return Employee.objects.all()
        return Employee.objects.filter(organization__in=user.organizations.all())

    def get_serializer_class(self):
        """
        Возвращает класс сериализатора в зависимости от действия
        """
        if self.action == 'list':
            return EmployeeListSerializer
        return EmployeeDetailSerializer

    def perform_create(self, serializer):
        """
        Привязываем создаваемого сотрудника к организации пользователя
        """
        if not self.request.user.is_superuser and self.request.user.organizations.count() == 1:
            serializer.save(organization=self.request.user.organizations.first())
        else:
            serializer.save()