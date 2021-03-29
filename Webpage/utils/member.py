import hashlib
import os
from django.contrib.auth.models import User
from member.models import profile
from keycloak import KeycloakAdmin
import random

def userToHash(username):
    ergebnis = hashlib.sha512(username).hexdigest()
    return ergebnis


'''Löschfunktion. Löscht zunächst das Profil, dann Keycloak und dann den eigentlichen User'''
def deleteGivenUser(ID) -> bool:
    # Finde den Nutzer
    user = User.objects.get(id = ID)

    # Lösch von Keycloak
    keycloak_admin = KeycloakAdmin(server_url=os.environ["Host"] + "sso/auth/",
                                   username=os.environ["Keycloak_Username"],
                                   password=os.environ["Keycloak_Password"],
                                   realm_name="ASV",
                                   client_secret_key=os.environ["OIDC_RP_CLIENT_SECRET"],
                                   verify=True)

    user_id_keycloak = keycloak_admin.get_user_id(user.username)
    response = keycloak_admin.delete_user(user_id=user_id_keycloak)

    # Lösch das Profil
    Profil = profile.objects.get(user=user)
    Profil.delete()

    # Lösche den Nutzer
    user.delete()
    return


'''
    Erzeugt aus einem gegebenen Namen und Nachnamen einen bisher nicht existenten Usernamen
'''
def createUsername(vorname, nachname) -> str:
    while True:
        ergebnis = vorname[0] + nachname[-1:3] + random.randrange(1,999)
        if User.Objects.filter(username = ergebnis).exists() is False:
            return ergebnis

'''
Erstelle einen neuen Nutzer und füge ihn den
'''
def newMember(vorname, nachname, country, hometown, Email)->bool:
    username = createUsername()
    if createNewUserInKeycloak(username, vorname, nachname, Email):
        user = User()
        user.username = username
        user.last_name = nachname
        user.first_name = vorname
        user.email = Email
        user.save()

        newProfile = profile(user=user, status=1)
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
    try:
        keycloak_admin = KeycloakAdmin(server_url = os.environ["Host"] + "sso/auth/",
                                       username= os.environ["Keycloak_Username"],
                                       password= os.environ["Keycloak_Password"],
                                       realm_name="ASV",
                                       client_secret_key=os.environ["OIDC_RP_CLIENT_SECRET"],
                                       verify=True)

        new_user = keycloak_admin.create_user({"email": Email,
                                               "username": username,
                                               "enabled": True,
                                               "firstName": vorname,
                                               "lastName": nachname})
        return True
    except:
        return False
