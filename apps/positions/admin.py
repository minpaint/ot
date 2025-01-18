from django.contrib import admin
from .models import Position

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'division',
        'department',
        'organization',
        'electrical_safety_group',
        'internship_period',
        'is_safety_responsible',
        'is_electrical_personnel'
    )
    list_filter = (
        'organization',
        'department',
        'electrical_safety_group',
        'is_safety_responsible',
        'is_electrical_personnel'
    )
    search_fields = ('name', 'division', 'safety_instructions')
    filter_horizontal = ('familiarization_documents',)
    ordering = ('organization', 'department', 'name')