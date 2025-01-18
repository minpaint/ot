from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render, redirect
from django.http import JsonResponse
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
