from django.contrib import admin
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory
from .models import Organization

@admin.register(Organization)
class OrganizationAdmin(TreeAdmin):
    """
    Админ-модель для управления организациями
    """
    form = movenodeform_factory(Organization)
    list_display = ('short_name', 'full_name', 'name_by')
    search_fields = ('short_name', 'full_name', 'name_by')
    list_per_page = 20

    fieldsets = (
        ('Информация на русском', {
            'fields': ('full_name', 'short_name', 'details_ru')
        }),
        ('Информация на белорусском', {
            'fields': ('name_by', 'details_by')
        }),
        ('Движение', {
            'fields': ('_position', '_ref_node_id')
        }),
    )