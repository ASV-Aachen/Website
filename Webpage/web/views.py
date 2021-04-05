from datetime import date

from django.contrib.auth import authenticate, login, logout
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
from utils.member import newMember
import random


# Frontpage (DONE)
from utils.menu import createMenuObject
from web.forms import changeInfoPage
from web.models import InfoPage


def MainPage(request):
    """
    Hauptseite, erreichbar mit "/" ist anders, je nachdem op  man angemeldet ist oder nicht.
    :param request:
    :return: Die Website
    """
    # Eingeloggte Mitglieder bekommen eine andere Homepagemit eigenen Links und eigenen Hinweisen (TODO)
    posts = blogPost.objects.all().order_by('-id')
    paginator = Paginator(posts, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if (request.user.is_authenticated):    
        CurrentUser = request.user
        Name = CurrentUser.first_name
        return render(request, "web/home.html", context={
                "News": page_obj,
                "UserName": Name,
            })
    else:    

        return render(request, "web/home.html", context={
                "News": page_obj,
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


'''
Eine einfache Übersicht über alle Infopages
'''
def infoPage(request):
    Themen = InfoPage.themen

    allePages = InfoPage.objects.all()

    Objects = []
    for kennung, titel in Themen:
        pages = InfoPage.objects.filter(status = kennung)

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
    current_url = resolve(request.path_info).url_name

    pageObject = get_object_or_404(InfoPage, status=theme, name=name)

    return render(request, "web/infoPage_singlePage.html", {"seite": pageObject})

'''
Aufzählung aller Seiten mit der Möglichkeit zu editieren
'''
def infoPageMenu(request):
    Objects = createMenuObject()

    return render(request, "web/infoPageMenu.html", {"objects": Objects})

'''
Editor für die Infoseiten
'''
def infoPageEditor(request):
    if request.method == "POST":
        # Eintragen in die DB
        form = changeInfoPage(request.POST)

        if form.is_valid():
            # abspeichern
            form.save()

        return redirect("infoMenu")
    else:
        # Formular laden
        if ('id' in request.GET):
            id = request.GET['id']
            # ID gegeben, also Daten laden

            page = get_object_or_404(InfoPage, id=id)
            form = changeInfoPage(instance=page)

            return render(request, "web/infoPageEditor.html", {"form":form})

    return redirect("infoMenu")
    pass

