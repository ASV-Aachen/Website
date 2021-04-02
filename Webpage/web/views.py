from datetime import date

from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.template import Context, Template
from django.template.base import logger
#from .models import *
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
        # TODO: redirect to sso/auth/realms/ASV/account/#/
        logout(request)
        
        Host = os.environ["Host"]

        TestUrl = "sso/auth/realms/ASV/protocol/openid-connect/logout?redirect_uri=" + Host

        return redirect(TestUrl)
    return redirect("ASV")


# Kleine Debug Test Seite: Zeigt an ob eine Person angemeldet ist und wenn ja, welche Permissions und Gruppen der Nutzer hat.
# Wird nur im Debug Modus gezeigt.
def UserTest(request):       
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

def autoPopulate(request):
    if request.method == "POST":
        anzahl = 50
        news = fakeNews(anzahl)

        Editoren = profile.objects.all()

        for i in news:
            aktuellerUser = random.choice(Editoren)
            new = blogPost(text = i['Text'], titel = i['Titel'], author = aktuellerUser.id, last_editor = "FAKENEWSTEST")
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