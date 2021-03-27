import os
from django.contrib.auth.models import User
from member.models import profile
from keycloak import KeycloakAdmin

'''
Erstelle einen neuen Nutzer und füge ihn den
'''
def newMember(username, vorname, nachname, country, hometown, Email, HandyNummer):
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
        newProfile.phone = HandyNummer
        newProfile.save()
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
