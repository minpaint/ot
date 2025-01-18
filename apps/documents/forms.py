from django import forms
from .models import Document
from apps.positions.models import Position

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = [
            'organization', 'department', 'name',
            'description', 'file', 'approval_date',
            'positions_for_familiarization'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'approval_date': forms.DateInput(attrs={'type': 'date'}),
            'positions_for_familiarization': forms.SelectMultiple(
                attrs={'size': '10'}
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Фильтруем должности по организации
        if 'organization' in self.
            org_id = self.data.get('organization')
            self.fields['positions_for_familiarization'].queryset = (
                Position.objects.filter(organization_id=org_id)
            )
        elif self.instance.pk:
            self.fields['positions_for_familiarization'].queryset = (
                Position.objects.filter(organization=self.instance.organization)
            )
        else:
            self.fields['positions_for_familiarization'].queryset = (
                Position.objects.none()
            )

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            ext = file.name.split('.')[-1].lower()
            if ext not in Document.ALLOWED_EXTENSIONS:
                raise forms.ValidationError(
                    f'Неподдерживаемый тип файла. Разрешены: '
                    f'{", ".join(Document.ALLOWED_EXTENSIONS)}'
                )
            if file.size > Document.MAX_SIZE_MB * 1024 * 1024:
                raise forms.ValidationError(
                    f'Размер файла не должен превышать {Document.MAX_SIZE_MB} МБ'
                )
        return file