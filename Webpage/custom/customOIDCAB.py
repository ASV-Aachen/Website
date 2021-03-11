
from django.contrib.auth.models import User
from mozilla_django_oidc.auth import OIDCAuthenticationBackend
import logging
from member.models import profile, role
import datetime
from django.contrib.auth.models import Group, Permission

def updateRoles(userProfile, claims):
    # Delete old Roles
    userProfile.roles.clear()

    # insert new roles
    for i in claims.get('roles'):
        newRole, created = role.objects.get_or_create(titel=i)
        profile.roles.add(newRole)

    return userProfile

def updateGroup(user, claims):
    # Gruppen laden
    user.groups.clear()
    for i in claims.get('groups'):
        NewGroup, created = Group.objects.get_or_create(name = i)
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
        except:
            pass

        newProfile = profile(user=user, status = 1,entry_date=datetime.date.today())
        newProfile.save()

        try:
            updateRoles(newProfile, claims)
            newProfile.save()
        except:
            logger.log(1, "can't assign role to Profile: " + newProfile)
            pass
        # user.save()

        return user

    def update_user(self, user, claims):
        logger = logging.getLogger(__name__)

        logger.error(claims)

        user.first_name = claims.get('given_name', '')
        user.last_name = claims.get('family_name', '')

        user.email = claims.get('email', '')
        
        try:
            user = updateGroup(user, claims)
            user = updateRoles(user, claims)
        except:
            pass

        userProfile = profile.getObject(profile, user=user)

        try:
            updateRoles(userProfile, claims)
            userProfile.save()
        except:
            logger.log(1, "can't assign role to Profile: " + userProfile)
            pass

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

    