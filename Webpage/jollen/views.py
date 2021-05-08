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
from datetime import datetime

# Create your views here.

# View um die eigenen einstellungen zu bearbeiten
# Index-View zum Dashborad als Startseite vom "Mein ASV"

def ubersicht(request):
    jollen = boot.objects.filter(isboat=True).order_by('klasse')
    return render(request, "jollen/ubersicht-jollen.html", context={
            "Jollen": jollen
        })

@login_required
def jollen_status(request):
    jollen = boot.objects.all().order_by('klasse')
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
        form = settings_status_form(request.POST, request.FILES)

        if form.is_valid():
            form.save(commit=False)
            form.instance.autor = request.user

            if jolle.message is None:
                temp = nachricht(status=form.instance.status, standort=form.instance.standort, text = form.instance.text, autor= request.user)
                temp.save()
                jolle.message = temp
            else:
                # neue Historie erstellen
                newHistory = nachricht_historie(text = jolle.message.text, autor = jolle.message.autor, date= jolle.message.date)
                newHistory.save()
                jolle.history.add(newHistory)
                
                form.instance.date = datetime.now()
                form.instance.autor = request.user
                form.instance.id = jolle.message.id

                form.save()


            jolle.save()
            
            # abspeichern
            
            
            return redirect('jollenStatus')
    else:
        form = settings_status_form(instance=jolle.message)
        form.instance.text = " "

        return render(request, "jollen/jollen_editor.html", {
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
        form = settings_description_form(request.POST, request.FILES)
        form.instance.id = jolle.instance.id

        if form.is_valid():
            # abspeichern
            form.save()
            
            return redirect('jollenStatus')
    else:
        form = settings_description_form(instance = jolle)

        return render(request, "jollen/jollen_editor.html", {
            "Jollen": jolle, 
            "form": form
            })
    pass



