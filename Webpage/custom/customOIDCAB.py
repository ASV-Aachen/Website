
from django.contrib.auth.models import User
from mozilla_django_oidc.auth import OIDCAuthenticationBackend
import logging

#{'sub': '03c991c1-c6cc-4af7-8092-bb6d794e3ec2', 'email_verified': True, 'name': 'christian baltzer', 'preferred_username': 'chris', 'given_name': 'christian', 'family_name': 'baltzer', 'email': 'christian@baltzer.de'}

class MyOIDCAB(OIDCAuthenticationBackend):
    def create_user(self, claims):
        user = super(MyOIDCAB, self).create_user(claims)

        logger = logging.getLogger(__name__)

        logger.error(claims)
        # user.email = claims.get(''. '')

        user.first_name = claims.get('given_name', '')
        user.last_name = claims.get('family_name', '')
        user.username = claims.get('preferred_username', '')

        user.email = claims.get('email', '')

        user.save()

        return user

    def update_user(self, user, claims):
        user.first_name = claims.get('given_name', '')
        user.last_name = claims.get('family_name', '')

        user.email = claims.get('email', '')
        
        user.save()

        return user
    
    def filter_users_by_claims(self, claims):
        sub = claims.get('preferred_username')
        if not sub:
            return self.UserModel.objects.none()

        try:
            profile = User.objects.get(username=sub)
            return profile.user

        except User.DoesNotExist:
            return self.UserModel.objects.none()

    