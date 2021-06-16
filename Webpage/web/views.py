from datetime import date

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.template import Context, Template
from django.template.base import logger
#from .models import *
from django.urls import resolve

from blog.models import blogPost
from django.http import HttpResponse
from django.contrib.auth.models import Permission
from django.conf import settings
import urllib.parse
import logging
import os
from utils.faker import *
from blog.models import blogPost
from member.models import profile
from utils.loginFunctions import *
from utils.member import newMember
import random


# Frontpage (DONE)
from utils.menu import createMenuObject
from web.forms import changeInfoPage, changeHeaderPage, changeLeftRight
from web.models import infoPage, infoPageHistory, HeadPage, frontHeader, standartPages, sponsoren


def MainPage(request):
    """
    Hauptseite, erreichbar mit "/" ist anders, je nachdem op man angemeldet ist oder nicht.
    :param request:
    :return: Die Website
    """
    posts = blogPost.objects.all().order_by('-id')
    paginator = Paginator(posts, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    sponsor = getSponsor()

    if (request.user.is_authenticated):    
        CurrentUser = request.user
        Name = CurrentUser.first_name
        return render(request, "web/home.html", context={
                "News": page_obj,
                "UserName": Name,
                "sponsor": sponsor,
            })
    else:    
        return render(request, "web/home.html", context={
                "News": page_obj,
                "sponsor": sponsor,
            })

# loginFunktion (DONE)
def loginFunction(request):
    """
    /login
    Login Funktion.
    POST    : Versucht die Anmeldung. Ist man angemeldet, so wird man zur Hauptseite weitergeleitet. Ist man nicht angemeldet, zur Login Page.
    GET     : Login Page
    :param request:
    :return:
    """
    if(request.user.is_authenticated):
        redirect("ASV")
    return redirect("oidc_authentication_init")

def logoutFunktion(request):
    if request.user.is_authenticated:
        logout(request)
        
        Host = os.environ["Host"]

        TestUrl = "sso/auth/realms/ASV/protocol/openid-connect/logout?redirect_uri=" + Host

        return redirect(TestUrl)
    return redirect("ASV")

@login_required
@user_passes_test(isUserPartOfGroup_Developer)
def autoPopulate(request):
    if request.method == "POST":
        anzahl = 50
        news = fakeNews(anzahl)

        Editoren = profile.objects.all()

        for i in news:
            aktuellerUser = random.choice(Editoren).user
            new = blogPost(text = i['Text'], titel = i['Titel'], author = aktuellerUser, last_editor = "FAKENEWSTEST")
            new.save()
        
        anzahl = 50
        fakeUsers = fakeNutzer(anzahl)
        for i in fakeUsers:
            newMember(
                i['vorname'],
                i['nachname'],
                i['country'],
                i['hometown'],
                i['Email']
            )

        return redirect("ASV")
    else:
        return render(request, "web/autoPopulate.html", {})

def unfertig(request):
    return render(request, "unfertig.html", {})

def errorPage(request):
    return render(request, "bulley/errorPage.html", {})

'''
Eine einfache Übersicht über alle Infopages
'''
def InfoPageView(request):
    Themen = infoPage.themen

    allePages = infoPage.objects.all()

    Objects = []
    for kennung, titel in Themen:
        pages = infoPage.objects.filter(status = kennung)

        zielObject = {
            "titel": titel,
            "seiten": pages,
            "kennung": kennung
        }

        Objects.append(zielObject)

    return render(request, "web/infoPage.html", {"objects": Objects})

'''
Aufrufen einer einzelnen Seite
'''
def infoPage_singlePage(request, theme, name):
    HeadObject = get_object_or_404(HeadPage, name=theme)
    pageObject = get_object_or_404(infoPage, headPage=HeadObject, name=name)

    return render(request, "web/infoPage_singlePage.html", {"seite": pageObject})

'''
Aufrufen einer einzelnen Seite
'''
def infoPage_singleHeader(request, theme):
    pageObject = get_object_or_404(HeadPage, name=theme)

    return render(request, "web/infoPage_singlePage.html", {"seite": pageObject})

'''
Aufzählung aller Seiten mit der Möglichkeit zu editieren
'''
@user_passes_test(isUserPartOfGroup_Editor)
@login_required
def infoPageMenu(request):
    Objects = createMenuObject()

    if request.method == "POST":
        # Eintragen in die DB
        form = changeLeftRight(request.POST, request.FILES)

        if form.is_valid():
            # abspeichern
            form.save(commit=False)

            form.instance.id = request.GET['1']

            form.save()

    form = changeLeftRight(instance=frontHeader.objects.all()[0])

    return render(request, "web/infoPageMenu.html", {"objects": Objects, "form": form})

'''
Editor für die Infoseiten
'''
@user_passes_test(isUserPartOfGroup_Editor)
@login_required
def infoPageEditor(request):
    if request.method == "POST":
        # Eintragen in die DB
        form = changeInfoPage(request.POST, request.FILES)

        if form.is_valid() and ('id' in request.GET):
            # abspeichern
            form.save(commit=False)
            bestehenderEintrag = get_object_or_404(infoPage, id=request.GET['id'])

            newhistory = infoPageHistory(
                titel=bestehenderEintrag.titel,
                text=bestehenderEintrag.text,
                description='',
                name=bestehenderEintrag.name,
                user_Editor=request.user.first_name + " " + request.user.last_name,
                datum = date.today()
            )
            newhistory.save()

            form.instance.id = request.GET['id']

            bestehenderEintrag.history.add(newhistory)
            form.save()
        else:
            logger = logging.getLogger(__name__)
            logger.error(form.errors)
        return redirect("infoMenu")
    else:
        # Formular laden
        if ('id' in request.GET):
            id = request.GET['id']
            # ID gegeben, also Daten laden

            page = get_object_or_404(infoPage, id=id)
            form = changeInfoPage(instance=page)

            if ('version' in request.GET) and page.history.filter(id=request.GET['version']).exists():
                # Wir suchen nach einer bestimten Version
                OldPost = page.history.get(id=request.GET['version'])
                page.titel = OldPost.titel
                page.text = OldPost.text

            hist = page.history.all().order_by('-id')

            return render(request, "web/infoPageEditor.html", {"form":form, "post": page, "hist": hist})

    return redirect("infoMenu")

'''
Editor für die Header Seiten
'''
@user_passes_test(isUserPartOfGroup_Editor)
@login_required
def infoPageEditor_Header(request):
    if request.method == "POST":
        # Eintragen in die DB
        form = changeHeaderPage(request.POST, request.FILES)

        if form.is_valid() and ('id' in request.GET):
            # abspeichern
            form.save(commit=False)
            bestehenderEintrag = get_object_or_404(HeadPage, id=request.GET['id'])

            newhistory = infoPageHistory(
                titel=bestehenderEintrag.titel,
                text=bestehenderEintrag.text,
                description=bestehenderEintrag.description,
                name=bestehenderEintrag.name,
                user_Editor=request.user.first_name + " " + request.user.last_name,
                datum = date.today()
            )
            newhistory.save()

            form.instance.id = request.GET['id']

            bestehenderEintrag.history.add(newhistory)
            form.save()
        else:
            logger = logging.getLogger(__name__)
            logger.error(form.errors)
        return redirect("infoMenu")
    else:
        # Formular laden
        if ('id' in request.GET):
            id = request.GET['id']
            # ID gegeben, also Daten laden

            page = get_object_or_404(HeadPage, id=id)
            form = changeHeaderPage(instance=page)

            if ('version' in request.GET) and page.history.filter(id=request.GET['version']).exists():
                # Wir suchen nach einer bestimten Version
                OldPost = page.history.get(id=request.GET['version'])
                page.titel = OldPost.titel
                page.text = OldPost.text

            hist = page.history.all().order_by('-id')

            return render(request, "web/infoPageEditor.html", {"form":form, "post": page, "hist": hist})

    return redirect("infoMenu")

# Impressum
def impressum(request):
    Seite = get_object_or_404(standartPages, titel = "Impressum")
    return render(request, "web/standart.html", {"seite": Seite})

# Datenschutz
def datenschutz(request):
    Seite = get_object_or_404(standartPages, titel = "Datenschutz")
    return render(request, "web/standart.html", {"seite": Seite})


def getSponsor():
    items = sponsoren.objects.all()

    # Laden der Startseite auch ohne hinterlegte Sponsoren (init-Zustand)
    if items.exists():
        return random.choice(items)
    else:
        return None

def show_all_Sponsor(request):
    sponsoren_All = sponsoren.objects.all()
    return render(request, "web/show_all_Sponsor.html", {"sponsoren": sponsoren_All})