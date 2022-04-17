from distutils.log import error
from operator import truediv
from urllib.request import Request
from django.http import Http404, HttpRequest, HttpResponseNotAllowed
from keycloak import KeycloakAdmin,KeycloakOpenID

from utils.keycloak import getKeycloackAdmin, getKeycloakOpenID
import requests
import os

def getUserInfo(token:str):
    url = os.environ["Host"] + "/sso/auth/realms/asv/protocol/openid-connect/userinfo"

    payload = ""
    headers = {"Authorization": "Bearer " + token}

    response = requests.request("GET", url, data=payload, headers=headers, verify=False)
    
    if (response.status_code == 200):
        return response.json(), False
    else:
        return None, True
   
def getUserGroups(userID: str):
    Keycloak = getKeycloackAdmin()
    return Keycloak.get_user_groups(userID)
        
def getToken(request):
    cookies = request.META.get('HTTP_COOKIE')
    cookies = cookies.split(";")
    token: str
    for i in cookies:
        if "token=" in i:
            token = i.replace('token=', '')
    return token

def checkToken(token: str, GroupsWithAccess)-> bool:
    
    try: 
        userinfo, iswrong = getUserInfo(token)
        if iswrong:
            return None
    except:
        return None
    
    groups = getUserGroups(userinfo["sub"])
    
    # Done: Check for correct Group
    for groupName in groups:
        if groupName["name"] in GroupsWithAccess:
            return True
        
    return None
