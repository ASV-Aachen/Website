from .models import account, season
from functools import reduce

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


# -----------------------------------------------------------------------------------------
'''
Alle Aktiven und geplante Projekte, sortiert nach Zeit, ein und ausklappbar
'''
def allAktivProjekts(request):

    aktiveProjecte = project.objects.filter(aktiv = True)

    return render(request, template_name="arbeitsstunden/allAktivProjects.html", context={
        "projekte": aktiveProjecte
    })

def newProjekt(request):
    if(request.method == "POST"):
        form = formProject(request.POST)
        if form.is_valid():
            form.save()
            # TODO
            return redirect("")
        
        return redirect("ErrorPage")
    else:
        form = formProject()
        return render(request, "Arbeitsstunden/form_template.html", {
            "form": form
        })
    pass

def showProjekt(request, projectID):
    project = get_object_or_404(project, id=projectID)
    return render(request, "Arbeitsstunden/showProjekt.html", {
            "project": project
        })

# Projekt Edit mit allen subprojekten und Übersichten
# bekommt daten über das Projekt und ein Formular zum ändern
def editProjekt(request, projectID):
    project = get_object_or_404(project, id=projectID)

    if(request.method == "POST"):
        form = formProject(request.POST)
        if form.is_valid():
            form.save(commit=False)
            form.instance.id = projectID
            form.save()
            # TODO
            return redirect("")
        
        return redirect("ErrorPage")
    else:
        form = formProject(instance=project)
        return render(request, "Arbeitsstunden/form_template.html", {
            "form": form
        })

def deleteProjekt(request, projectID):
    projekt = get_object_or_404(project, id = projectID)

    if 'key' in request.GET and request.GET['key'] != "":
                # Lösche den Nutzer
        givenKey = request.GET['key']
        if givenKey == hashlib.sha512(str(projekt).encode('utf-8')).hexdigest():
            projekt.delete()
            return redirect("")
    else:
        key = hashlib.sha512(str(projekt).encode('utf-8')).hexdigest()
        # sende Seite
        return render(request, "arbeitsstunden/delete.html", {"hash": key, "project": projekt})



# -----------------------------------------------------------------------------------------
def newSubprojectToProject(request, idProject):
    projekt = get_object_or_404(project, id = idProject)
    if(request.method == "POST"):
        form = formSubProject(request.POST)
        if form.is_valid():
            form.save(commit=False)
            form.instance.project = projekt
            form.save()
            # TODO
            return redirect("")
        return redirect("ErrorPage")
    else:
        form = formSubProject()
        return render(request, "Arbeitsstunden/form_template.html", {
            "form": form
        })

def newSubprojekt(request):
    if(request.method == "POST"):
        form = formSubProject(request.POST)
        if form.is_valid():
            form.save()
            # TODO
            return redirect("")
        return redirect("ErrorPage")
    else:
        form = formSubProject()
        return render(request, "Arbeitsstunden/form_template.html", {
            "form": form
        })

# Edit eines Subprojektes
def editSubproject(request, idSubproject):
    project = get_object_or_404(subproject, id=idSubproject)

    if(request.method == "POST"):
        form = formProject(request.POST)
        if form.is_valid():
            form.save(commit=False)
            form.instance.id = idSubproject
            form.save()
            # TODO
            return redirect("")
        
        return redirect("ErrorPage")
    else:
        form = formProject(instance=project)
        return render(request, "Arbeitsstunden/form_template.html", {
            "form": form
        })

def deleteSubproject(request, idSubproject):
    projekt = get_object_or_404(subproject, id = idSubproject)

    if 'key' in request.GET and request.GET['key'] != "":
                # Lösche den Nutzer
        givenKey = request.GET['key']
        if givenKey == hashlib.sha512(str(projekt).encode('utf-8')).hexdigest():
            projekt.delete()
            return redirect("")
    else:
        key = hashlib.sha512(str(projekt).encode('utf-8')).hexdigest()
        # sende Seite
        return render(request, "arbeitsstunden/delete.html", {"hash": key, "project": projekt})



# -----------------------------------------------------------------------------------------
# API Endpunkt, einfügen eines neuen subProjektes. KEINE WEBSITE, HÖCHSTENS ERROR CODE
def newWork(request, idSubProject):
    project = get_object_or_404(work, id=idWork)
    parent = get_object_or_404(subproject, id = idSubProject)

    if(request.method == "POST"):
        form = formProject(request.POST)
        if form.is_valid():
            form.save(commit=False)
            form.instance.id = idWork
            form.save()
            parent.parts.add(project)
            # TODO
            return redirect("")
        
        return redirect("ErrorPage")
    else:
        form = formProject(instance=project)
        return render(request, "Arbeitsstunden/form_template.html", {
            "form": form
        })

def editWork(request, idWork):    
    project = get_object_or_404(work, id=idWork)

    if(request.method == "POST"):
        form = formProject(request.POST)
        if form.is_valid():
            form.save(commit=False)
            form.instance.id = idWork
            form.save()
            # TODO
            return redirect("")
        
        return redirect("ErrorPage")
    else:
        form = formProject(instance=project)
        return render(request, "Arbeitsstunden/form_template.html", {
            "form": form
        })

def deleteWork(request, idWork):
    projekt = get_object_or_404(work, id = idWork)

    if 'key' in request.GET and request.GET['key'] != "":
                # Lösche den Nutzer
        givenKey = request.GET['key']
        if givenKey == hashlib.sha512(str(projekt).encode('utf-8')).hexdigest():
            projekt.delete()
            return redirect("")
    else:
        key = hashlib.sha512(str(projekt).encode('utf-8')).hexdigest()
        # sende Seite
        return render(request, "arbeitsstunden/delete.html", {"hash": key, "project": projekt})



# -----------------------------------------------------------------------------------------
# Übersicht mit Statistiken über alle seasons
def seasonOverview(request):
    return render(request, template_name="arbeitsstunden/seasonOverview.html", context={
        "seasons": season.objects.all()
    })


# Statistik über eine einzelne Season mit Statistik und allen entsprechenden Projekten
def singleSeasonOverview(request, seasonId):
    return render(request, template_name="arbeitsstunden/singleSeasonOverview.html", context={
        "season": season.objects.filter(id=seasonId)
    })

# -----------------------------------------------------------------------------------------
# Übersicht über die Kostenstellen, mit Einsicht in laufende Projekte in der aktuellen Season
def costCenterOverview(request):
    return render(request, template_name="arbeitsstunden/costCenterOverview.html", context={
        "center": costCenter.objects.all()
    })


def singleCostCenterOverview(request, centerID):
    return render(request, template_name="arbeitsstunden/singleCostCenterOverview.html", context={
        "center": costCenter.objects.filter(id = centerID)
    })
