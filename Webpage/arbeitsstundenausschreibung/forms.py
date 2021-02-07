from django import forms

from .models import Arbeitsstundenausschreibung

class ArbeitsstundenausschreibungForm(forms.ModelForm):

    class Meta:
        model = Arbeitsstundenausschreibung
        fields = ("Titel", "Beschreibung", "Boote", "Tags", "Verantwortlich")