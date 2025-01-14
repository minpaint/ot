
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import EmployeeForm
from apps.positions.models import Profession
from apps.organizations.models import Organization
from apps.organizations.utils.permissions import user_has_organization_access
from django.contrib.auth.decorators import login_required

@login_required
def create_employee(request):
    """
    Представление для создания нового сотрудника.

    Args:
        request: Объект запроса Django.

    Returns:
         HttpResponse: Страница с формой для создания сотрудника
    """
    if request.method == 'POST':
         form = EmployeeForm(request.POST)
         if form.is_valid():
             employee = form.save(commit=False)
             user_has_organization_access(request.user, employee.organization.id)
             employee.save()
             return redirect('employee_list') # Предполагаем, что есть URL для списка сотрудников
    else:
        form = EmployeeForm()
    organizations = Organization.objects.all()
    return render(request, 'employees/employee_form.html', {'form': form, 'organizations': organizations})

@login_required
def get_professions(request):
    """
    Представление для получения списка профессий по организации.

    Args:
         request: Объект запроса Django.

    Returns:
         JsonResponse: JSON-ответ со списком профессий.
    """
    organization_id = request.GET.get('organization_id')
    professions = Profession.objects.filter(organization_id=organization_id)
    data = [{"id": prof.id, "department_name": prof.department_name} for prof in professions]
    return JsonResponse(data, safe=False)
