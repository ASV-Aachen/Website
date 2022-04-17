


def set_aktiv(id: str, keycloak_admin):
    try:
        keycloak_admin.update_user(user_id=id, 
                                      payload={'enabled': 'True'}) 
    except Exception as e:
        print(id)
        print(e)
        

def sendPasswordToKeycloak(id: str, password: str, keycloak_admin):
    keycloak_admin.set_user_password(user_id=id, password=password, temporary=True)