from functools import reduce

from django.db.models import F
from django.db.models.functions import Coalesce
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.views.generic import DeleteView

from arbeitsstunden.forms import ArbeitsstundenausschreibungForm, ProjectForm, ArbeitseinheitForm, \
    ArbeitsbeteiligungForm
from arbeitsstunden.models import Arbeitsstundenausschreibung, Arbeitsbeteiligung, Saison, Projekt, Arbeitseinheit
from django.urls import resolve

from arbeitsstunden.utils import get_aktuelle_saison, check_authentication_redirect_if_fails
from member.models import profile


'''
- Übersicht über das eigene Konto
- allgemeine Arbeitsstunden
- Übersicht über aktuelle Projekte
- Übersicht über letzte Eintragungen (Newsfead TODO: #159)
'''
def dashboard(request):
    
    pass

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
