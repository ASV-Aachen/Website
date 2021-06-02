from functools import reduce

from django.db.models import F
from django.db.models.functions import Coalesce
from django.shortcuts import render, redirect, get_object_or_404
import hashlib
# Create your views here.
from django.views.generic import DeleteView

from .models import *
from .forms import *
from django.urls import resolve

from member.models import profile
from datetime import datetime


'''
- Übersicht über das eigene Konto
- allgemeine Arbeitsstunden
- Übersicht über aktuelle Projekte
- Übersicht über letzte Eintragungen (Newsfead TODO: #159)
'''
def dashboard(request):
    current_account = profile.objects.get(user=request.user).workingHoursAccount
    last_Works = work.objects.filter(employee = current_account)

    return render(request, template_name="arbeitsstunden/dashboard.html", context={
        "konto": current_account,
        "seasons": season.objects.all()[-5],
        "kostenstelle": costCenter.objects.all(),
        "last_Work": last_Works
    })

'''
Alle Aktiven und geplante Projekte, sortiert nach Zeit, ein und ausklappbar
'''
def allAktivProjekts(request):
    pass

# Projekt Edit mit allen subprojekten und Übersichten
def editProjekt(request):
    pass

# Edit eines Subprojektes
def editSubproject(request, idSubproject):
    pass

# API Endpunkt, einfügen eines neuen subProjektes. KEINE WEBSITE, HÖCHSTENS ERROR CODE
def API_editWork(request, nameSubProject):    
    pass

# Übersicht mit Statistiken über alle seasons
def seasonOverview(request):
    pass

# Statistik über eine einzelne Season mit Statistik und allen entsprechenden Projekten
def singleSeasonOverview(request, seasonId):
    pass

# Übersicht über die Kostenstellen, mit Einsicht in laufende Projekte in der aktuellen Season
def costCenterOverview(request):
    pass


def singleCostCenterOverview(request, seasonID):
    pass
