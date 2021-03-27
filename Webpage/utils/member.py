from keycloak import KeycloakAdmin

'''
Erstelle einen neuen Nutzer und füge ihn den
'''
def newMember(username, vorname, nachname, country, hometown, Email, HandyNummer):
    # TODO
    pass

'''
    Stelle eine verbindung zu Keycloak her und füge den gegebenen Nutzer neu in Keycloak ein
'''
def createNewUserInKeycloak(username, vorname, nachname, Email) -> bool:
    #TODO
    keycloak_admin = KeycloakAdmin(server_url="http://localhost:8080/auth/",
                                   username='example-admin',
                                   password='secret',
                                   realm_name="ASV",
                                   user_realm_name="only_if_other_realm_than_master",
                                   client_secret_key="client-secret",
                                   verify=True)

    new_user = keycloak_admin.create_user({"email": Email,
                                           "username": username,
                                           "enabled": True,
                                           "firstName": vorname,
                                           "lastName": nachname})
    pass
