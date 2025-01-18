from django.contrib import admin
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory
from .models import Department

@admin.register(Department)
class DepartmentAdmin(TreeAdmin):
    """
    Админ-модель для управления подразделениями
    """
    form = movenodeform_factory(Department)
    list_display = ('name', 'short_name', 'organization')
    list_filter = ('organization',)
    search_fields = ('name', 'short_name')
    list_per_page = 20

    fieldsets = (
        ('Основные сведения', {
            'fields': ('organization', 'name', 'short_name')
        }),
        ('Движение', {
            'fields': ('_position', '_ref_node_id')
        }),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('organization')