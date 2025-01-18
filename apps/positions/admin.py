from django.contrib import admin
from django import forms
from .models import Position

class PositionAdminForm(forms.ModelForm):
    """
    Форма для создания/редактирования должности
    """
    class Meta:
        model = Position
        fields = '__all__'
        widgets = {
            'safety_instructions': forms.TextInput(
                attrs={'placeholder': 'Пример: 1-01, 1-02, 2-01'}
            ),
            'contract_instructions': forms.Textarea(
                attrs={'rows': 3}
            ),
        }

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    """
    Админ-модель для управления должностями
    """
    form = PositionAdminForm
    list_display = (
        'name',
        'organization',
        'department',
        'division',
        'electrical_safety_group',
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
    list_per_page = 20

    fieldsets = (
        ('Основные сведения', {
            'fields': (
                'organization',
                'department',
                'name',
                'division'
            )
        }),
        ('Охрана труда', {
            'fields': (
                'safety_instructions',
                'electrical_safety_group',
                'internship_period',
                'is_safety_responsible',
                'is_electrical_personnel'
            )
        }),
        ('Документация', {
            'fields': (
                'contract_instructions',
                'familiarization_documents'
            )
        }),
    )

    filter_horizontal = ('familiarization_documents',)

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