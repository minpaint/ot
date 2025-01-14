
from django import forms
from .models import Employee
from apps.organizations.models import Department, Organization
from apps.positions.models import Profession

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['organization', 'full_name', 'full_name_dative', 'birth_date', 'profession', 'is_contract_work', 'address', 'phone', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['profession'].queryset = Profession.objects.none()

        if 'organization' in self.data:
            try:
                organization_id = int(self.data.get('organization'))
                self.fields['profession'].queryset = Profession.objects.filter(organization_id=organization_id)
            except (ValueError, TypeError):
                pass
