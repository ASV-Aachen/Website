from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.forms import fields
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from phonenumber_field.formfields import PhoneNumberField

from .models import *


class settings_status(ModelForm):
    class Meta:
        model = nachricht
        # Anpassen vom Status und Nachricht des Bootes
        fields = ['staus', 'standort', 'text']

class settings_description(ModelForm):
    class Meta:
        model = boot
        #  Anpassen vom Namen, Beschreibungstext, Bootsclasse und co

        fields = ['name', 'description', 'obman', 'image']
        widgets = {
            'image': forms.FileInput(attrs={'style': 'display: none;', 'class': 'form-control', 'required': False, })
        }
