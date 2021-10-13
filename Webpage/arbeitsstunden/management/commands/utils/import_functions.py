
from datetime import datetime
from typing import List
from arbeitsstunden.models import account, costCenter, project, season, work
from utils.member import newMember
import arbeitsstunden.management.commands.utils.data as interfaces

def getStatus(Status: str)-> int:
    if(Status == "Anwärter"): return 1
    if(Status == "Aktives Mitglied"): return 2
    if(Status == "Inaktives Mitglied"): return 3
    if(Status == "Alter Herr"): return 4
    if(Status == "Außerordentliches Mitglied"): return 5
    if(Status == "Ehrenmitglied"): return 6
    return 1

def Nutzerliste(Liste: List[interfaces.Nutzer]):
    
    import requests
    requests.packages.urllib3.disable_warnings() 

    
    from arbeitsstunden.management.commands.utils.csv import bcolors
    import sys
    for i in Liste:
        print("Loading -> " + i.Vorname + " " + i.Nachname)
        try:
            current_user_status = getStatus(i.Status)
            current_user_eintrittsdatum = i.Eintrittsdatum.split(".")[2] + "-" + i.Eintrittsdatum.split(".")[1] + "-" + i.Eintrittsdatum.split(".")[0]
            
            newMember(i.Vorname, i.Nachname, "Deutschland", "Aachen", i.E_Mail, eintrittsdatum=datetime.fromisoformat(current_user_eintrittsdatum), status = current_user_status)
            
            sys.stdout.write("\033[F") # Cursor up one line
        except Exception as inst:
            print(bcolors.FAIL + "[FAIL]" + bcolors.ENDC + i.Nachname + " couldn't be imported: " + str(inst))
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
        try:
            temp, _ = season.objects.get_or_create(
                year = i.year,
                hours = i.obligatory_minutes/60
            )
        except:
            temp = season.objects.get(year = i.year)
            temp.hours = i.obligatory_minutes
            temp.save()

    newCostcenter = costCenter(name="import", description="----")
    newCostcenter.save()
    
    import sys 
    
    for i in Array_project:
        print("Loading -> " + i.name)
        sys.stdout.write("\033[F") # Cursor up one line
        currentCenter, _ = costCenter.objects.get_or_create(
            name = i.name,
            description = i.description,
        )
        
        currentProjects: List[interfaces.project_item] = []
        for x in Array_project_item:
            if x.project_id == i.id: 
                currentProjects.append(x)
                Array_project_item.remove(x)

        for projects_items in currentProjects:
            currentProject, _ = project.objects.get_or_create(
                name = projects_items.title,
                season = season.objects.get_or_create(year = int(projects_items.season))[0],
                description = projects_items.description,
                costCenter = currentCenter,
            )
            
            workingParts: List[interfaces.project_item_hour] = []
            for y in Array_project_item_hour:
                if y.project_item_id == projects_items.id:
                    workingParts.append(y)
                    Array_project_item_hour.remove(y)
            
            for works in workingParts:
                currentWork, _ = work.objects.get_or_create(
                    name = works.id,
                    hours = works.duration,
                    startDate = projects_items.date
                )
                
                # add current work to Project
                currentProject.parts.add(currentWork)
                
                # employye Namen suchen
                employeeIndex = next((index for (index, d) in enumerate(Array_member) if d.id == works.member_id), None)
                
                # Employye account suchen und hinzufügen
                if(employeeIndex is not None):
                    temp, _ = account.objects.get_or_create(
                            name = Array_member[employeeIndex].first_name + " " + Array_member[employeeIndex].last_name
                        )
                    currentWork.employee.add(temp)
                
    pass

