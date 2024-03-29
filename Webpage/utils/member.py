import hashlib
import os
import datetime

from django.contrib.auth.models import User
from cruises.models import sailor
from member.models import profile
# from arbeitsstunden.models import account
import member.models as memberModel
from keycloak import KeycloakAdmin
import random
from django import template
import gender_guesser.detector as gender

import utils.keycloak as keycloak


def userToHash(username):
    ergebnis = hashlib.sha512(str(username).encode('utf-8')).hexdigest()
    return ergebnis


'''Löschfunktion. Löscht zunächst das Profil, dann Keycloak und dann den eigentlichen User'''
def deleteGivenUser(ID) -> bool:
    # Finde den Nutzer
    user = User.objects.get(id = ID)

    try:
        # Lösch von Keycloak
        keycloak_admin = keycloak.getKeycloackAdmin()

        user_id_keycloak = keycloak_admin.get_user_id(user.username)
        response = keycloak_admin.delete_user(user_id=user_id_keycloak)

        # Lösch das Profil
        Profil = memberModel.profile.objects.get(user=user)
        Profil.delete()

        # Lösche den Nutzer
        user.delete()
        return True
    except:
        return False


'''
    Erzeugt aus einem gegebenen Namen und Nachnamen einen bisher nicht existenten Usernamen
'''
def createUsername(vorname, nachname) -> str:
    while True:
        ergebnis = vorname + nachname + str(random.randrange(1,999))
        if User.objects.filter(username = ergebnis).exists() is False:
            ergebnis = ergebnis.replace(" ", "")
            return ergebnis

'''
Erstelle einen neuen Nutzer und füge ihn den
'''
def newMember(vorname, nachname, country, hometown, Email, eintrittsdatum=datetime.date.today(), status=1)->bool:
    username = createUsername(vorname, nachname)
    if createNewUserInKeycloak(username, vorname, nachname, Email):
        user = User()
        user.username = username
        user.last_name = nachname
        user.first_name = vorname
        user.email = Email
        user.save()
        
        # temp, _ = account.objects.get_or_create(name=user.first_name + " " + user.last_name)
        # user.workingHoursAccount = temp

        newProfile = memberModel.profile(user=user, status=status, entry_date=datetime.date.today())
        newProfile.hometown = hometown
        newProfile.country = country
        newProfile.entry_date = eintrittsdatum
        newProfile.save()
        return True, username
    else:
        return False
    pass

'''
    Stelle eine verbindung zu Keycloak her und füge den gegebenen Nutzer neu in Keycloak ein
'''
def createNewUserInKeycloak(username, vorname, nachname, Email) -> bool:
    keycloak_admin = keycloak.getKeycloackAdmin()

    new_user = keycloak_admin.create_user({"email": Email,
                                           "username": username,
                                           "enabled": False,
                                           "firstName": vorname,
                                           "lastName": nachname})

    return True

def getGender(name):
    d = gender.Detector(case_sensitive=False)
    ergebniss = d.get_gender(name)

    if ergebniss == "female":
        return "F"
    if ergebniss == "andy" or ergebniss == "unknown":
        return "X"
    return "M"
    

register = template.Library()

@register.simple_tag
def genderTitel(titel, gender) -> str:
    dict = {
        "1. Vorsitzender": "1. Vorsitzende",
        "2. Kassenwart bzw. Kassenwart der Altherrenschaft": "2. Kassenwartin bzw. Kassenwartin der Altherrenschaft",
        "2. Vorsitzender bzw. Vorsitzender der Altherrenschschaft": "2. Vorsitzende bzw. Vorsitzende der Altherrenschschaft",
        "Admin": "Admin",
        "Ausbildungswart": "Ausbildungswartin",
        "Bauchladenobmann": "Bauchladenobfrau",
        "Bierwart": "Bierwartin",
        "Entwickler": "Entwicklerin",
        "Etagenobmann": "Etagenobfrau",
        "Hallenobmann": "Hallenobfrau",
        "Homepageobmann": "Homepageobfrau",
        "Kassenwart": "Kassenwartin",
        "Pressesprecher": "Pressesprecherin",
        "Regattawart": "Regattawartin",
        "Rurseeobmann": "Rurseeobfrau",
        "Schifferratsvorsitzender": "Schifferratsvorsitzende",
        "Schriftwart": "Schriftwartin",
        "Seekartenobmann": "Seekartenobfrau",
        "Seereisenkoordinator": "Seereisenkoordinatorin",
        "Seeschiffobmann": "Seeschiffobfrau",
        "Stegobmann": "Stegobfrau",
        "Stellvertretender Vorstand": "",
        "Takelmeister": "Takelmeisterin",
        "Verbandsobmann": "Verbandsobfrau"
    }


    value = str(titel)

    if (gender == "F"):
        try:
            return dict[value]
        except:
            return titel
    return titel


def createSailors():
        
    for user in profile.objects.all():
        if user.sailorID is None:
            temp, _ = sailor.objects.get_or_create(name=user.user.first_name + " " + user.user.last_name, givenName=user.user.first_name, sirName=user.user.last_name)
            user.sailorID = temp
            user.save()