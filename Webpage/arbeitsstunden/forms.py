from django import forms
from django.forms import CheckboxSelectMultiple, DateField

from .models import Arbeitsstundenausschreibung

class ArbeitsstundenausschreibungForm(forms.ModelForm):

    class Meta:
        model = Arbeitsstundenausschreibung
        fields = ("Titel", "Beschreibung", "Projekt", "Tags", "Umfang", "Fertigstellungstermin")
        widgets = {
            "Tags": CheckboxSelectMultiple(),
            #"Fertigstellungstermin": DateField()
        }