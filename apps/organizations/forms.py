from django import forms
from .models import Organization

class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ['full_name', 'short_name', 'details_ru', 'details_by', 'parent']
        widgets = {
            'details_ru': forms.Textarea(attrs={'rows': 4}),
            'details_by': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Исключаем текущую организацию и её потомков из списка родителей
        if self.instance.pk:
            descendants = self.instance.get_descendants()
            self.fields['parent'].queryset = (
                Organization.objects.exclude(pk__in=[self.instance.pk] + 
                [d.pk for d in descendants])
            )