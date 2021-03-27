import os
from django.contrib.auth.models import User
from member.models import profile
from keycloak import KeycloakAdmin
import random

def userToHash(username):
    ergebnis = ""
    # TODO
    return ergebnis


'''Löschfunktion. Löscht zunächst das Profil, dann Keycloak und dann den eigentlichen User'''
def deleteGivenUser(ID):
    pass


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

        newProfile = profile(user=user, status=1, entry_date=datetime.date.today())
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
    #TODO
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
