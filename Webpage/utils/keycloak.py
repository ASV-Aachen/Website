import os

from django.contrib.auth.models import User, Group
from keycloak import KeycloakAdmin, KeycloakOpenID
from cruises.models import sailor

from member.models import role, profile

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def getKeycloackAdmin()-> KeycloakAdmin:
    keycloak_admin = KeycloakAdmin(server_url=os.environ["Host"] + "/sso/auth/",
                                   username=os.environ["KEYCLOAK_USER"],
                                   password=os.environ["KEYCLOAK_PASSWORD"],
                                   verify=False,
                                   realm_name="ASV",
                                   user_realm_name="master",)
    return keycloak_admin

def getKeycloakOpenID()->KeycloakOpenID:
    keycloak_openid = KeycloakOpenID(server_url=os.environ["Host"] + "/sso/auth/",
                    client_id=os.environ["OIDC_RP_CLIENT_ID"],
                    realm_name="ASV",
                    client_secret_key=os.environ["OIDC_RP_CLIENT_SECRET"])
    return keycloak_openid

'''
Get all Roles from Keycloak and add to Django
'''
def auto_Update_Roles():
    admin = getKeycloackAdmin()

    realm_roles = admin.get_realm_roles()

    for i in realm_roles:
        try:
            role.objects.get_or_create(titel=i['name'], description=i['description'])
        except Exception as e:
            role.objects.get_or_create(titel=i['name'])

'''
Get all Groups from Keycloak and add to Django
'''
def auto_Update_Groups():
    admin = getKeycloackAdmin()

    groups = admin.get_groups()
    
    print(groups)

    for i in groups:
        try:
            Group.objects.get_or_create(name=i['name'])
        except:
            # print(i)
            continue

    return


'''
Ziehe dir die Informationen über den Nutzer und Update die Daten in Django
'''
def update_all_Users():
    # Zieh die alle Nutzer
    all_Users = User.objects.all()

    keycloak_admin = getKeycloackAdmin()

    # Für jeden Nutzer:
    for user in all_Users:
        try:
            # Zieh dir die Daten aus Keycloak
            try:
                user_id_keycloak = keycloak_admin.get_user_id(username=user.username)
                keycloak_user = keycloak_admin.get_user(user_id=user_id_keycloak)
            except:
                continue

            # keycloak_user:
            # username      string
            # email         string
            # groups        < string > array
            # firstName     string
            # lastName      string
            # realmRoles    < string > array

            user.firstName = keycloak_user['firstName']
            user.lastName = keycloak_user['lastName']
            user.email = keycloak_user['email']

            # realm Roles
            # print("----------------------------")

            # GET /{realm}/users/{id}/groups
            groups = keycloak_admin.get_user_groups(user_id=user_id_keycloak)
            # print(groups)

            user.groups.clear()
            for i in groups:
                newGroup, created = Group.objects.get_or_create(name=i['name'])
                user.groups.add(newGroup)

            
            # GET /{realm}/users/{id}/roles
            roles = keycloak_admin.get_realm_roles_of_user(user_id=user_id_keycloak)
            # print(roles)

            userProfile = profile.objects.get(user=user)
            userProfile.roles.clear()
            
            for i in roles:
                if i == "default-roles-asv":
                    continue
                newRole, created = role.objects.get_or_create(titel=i['name'])
                userProfile.roles.add(newRole)

            user.is_staff = user.groups.filter(name='Admin').exists()
            user.is_superuser = user.groups.filter(name='Admin').exists()
                    
            userProfile.save()
            user.save()
            
            # print(user.groups.filter(name='Admin').exists())
        
        except:
            print(user.firstName + user.lastName)
            continue
    
    return

