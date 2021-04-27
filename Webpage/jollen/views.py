#from django.contrib.auth import authenticate
import csv
import io

from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from .forms import *
from .models import *

# Create your views here.

# View um die eigenen einstellungen zu bearbeiten
# Index-View zum Dashborad als Startseite vom "Mein ASV"

def ubersicht(request):
    # Wenn angemeldet
    jollen = boot.objects.all()
    if (request.user.is_authenticated):
        return render(request, "jollen/ubersicht_mitglied.html", context={
                "Jollen": jollen
            })
    # wenn nicht
    else:
        return render(request, "jollen/ubersicht_gast.html", context={
                "Jollen": jollen
            })
    pass
    

def description(request, name):
    jolle = get_object_or_404(boot, name=name)
    return render(request, "jollen/description.html", context={
                    "Jolle": jolle
                })


@login_required
def settings_status(request, name):
    # Anpassen vom Status und Nachricht des Bootes
    jolle = get_object_or_404(boot, name=name)

    if request.method == "POST":
        # Eintragen in die DB
        form = settings_status(request.POST, request.FILES)

        if form.is_valid():
            form.save(commit=False)
            form.instance.autor = request.user
            
            # neue Historie erstellen
            newHistory = nachricht_historie(text = form.instance.text, autor = form.instance.autor)
            newHistory.save()
            jolle.history.add(newHistory)
            jolle.save()
            
            # abspeichern
            form.save()
            
            return redirect('jollenÜbersicht')
    else:
        form = settings_status(instance = jolle.message)

        return render(request, "web/jollen_editor.html", {
            "jolle": jolle, 
            "form": form
            })


    pass

@login_required
@user_passes_test(isUserPartOfGroup_Editor)
def settings_description(request, name):
    # Anpassen vom Namen, Beschreibungstext, Bootsclasse und co
    #TODO
    jolle = get_object_or_404(boot, name=name)

    if request.method == "POST":
        # Eintragen in die DB
        form = settings_description(request.POST, request.FILES)

        if form.is_valid():
            # abspeichern
            form.save()
            
            return redirect('jollenÜbersicht')
    else:
        form = settings_description(instance = jolle)

        return render(request, "web/jollen_editor.html", {
            "jolle": jolle, 
            "form": form
            })
    pass


'''
- [ ] Boote ins MenüObject einfügen
    - [ ] Header-Generierung anpassen
'''