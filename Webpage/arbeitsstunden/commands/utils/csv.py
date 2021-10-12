from pathlib import Path
from typing import Match

from Webpage.arbeitsstunden.commands.utils.data import member, project, project_item, project_item_hour, season, user
from Webpage.arbeitsstunden.commands.utils.import_functions import Arbeitsstunden, Nutzerliste


path = "../import/"
files = [
    "member",
    "project_item_hour",
    "project_item",
    "project",
    "reduction",
    "season",
    "user"
]

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def checkForImport():

    # check which files are there
    newFiles = files.copy()
    for i in files:
        current_path = path + "Arbeitsstunden/" + i + ".csv"
        my_file = Path(current_path)
        if my_file.is_file() is False:
            # file doesn't exists        
            newFiles.remove(i)
            print(bcolors.FAIL + "[FAIL] " + bcolors.ENDC + i + " doesn't exist")
        else:
            print(bcolors.OKGREEN + "[SUCCESS] " + bcolors.ENDC + i + " is found")
    
    my_file = Path(path + "Nutzer/" + "NutzerListe.csv")
    listeIsThere = False
    
    if my_file.is_file() is False:
        # file doesn't exists        
        print(bcolors.FAIL + "[FAIL]" + bcolors.ENDC + " NutzerListe" + " doesn't exist")
    else:
        print(bcolors.OKGREEN + "[SUCCESS]" + bcolors.ENDC + " NutzerListe" + " is found")
        listeIsThere = True
        
    
    # give back a list
    return newFiles, listeIsThere
    

def importfiles(newFiles):

    Array_user = []
    Array_project = []
    Array_project_item = []
    Array_project_item_hour = []
    Array_season = []
    Array_member = []
    
    import csv
    from data import Nutzer 
    
    newPath = path + "Arbeitsstunden/"

    # Array_Nutzer
    with open(( newPath + "user" + ".csv"), newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            temp = user(
                id = row[0],
                member_id = row[1],
                email = row[2],
                password = row[3],
                role = row[4]
            )
            Array_user.append(temp)
    
    # array_project
    with open(( newPath + "project" + ".csv"), newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            temp = project(
                id = row[0],
                name = row[1],
                description = row[2],
                first_season = row[3],
                last_season = row[4]
            )
            Array_project.append(temp)
    
    #Array_project_item
    with open(( newPath + "Array_project_item" + ".csv"), newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            temp = project_item(
                id = row[0],
                project_id = row[1],
                season = row[2],
                date = row[3],
                title = row[4],
                description = row[5]
            )
            Array_project_item.append(temp)
    
    #project_item_hour
    with open(( newPath + "project_item_hour" + ".csv"), newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            temp = project_item_hour(
                id = row[0],
                project_item_id = row[1],
                member_id= row[2],
                duration = row[3]
            )
            Array_project_item_hour.append(temp)
    
    # season
    with open(( newPath + "season" + ".csv"), newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            temp = season(
                year = row[0],
                obligatory_minutes = row[1]
            )
            Array_season.append(temp)
    
    # member
    with open(( newPath + "member" + ".csv"), newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            temp = member(
                id = row[0],
                user_id = row[1],
                first_name = row[2],
                last_name = row[3]
            )
            Array_member.append(temp)
    
    
    
    return Array_user, Array_project,Array_project_item,Array_project_item_hour,Array_season,Array_member


async def importCSV():
        
    # Check which data file can be found
    importable_files, listeIsThere = checkForImport()
    print("---------------------------------------")
    
    Array_Hours = []
    
    Array_nutzer = []
    
    if(len(importable_files) == 8):
        Array_user, Array_project, Array_project_item, Array_project_item_hour, Array_season, Array_member = importfiles(importable_files)
    
    # import Nutzer Liste
    if listeIsThere:
        # import Nutzerliste
        
        import csv
        from data import Nutzer 

        with open((path + "Nutzer/" + "NutzerListe.csv"), newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            for row in spamreader:
                temp = Nutzer(
                    Nachname= row[0],
                    Vorname= row[1],
                    Eintrittsdatum=row[2],
                    Status=row[3],
                    E_Mail=row[4]
                )
                Array_nutzer.append(temp)
    print(bcolors.OKGREEN + "[SUCCESS]" + bcolors.ENDC + " imported User-Data")
    print(bcolors.OKCYAN + "[INFO]" + bcolors.OKCYAN + str(len(Array_nutzer)) + " users ready for import")
    
    # Gib je nach Option eine Check Meldung raus.
    
    print("---------------------------------------")
    print(bcolors.OKCYAN + "[INFO]" + bcolors.OKCYAN + str(len(Array_nutzer)) + " Starting import")
    

    Nutzerliste(Array_nutzer)
    Arbeitsstunden(
        Array_user, 
        Array_project,
        Array_project_item,
        Array_project_item_hour,
        Array_season,
        Array_member
    )
        
    pass