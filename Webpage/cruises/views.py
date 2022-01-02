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
    yearDropdown = []
    for y in range((datetime.datetime.now().year), 2011, -1):
        yearDropdown.append(y)
    if ('id' in request.GET):
        id = request.GET['id']
        if(cruise.objects.filter(id=id).exists()):
            reise = cruise.objects.get(id=id)
            cruiseShares = cruiseShare.objects.all().filter(Cruise=reise)
            if ('year' in request.GET):
                year = request.GET['year']
                cruises = cruise.objects.filter(startDate__year=year).order_by('startDate')
                return render(request, "cruises/cruisesOverview.html", context={"cruises": cruises, "reise": reise, "cruiseShares": cruiseShares, "yearDropdown": yearDropdown, "selectedYear": year})
            cruises = cruise.objects.all().order_by('startDate')
            return render(request, "cruises/cruisesOverview.html", context={"cruises": cruises, "reise": reise, "cruiseShares": cruiseShares})
    elif ('year' in request.GET):
        year = request.GET['year']
        cruises = cruise.objects.filter(startDate__year=year).order_by('startDate')
        return render(request, "cruises/cruisesOverview.html", context={"cruises": cruises, "yearDropdown": yearDropdown, "selectedYear": year})
    else:
        selectedYear=datetime.datetime.now().year
        cruises = cruise.objects.filter(startDate__year=selectedYear).order_by('startDate')

        return render(request, "cruises/cruisesOverview.html", context={"cruises": cruises, "yearDropdown": yearDropdown, "selectedYear": selectedYear})

def overviewx(request, id):
    if(cruise.objects.filter(id=id).exists()):
        cruises = cruise.objects.all().order_by('startDate')
        reise = cruise.objects.get(id=id)
        cruiseShares = cruiseShare.objects.all().filter(Cruise=reise)
        return render(request, "cruises/cruisesOverview.html", context={"cruises": cruises, "reise": reise, "cruiseShares": cruiseShares})


def newCruise(request):
    if(request.method == "POST"):
        form = formCruise(request.POST)
        if form.is_valid():
            form.save(commit=False)
#            if request.GET['id'] != "":
#                if (cruise.objects.filter(id = request.GET['id']).exists()):
#                    form.instance.id = request.GET['id']
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

def editCruise(request):
    if(request.method == "POST"):
        form = formCruise(request.POST)
        if form.is_valid():
            form.save(commit=False)
            if request.GET['id'] != "":
                if (cruise.objects.filter(id = request.GET['id']).exists()):
                    form.instance.id = request.GET['id']
            form.save()
            if request.POST['sailors'] != "|":
                for i in request.POST["sailors"][1:-1].split('|'):
                    idx = int(i)
                    responsible = get_object_or_404(account, id=idx)
                    
                    form.instance.sailors.add(responsible)


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
                cruiseShares = cruiseShare.objects.all().filter(Cruise=reise)
#                sailors = []
#                for share in cruiseShares:
#                    sailors.append(share.cosailor)
                return render(request, "cruises/form_template.html", {"form": form, "cruise": reise, "cruiseShares" : cruiseShares}) #, "sailors": sailors
            else:
                # ID ist zwar gegeben, existiert aber nicht
                return redirect("cruisesOverview")

        else:
            # Keine ID gegeben, neuen Artikel anlegen
            form = formCruise()
            return render(request, "cruises/form_template.html", {"form": form})
    pass

def deleteCruise(request):
    if ('id' in request.GET) and request.GET['id'] != "":

        id = request.GET['id']
        cruise.objects.get(id=id).delete()

    return redirect("cruisesOverview")

def deleteCruiseShare(request):
    yearDropdown = []
    for y in range((datetime.datetime.now().year), 2011, -1):
        yearDropdown.append(y)
    
    if ('id' in request.GET) and request.GET['id'] != "":
        id = request.GET['id']
        cruiseShare.objects.get(id=id).delete()

    if ('cid' in request.GET) and request.GET['cid'] != "":
        cid = request.GET['cid']
        if ('year' in request.GET):
            year = request.GET['year']
            reise = cruise.objects.get(id=cid)
            cruiseShares = cruiseShare.objects.all().filter(Cruise=reise)
            cruises = cruise.objects.filter(startDate__year=year).order_by('startDate')
            return render(request, "cruises/cruisesOverview.html", context={"cruises": cruises, "reise": reise, "cruiseShares": cruiseShares, "yearDropdown": yearDropdown, "selectedYear": year})
        return redirect('cruisesOverview', id=cid)
    return redirect("cruisesOverview")


def makeCrew(request):
    yearDropdown = []
    for y in range((datetime.datetime.now().year), 2011, -1):
        yearDropdown.append(y)

    if ('id' in request.GET) and request.GET['id'] != "":
        id = request.GET['id']
        share = cruiseShare.objects.get(id=id)
        share.SailAs = 'C'
        share.save()

    if ('cid' in request.GET) and request.GET['cid'] != "":
        cid = request.GET['cid']
        if ('year' in request.GET):
            year = request.GET['year']
            reise = cruise.objects.get(id=cid)
            cruiseShares = cruiseShare.objects.all().filter(Cruise=reise)
            cruises = cruise.objects.filter(startDate__year=year).order_by('startDate')
            return render(request, "cruises/cruisesOverview.html", context={"cruises": cruises, "reise": reise, "cruiseShares": cruiseShares, "yearDropdown": yearDropdown, "selectedYear": year})
        return redirect('cruisesOverview', id=cid)
    return redirect("cruisesOverview")

def makeWatch(request):
    yearDropdown = []
    for y in range((datetime.datetime.now().year), 2011, -1):
        yearDropdown.append(y)
    
    if ('id' in request.GET) and request.GET['id'] != "":
        id = request.GET['id']
        share = cruiseShare.objects.get(id=id)
        share.SailAs = 'W'
        share.save()
        
    if ('cid' in request.GET) and request.GET['cid'] != "":
        cid = request.GET['cid']
        if ('year' in request.GET):
            year = request.GET['year']
            reise = cruise.objects.get(id=cid)
            cruiseShares = cruiseShare.objects.all().filter(Cruise=reise)
            cruises = cruise.objects.filter(startDate__year=year).order_by('startDate')
            return render(request, "cruises/cruisesOverview.html", context={"cruises": cruises, "reise": reise, "cruiseShares": cruiseShares, "yearDropdown": yearDropdown, "selectedYear": year})
        return redirect('cruisesOverview', id=cid)
    return redirect("cruisesOverview")

def makeSkipper(request):
    yearDropdown = []
    for y in range((datetime.datetime.now().year), 2011, -1):
        yearDropdown.append(y)
   
    if ('id' in request.GET) and request.GET['id'] != "":
        id = request.GET['id']
        share = cruiseShare.objects.get(id=id)
        share.SailAs = 'S'
        share.save()
   
    if ('cid' in request.GET) and request.GET['cid'] != "":
        cid = request.GET['cid']
        if ('year' in request.GET):
            year = request.GET['year']
            reise = cruise.objects.get(id=cid)
            cruiseShares = cruiseShare.objects.all().filter(Cruise=reise)
            cruises = cruise.objects.filter(startDate__year=year).order_by('startDate')
            return render(request, "cruises/cruisesOverview.html", context={"cruises": cruises, "reise": reise, "cruiseShares": cruiseShares, "yearDropdown": yearDropdown, "selectedYear": year})
        return redirect('cruisesOverview', id=cid)
    return redirect("cruisesOverview")