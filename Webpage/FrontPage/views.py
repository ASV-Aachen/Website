from datetime import date

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.template import Context, Template
from .models import *

# Object for Header logged in and not logged in (name and url)
def GetMenu(request):
    if (request.user.is_authenticated):
        Object = [{
            "link":"#",
            "Name":"Mein ASV"
        },{
            "link":"/arbeitsstunden",
            "Name":"Arbeitsstundenausschreibung"
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
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("ASV")
        else:
            return redirect("login")
    if request.method =="GET":
        return render(request, template_name="login.html")

def logoutFunktion(request):
    if request.user.is_authenticated:
        logout(request)
