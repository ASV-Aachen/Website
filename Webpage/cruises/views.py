from functools import reduce

from django.db.models import F, Case, When
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

def sailorOverview(request):
    sailors = sailor.objects.all().order_by('givenName')
    return render(request, "cruises/sailorOverview.html", context={"sailors": sailors})

def sailorDetails(request):
    if ('id' in request.GET):
        id = request.GET['id']
        sailorId = sailor.objects.get(id=id)
        cruiseShares = cruiseShare.objects.all().filter(cosailor=id).order_by('Cruise__startDate')
        licenses = license.objects.all().filter(Owner=id)
        return render(request, "cruises/sailorDetails.html", context={"sailor": sailorId, "shares": cruiseShares, "licenses":licenses})
    else:
        sailors = sailor.objects.all().order_by('givenName')
        return render(request, "cruises/sailorOverview.html", context={"sailors": sailors})

def addLicense(request):
    if(request.method == "POST"):
        form = formLicense(request.POST)
        if form.is_valid():
            form.save(commit=False)
            id = request.GET['id']
            sailorId = sailor.objects.get(id=id)
            form.instance.Owner=sailorId
            form.save()
        if ('id' in request.GET):
            id = request.GET['id']
            sailorId = sailor.objects.get(id=id)
            cruiseShares = cruiseShare.objects.all().filter(cosailor=id).order_by('Cruise__startDate')
            licenses = license.objects.all().filter(Owner=id)
            return render(request, "cruises/sailorDetails.html", context={"sailor": sailorId, "shares": cruiseShares, "licenses":licenses})
        else:
            sailors = sailor.objects.all().order_by('givenName')
            return render(request, "cruises/sailorOverview.html", context={"sailors": sailors})
    else:
        if ('id' in request.GET):
            id = request.GET['id']
            # ID gegeben, also Daten laden
            if(sailor.objects.filter(id=id).exists()):
                # ID existiert, also zurückgeben
                owner = sailor.objects.get(id=id)
                form = formLicense()
                return render(request, "cruises/form_template.html", {"form": form, "Owner": owner})
            else:
                # ID ist zwar gegeben, existiert aber nicht
                return redirect("sailorOverview")

        else:
            # Keine ID gegeben, neuen Artikel anlegen
            form = formLicense()
            return render(request, "cruises/form_template.html", {"form": form})
    pass

def overview(request):
    yearDropdown = []
    for y in range((datetime.datetime.now().year), 2011, -1):
        yearDropdown.append(y)
    pos = ['S', 'W', 'C']
    order = Case(*[When(SailAs=SailAs, then=en) for en, SailAs in enumerate(pos)])
    if ('id' in request.GET):
        id = request.GET['id']
        if(cruise.objects.filter(id=id).exists()):
            reise = cruise.objects.get(id=id)
            cruiseShares = cruiseShare.objects.all().filter(Cruise=reise).order_by(order,'cosailor')
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
        year=datetime.datetime.now().year
        cruises = cruise.objects.filter(startDate__year=year).order_by('startDate')
        return render(request, "cruises/cruisesOverview.html", context={"cruises": cruises, "yearDropdown": yearDropdown, "selectedYear": year})

def newCruise(request):
    yearDropdown = []
    for y in range((datetime.datetime.now().year), 2011, -1):
        yearDropdown.append(y)
    if ('year' in request.GET):
        year = request.GET['year']
    else:
        year = datetime.datetime.now().year
    pos = ['S', 'W', 'C']
    order = Case(*[When(SailAs=SailAs, then=en) for en, SailAs in enumerate(pos)])
    if(request.method == "POST"):
        form = formCruise(request.POST)
        if form.is_valid():
            form.save(commit=False)
