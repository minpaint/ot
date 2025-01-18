from django.contrib import admin
from .models import Employee


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    """
    Админ-модель для управления сотрудниками
    """
    list_display = (
        'last_name',
        'first_name',
        'middle_name',
        'organization',
        'department',
        'position',
        'is_contractor'
    )

    list_filter = (
        'organization',
        'department',
        'position',
        'is_contractor'
    )

    search_fields = (
        'last_name',
        'first_name',
        'middle_name',
        'full_name_dative',
        'email',
        'phone'
    )

    list_per_page = 20

    fieldsets = (
        ('Персональные данные', {
            'fields': (
                ('last_name', 'first_name', 'middle_name'),
                'full_name_dative',
                'birth_date'
            )
        }),
        ('Должность', {
            'fields': (
                'organization',
                'department',
                'position',
                'is_contractor'
            )
        }),
        ('Контактная информация', {
            'fields': (
                'address',
                'phone',
                'email'
            )
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'organization',
            'department',
            'position'
        )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "department":
            if request.method == "GET" and "organization" in request.GET:
                kwargs["queryset"] = db_field.related_model.objects.filter(
                    organization_id=request.GET["organization"]
                )
        elif db_field.name == "position":
            if request.method == "GET":
                filters = {}
                if "organization" in request.GET:
                    filters["organization_id"] = request.GET["organization"]
                if "department" in request.GET:
                    filters["department_id"] = request.GET["department"]
                if filters:
                    kwargs["queryset"] = db_field.related_model.objects.filter(
                        **filters
                    )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)