
from django import forms
from django.db.models import fields
from django.forms import CheckboxSelectMultiple, DateInput
from django.http import request

from ajax_select.fields import AutoCompleteSelectField, AutoCompleteSelectMultipleField

from .models import *

class formCruise(forms.ModelForm):
    class Meta:
        model = cruise
        fields = ['name', 'description', 'startDate', 'endDate', 'startPort', 'endPort', 'maxBerths']
    #skipper = AutoCompleteSelectMultipleField('skipper', help_text="Bitte füge einen Verantwortlichen ein", required=True)