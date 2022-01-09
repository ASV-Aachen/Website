
from django import forms
from django.db.models import fields
from django.forms import CheckboxSelectMultiple, DateInput
from django.http import request

from ajax_select.fields import AutoCompleteSelectField, AutoCompleteSelectMultipleField

from .models import *


class DateInput(forms.DateInput):
    input_type = 'date'

class formCruise(forms.ModelForm):
    
    class Meta:
        model = cruise
        fields = ['name', 'description', 'startDate', 'endDate', 'startPort', 'endPort', 'maxBerths']
        widgets = {
            "startDate": DateInput(),
            "endDate": DateInput()
        }
    #sailor = AutoCompleteSelectMultipleField('skippers', help_text="Schiffer", required=False)
    #sailor = AutoCompleteSelectMultipleField('watches', help_text="Wachführer", required=False)
    sailors = AutoCompleteSelectMultipleField('sailors', required=False)
    distance = forms.CharField(required=False, max_length=10)

class formLicense(forms.ModelForm):
    
    class Meta:
        model = license
        fields = ['Type', 'Since', 'LicenseNumber']