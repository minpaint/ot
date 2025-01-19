from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from .models import Department


class DepartmentAdmin(DraggableMPTTAdmin):
    list_display = (
        'tree_actions',
        'indented_title',
        'organization',
        'short_name',
        'is_active'
    )
    list_display_links = ('indented_title',)
    list_filter = ('organization', 'is_active')
    search_fields = ('name', 'short_name')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('organization')


admin.site.register(Department, DepartmentAdmin)