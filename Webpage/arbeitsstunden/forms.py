from django import forms
from django.forms import CheckboxSelectMultiple, DateInput

from .models import Arbeitsstundenausschreibung, Projekt, Arbeitseinheit, Arbeitsbeteiligung


class ArbeitsstundenausschreibungForm(forms.ModelForm):
    class Meta:
        model = Arbeitsstundenausschreibung
        fields = ("Titel", "Beschreibung", "Projekt", "Tags", "Umfang", "Fertigstellungstermin")
        widgets = {
            "Tags": CheckboxSelectMultiple(),
            # "Fertigstellungstermin": DateField()
        }


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Projekt
        fields = ("Saison", "Name", "Beschreibung", "Verantwortlich")
        widgets = {
            "Verantwortlich": CheckboxSelectMultiple(),
        }


class ArbeitseinheitForm(forms.ModelForm):
    class Meta:
        model = Arbeitseinheit
        fields = ("Projekt", "Beschreibung", "Datum", "Ausschreibung")
        widgets = {
            "Datum": DateInput(format='%d.%m.%Y', attrs={'type': 'date'})
        }


class ArbeitsbeteiligungForm(forms.ModelForm):
    class Meta:
        model = Arbeitsbeteiligung
        fields = ("Arbeitseinheit", "Arbeitsleistender", "Arbeitszeit")
