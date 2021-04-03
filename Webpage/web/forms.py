from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.forms import fields
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from phonenumber_field.formfields import PhoneNumberField

from web.models import InfoPage


class changeInfoPage(ModelForm):
    class Meta:
        model = InfoPage
        # db_table = Profile
        fields = ['status', 'titel', 'text', 'description', 'name']


