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
    AllUsers = profile.objects.values_list('user', 'gender_role', 'hometown', 'status')
    erg: list = []
    for i in AllUsers:
        erg.append(model_to_dict(i))
    
    return JsonResponse(erg, safe=False)

@user_passes_test(isUserPartOfGroup_Developer)
@login_required
def user(request)-> JsonResponse:
    AllUsers = User.objects.all()
    erg: list = []
    for i in AllUsers:
        erg.append(model_to_dict(i))
    
    return JsonResponse(erg, safe=False)

@user_passes_test(isUserPartOfGroup_Developer)
@login_required
def groupMember(request, status:int):
    foundUsers = profile.objects.get(status=status).values('user', 'gender_role', 'hometown', 'status')
    
    erg: list = []
    for i in foundUsers:
        erg.append(model_to_dict(i))
    
    return JsonResponse(erg, safe=False)

'''
{
    id: 0
    update: True,
    person: {
        vorname: 
        nachname: 
        
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
                hometown        =jsonData["hometown"],
                Email           =jsonData["Email"],
                eintrittsdatum  =jsonData["eintrittsdatum"],
                status          =jsonData["status"],
            )
            return HttpResponse("added new User", status = 200)
    
    except Exception as e:
        return HttpResponse(e, status=400)
