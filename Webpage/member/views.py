#from django.contrib.auth import authenticate
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from .models import profile
from django.contrib.auth.models import User
from .forms import changePersonalInfo


# Create your views here.

# View um die eigenen einstellungen zu bearbeiten
# Index-View zum Dashborad als Startseite vom "Mein ASV"

def index(request):
    return render(request, "member/Dashboard.html")

# Mitgliederverzeichnis
def member_directory(request):
    if (request.user.is_authenticated):
        context = {'personen': profile.objects.all()}
        return render(request, template_name="member/Mitgliderverzeichnis.html", context=context)
    else:
        return redirect("ASV")

# Anzeige für den Einzelnen Nutzer
def single_user(request):
    if (request.user.is_authenticated):
        User = request.GET.get('id', '')
        context = {'User': profile.objects.get(id=User)}
        return render(request, template_name="member/Nutzer.html", context=context)
    else:
        return redirect("ASV")
    pass


# Bearbeiten
def settings(request):
    if (request.user.is_authenticated):
        Profil = get_object_or_404(profile, user=request.user)

        if request.method == "POST":
            form = changePersonalInfo(request.POST, request.FILES, instance=Profil)
            
            if form.is_valid():

                form.save(commit=False)
                form.instance.user_id = request.user.id
                form.save()

                return redirect("ASV")
        else:
            form = changePersonalInfo(instance=Profil)
        return render(request, "member/Einstellungen.html", {"form": form, "profil": Profil})
    else:
        return redirect("ASV")


# -------------------------------------------------------
# ADMIN BEREICH

# Erstelle das Member Haupt Menüs mit den Buttons für Funktionen und Auswertungen über die Mitglieder
def memberMenu(request):

    return render(request, "member/memberMenu.html")

# Anzeige aller Member
def alleMember(request):
    member = profile.objects.all().order_by('-id')
    paginator = Paginator(member, 50)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "member/alleMember.html", {"page_obj": page_obj})

# Möglicher Export aller Mitglieder
def exportPage(request):
    #TODO
    pass

# Editor zum erstellen des neuen Nutzers
def newMemberEditor(request):
    #TODO
    pass

# Seite für einen möglichen Massenimport von Daten in Form einer CSV Datei.
def massenimport(request):
    #TODO
    pass