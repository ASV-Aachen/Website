from django import forms
from django.db.models import fields
from django.forms import CheckboxSelectMultiple, DateInput
from django.http import request

from .models import *


class formProject(forms.ModelForm):
    class Meta:
        model = project
        fields = ("name", "description", "tags", "responsible", "costCenter", "planedHours")


class formSubProject(forms.ModelForm):
    class Meta:
        model = subproject
        fields = ("name", "description", "voluntary", "planed", "endDate", "planedHours")

class formWork(forms.ModelForm):
    class Meta:
        model = work
        fields = ("employee", "hours", "description", "date")

class hours(forms.ModelForm):
    
    class Meta:
        model = customHours
        fields = ("percentege", )