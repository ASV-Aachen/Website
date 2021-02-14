from django import forms
from django.forms import CheckboxSelectMultiple

from .models import Arbeitsstundenausschreibung

class ArbeitsstundenausschreibungForm(forms.ModelForm):

    class Meta:
        model = Arbeitsstundenausschreibung
        fields = ("Titel", "Beschreibung", "Projekt", "Tags")
        widgets = {
            "Tags": CheckboxSelectMultiple()
        }