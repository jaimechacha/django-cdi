from django import forms
from django.forms import ModelForm

from core.school.models import *


class StudentMedicalRecordForm(ModelForm):
    class Meta:
        model = StudentMedicalRecord
        fields = '__all__'
        widgets = {
            'weight': forms.NumberInput(
                attrs={'class': 'form-control', 'placeholder': 'Ingrese el peso'}
            ),
            'size': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Ingrese la talla'}
            ),
            'height': forms.NumberInput(
                attrs={'class': 'form-control', 'placeholder': 'Ingrese la altura'}
            ),
            'blood_group': forms.Select(
                attrs={'class': 'form-control'}
            ),
            'donor': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}
            ),
            'vaccine_card': forms.FileInput(
                attrs={'class': 'form-control'}
            ),
            'disability': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}
            ),
            'disability_type': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Ingrese tipo de discapacidad'}
            ),
            'disability_per': forms.NumberInput(
                attrs={'class': 'form-control', 'placeholder': 'Ingrese porcentaje de discapacidad'}
            ),
            'allergies': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}
            ),
            'allergies_desc': forms.Textarea(
                attrs={'class': 'form-control', 'rows': '3'}
            ),
            'allergy_treatment': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Ingrese tratamiento de alergia'}
            ),
            'diseases_suffered': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}
            ),
            'diseases_suffered_desc': forms.Textarea(
                attrs={'class': 'form-control', 'rows': '3'}
            ),
            'pre_diseases': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}
            ),
            'pre_diseases_desc': forms.Textarea(
                attrs={'class': 'form-control', 'rows': '3'}
            ),
            'cat_illnesses': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}
            ),
            'cat_illnesses_desc': forms.Textarea(
                attrs={'class': 'form-control', 'rows': '3'}
            ),
            'medication': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}
            ),
            'medication_type': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Ingrese tipo de medicación'}
            ),
            'medication_schedule': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Ingrese horario de medicación'}
            )
        }


class CountryForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Country
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ingrese un nombre'}),
        }

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class ProvinceForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Province
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ingrese un nombre'}),
            'code': forms.TextInput(attrs={'placeholder': 'Ingrese un código'}),
            'country': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;'}),
        }

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class CantonForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Canton
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ingrese un nombre'}),
            'province': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;'}),
        }

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class ParishForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Parish
        fields = 'canton', 'name'
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ingrese un nombre'}),
            'canton': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;'}),
        }

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class JobForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Job
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ingrese un nombre'}),
        }

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class ShiftsForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Shifts
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ingrese un nombre'}),
        }

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class TypeEventForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = TypeEvent
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ingrese un nombre'}),
        }

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data

class CursosForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Cursos
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ingrese el nombre del curso'}),
            'descrip': forms.TextInput(attrs={'placeholder': 'Ingrese una descripción del curso'}),
        }

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data




class MatterForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Matter
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ingrese un nombre'}),
            'level': forms.Select(attrs={'class': 'form-control select2', 'style': 'width:100%'}),
        }

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class BreakfastForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Breakfast
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ingrese un nombre'}),
        }
        exclude = ['state']

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class TypeActivityForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = TypeActivity
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ingrese un nombre'}),
        }

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class TypeCVitaeForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = TypeCVitae
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ingrese un nombre'}),
        }

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class TypeResourceForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = TypeResource
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ingrese un nombre'}),
        }

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class ConferenceThemeForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = ConferenceTheme
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ingrese un nombre'}),
        }

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class TeacherForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['parish'].queryset = Parish.objects.none()

    class Meta:
        model = Teacher
        fields = 'first_name', 'last_name', 'dni', 'email', 'gender', 'mobile', 'phone', 'birthdate', 'address', 'parish'
        widgets = {
            'gender': forms.Select(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%;'
            }),
            'parish': forms.Select(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%;'
            }),
            'mobile': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese su número celular',
                    'class': 'form-control',
                    'autocomplete': 'off'
                }
            ),
            'phone': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese su número convencional',
                    'class': 'form-control',
                    'autocomplete': 'off'
                }
            ),
            'address': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese una dirección',
                    'class': 'form-control',
                    'autocomplete': 'off',
                }
            ),
        }
        exclude = ['user']

    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off',
        'placeholder': 'Ingrese sus nombres'
    }), label='Nombres', max_length=50)

    birthdate = forms.DateField(input_formats=['%Y-%m-%d'], widget=forms.TextInput(
        attrs={
            'class': 'form-control datetimepicker-input',
            'id': 'birthdate',
            'value': datetime.now().strftime('%Y-%m-%d'),
            'data-toggle': 'datetimepicker',
            'data-target': '#birthdate'
        }), label='Fecha de nacimiento')

    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off',
        'placeholder': 'Ingrese sus apellidos'
    }), label='Apellidos', max_length=50)

    dni = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off',
        'placeholder': 'Ingrese su número de cedula'
    }), label='Número de cedula', max_length=10)

    email = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off',
        'placeholder': 'Ingrese su email'
    }), label='Email', max_length=50)

    image = forms.ImageField(widget=forms.FileInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off'
    }), label='Imagen')


class StudentForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['parish'].queryset = Parish.objects.none()

    class Meta:
        model = Student
        fields = '__all__'
        widgets = {
            'gender': forms.Select(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%;'
            }),
            'parish': forms.Select(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%;'
            }),
            'mobile': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese su número celular',
                    'class': 'form-control',
                    'autocomplete': 'off'
                }
            ),
            'phone': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese su número convencional',
                    'class': 'form-control',
                    'autocomplete': 'off'
                }
            ),
            'address': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese una dirección',
                    'class': 'form-control',
                    'autocomplete': 'off',
                }
            ),
            'birth_country': forms.Select(
                attrs={
                    'class': 'form-control select2',
                    'style': 'width: 100%;'
                }
            ),
            'birth_province': forms.Select(
                attrs={
                    'class': 'form-control select2',
                    'style': 'width: 100%;'
                }
            ),
            'birth_city': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese ciudad de nacimiento',
                    'class': 'form-control',
                    'autocomplete': 'off',
                }
            ),
            'nationality': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese nacionalidad',
                    'class': 'form-control',
                    'autocomplete': 'off',
                }
            ),
            'age': forms.NumberInput(
                attrs={
                    'placeholder': 'Ingrese edad',
                    'class': 'form-control',
                    'autocomplete': 'off',
                    'required': 'true'
                }
            ),
            'ethnicity': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese etnia',
                    'class': 'form-control',
                    'autocomplete': 'off',
                }
            ),
            'religion': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese religión',
                    'class': 'form-control',
                    'autocomplete': 'off',
                }
            ),
            'emergency_number': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese número de emergencia',
                    'class': 'form-control',
                    'autocomplete': 'off',
                }
            ),
        }
        exclude = ['user']

    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off',
        'placeholder': 'Ingrese sus nombres'
    }), label='Nombres', max_length=50)

    birthdate = forms.DateField(input_formats=['%Y-%m-%d'], widget=forms.TextInput(
        attrs={
            'class': 'form-control datetimepicker-input',
            'id': 'birthdate',
            'value': datetime.now().strftime('%Y-%m-%d'),
            'data-toggle': 'datetimepicker',
            'data-target': '#birthdate'
        }), label='Fecha de nacimiento')

    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off',
        'placeholder': 'Ingrese sus apellidos'
    }), label='Apellidos', max_length=50)

    dni = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off',
        'placeholder': 'Ingrese su número de cedula'
    }), label='Número de cedula', max_length=10)

    email = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off',
        'placeholder': 'Ingrese su email'
    }), label='Email', max_length=50)

    image = forms.ImageField(widget=forms.FileInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off'
    }), label='Imagen')


class CVitaeForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = CVitae
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Ingrese un nombre',
                'class': 'form-control',
                'autocomplete': 'off'
            }),
            'typecvitae': forms.Select(attrs={
                'class': 'form-control select2',
                'style': 'width:100%'
            }),
            'details': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'cols': 3,
                'placeholder': 'Ingrese una descripción',
                'autocomplete': 'off'
            }),
            'start_date': forms.DateInput(format='%Y-%m-%d', attrs={
                'class': 'form-control datetimepicker-input',
                'id': 'start_date',
                'value': datetime.now().strftime('%Y-%m-%d'),
                'data-toggle': 'datetimepicker',
                'data-target': '#start_date'
            }),
            'end_date': forms.DateInput(format='%Y-%m-%d', attrs={
                'class': 'form-control datetimepicker-input',
                'id': 'end_date',
                'value': datetime.now().strftime('%Y-%m-%d'),
                'data-toggle': 'datetimepicker',
                'data-target': '#end_date'
            }),
        }
        exclude = ['teacher']

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class ContractsForm(ModelForm):
    def __init__(self, *args, **kwargs):
        exclude = kwargs.pop('excludefields', [])
        super().__init__(*args, **kwargs)
        for field in exclude:
            del self.fields[field]

    class Meta:
        model = Contracts
        fields = '__all__'
        widgets = {
            'teacher': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;'}),
            'job': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;'}),
            'shifts': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;'}),
            'start_date': forms.DateInput(format='%Y-%m-%d', attrs={
                'class': 'form-control datetimepicker-input',
                'id': 'start_date',
                'value': datetime.now().strftime('%Y-%m-%d'),
                'data-toggle': 'datetimepicker',
                'data-target': '#start_date'
            }),
            'end_date': forms.DateInput(format='%Y-%m-%d', attrs={
                'class': 'form-control datetimepicker-input',
                'id': 'end_date',
                'value': datetime.now().strftime('%Y-%m-%d'),
                'data-toggle': 'datetimepicker',
                'data-target': '#end_date'
            }),
            'base_salary': forms.TextInput(),
        }


class EventsForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['contract'].widget.attrs['autofocus'] = True

    class Meta:
        model = Events
        fields = 'contract', 'date_permit', 'typeevent', 'desc', 'valor'
        widgets = {
            'contract': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;'}),
            'typeevent': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;'}),
            'desc': forms.Textarea(
                attrs={'class': 'form-control', 'rows': '3', 'cols': 3, 'placeholder': 'Ingrese una descripción'}),
        }
        exclude = ['start_date', 'end_date', 'start_time', 'end_time', 'state']

    date_permit = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
        }), label='Fecha y hora de permiso')

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class PeriodForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Period
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Ingrese un nombre',
                'class': 'form-control',
                'autocomplete': 'off'
            }),
        }

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class AssignmentTeacherPeriodForm(forms.Form):
    contract = forms.ModelChoiceField(queryset=Contracts.objects.filter(state=True), widget=forms.Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%;'
    }))

    period = forms.ModelChoiceField(queryset=Period.objects.filter(state=True), widget=forms.Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%;'
    }))


class MatriculationForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['student'].queryset = Student.objects.filter()

    class Meta:
        model = Matriculation
        fields = '__all__'
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;'}),
            'level': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;'}),
        }

    period = forms.ModelChoiceField(widget=forms.Select(
        attrs={
            'class': 'form-control select2',
            'style': 'width: 100%;'
        }), queryset=Period.objects.filter(state=True))


class AssistanceForm(ModelForm):
    def __init__(self, *args, **kwargs):
        edit = kwargs.pop('edit', False)
        super().__init__(*args, **kwargs)
        if edit:
            self.fields['date_joined'].widget.attrs['disabled'] = True

    class Meta:
        model = Assistance
        fields = '__all__'
        widgets = {
            'date_joined': forms.DateInput(format='%Y-%m-%d', attrs={
                'class': 'form-control datetimepicker-input',
                'id': 'date_joined',
                'value': datetime.now().strftime('%Y-%m-%d'),
                'data-toggle': 'datetimepicker',
                'data-target': '#date_joined'
            }),
            'year': forms.TextInput(attrs={
                'id': 'year',
                'class': 'form-control datetimepicker-input',
                'data-toggle': 'datetimepicker',
                'data-target': '#year',
            }),
            'month': forms.Select(
                attrs={
                    'id': 'month',
                    'class': 'form-control select2',
                    'style': 'width: 100%'
                })
        }
        exclude = ['state']

    date_range = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off',
    }))

    period = forms.ModelChoiceField(widget=forms.Select(
        attrs={
            'class': 'form-control select2',
            'style': 'width: 100%;'
        }), queryset=Period.objects.filter(state=True))


class TutorialsForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['contract'].queryset = Contracts.objects.filter(state=True)

    class Meta:
        model = Tutorials
        fields = '__all__'
        widgets = {
            'date_joined': forms.DateInput(format='%Y-%m-%d', attrs={
                'class': 'form-control datetimepicker-input',
                'id': 'date_joined',
                'value': datetime.now().strftime('%Y-%m-%d'),
                'data-toggle': 'datetimepicker',
                'data-target': '#date_joined'
            }),
            'contract': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;'}),
            'horary': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;'}),
            'desc': forms.Textarea(attrs={'rows': '3', 'cols': 3, 'placeholder': 'Ingrese una descripción'}),
        }

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class SchoolFeedingForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['student'].queryset = Student.objects.filter()

    class Meta:
        model = SchoolFeeding
        fields = '__all__'
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;'}),
            'breakfast': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;'}),
            'date_joined': forms.DateInput(format='%Y-%m-%d', attrs={
                'class': 'form-control datetimepicker-input',
                'id': 'date_joined',
                'value': datetime.now().strftime('%Y-%m-%d'),
                'data-toggle': 'datetimepicker',
                'data-target': '#date_joined'
            }),
            'cant': forms.TextInput(),
            'desc': forms.Textarea(attrs={'rows': '3', 'cols': 3, 'placeholder': 'Ingrese una descripción'}),
        }
        exclude = ['date_joined']

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class PsychologicalOrientationForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = PsychologicalOrientation
        fields = '__all__'
        widgets = {
            'matriculation': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;'}),
            'date_joined': forms.DateInput(format='%Y-%m-%d', attrs={
                'class': 'form-control datetimepicker-input',
                'id': 'date_joined',
                'value': datetime.now().strftime('%Y-%m-%d'),
                'data-toggle': 'datetimepicker',
                'data-target': '#date_joined'
            }),
            'cant': forms.TextInput(),
            'desc': forms.Textarea(attrs={'rows': '6', 'cols': '6', 'placeholder': 'Ingrese una descripción'}),
        }

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class ResourcesForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['typeresource'].widget.attrs['autofocus'] = True
        self.fields['perioddetail'].queryset = PeriodDetail.objects.none()

    class Meta:
        model = Resources
        fields = 'period', 'perioddetail', 'typeresource', 'date_range', 'web_address', 'desc'
        widgets = {
            'typeresource': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;'}),
            'perioddetail': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;'}),
            'start_date': forms.DateInput(format='%Y-%m-%d', attrs={
                'class': 'form-control datetimepicker-input',
                'id': 'start_date',
                'value': datetime.now().strftime('%Y-%m-%d'),
                'data-toggle': 'datetimepicker',
                'data-target': '#start_date'
            }),
            'end_date': forms.DateInput(format='%Y-%m-%d', attrs={
                'class': 'form-control datetimepicker-input',
                'id': 'end_date',
                'value': datetime.now().strftime('%Y-%m-%d'),
                'data-toggle': 'datetimepicker',
                'data-target': '#end_date'
            }),
            'web_address': forms.TextInput(attrs={
                'placeholder': 'Ingrese una dirección url'
            }),
            'desc': forms.Textarea(attrs={
                'placeholder': 'Ingrese una descripción',
                'rows': 3,
                'cols': 3
            }),
        }

    period = forms.ModelChoiceField(widget=forms.Select(
        attrs={
            'class': 'form-control select2',
            'style': 'width: 100%;'
        }), queryset=Period.objects.filter(state=True), label='Periodo')

    date_range = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off'
    }), label='Fecha de inicio/finalización')

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class ActivitiesForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['perioddetail'].widget.attrs['autofocus'] = True
        self.fields['perioddetail'].queryset = PeriodDetail.objects.none()

    class Meta:
        model = Activities
        fields = 'name', 'period', 'perioddetail', 'typeactivity', 'date_range', 'web_address', 'rubric', 'desc'
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Ingrese un nombre o titulo'
            }),
            'typeactivity': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;'}),
            'perioddetail': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;'}),
            'start_date': forms.DateInput(format='%Y-%m-%d', attrs={
                'class': 'form-control datetimepicker-input',
                'id': 'start_date',
                'value': datetime.now().strftime('%Y-%m-%d'),
                'data-toggle': 'datetimepicker',
                'data-target': '#start_date'
            }),
            'end_date': forms.DateInput(format='%Y-%m-%d', attrs={
                'class': 'form-control datetimepicker-input',
                'id': 'end_date',
                'value': datetime.now().strftime('%Y-%m-%d'),
                'data-toggle': 'datetimepicker',
                'data-target': '#end_date'
            }),
            'web_address': forms.TextInput(attrs={
                'placeholder': 'Ingrese una dirección url'
            }),
            'desc': forms.Textarea(attrs={
                'placeholder': 'Ingrese una descripción',
                'rows': 3,
                'cols': 3
            }),
        }

    period = forms.ModelChoiceField(widget=forms.Select(
        attrs={
            'class': 'form-control select2',
            'style': 'width: 100%;'
        }), queryset=Period.objects.filter(state=True), label='Periodo')

    date_range = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off'
    }), label='Fecha de inicio/finalización')

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class CompanyForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True
        for form in self.visible_fields():
            form.field.widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

    class Meta:
        model = Company
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ingrese un nombre'}),
            'coordinates': forms.TextInput(attrs={'placeholder': 'Ingrese unas coordenadas'}),
            'ruc': forms.TextInput(attrs={'placeholder': 'Ingrese un ruc'}),
            'mobile': forms.TextInput(attrs={'placeholder': 'Ingrese un teléfono celular'}),
            'email': forms.TextInput(attrs={'placeholder': 'Ingrese un email'}),
            'address': forms.TextInput(attrs={'placeholder': 'Ingrese una dirección'}),
            'mission': forms.Textarea(attrs={'placeholder': 'Ingrese una descripción', 'rows': 3, 'cols': 3}),
            'vision': forms.Textarea(attrs={'placeholder': 'Ingrese una descripción', 'rows': 3, 'cols': 3}),
            'about_us': forms.Textarea(attrs={'placeholder': 'Ingrese una descripción', 'rows': 3, 'cols': 3}),
            'desc': forms.Textarea(attrs={'placeholder': 'Ingrese una descripción', 'rows': 3, 'cols': 3}),
        }

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class ConferencesForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['contract'].queryset = Contracts.objects.filter(state=True)

    class Meta:
        model = Conferences
        fields = '__all__'
        widgets = {
            'contract': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;'}),
            'conferencetheme': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;'}),
            'date_joined': forms.DateInput(format='%Y-%m-%d', attrs={
                'class': 'form-control datetimepicker-input',
                'id': 'date_joined',
                'value': datetime.now().strftime('%Y-%m-%d'),
                'data-toggle': 'datetimepicker',
                'data-target': '#date_joined'
            }),
            'name': forms.TextInput(attrs={'placeholder': 'Ingrese un nombre'}),
            'desc': forms.Textarea(attrs={'rows': '3', 'cols': 3, 'placeholder': 'Ingrese una descripción'}),
        }

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data




class NoteDetailsForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    class Meta:
       
        model = NoteDetails
        fields = 'name',  'typeactivity', 'date_range', 'desc'
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Ingrese un nombre o titulo'
            }),
            'typeactivity': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;'}),
            
            'start_date': forms.DateInput(format='%Y-%m-%d', attrs={
                'class': 'form-control datetimepicker-input',
                'id': 'start_date',
                'value': datetime.now().strftime('%Y-%m-%d'),
                'data-toggle': 'datetimepicker',
                'data-target': '#start_date'
            }),
            'end_date': forms.DateInput(format='%Y-%m-%d', attrs={
                'class': 'form-control datetimepicker-input',
                'id': 'end_date',
                'value': datetime.now().strftime('%Y-%m-%d'),
                'data-toggle': 'datetimepicker',
                'data-target': '#end_date'
            }),
            'desc': forms.Textarea(attrs={
                'placeholder': 'Ingrese una descripción',
                'rows': 3,
                'cols': 3
            }),
        }
        
    date_range = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off'
    }), label='Fecha de inicio/finalización')

    """ 
    score = forms.ModelChoiceField(queryset=Scores.objects.all(), widget=forms.Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%;'
    })) 
    """

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data
