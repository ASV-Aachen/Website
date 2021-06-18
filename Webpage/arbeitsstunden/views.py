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

MOVED TO THE MAIN DASHBOARD
'''
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


# Übersicht über alle Accounts die diese Saison schon was gemacht haben
def overview(request):
    # TODO:
    season = getCurrentSeason()
    allAccounts = account.objects.all()

    personObjects = []

    for person in allAccounts:
        
        try:
            custom_hours = customHours.objects.get(used_account = person)
            profil = profile.objects.get(workingHoursAccount = person)
            gebrauchteStunden = custom_hours.getCustomHours()
            gearbeiteteStunden = person.HowManyHoursDoesUserHaveToWork()
            temp = {
                "gebrauchteStunden": gebrauchteStunden,
                "gearbeiteteStunden": gearbeiteteStunden,
                "Profil": profil,
                "user": profil.user, 
                "name": person.name,
                "darfSegeln": gebrauchteStunden == gearbeiteteStunden
            }
            personObjects.append(custom_hours)
        except:
            continue

        
        pass

    return render(request, template_name="arbeitsstunden/arbeitsstundenOverview.html", context={
        "personen": personObjects,
        "season": season
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
# API Endpunkt, einfügen eines neuen subProjektes. KEINE WEBSITE, HÖCHSTENS ERROR CODE
def addWork(request, projectID):
    project = get_object_or_404(work, id=projectID)

    if(request.method == "POST"):
        form = formProject(request.POST)
        if form.is_valid():
            form.save(commit=False)
            form.instance.id = projectID
            form.save()
            project.parts.add(project)
            # TODO
            return redirect("")
        
        return redirect("ErrorPage")
    else:
        form = formProject(instance=project)
        return render(request, "Arbeitsstunden/form_template.html", {
            "form": form
        })

def editWork(request, workID):    
    project = get_object_or_404(work, id=workID)

    if(request.method == "POST"):
        form = formProject(request.POST)
        if form.is_valid():
            form.save(commit=False)
            form.instance.id = workID
            form.save()
            # TODO
            return redirect("")
        
        return redirect("ErrorPage")
    else:
        form = formProject(instance=project)
        return render(request, "Arbeitsstunden/form_template.html", {
            "form": form
        })

def deleteWork(request, workID):
    projekt = get_object_or_404(work, id = workID)

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
    curentSeason = season.objects.filter(id=seasonId)
    projectsOfthatSeason = project.objects.filter(season = curentSeason)
    # projectsOfthatSeason = projectsOfthatSeason.filter(aktiv=True)

    return render(request, template_name="arbeitsstunden/singleSeasonOverview.html", context={
        "season": curentSeason,
        "projekte": projectsOfthatSeason
    })

# -----------------------------------------------------------------------------------------
# Übersicht über die Kostenstellen, mit Einsicht in laufende Projekte in der aktuellen Season
def costCenterOverview(request):
    allCenters = costCenter.objects.all()
    seasons = season.objects.all()[-5]
    
    data = []
    
    for i in allCenters:
        
        timedata = []
        
        projects = project.objects.filter(costCenter = i)
        
        for x in seasons:
            counter = 0
            seasonalData = projects.filter(season = x)
            for b in seasonalData:
                counter += b.workedHours()
            
            timedata.append({
                "season": x,
                "hours": counter
            })
        temp = {
            "center": i,
            "time": timedata
        }
        data.append(temp)  

    return render(request, template_name="arbeitsstunden/costCenterOverview.html", context={
        "centers": data 
    })



