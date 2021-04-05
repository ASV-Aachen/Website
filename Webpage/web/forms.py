from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.forms import fields
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from phonenumber_field.formfields import PhoneNumberField

from web.models import infoPage


class changeInfoPage(ModelForm):
    class Meta:
        model = infoPage
        # db_table = Profile
        fields = ['id', 'status', 'titel', 'text', 'description', 'name']


