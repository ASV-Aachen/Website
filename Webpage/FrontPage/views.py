from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .models import Blogeintrag

# Frontpage (DONE)
def MainPage(request):
    """
    Hauptseite, erreichbar mit "/" ist anders, je nachdem op  man angemeldet ist oder nicht.
    :param request:
    :return: Die Website
    """
    # Eingeloggte Mitglieder bekommen eine andere Homepagemit eigenen Links und eigenen Hinweisen
    if(request.user.is_authenticated):
        return render(request, "Home_LoggedIn.html")
    return render(request, template_name="Home_NotLoggedIn.html", context={"News": Blogeintrag.objects.all().order_by('-id')[:5]})


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
    if (request.method == "POST"):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            return redirect("/login")
    if (request.method =="GET"):
        return render(request, template_name="login.html")


# Alle News (TODO)



# Einzelne News Page (DONE)
def EinzelNews(request):
    try:
        id = request.GET.get('id', '')
        return render(request, template_name="newsPage.html", context={'News': Blogeintrag.objects.get(id=id)})
    except:
        return redirect("/")

