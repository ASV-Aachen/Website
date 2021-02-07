from datetime import date

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.template import Context, Template
from django.template.base import logger
from .models import *
from django.http import HttpResponse
from django.contrib.auth.models import Permission
from django.conf import settings
import urllib.parse
import logging
import os


# Object for Header logged in and not logged in (name and url)
def GetMenu(request):
    if (request.user.is_authenticated):
        Object = [{
            "link":"#",
            "Name":"Mein ASV"
        },{
            "link":"/wiki",
            "Name":"Wiki"
        },{
            "link":"#",
            "Name":"Mitgliedererzeichnis"
        },{
            "link":"#",
            "Name":"Einstellungen"
        },{
            "link":"#",
            "Name":"logout"
        }]
    else:
        Object = [{
            "link":"/login",
            "Name":"Login"
        }]
        pass
    return Object


# Frontpage (DONE)
def MainPage(request):
    """
    Hauptseite, erreichbar mit "/" ist anders, je nachdem op  man angemeldet ist oder nicht.
    :param request:
    :return: Die Website
    """
    # Eingeloggte Mitglieder bekommen eine andere Homepagemit eigenen Links und eigenen Hinweisen (TODO)
    if (request.user.is_authenticated):    
        CurrentUser = request.user
        Name = CurrentUser.first_name
        return render(request, "home.html", context={
                "News": BlogEintrag.objects.all().order_by('-id')[:5],
                "UserName": Name,
                "UserLinks": GetMenu(request)
            })
    else:    
        CurrentUser = request.user
        return render(request, "home.html", context={
                "News": BlogEintrag.objects.all().order_by('-id')[:5],
                "UserLinks": GetMenu(request)
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
        # TODO: redirect to sso/auth/realms/ASV/account/#/
        logout(request)
        
        Host = os.environ["Host"]

        TestUrl = "sso/auth/realms/ASV/protocol/openid-connect/logout?redirect_uri=" + Host

        return redirect(TestUrl)
    return redirect("ASV")

# Alle News (TODO)
def News(request):
    try:
        Seite = request.GET.get('Seite', '')
        maxSeiten = request.GET['MaxSeiten']
        obersteNews = ((Seite-1)*5)
        context = {
            "AktuelleID": Seite,
            "maxSeiten": maxSeiten,
            "News": BlogEintrag.objects.all().order_by('-id')[obersteNews:obersteNews+5],
            "UserLinks": GetMenu(request)
        }
    except:
        Seite = 1
        obersteNews = 0
        idAnzahl = len(BlogEintrag.objects.all())
        MaxSeiten = idAnzahl / 5

        context = {
            "AktuelleID": Seite,
            "maxSeiten": MaxSeiten,
            "News": BlogEintrag.objects.all().order_by('-id')[obersteNews:obersteNews+5],
            "UserLinks": GetMenu(request)
        }

    return render(request, template_name="News.html", context=context)

    pass


# Einzelne News Page (DONE)
def EinzelNews(request):
    """
    Je nach ID gibt das System eine spezielle News zurück.
    Alle News müssen Offen sein
    :param request:
    :return:
    """
    try:
        id = request.GET.get('id', '')
        return render(request, template_name="newsPage.html", context={'News': BlogEintrag.objects.get(id=id), "UserLinks": GetMenu(request)})
    except:
        return redirect("ASV")

def NeueNews(request):
    if request.user.is_authenticated:
        if request.POST:
            # Neue Nachricht eingefügt
            User = request.user
            Titel = request.POST['Titel']
            Text = request.POST['Text']
            Datum = date.today()

            NewText = BlogEintrag(Titel=Titel, Text=Text, Autor=User, Datum=Datum)
            NewText.save()
            pass
        if request.GET:
            # Editor
            return render(request, template_name="NewNews.html")
            pass
    else:
        return redirect('ASV')

# Kleine Debug Test Seite: Zeigt an ob eine Person angemeldet ist und wenn ja, welche Permissions und Gruppen der Nutzer hat.
# Wird nur im Debug Modus gezeigt.
def UserTest(request):
    if (settings.DEBUG):            
        Text = ""
        if request.user.is_authenticated:
            Text = "<h1>Angemeldet!</h1> \n"
            user = request.user
            Text += (user.get_username())
            Text += ("<br>")
            Text += user.email
            Text += ("<br>")

            perm_tuple = [(x.id, x.name) for x in Permission.objects.filter(user=user)]
            l_as_list = list(user.groups.values_list('name',flat = True))

            Text += ("Groups: " +  ' - '.join(str(e) for e in l_as_list))
            Text += ("<br>Permissions: " + ' - '.join(str(e) for e in perm_tuple))

            Text += ("<br>")

            roles = user

            
            pass
        else:
            Text = "<h1>Nicht angemeldet!</h1> \n"
        return HttpResponse(Text)
    else:
        return redirect('ASV')