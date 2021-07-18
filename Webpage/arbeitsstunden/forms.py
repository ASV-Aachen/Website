
from django import forms
from django.db.models import fields
from django.forms import CheckboxSelectMultiple, DateInput
from django.http import request

from ajax_select.fields import AutoCompleteSelectField, AutoCompleteSelectMultipleField

from .models import *


class formProject(forms.ModelForm):
    class Meta:
        model = project
        fields = ("name", "description", "costCenter", "planedHours")
        
    tags = AutoCompleteSelectMultipleField('tags', required=False, help_text=None)
    responsible = AutoCompleteSelectMultipleField('responsible', help_text="Bitte füge einen Verantwortlichen ein")


class formWork(forms.ModelForm):
    #employee = AutoCompleteSelectMultipleField('account')
    class Meta:

        model = work
        fields = ("name", "hours", "startDate", "endDate")
    employe = AutoCompleteSelectMultipleField('employee', help_text="Wer hat mitgearbeitet?")


class hours(forms.ModelForm):
    
    class Meta:
        model = customHours
        fields = ("percentege", )