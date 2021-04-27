#from django.contrib.auth import authenticate
import csv
import io

from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404



# Create your views here.

# View um die eigenen einstellungen zu bearbeiten
# Index-View zum Dashborad als Startseite vom "Mein ASV"

def ubersicht(request):
    # Wenn angemeldet

    # wenn nicht

    return render(request, "member/Dashboard.html")

def description(request, name):
    #TODO
    pass

@login_required
def settings_status(request, name):
    # Anpassen vom Status und Nachricht des Bootes
    #TODO
    pass

@login_required
@user_passes_test(isUserPartOfGroup_Editor)
def settings_description(request, name):
    # Anpassen vom Namen, Beschreibungstext, Bootsclasse und co
    #TODO
    pass


'''
- [ ] View mit Übersicht
    - Neue Nachrichten und Status nur zeigen wenn man angemeldet ist
- [ ] Einzelsicht der Boote mit Beschreibungstext

- [ ] View zum bearbeiten...
    - ... vom Status
    - ... vom Beschreibungstext
    - [ ] Jedes Mitglied sollte den Status ändern können
- [ ] Boote ins MenüObject einfügen
    - [ ] Header-Generierung anpassen
'''