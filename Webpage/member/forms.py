from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.forms import fields
from django.utils.translation import ugettext_lazy as _

from .models import Profile

class changePersonalInfo(ModelForm):
    
    class Meta:
        model = Profile
        # db_table = Profile
        fields = ['HandyNummer','Heimatstadt', 'profile_image']
    
        widgets = {
            'image': forms.FileInput(attrs= {'style':'display: none;','class':'form-control', 'required': False,})
        }
    