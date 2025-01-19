from django.http import JsonResponse
from .models import Department

def get_departments_by_organization(request):
    organization_id = request.GET.get('organization_id')
    if organization_id:
        departments = Department.objects.filter(
            organization_id=organization_id,
            is_active=True
        ).order_by('path')

        data = [
            {
                'id': dept.id,
                'name': dept.get_display_name(),
                'short_name': dept.short_name,
                'depth': dept.get_depth()
            }
            for dept in departments
        ]
        return JsonResponse({'departments': data})
    return JsonResponse({'departments': []})
