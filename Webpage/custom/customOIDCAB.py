
from django.contrib.auth.models import User
from mozilla_django_oidc.auth import OIDCAuthenticationBackend
import logging
from member.models import profile, position_in_the_club
import datetime
from django.contrib.auth.models import Group, Permission

#{'sub': '03c991c1-c6cc-4af7-8092-bb6d794e3ec2', 'email_verified': True, 'name': 'christian baltzer', 'preferred_username': 'chris', 'given_name': 'christian', 'family_name': 'baltzer', 'email': 'christian@baltzer.de'}

def updateGroupandRole(user, claims):
    # Gruppen laden
    user.groups.clear()
    for i in claims.get('groups'):
        NewGroup, created = Group.objects.get_or_create(name = i)
        # NewGroup.save()
        user.groups.add(NewGroup)
        pass

    return user
    pass

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
            user = updateGroupandRole(user, claims)
        except:
            pass
        

        profile = profile(user=user, status = 1,entrydate=datetime.date(1997, 10, 19))
        profile.save()

        # user.save()

        return user

    def update_user(self, user, claims):
        user.first_name = claims.get('given_name', '')
        user.last_name = claims.get('family_name', '')

        user.email = claims.get('email', '')
        
        try:
            user = updateGroupandRole(user, claims)
        except:
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

    