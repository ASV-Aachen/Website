from http.client import HTTPS_PORT
import struct
from turtle import home
from urllib import request
from warnings import catch_warnings
from django.http import HttpResponsePermanentRedirect
from django.http.response import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from utils.member import createSailors
from api.middelware import basicAuthMiddelware
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
from django.utils.decorators import decorator_from_middleware

@decorator_from_middleware(basicAuthMiddelware)
def sync_everything(request):
    # Sync website with Keycloak
    try:
        auto_Update_Roles() 
        auto_Update_Groups()
        update_all_Users()
        createSailors()
        return HttpResponse(status=200)
    except Exception as e:
        return HttpResponse(e, status=500)
        

@decorator_from_middleware(basicAuthMiddelware)
def addUser(request):
    
    if request.method != "POST":
        return HttpResponse(status=405)
    
    # daten aus request schälen
    try:
        jsonData = json.loads((request.body))
        current_user_eintrittsdatum = jsonData["entryDate"].split(".")[2] + "-" + jsonData["entryDate"].split(".")[1] + "-" + jsonData["entryDate"].split(".")[0]
        mail: str                   = jsonData["mail"]
        first_name: str             = jsonData["first_name"]
        last_name: str              = jsonData["last_name"]
        status: str                 = jsonData["status"]
        password: str
        mail: str
        username: str
        id: str
    except:
        return HttpResponse("Missing Values", status=400)
    # ----------------------------
    
    keycloak_admin = getKeycloackAdmin()
    
    # in Keycloak && Website einfügen
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
    mail = createMail(password)

    # Mail versenden
    sendMail(mail=mail)
    
    # Add image (if it's there)
    # TODO:
    
    return HttpResponse("Update Successfull", status=200)


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
