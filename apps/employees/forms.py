from django import forms
from .models import Employee
from apps.departments.models import Department
from apps.positions.models import Position

class EmployeeForm(forms.ModelForm):
    contracts = forms.ChoiceField(
        choices=[(True, 'Да'), (False, 'Нет')],
        label='Работы по договору подряда',
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=False
    )
    rosts = forms.ChoiceField(
        choices=[(size, size) for size in ["158-164", "170-176", "182-188", "194-200"]],
        label='Рост',
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=False
    )
    clothesSizes = forms.ChoiceField(
        choices=[(size, size) for size in ["44-46", "48-50", "52-54", "56-58", "60-62", "64-66"]],
        label='Размер одежды',
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=False
    )
    shoeSizes = forms.ChoiceField(
        choices=[(size, size) for size in ["36", "37", "38", "39", "40", "41", "42", "43", "44", "45", "46", "47", "48"]],
        label='Размер обуви',
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=False
    )
    class Meta:
        model = Employee
        fields = [
            'organization', 'department', 'position',
            'last_name', 'first_name', 'middle_name',
             'gender', 'birth_date',
             'employment_date', 'personnel_number',
            'email', 'phone', 'is_contractor',
             'height', 'clothing_size', 'shoe_size'
         ]
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'employment_date': forms.DateInput(attrs={'type': 'date'}),
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Фильтруем подразделения и должности по организации
        if 'organization' in self.data:
            org_id = self.data.get('organization')
            self.fields['department'].queryset = Department.objects.filter(
                organization_id=org_id
            )
            self.fields['position'].queryset = Position.objects.filter(
                organization_id=org_id
            )
        elif self.instance.pk:
            self.fields['department'].queryset = Department.objects.filter(
                organization=self.instance.organization
            )
            self.fields['position'].queryset = Position.objects.filter(
                organization=self.instance.organization
            )
        else:
            self.fields['department'].queryset = Department.objects.none()
            self.fields['position'].queryset = Position.objects.none()