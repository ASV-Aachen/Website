#from django.contrib.auth import authenticate
import csv
import io

from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404

from utils.member import newMember, userToHash, deleteGivenUser
from .models import profile
from django.contrib.auth.models import User
from .forms import changePersonalInfo, createNewMember


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

    if(request.method == "POST"):
        form = createNewMember(request.POST)
        vorname = form.instance.last_name
        nachname = form.instance.first_name
        country = "Germany"
        hometown = "Aachen"
        email = form.instance.email

        if newMember(vorname, nachname, country, hometown, email):
            return redirect("MemberMenu")
        else:
            return render(request, "ErrorPage.html")
    else:
        form = createNewMember()
        # TODO: HTML ANLEGEN
        return render(request, "member/newMemberEditor.html", {"form": form})


# Seite für einen möglichen Massenimport von Daten in Form einer CSV Datei.
def massenimport(request):
    #TODO
    if request.method == "POST":
        # Datei geladen
        file = request.FILES['file']
        if file.name.endsweith(".csv"):
            data_set = file.decode('UTF-8')
            io_string = io.StringIO(data_set)

            for column in csv.reader(io_string, delimiter=',', quotechar = "|"):
                if(column[0] == "vorname"): continue
                newMember(column[0], column[1], column[2], column[3], column[4])

        return redirect("MemberMenu")
    else:
        return render(request, "member/massenImport.html")

'''
    Erstellt eine Seite mit einem hash des Nutzernamen. Wird dieser zurück gesendet wissen wir das es ernst gemeint ist.
'''
def deleteUser(request):
    if request.GET['id'] != "":
        if User.Objects.filter(id=id).exists() is True:
            # Erzeuge hash
            user = User.Objects.filter(id=id)[0]

            if request.GET['key'] != "":
                # Lösche den Nutzer
                givenKey = request.GET['key']
                if givenKey == userToHash(user.username):
                    deleteGivenUser(user.id)
                    return redirect("MemberMenu")
                return render(request, "ErrorPage.html")
            else:
                key = userToHash(user.username)
                # sende Seite
                return render(request, "member/deleteUser.html", {"hash": key, "user": user})
        else:
            return redirect("MemberMenu")
    else:
        return redirect("MemberMenu")