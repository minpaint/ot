from django import forms

class EmployeeSearchForm(forms.Form):
    query = forms.CharField(
        label='Поиск',
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'ФИО, должность или подразделение...',
            'class': 'form-control'
        })
    )
    organization = forms.ModelChoiceField(
        label='Организация',
        queryset=None,
        required=False,
        empty_label='Все организации',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    department = forms.ModelChoiceField(
        label='Подразделение',
        queryset=None,
        required=False,
        empty_label='Все подразделения',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    position = forms.ModelChoiceField(
        label='Должность',
        queryset=None,
        required=False,
        empty_label='Все должности',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    def __init__(self, *args, **kwargs):
        organization_queryset = kwargs.pop('organization_queryset', None)
        department_queryset = kwargs.pop('department_queryset', None)
        position_queryset = kwargs.pop('position_queryset', None)

        super().__init__(*args, **kwargs)

        if organization_queryset is not None:
            self.fields['organization'].queryset = organization_queryset
        if department_queryset is not None:
            self.fields['department'].queryset = department_queryset
        if position_queryset is not None:
            self.fields['position'].queryset = position_queryset

class DocumentSearchForm(forms.Form):
    query = forms.CharField(
        label='Поиск',
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Название или описание документа...',
            'class': 'form-control'
        })
    )
    organization = forms.ModelChoiceField(
        label='Организация',
        queryset=None,
        required=False,
        empty_label='Все организации',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    department = forms.ModelChoiceField(
        label='Подразделение',
        queryset=None,
        required=False,
        empty_label='Все подразделения',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    date_from = forms.DateField(
        label='Дата с',
        required=False,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        })
    )
    date_to = forms.DateField(
        label='Дата по',
        required=False,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        })
    )

    def __init__(self, *args, **kwargs):
        organization_queryset = kwargs.pop('organization_queryset', None)
        department_queryset = kwargs.pop('department_queryset', None)

        super().__init__(*args, **kwargs)

        if organization_queryset is not None:
            self.fields['organization'].queryset = organization_queryset
        if department_queryset is not None:
            self.fields['department'].queryset = department_queryset

    def clean(self):
        cleaned_data = super().clean()
        date_from = cleaned_data.get('date_from')
        date_to = cleaned_data.get('date_to')

        if date_from and date_to and date_from > date_to:
            raise forms.ValidationError(
                'Дата начала не может быть позже даты окончания'
            )

        return cleaned_data