from urllib.request import Request
from django.http import Http404, HttpRequest, HttpResponseNotAllowed
from keycloak import KeycloakAdmin,KeycloakOpenID

from utils.keycloak import getKeycloackAdmin, getKeycloakOpenID

def basicAuthMiddelware(get_response):
    # One-time configuration and initialization.
    admin: KeycloakAdmin    = getKeycloackAdmin()
    openId: KeycloakOpenID  = getKeycloakOpenID()

    def middleware(request: Request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = get_response(request)
        token = request.META.get('HTTP_AUTHORIZATION')
        
        try: 
            userinfo = openId.userinfo(token)
        except:
            return HttpResponseNotAllowed
        print(userinfo)
        
        # TODO: Check for correct Group

        # TODO:
        # Code to be executed for each request/response after
        # the view is called.
        
        

        return response

    return middleware
