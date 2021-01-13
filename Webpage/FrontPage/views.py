from datetime import date

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .models import *

# Frontpage (DONE)
def MainPage(request):
    """
    Hauptseite, erreichbar mit "/" ist anders, je nachdem op  man angemeldet ist oder nicht.
    :param request:
    :return: Die Website
    """
    # Eingeloggte Mitglieder bekommen eine andere Homepagemit eigenen Links und eigenen Hinweisen (TODO)
    if request.user.is_authenticated:
        CurrentUser = request.user
        Name = CurrentUser.first_name
        return render(request, "Home_LoggedIn.html", context={
                "News": BlogEintrag.objects.all().order_by('-id')[:5],
                "UserName": Name
            })
    return render(request, template_name="Home_NotLoggedIn.html", context={"News": BlogEintrag.objects.all().order_by('-id')[:5]})


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
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            return redirect("/login")
    if request.method =="GET":
        return render(request, template_name="login.html")


# Alle News (TODO)



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
        return render(request, template_name="newsPage.html", context={'News': BlogEintrag.objects.get(id=id)})
    except:
        return redirect("ASV")

def NeueNews(request):
    if request.user.is_authenticated():
        if request.POST:
            # Neue Nachricht eingefügt
            User = request.user
            Titel = request.POST.get('Titel', '')
            Text = request.POST.get('Text', '')
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