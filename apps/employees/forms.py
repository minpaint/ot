from django import forms
from .models import Employee
from apps.departments.models import Department
from apps.positions.models import Position

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = [
            'organization', 'department', 'position',
            'last_name', 'first_name', 'middle_name',
            'birth_date', 'address', 'phone', 'email',
            'photo'
        ]
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3}),
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