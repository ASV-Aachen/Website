from django import forms
from django.db.models import fields
from django.forms import CheckboxSelectMultiple, DateInput
from django.http import request

from .models import *


class formProject(forms.ModelForm):
    class Meta:
        model = project
        fields = ("name", "description", "tags", "responsible", "costCenter", "plannedHours")


class formSubProject(forms.ModelForm):
    class Meta:
        model = subproject
        fields = ("name", "description", "voluntary", "planed", "endDate", "planedHours")

class formWork(request):
    class Meta:
        model = work
        fields = ("employee", "hours", "description", "date")