from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Employee, Department, Position
from .forms import EmployeeForm
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
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

def get_departments(request):
    organization_id = request.GET.get('organization')
    departments = Department.objects.filter(organization_id=organization_id).values('id', 'name')
    return JsonResponse({'departments': list(departments)})

def get_positions(request):
    department_id = request.GET.get('department')
    positions = Position.objects.filter(department_id=department_id).values('id', 'name')
    return JsonResponse({'positions': list(positions)})


def employee_create(request):
    """Представление для создания сотрудника"""
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES)
        if form.is_valid():
           form.save()
           return redirect('employees:employee-list')  # Перенаправление после создания
    else:
        form = EmployeeForm()
    return render(request, 'employees/employee_form.html', {'form': form})