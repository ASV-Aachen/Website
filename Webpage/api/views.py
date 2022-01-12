from django.http.response import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from member.models import profile
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required, user_passes_test
from utils.loginFunctions import isUserPartOfGroup_Developer
import json
from utils.member import newMember, getGender
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
# Create your views here.

@user_passes_test(isUserPartOfGroup_Developer)
@login_required
def member(request)-> JsonResponse:
    AllUsers = profile.objects.all()
    erg: list = []
    for i in AllUsers:
        erg.append({
            "vorname": i.user.first_name,
            "nachname": i.user.last_name,
            "status": i.status
        })
    
    return JsonResponse(erg, safe=False)

@user_passes_test(isUserPartOfGroup_Developer)
@login_required
def groupMember(request, status:int):
    foundUsers = profile.objects.all().filter(status=status)
    
    erg: list = []
    for i in foundUsers:
        erg.append({
            "vorname": i.user.first_name,
            "nachname": i.user.last_name,
            "status": i.status
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

@user_passes_test(isUserPartOfGroup_Developer)
@login_required
def addMember(request):
    if request.method != "POST":
        return HttpResponse("only Post allowed", status=405)
        
    try:
        jsonData = json.loads((request.body))
        if jsonData["update"] == True:
            person_profile = get_object_or_404(profile, id=jsonData["id"])
            
            person_profile.status = jsonData["person"]['status']
            
            if jsonData['genderUpdate']:
                person_profile.gender = getGender(person_profile.user.first_name)

            person_profile.save()
            return HttpResponse("update Successfull", status=200)
            
        else:
            jsonData = jsonData["person"]
            newMember(
                vorname         =jsonData["vorname"],
                nachname        =jsonData["nachname"],
                Email           =jsonData["e-mail"],
                eintrittsdatum  =jsonData["eintrittsdatum"],
                status          =jsonData["status"],
            )
            return HttpResponse("added new User", status = 200)
    
    except Exception as e:
        return HttpResponse(e, status=400)
