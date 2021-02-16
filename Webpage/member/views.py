#from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from .models import Profile

# Create your views here.

# View um die eigenen einstellungen zu bearbeiten
# Index-View zum Dashborad als Startseite vom "Mein ASV"

def index(request):
    return render(request, "member/dashboard.html")

# Mitgliederverzeichnis
def Migliederverzeichnis(request):
    if (request.user.is_authenticated):
        context = {'Personen': Profile.objects.all()}
        return render(request, template_name="member/Mitgliderverzeichnis.html", context=context)
    else:
        return redirect("ASV")

# Anzeige für den Einzelnen Nutzer
def EinzelNutzer(request):
    if (request.user.is_authenticated):
        User = request.GET.get('id', '')
        context = {'User': Profile.objects.get(id=User)}
        return render(request, template_name="member/Nutzer.html", context=context)
    else:
        return redirect("ASV")
    pass


# Bearbeiten
def Einstellungen(request):
    if (request.user.is_authenticated):
        if request.GET:
            id = request.user.id
            return render(request, template_name="member/Einstellungen.html", context={'News': Profile.objects.get(id=id)})
        if request.POST:
            id = request.user.id
            AktuellerNutzer = Profile.objects.get(id=id)

            AktuellerNutzer.Heimatstadt = request.POST.get('Heimatstadt')
            AktuellerNutzer.PLZ = request.POST.get("PLZ")
            AktuellerNutzer.Land = request.POST.get("Land")

            AktuellerNutzer.EMail = request.POST.get("EMail")
            AktuellerNutzer.HandyNummer = request.POST.get("HandyNummer")
            AktuellerNutzer.save()

            return redirect("ASV")
            pass
    else:
        return redirect("ASV")


# Passwort ändern
# TODO