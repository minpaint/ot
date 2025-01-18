from django.contrib import admin
from .models import Document


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    """
    Админ-модель для управления документами
    """
    list_display = (
        'name',
        'organization',
        'department',
        'approval_date'
    )

    list_filter = (
        'organization',
        'department',
        'approval_date'
    )

    search_fields = ('name',)
    date_hierarchy = 'approval_date'
    list_per_page = 20

    fieldsets = (
        ('Основная информация', {
            'fields': (
                'name',
                'organization',
                'department',
                'approval_date'
            )
        }),
        ('Файл', {
            'fields': ('file',)
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'organization',
            'department'
        )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "department":
            if request.method == "GET" and "organization" in request.GET:
                kwargs["queryset"] = db_field.related_model.objects.filter(
                    organization_id=request.GET["organization"]
                )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)