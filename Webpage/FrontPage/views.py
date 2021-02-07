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

    redirect("ASV")

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
    if request.user.is_authenticated():
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