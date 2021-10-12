from functools import _Descriptor
from os import access, name
from typing import List
from Webpage.arbeitsstunden.commands.utils.csv import bcolors
from Webpage.arbeitsstunden.models import account, costCenter, project, season, work
from Webpage.utils.member import newMember
import Webpage.arbeitsstunden.commands.utils.data as interfaces

def getStatus(Status: str)-> int:
    if(Status == "Anwärter"): return 1
    if(Status == "Aktives Mitglied"): return 2
    if(Status == "Inaktives Mitglied"): return 3
    if(Status == "Alter Herr"): return 4
    if(Status == "Außerordentliches Mitglied"): return 5
    if(Status == "Ehrenmitglied"): return 6
    return 1

def Nutzerliste(Liste: List[interfaces.Nutzer]):
    
    for i in Liste:
        try:
            current_user_status = getStatus(i.Status)
            current_user_eintrittsdatum = i.Eintrittsdatum
            newMember(i.Vorname, i.Nachname, "Deutschland", "Aachen", i.E_Mail, eintrittsdatum=current_user_eintrittsdatum, status = current_user_status)
            pass
        except:
            print(bcolors.FAIL + "[FAIL]" + bcolors.ENDC + i.Nachname + " couldn't be imported")
        pass
    
    
    
    pass

def Arbeitsstunden(
        Array_user: List[interfaces.user], 
        Array_project: List[interfaces.project], 
        Array_project_item: List[interfaces.project_item], 
        Array_project_item_hour: List[interfaces.project_item_hour], 
        Array_season: List[interfaces.season], 
        Array_member: List[interfaces.member]
    ):
    
    # season
    for i in Array_season:
        temp, _ = season.objects.get_or_create(
            year = i.year,
            hours = i.obligatory_minutes
        )

    newCostcenter = costCenter(name="import", description="----")
    newCostcenter.save()
    
    for i in Array_project:
        currentCenter, _ = costCenter.objects.get_or_create(
            name = i.name,
            description = i.description,
        )
        
        currentProjects: List[interfaces.project_item] = []
        for x in Array_project_item:
            if x.project_id == i.id: 
                currentProjects.append(x)
                Array_project_item.pop(x)

        for projects_items in currentProjects:
            currentProject, _ = project.objects.get_or_create(
                name = projects_items.title,
                season = projects_items.season,
                description = projects_items.description,
                costCenter = currentCenter,
            )
            
            workingParts: List[interfaces.project_item_hour] = []
            for y in Array_project_item_hour:
                if y.project_item_id == projects_items.id:
                    workingParts.append(y)
                    Array_project_item_hour.pop(y)
            
            for works in workingParts:
                currentWork, _ = work.objects.get_or_create(
                    name = "imported",
                    hours = works.duration,
                    startDate = projects_items.date
                )
                
                # add current work to Project
                currentProject.parts.add(currentWork)
                
                # employye Namen suchen
                employeeIndex = next((index for (index, d) in enumerate(Array_member) if d.id == works.member_id), None)
                
                # Employye account suchen und hinzufügen
                temp, _ = account.objects.get_or_create(
                        name = Array_member[employeeIndex].Vorname + " " + Array_member[employeeIndex].Nachname
                    )
                currentWork.add(temp)
                
    pass

