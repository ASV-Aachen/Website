from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.forms import fields
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from phonenumber_field.formfields import PhoneNumberField

from .models import profile

class changePersonalInfo(ModelForm):
    
    class Meta:
        model = profile
        # db_table = Profile
        fields = ['phone','mobile', 'status', 'hometown', 'profile_image']
    
        widgets = {
            'image': forms.FileInput(attrs= {'style':'display: none;','class':'form-control', 'required': False,})
        }

class createNewMember(ModelForm):
    class Meta:
        model = User

        fields = ['last_name', 'first_name', 'email']
