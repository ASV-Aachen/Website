from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.forms import fields
from django.utils.translation import ugettext_lazy as _
from phonenumber_field.formfields import PhoneNumberField
from tinymce.widgets import TinyMCE

from .models import blogPost


class newBlogEntry(ModelForm):
    class Meta:
        model = blogPost
        fields = ['titel', 'text']