#            if request.GET['id'] != "":
#                if (cruise.objects.filter(id = request.GET['id']).exists()):
#                    form.instance.id = request.GET['id']
            form.save()
            if request.POST['sailors'] != "|":
                for i in request.POST["sailors"][1:-1].split('|'):
                    idx = int(i)
                    responsible = get_object_or_404(sailor, id=idx)
                    form.instance.sailors.add(responsible)
        
            return redirect("cruisesOverview")
        form.errors.as_data()
        cruises = cruise.objects.filter(startDate__year=year).order_by('startDate') 
        cid=form.id
        reise = cruise.objects.get(id=cid)
        cruiseShares = cruiseShare.objects.all().filter(Cruise=reise).order_by(order,'cosailor')
        return render(request, "cruises/cruisesOverview.html", context={"cruises": cruises, "reise": reise, "cruiseShares": cruiseShares, "yearDropdown": yearDropdown, "selectedYear": year})
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
    yearDropdown = []
    for y in range((datetime.datetime.now().year), 2011, -1):
        yearDropdown.append(y)
    if ('year' in request.GET):
        year = request.GET['year']
    else:
        year = datetime.datetime.now().year
    if ('id' in request.GET):
        cid = request.GET['id']
    else:
        cid = 1
    pos = ['S', 'W', 'C']
    order = Case(*[When(SailAs=SailAs, then=en) for en, SailAs in enumerate(pos)])
    if(request.method == "POST"):
        form = formCruise(request.POST)
        cruises = cruise.objects.filter(startDate__year=year).order_by('startDate') 
        if form.is_valid():
            form.save(commit=False)
            if request.GET['id'] != "":
                if (cruise.objects.filter(id = request.GET['id']).exists()):
                    form.instance.id = request.GET['id']
            form.save()
            if request.POST['sailors'] != "|":
                for i in request.POST["sailors"][1:-1].split('|'):
                    idx = int(i)
                    person = get_object_or_404(sailor, id=idx)
                    cs1 = cruiseShare(cosailor = person, Cruise = form.instance)
                    if (person.ownedPatent):
                        cs1.SailAs=person.ownedPatent.Type
                    cs1.save()
         #   return render(request, "cruises/cruisesOverview.html", context={"cruises": cruises, "yearDropdown": yearDropdown, "reise": 1, "selectedYear": year})
        form.errors.as_data()
        reise = cruise.objects.get(id=cid)
        cruiseShares = cruiseShare.objects.all().filter(Cruise=reise).order_by(order,'cosailor')
        return render(request, "cruises/cruisesOverview.html", context={"cruises": cruises, "reise": reise, "cruiseShares": cruiseShares, "yearDropdown": yearDropdown, "selectedYear": year})
        
        #return render(request, "cruises/cruisesOverview.html", context={"cruises": cruises, "yearDropdown": yearDropdown, "id": cid, "selectedYear": year})
    else:
        if ('id' in request.GET):
            id = request.GET['id']
            # ID gegeben, also Daten laden
            if(cruise.objects.filter(id=id).exists()):
                # ID existiert, also zurückgeben
                reise = cruise.objects.get(id=id)
                form = formCruise(instance=reise)
                cruiseShares = cruiseShare.objects.all().filter(Cruise=reise)
                return render(request, "cruises/form_template.html", {"form": form, "cruise": reise, "cruiseShares" : cruiseShares, "yearDropdown": yearDropdown, "selectedYear": year}) 
            else:
                # ID ist zwar gegeben, existiert aber nicht
                cruises = cruise.objects.filter(startDate__year=year).order_by('startDate')
                return render(request, "cruises/cruisesOverview.html", context={"cruises": cruises, "yearDropdown": yearDropdown, "selectedYear": year})
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
    pos = ['S', 'W', 'C']
    order = Case(*[When(SailAs=SailAs, then=en) for en, SailAs in enumerate(pos)])
    
    if ('id' in request.GET) and request.GET['id'] != "":
        id = request.GET['id']
        cruiseShare.objects.get(id=id).delete()

    if ('cid' in request.GET) and request.GET['cid'] != "":
        cid = request.GET['cid']
        if ('year' in request.GET):
            year = request.GET['year']
            reise = cruise.objects.get(id=cid)
            cruiseShares = cruiseShare.objects.all().filter(Cruise=reise).order_by(order,'cosailor')
            cruises = cruise.objects.filter(startDate__year=year).order_by('startDate')
            return render(request, "cruises/cruisesOverview.html", context={"cruises": cruises, "reise": reise, "cruiseShares": cruiseShares, "yearDropdown": yearDropdown, "selectedYear": year})
        return redirect('cruisesOverview', id=cid)
    return redirect("cruisesOverview")


def makeCrew(request):
    yearDropdown = []
    for y in range((datetime.datetime.now().year), 2011, -1):
        yearDropdown.append(y)
    pos = ['S', 'W', 'C']
    order = Case(*[When(SailAs=SailAs, then=en) for en, SailAs in enumerate(pos)])

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
            cruiseShares = cruiseShare.objects.all().filter(Cruise=reise).order_by(order,'cosailor')
            cruises = cruise.objects.filter(startDate__year=year).order_by('startDate')
            return render(request, "cruises/cruisesOverview.html", context={"cruises": cruises, "reise": reise, "cruiseShares": cruiseShares, "yearDropdown": yearDropdown, "selectedYear": year})
        return redirect('cruisesOverview', id=cid)
    return redirect("cruisesOverview")

def makeWatch(request):
    yearDropdown = []
    for y in range((datetime.datetime.now().year), 2011, -1):
        yearDropdown.append(y)
    pos = ['S', 'W', 'C']
    order = Case(*[When(SailAs=SailAs, then=en) for en, SailAs in enumerate(pos)])
    
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
            cruiseShares = cruiseShare.objects.all().filter(Cruise=reise).order_by(order,'cosailor')
            cruises = cruise.objects.filter(startDate__year=year).order_by('startDate')
            return render(request, "cruises/cruisesOverview.html", context={"cruises": cruises, "reise": reise, "cruiseShares": cruiseShares, "yearDropdown": yearDropdown, "selectedYear": year})
        return redirect('cruisesOverview', id=cid)
    return redirect("cruisesOverview")

def makeSkipper(request):
    yearDropdown = []
    for y in range((datetime.datetime.now().year), 2011, -1):
        yearDropdown.append(y)
    pos = ['S', 'W', 'C']
    order = Case(*[When(SailAs=SailAs, then=en) for en, SailAs in enumerate(pos)])
   
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
            cruiseShares = cruiseShare.objects.all().filter(Cruise=reise).order_by(order,'cosailor')
            cruises = cruise.objects.filter(startDate__year=year).order_by('startDate')
            return render(request, "cruises/cruisesOverview.html", context={"cruises": cruises, "reise": reise, "cruiseShares": cruiseShares, "yearDropdown": yearDropdown, "selectedYear": year})
        return redirect('cruisesOverview', id=cid)
    return redirect("cruisesOverview")

def setWatch(request):
    if ('id' in request.GET) and request.GET['id'] != "":
        id = request.GET['id']
        sailorId = sailor.objects.get(id=id)
        p1 = patent(Type = 'W')
        p1.save()
        sailorId.ownedPatent = p1
        sailorId.save()
    return redirect("sailorOverview")

def setSkipper(request):
    if ('id' in request.GET) and request.GET['id'] != "":
        id = request.GET['id']
        sailorId = sailor.objects.get(id=id)
        p1 = patent(Type = 'S')
        p1.save()
        sailorId.ownedPatent = p1
        sailorId.save()
    return redirect("sailorOverview")
