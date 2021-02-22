#from django.contrib.auth import authenticate
from django.shortcuts import render, redirect, get_object_or_404
from .models import Profile
from django.contrib.auth.models import User
from .forms import changePersonalInfo


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
        Profil = get_object_or_404(Profile, user=request.user)

        if request.method == "POST":
            form = changePersonalInfo(request.POST, request.FILES, instance=Profil)
            
            if form.is_valid():

                form.save(commit=False)
                form.instance.user_id = request.user.id
                form.save()

                return redirect("ASV")
        else:
            form = changePersonalInfo(instance=Profil)
        return render(request, "member/Einstellungen.html", {"form": form})
    else:
        return redirect("ASV")


# Passwort ändern
# TODO