from django import forms
from django.forms import CheckboxSelectMultiple, DateInput

from .models import Cruise, Sailor, CruiseShare, License

class CruiseForm(forms.ModelForm):
    class Meta:
        model = Cruise
        fields = ("CruiseName", "CruiseDescription", "StartDate", "EndDate", "StartPort", "EndPort", "MaxBerths")
        widgets = {
            "StartDate": DateInput(format='%d.%m.%Y', attrs={'type': 'date'}),
            "EndDate": DateInput(format='%d.%m.%Y', attrs={'type': 'date'})
        }