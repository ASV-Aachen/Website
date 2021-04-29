#from django.contrib.auth import authenticate
import csv
import io

from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django import template

from .forms import *
from .models import *
from utils.loginFunctions import *

# Create your views here.

# View um die eigenen einstellungen zu bearbeiten
# Index-View zum Dashborad als Startseite vom "Mein ASV"

def ubersicht(request):
    jollen = boot.objects.filter(isboat=True)
    return render(request, "jollen/ubersicht-jollen.html", context={
            "Jollen": jollen
        })

@login_required
def jollen_status(request):
    jollen = boot.objects.all()
    return render(request, "jollen/jollen_status.html", context={
        "Jollen": jollen
    })



def description(request, name):
    jolle = get_object_or_404(boot, name=name)
    return render(request, "jollen/description.html", context={
                    "Jollen": jolle
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
            "Jollen": jolle, 
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
            "Jollen": jolle, 
            "form": form
            })
    pass



