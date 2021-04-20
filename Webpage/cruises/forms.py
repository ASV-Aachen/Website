from django import forms
from django.forms import CheckboxSelectMultiple, DateInput
from django.contrib.admin.widgets import FilteredSelectMultiple

from .models import Cruise, Sailor, CruiseShare, License
from member.models import profile


class CruiseForm(forms.ModelForm):
    class Meta:
        model = Cruise
        fields = ("CruiseName", "CruiseDescription", "StartDate", "EndDate", "StartPort", "EndPort", "MaxBerths")
        widgets = {
            "StartDate": DateInput(format='%d.%m.%Y', attrs={'type': 'date'}),
            "EndDate": DateInput(format='%d.%m.%Y', attrs={'type': 'date'})
        }
        labels = {
            "CruiseName": "Seereise",
            "CruiseDescription" : "Beschreibung",
            "StartDate" : "Startdatum",
            "EndDate" : "Enddatum",
            "StartPort" : "Ausgangshafen",
            "EndPort" : "Zielhafen",
            "MaxBerths" : "max. Kojen",
        }
    Sailors =  forms.ModelMultipleChoiceField(widget=FilteredSelectMultiple("Sailors", is_stacked=False),queryset=profile.objects.all())