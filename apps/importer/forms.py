from django import forms
from apps.importer.models import ImportSession

class ImportForm(forms.ModelForm):
    CONTENT_TYPES = [
        ('organization', 'Организации'),
        ('department', 'Подразделения'),
        ('position', 'Должности'),
        ('employee', 'Сотрудники'),
    ]

    content_type = forms.ChoiceField(
        label='Тип данных',
        choices=CONTENT_TYPES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = ImportSession
        fields = ['file', 'content_type']
        widgets = {
            'file': forms.FileInput(attrs={'accept': '.xlsx,.xls'})
        }

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            ext = file.name.split('.')[-1].lower()
            if ext not in ['xlsx', 'xls']:
                raise forms.ValidationError(
                    'Поддерживаются только файлы Excel (.xlsx, .xls)'
                )
        return file