import os
from keycloak import KeycloakAdmin



def getKeycloackAdmin():
    # Lösch von Keycloak
    keycloak_admin = KeycloakAdmin(server_url=os.environ["Host"] + "sso/auth/",
                                   username=os.environ["Keycloak_Username"],
                                   password=os.environ["Keycloak_Password"],
                                   realm_name="ASV",
                                   client_secret_key=os.environ["OIDC_RP_CLIENT_SECRET"],
                                   verify=True)
    return keycloak_admin


'''
Get all Roles from Keycloak and add to Django
'''
def auto_Update_Roles():
    #TODO
    pass

'''
Get all Groups from Keycloak and add to Django
'''
def auto_Update_Groups():
    # TODO
    pass


'''
Ziehe dir die Informationen über den Nutzer und Update die Daten in Django
'''
def update_all_Users():
    # TODO
    pass
