import os

from django.contrib.auth.models import User, Group
from keycloak import KeycloakAdmin

from member.models import role


def getKeycloackAdmin():
    keycloak_admin = KeycloakAdmin(server_url=os.environ["Host"] + "/sso/auth/",
                                   username=os.environ["KEYCLOAK_USER"],
                                   password=os.environ["KEYCLOAK_PASSWORD"],
                                   verify=False,
                                   realm_name="ASV",
                                   user_realm_name="master",)
    return keycloak_admin


'''
Get all Roles from Keycloak and add to Django
'''
def auto_Update_Roles():
    admin = getKeycloackAdmin()

    realm_roles = admin.get_realm_roles()

    for i in realm_roles:
        role.objects.get_or_create(titel=i.name)

'''
Get all Groups from Keycloak and add to Django
'''
def auto_Update_Groups():
    admin = getKeycloackAdmin()

    groups = admin.get_groups()

    for i in groups:
        Group.objects.get_or_create(name=i.name)

    return


'''
Ziehe dir die Informationen über den Nutzer und Update die Daten in Django
'''
def update_all_Users():
    # Zieh die alle Nutzer
    all_Users = User.Objects.all()

    keycloak_admin = getKeycloackAdmin()

    # Für jeden Nutzer:
    for user in all_Users:
        # Zieh dir die Daten aus Keycloak
        user_id_keycloak = keycloak_admin.get_user_id(username=user.username)
        keycloak_user = keycloak_admin.get_user(user_id=user_id_keycloak)

        # Update data of User
        # DONE: Muss noch konkretisiert werden!!!
        # Welche Daten wollen wir eigentlich ziehen und updaten?
        # Ist der Nutzer noch Admin???

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


        for i in keycloak_user['role']:
            newRole, created = role.objects.get_or_create(titel=i)
            user.roles.add(newRole)

        for i in keycloak_user['groups']:
            NewGroup, created = Group.objects.get_or_create(name=i)
            # NewGroup.save()
            user.groups.add(NewGroup)

        user.is_staff = user.groups.filter(name='Admin').exists()
        user.is_admin = user.groups.filter(name='Admin').exists()

        user.save()

    return

