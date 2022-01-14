
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from mozilla_django_oidc.auth import OIDCAuthenticationBackend
import logging
from member.models import profile, role
import datetime
from django.contrib.auth.models import Group, Permission

def updateRoles(userProfile, claims):
    # Delete old Roles
    userProfile.roles.clear()

    # insert new roles
    for i in claims.get('Roles'):
        if i == "default-roles-asv":
            continue

        newRole, created = role.objects.get_or_create(titel=i)
        userProfile.roles.add(newRole)

    return userProfile

def updateGroup(user, claims):
    # Gruppen laden
    user.groups.clear()
    for i in claims.get('group'):
        GroupName = ""
        try:
            Subgroups = i.split("/")
            GroupName = Subgroups[-1]
        except:
            pass

        NewGroup, created = Group.objects.get_or_create(name=GroupName)
        # NewGroup.save()
        user.groups.add(NewGroup)

    return user

class MyOIDCAB(OIDCAuthenticationBackend):
    def create_user(self, claims):
        user = super(MyOIDCAB, self).create_user(claims)

        logger = logging.getLogger(__name__)

        logger.error(claims)

        user.first_name = claims.get('given_name', '')
        user.last_name = claims.get('family_name', '')
        user.username = claims.get('preferred_username', '')

        user.email = claims.get('email', '')
 
        user.save()

        try:
            user = updateGroup(user, claims)
        except Exception as e:
            logger.error("Group Error" + str(e))
            pass

        newProfile = profile(user=user, status = 1,entry_date=datetime.date.today())
        newProfile.save()

        try:
            updateRoles(newProfile, claims)
            newProfile.save()
        except Exception as e:
            logger.error("Role Error: " + str(e))
            pass
        # user.save()

        user.is_staff = user.groups.filter(name='Admin').exists()
        user.is_superuser = user.groups.filter(name='Admin').exists()
        user.save()

        return user

    def update_user(self, user, claims):
        logger = logging.getLogger(__name__)

        # logger.error(claims)

        user.first_name = claims.get('given_name', '')
        user.last_name = claims.get('family_name', '')

        user.email = claims.get('email', '')
        
        try:
            user = updateGroup(user, claims)
        except Exception as e:
            logger.error("Group Error" + str(e))
            pass

        userProfile = profile.objects.get(user=user)

        try:
            updateRoles(userProfile, claims)
            userProfile.save()
        except Exception as e:
            logger.error("Role Error" + str(e))
            pass

        user.is_staff = user.groups.filter(name='Admin').exists()
        user.is_superuser = user.groups.filter(name='Admin').exists()

        user.save()

        return user
    
    def filter_users_by_claims(self, claims):
        sub = claims.get('preferred_username')
        if not sub:
            return self.UserModel.objects.none()
        try:
            profile = User.objects.get(username=sub)
            profileListe = []
            profileListe.append(profile)
            return profileListe

        except User.DoesNotExist:
            return self.UserModel.objects.none()

    