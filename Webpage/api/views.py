from cProfile import Profile
from http.client import HTTPS_PORT
from turtle import home
from django.http import HttpResponseForbidden, HttpResponsePermanentRedirect
from django.http.response import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from api.middelware import checkToken, getToken
from utils.member import createSailors
from utils.keycloak_f.utils import sendPasswordToKeycloak, set_aktiv
from utils.mail.createMails import createMail
from utils.mail.password import createPassword
from utils.mail.sendmail import sendMail
from utils.keycloak import getKeycloackAdmin
from utils.keycloak import auto_Update_Groups, auto_Update_Roles, update_all_Users
from member.models import profile
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required, user_passes_test
from utils.loginFunctions import isUserPartOfGroup_Developer
import json
from utils.member import newMember, getGender
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.clickjacking import xframe_options_sameorigin

GroupsWithAccess = [
    "Entwickler",
    "Admin",
]

def checkforToken(request):
    token = getToken(request) 

    if token is None:
        print("No Token")
        return None
    userInfo = checkToken(token, GroupsWithAccess)
    return userInfo

@xframe_options_sameorigin
@csrf_exempt
def sync_everything(request):
    userInfo = checkforToken(request)
    if userInfo is None:
        return HttpResponse(status=401)
        
    # Sync website with Keycloak
    try:
        auto_Update_Roles() 
        # auto_Update_Groups()
        update_all_Users()
        createSailors()
        return HttpResponse(status=200)
    except Exception as e:
        return HttpResponse(e, status=500)

@xframe_options_sameorigin      
@csrf_exempt
def addUser(request):
    userInfo = checkforToken(request)
    if userInfo is None:
        return HttpResponse(status=401)
    
    if request.method != "POST":
        return HttpResponse(status=405)
    
    print(request.POST)
    
    # daten aus request schälen
    try:
        # current_user_eintrittsdatum = jsonData["entryDate"].split(".")[2] + "-" + jsonData["entryDate"].split(".")[1] + "-" + jsonData["entryDate"].split(".")[0]
        current_user_eintrittsdatum = request.POST["entryDate"]
        mail: str                   = request.POST["mail"]
        first_name: str             = request.POST["first_name"]
        last_name: str              = request.POST["last_name"]
        status: str                 = request.POST["status"]
        password: str
        mail: str
        username: str
        id: str
    except Exception as e:
        return HttpResponse(e, status=400)
    # ----------------------------
    
    keycloak_admin = getKeycloackAdmin()
    
    # in Keycloak && Website einfügen
    if current_user_eintrittsdatum == "":
        sucess, username = newMember(
                    vorname=first_name,
                    nachname= last_name,
                    country= "Deutschland",
                    hometown="Aachen",
                    Email=mail,
                    status=getStatus(status)
                )
    else: 
        sucess, username = newMember(
                    vorname=first_name,
                    nachname= last_name,
                    country= "Deutschland",
                    hometown="Aachen",
                    Email=mail,
                    status=getStatus(status),
                    eintrittsdatum=current_user_eintrittsdatum
                )
    if (not sucess):
        return HttpResponse("User konnte nicht angelegt werden", status=500)
    
    # Password erstellen
    password = createPassword()
    
    # Get ID from Keycloak
    id = keycloak_admin.get_user_id(username=username)
    
    # set password
    sendPasswordToKeycloak(id=id, password=password, keycloak_admin=keycloak_admin)
    
    # aktivieren
    set_aktiv(id=id, keycloak_admin=keycloak_admin)
    
    # create Mail
    mailToSend = createMail(password)

    # Mail versenden
    sendMail(TO= mail,mail=mailToSend)
    
    # Add image (if it's there)
    try: 
        file = request.FILES['userImage']
        print(file)
        temp_profile = profile.objects.get(user = User.objects.get(username=username))
        
        temp_profile.profile_image = file
        temp_profile.save()
        
    except:
        pass
    
    return HttpResponse("Update Successfull", status=200)

def addUser_Image(request):
    userInfo = checkforToken(request)
    if userInfo is None:
        return HttpResponse(status=401)
    pass

@user_passes_test(isUserPartOfGroup_Developer)
@login_required
def member(request)-> JsonResponse:
    AllUsers = profile.objects.all()
    erg: list = []
    for i in AllUsers:
        erg.append({
            "vorname": i.user.first_name,
            "nachname": i.user.last_name,
            "status": i.status,
            "mail": i.user.email,
            "username": i.user.username,
            "aktiv": i.user.is_active
        })
    
    return JsonResponse(erg, safe=False)

'''
{
    id: 0
    update: True,
    person: {
        vorname: 
        nachname: 
        eintrittsdatum:
        status:
        e-mail:
    }
    genderUpdate: True,
}
'''

def getStatus(Status: str)-> int:
    if(Status == "Anwärter"): return 1
    if(Status == "Aktives Mitglied"): return 2
    if(Status == "Inaktives Mitglied"): return 3
    if(Status == "Alter Herr"): return 4
    if(Status == "Außerordentliches Mitglied"): return 5
    if(Status == "Ehrenmitglied"): return 6
    return 1

@user_passes_test(isUserPartOfGroup_Developer)
@csrf_exempt
@login_required
def addMember(request):
    if request.method != "POST":
        return HttpResponse("only Post allowed", status=405)
        
    try:
        jsonData = json.loads((request.body))
        if jsonData["update"] == True:
            user = get_object_or_404(User, email=jsonData['person']['e-mail'])
            person_profile = get_object_or_404(profile, user=user)
            
            person_profile.status = getStatus(jsonData["person"]['status'])
            
            if jsonData['genderUpdate']:
                person_profile.gender = getGender(person_profile.user.first_name)

            person_profile.save()
            return HttpResponse("update Successfull", status=200)
            
        else:
            jsonData = jsonData["person"]
            current_user_eintrittsdatum = jsonData["eintrittsdatum"].split(".")[2] + "-" + jsonData["eintrittsdatum"].split(".")[1] + "-" + jsonData["eintrittsdatum"].split(".")[0]
            newMember(
                jsonData["vorname"],
                jsonData["nachname"],
                "Deutschland", 
                "Aachen",
                jsonData["e-mail"],
                eintrittsdatum  = datetime.fromisoformat(current_user_eintrittsdatum),
                status          = getStatus(jsonData["status"]),
            )
            return HttpResponse("added new User", status = 200)
    
    except Exception as e:
        return HttpResponse(e, status=400)
