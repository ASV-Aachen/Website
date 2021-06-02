import hashlib
import os
import datetime

from django.contrib.auth.models import User
from member.models import profile
from keycloak import KeycloakAdmin
import random

import gender_guesser.detector as gender

from utils.keycloak import getKeycloackAdmin


def userToHash(username):
    ergebnis = hashlib.sha512(str(username).encode('utf-8')).hexdigest()
    return ergebnis


'''Löschfunktion. Löscht zunächst das Profil, dann Keycloak und dann den eigentlichen User'''
def deleteGivenUser(ID) -> bool:
    # Finde den Nutzer
    user = User.objects.get(id = ID)

    try:
        # Lösch von Keycloak
        keycloak_admin = getKeycloackAdmin()

        user_id_keycloak = keycloak_admin.get_user_id(user.username)
        response = keycloak_admin.delete_user(user_id=user_id_keycloak)

        # Lösch das Profil
        Profil = profile.objects.get(user=user)
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
        ergebnis = vorname[0] + nachname[-1:3] + str(random.randrange(1,999))
        if User.objects.filter(username = ergebnis).exists() is False:
            return ergebnis

'''
Erstelle einen neuen Nutzer und füge ihn den
'''
def newMember(vorname, nachname, country, hometown, Email)->bool:
    username = createUsername(vorname, nachname)
    if createNewUserInKeycloak(username, vorname, nachname, Email):
        user = User()
        user.username = username
        user.last_name = nachname
        user.first_name = vorname
        user.email = Email
        user.save()

        newProfile = profile(user=user, status=random.randint(1, 6), entry_date=datetime.date.today())
        newProfile.hometown = hometown
        newProfile.country = country
        newProfile.save()
        return True
    else:
        return False
    pass

'''
    Stelle eine verbindung zu Keycloak her und füge den gegebenen Nutzer neu in Keycloak ein
'''
def createNewUserInKeycloak(username, vorname, nachname, Email) -> bool:
    keycloak_admin = getKeycloackAdmin()

    new_user = keycloak_admin.create_user({"email": Email,
                                           "username": username,
                                           "enabled": False,
                                           "firstName": vorname,
                                           "lastName": nachname})

    return True

def getGender(name):
    d = gender.Detector()
    ergebniss = d.get_gender(name)

    if ergebniss == "female":
        return "F"
    if ergebniss == "andy":
        return "X"
    return "M"
    