from django.core import exceptions
from django.core.checks.messages import Error
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
from django.contrib.auth.decorators import login_required, user_passes_test

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
@login_required
def overview(request):
    season = getCurrentSeason()[0]
    allAccounts = account.objects.all()

    aktive = []
    andereMitglieder = []

    for account_of_person in allAccounts:
            try:
                custom_hours = customHours.objects.get(used_account = account_of_person)
                all_profil = profile.objects.all()
                users_profil = all_profil.get(workingHoursAccount = account_of_person)

                gebrauchteStunden = custom_hours.getCustomHours()
                gearbeiteteStunden = account_of_person.workedHours(season = season)
                
                temp = {
                    "gebrauchteStunden": gebrauchteStunden,
                    "gearbeiteteStunden": gearbeiteteStunden,
                    "Profil": users_profil,
                    "user": users_profil.user, 
                    "name": account_of_person.name,
                    "darfSegeln": gebrauchteStunden < gearbeiteteStunden
                }

                if users_profil.status == 1 or users_profil.status == 2:
                    aktive.append(temp)
                else:
                    andereMitglieder.append(temp)
            
            except Exception as e:
                print(e)
                continue
                pass

    return render(request, template_name="arbeitsstunden/arbeitsstundenOverview.html", context={
        "personen": aktive,
        "andere": andereMitglieder,
        "season": season
    })


# -----------------------------------------------------------------------------------------
'''
Alle Aktiven und geplante Projekte, sortiert nach Zeit, ein und ausklappbar
'''
@login_required
def allAktivProjekts(request):

    aktiveProjecte = project.objects.filter(aktiv = True)
    formForProject = formProject()

    return render(request, template_name="arbeitsstunden/allAktivProjects.html", context={
        "projekte": aktiveProjecte,
        "form": formForProject
    })

@login_required
def newProjekt(request):
    if(request.method == "POST"):
        form = formProject(request.POST)
        if form.is_valid():
            form.save(commit=False)
            form.instance.season = getCurrentSeason()[0]
            form.save()

            return redirect("projekte_overview")
        
        return redirect("ErrorPage")
    else:
        form = formProject()
        return render(request, "arbeitsstunden/form_template.html", {
            "form": form
        })
    pass

@login_required
def showProjekt(request, projectID):
    projekteToShow = get_object_or_404(project, pk=projectID)

    Projektform = formProject(instance = projekteToShow)
    newWorkForm = formWork()
    
    return render(request, "arbeitsstunden/showProjekt.html", {
            "project": projekteToShow,
            "Projektform": Projektform,
            "newWorkForm": newWorkForm
        })

# Projekt Edit mit allen subprojekten und Übersichten
# bekommt daten über das Projekt und ein Formular zum ändern
@login_required
def editProjekt(request, projectID):
    projekteToShow = get_object_or_404(project, id=projectID)

    if(request.method == "POST"):
        form = formProject(request.POST)
        if form.is_valid():
            form.save(commit=False)

            form.instance.id = projectID
            form.save()

            if request.POST["responsible"] is not "|":
                for x in projekteToShow.responsible.all():
                    projekteToShow.responsible.remove(x)

            for i in request.POST["responsible"][1:-1].split('|'):
                id = int(i)
                responsible = get_object_or_404(User, id=id)
                
                projekteToShow.responsible.add(responsible)

            # TODO
            return redirect("projekte_detail", projectID)
        
        # return redirect("ErrorPage")
    return redirect("projekte_detail", projectID)

@login_required
# @user_passes_test(isUserPartOfGroup_Takel)
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

@login_required
def addWork(request, projectID):
    used_Projekt = get_object_or_404(project, id=projectID)
    # realprojektID = get_object_or_404(project, project in parts)
    id = used_Projekt.id

    if(request.method == "POST"):
        form = formWork(request.POST)
        if form.is_valid():
            form.save(commit=False)
            # form.instance.id = projectID
            form.save()
            used_Projekt.parts.add(form.instance)
            
            for i in request.POST["employe"][1:-1].split('|'):
                idx = int(i)
                responsible = get_object_or_404(account, id=idx)
                
                form.instance.employee.add(responsible)

            return redirect("projekte_detail", projectID=id)
        
        return redirect("ErrorPage")
    else:
        form = formProject(instance=project)
        return render(request, "arbeitsstunden/form_template.html", {
            "form": form
        })

@login_required
def editWork(request, workID):    
    project = get_object_or_404(work, id=workID)
    realprojektID = get_object_or_404(project, project in parts)
    id = project.id

    if(request.method == "POST"):
        form = formWork(request.POST)
        if form.is_valid():
            form.save(commit=False)
            form.instance.id = workID
            form.save()
            # TODO
            return redirect("projekte_detail", projectID = id)
        
        return redirect("ErrorPage")
    else:
        form = formProject(instance=project)
        return render(request, "arbeitsstunden/form_template.html", {
            "form": form
        })

@login_required
# @user_passes_test(isUserPartOfGroup_Takel)
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
@login_required
def seasonOverview(request):
    return render(request, template_name="arbeitsstunden/seasonOverview.html", context={
        "seasons": season.objects.all()
    })


# Statistik über eine einzelne Season mit Statistik und allen entsprechenden Projekten
@login_required
# @user_passes_test(isUserPartOfGroup_Takel)
def singleSeasonOverview(request, year):
    curentSeason = season.objects.get(year=year)
    projectsOfthatSeason = project.objects.filter(season = curentSeason)
    # projectsOfthatSeason = projectsOfthatSeason.filter(aktiv=True)

    return render(request, template_name="arbeitsstunden/singleSeasonOverview.html", context={
        "season": curentSeason,
        "projekte": projectsOfthatSeason
    })

# -----------------------------------------------------------------------------------------
# Übersicht über die Kostenstellen, mit Einsicht in laufende Projekte in der aktuellen Season
@login_required
def costCenterOverview(request):
    allCenters = costCenter.objects.all()
    seasons = season.objects.all()[:5]
    
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



