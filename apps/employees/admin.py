from django.contrib import admin
from .models import Employee

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = (
        'last_name',
        'first_name',
        'middle_name',
        'position',
        'department',
        'organization',
        'is_active'
    )
    list_filter = (
        'organization',
        'department',
        'is_active'
    )
    search_fields = (
        'last_name',
        'first_name',
        'middle_name'
    )
    ordering = ('last_name', 'first_name')
