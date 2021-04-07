from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.forms import fields
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from phonenumber_field.formfields import PhoneNumberField

from web.models import infoPage, HeadPage


class changeInfoPage(ModelForm):
    class Meta:
        model = infoPage
        # db_table = Profile
        fields = ['headPage', 'titel', 'text', 'name']

class changeHeaderPage(ModelForm):
    class Meta:
        model = HeadPage
        # db_table = Profile
        fields = ['titel', 'text', 'description', 'name', 'image']
        widgets = {
            'image': forms.FileInput(attrs={'style': 'display: none;', 'class': 'form-control', 'required': False, })
        }
