from functools import reduce

from django.db.models import F
from django.db.models.functions import Coalesce

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.template import Context, Template
from django.template.base import logger
from django.http import HttpResponse


# Create your views here.
from django.views.generic import DeleteView

from django.urls import resolve
from .forms import *
from .models import *
from .utils import get_aktuelle_saison, check_authentication_redirect_if_fails
from member.models import profile
from utils.loginFunctions import *
from utils.member import userToHash


def overview(request):

    cruises = cruise.objects.all()
    return render(request, "cruises/cruisesOverview.html", context={
        "cruises": cruises
    })


def newCruise(request):
    if(request.method == "POST"):
        form = formCruise(request.POST)
        if form.is_valid():
            form.save(commit=False)
            if request.GET['id'] != "":
                if (cruise.objects.filter(id = request.GET['id']).exists()):
                    form.instance.id = request.GET['id']
            form.save()

            return redirect("cruisesOverview")
        form.errors.as_data()
        return redirect("cruisesOverview")
    else:
        if ('id' in request.GET):
            id = request.GET['id']
            # ID gegeben, also Daten laden
            if(cruise.objects.filter(id=id).exists()):
                # ID existiert, also zurückgeben
                reise = cruise.objects.get(id=id)
                form = formCruise(instance=reise)
                return render(request, "cruises/form_template.html", {"form": form, "cruise": reise})
            else:
                # ID ist zwar gegeben, existiert aber nicht
                return redirect("cruisesOverview")

        else:
            # Keine ID gegeben, neuen Artikel anlegen
            form = formCruise()
            return render(request, "cruises/form_template.html", {"form": form})
    pass

def deleteCruise(request):
    if ('id' in request.GET) and request.GET['id'] != "" and cruise.objects.get(id=id).exists():

        id = request.GET['id']

        if 'key' in request.GET and request.GET['key'] != "":
            # Lösche den Nutzer
            givenKey = request.GET['key']
            if givenKey == userToHash(id):
                cruise.objects.get(id=id).delete()
                return redirect("cruisesOverview")
        else:
            key = userToHash(id)
            # sende Seite
            return render(request, "cruise/delete.html", {"hash": key, "cruise": cruise.objects.get(id=id)})


    return redirect("cruisesOverview")