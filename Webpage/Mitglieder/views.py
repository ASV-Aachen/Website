from django.shortcuts import render, redirect
from .models import Profile

# Create your views here.

# View um die eigenen einstellungen zu bearbeiten

# Mitgliederverzeichnis
# TODO

# Bearbeiten
# TODO
def MitgliedBearbeiten(request):
    if request.user.is_authenticated():
        if request.GET:
            id = request.user.id
            return render(request, template_name="MitgliedBearbeiten.html", context={'News': Profile.objects.get(id=id)})
        if request.POST:
            id = request.user.id
            AktuellerNutzer = Profile.objects.get(id=id)

            AktuellerNutzer.Heimatstadt = request.POST.get('Heimatstadt')
            AktuellerNutzer.PLZ = request.POST.get("PLZ")
            AktuellerNutzer.Land = request.POST.get("Land")

            AktuellerNutzer.EMail = request.POST.get("EMail")
            AktuellerNutzer.HandyNummer = request.POST.get("HandyNummer")
            AktuellerNutzer.save()

            return redirect("/")
            pass
    else:
        return redirect("/")


# Passwort ändern
# TODO