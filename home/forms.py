from django import forms
from .models import Departments, PBI
from django.forms.models import model_to_dict


class LoginForm(forms.Form):
    username = forms.CharField(label="Kullanıcı Adı:")
    password = forms.CharField(label="Parola", widget=forms.PasswordInput)


class Department_Form(forms.ModelForm):
    class Meta:
        model = Departments
        fields = ['department_name', 'department_mail']


FRUIT_CHOICES = [
    ('orange', 'Oranges'),
    ('cantaloupe', 'Cantaloupes'),
    ('mango', 'Mangoes'),
    ('honeydew', 'Honeydews'),
]


def queryset_to_dict(qs, fields=None, exclude=None):
    my_list = []
    for x in qs:
        my_list.append(model_to_dict(x, fields=fields, exclude=exclude))
    return my_list


class Pbi_Form(forms.ModelForm):
    workorder_date = forms.DateTimeField(
        required=False,
        input_formats=['%d/%m/%Y'],
        widget=forms.DateTimeInput(format='%d/%m/%Y'))
    start_date = forms.DateTimeField(
        required=False,
        input_formats=['%d/%m/%Y'],
        widget=forms.DateTimeInput(format='%d/%m/%Y'))
    finish_date = forms.DateTimeField(
        required=False,
        input_formats=['%d/%m/%Y'],
        widget=forms.DateTimeInput(format='%d/%m/%Y'))
    actual_date = forms.DateTimeField(
        required=False,
        input_formats=['%d/%m/%Y'],
        widget=forms.DateTimeInput(format='%d/%m/%Y')
    )

    class Meta:
        model = PBI
        fields = ['department', 'sprint', 'end_day_index', 'pbi_type', 'pbi', 'classficition', 'workorder_date',
                  'start_date', 'finish_date', 'actual_date']

        PBI_TYPES = (
            ("TODO", "TODO"),
            ("INPROGRESS", "INPROGRESS"),
            ("DONE", "DONE"),
        )
        End_day_index = (
            ("3", "3"),
            ("5", "5"),
            ("10", "10"),
        )

        widgets = {

            'pbi_type': forms.Select(choices=PBI_TYPES),
            'end_day_index': forms.Select(choices=End_day_index),
            'workorder_date': forms.DateInput(format='dd/mm/yy'),
            'pbi':forms.Textarea(attrs={'rows':3, 'cols':23})

        }
