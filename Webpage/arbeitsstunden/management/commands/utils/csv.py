from pathlib import Path
from typing import Match
from arbeitsstunden.management.commands.utils.data import reduction

from arbeitsstunden.management.commands.utils.data import member, project, project_item, project_item_hour, season, user, Nutzer
from arbeitsstunden.management.commands.utils.import_functions import Arbeitsstunden, Nutzerliste


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
    Array_reduction = []
    
    import csv 
    
    newPath = path + "Arbeitsstunden/"

    # Array_Nutzer
    with open(( newPath + "user" + ".csv"), newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            temp = user()
            temp.id = row[0]
            temp.member_id = row[1]
            temp.email = row[2]
            temp.password = row[3]
            temp.role = row[4]
            Array_user.append(temp)
    
    # array_project
    with open(( newPath + "project" + ".csv"), newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            temp = project()
            temp.id = row[0]
            temp.name = row[1]
            temp.description = row[2]
            temp.first_season = row[3]
            temp.last_season = row[4]
            Array_project.append(temp)
    
    #Array_project_item
    with open(( newPath + "project_item" + ".csv"), newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            temp = project_item()
            temp.id = row[0]
            temp.project_id = row[1]
            temp.season = row[2]
            temp.date = row[3]
            temp.title = row[4]
            temp.description = row[5]
            Array_project_item.append(temp)
    
    #project_item_hour
    with open(( newPath + "project_item_hour" + ".csv"), newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            temp = project_item_hour()
            temp.id = row[0]
            temp.project_item_id = row[1]
            temp.member_id= row[2]
            temp.duration = row[3]
            Array_project_item_hour.append(temp)
    
    # season
    with open(( newPath + "season" + ".csv"), newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            temp = season()
            temp.year = int(row[0])
            temp.obligatory_minutes = row[1]
            Array_season.append(temp)
    
    # member
    with open(( newPath + "member" + ".csv"), newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            temp = member()
            temp.id = row[0]
            temp.user_id = row[1]
            temp.first_name = row[2].replace("\"", "")
            temp.last_name = row[3].replace("\"", "")
            Array_member.append(temp)
    
    # reduction
    with open(( newPath + "reduction" + ".csv"), newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            temp = reduction()
            temp.id = row[0]
            temp.season_id = row[1]
            temp.member_id = row[2]
            temp.status = row[3]
            temp.reduction = row[4]
            Array_reduction.append(temp)
    
    
    
    return Array_user, Array_project,Array_project_item,Array_project_item_hour,Array_season,Array_member, Array_reduction


def importCSV():
        
    # Check which data file can be found
    importable_files, listeIsThere = checkForImport()
    print("---------------------------------------")
    
    Array_nutzer = []
    
    Array_user, Array_project, Array_project_item, Array_project_item_hour, Array_season, Array_member, Array_reduction = importfiles(importable_files)
    
    # import Nutzer Liste
    if listeIsThere:
        # import Nutzerliste
        
        import csv

        with open((path + "Nutzer/" + "NutzerListe.csv"), newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
            for row in spamreader:
                temp = Nutzer()
                temp.Nachname= row[0].replace("\"", "")
                temp.Vorname= row[1].replace("\"", "")
                temp.Eintrittsdatum=row[2]
                temp.Status=row[3]
                temp.E_Mail=row[4]
                Array_nutzer.append(temp)
    print(bcolors.OKGREEN + "[SUCCESS]" + bcolors.ENDC + " imported User-Data")
    print(bcolors.OKCYAN + "[INFO] " + bcolors.ENDC + str(len(Array_nutzer)) + " users ready for import")
    
    # Gib je nach Option eine Check Meldung raus.
    
    print("---------------------------------------")
    print(bcolors.OKCYAN + "[INFO]" + bcolors.ENDC + " Starting import NUTZERLISTE")
    Nutzerliste(Array_nutzer)
    print(bcolors.OKGREEN + "[SUCCESS]" + bcolors.ENDC + " Finished")
    
    print(bcolors.OKCYAN + "[INFO]" + bcolors.ENDC + " Starting import Arbeitsstunden")
    
    Arbeitsstunden(
        Array_user, 
        Array_project,
        Array_project_item,
        Array_project_item_hour,
        Array_season,
        Array_member,
        Array_reduction
    )
    print(bcolors.OKGREEN + "[SUCCESS]" + bcolors.ENDC + " Finished")
    
    pass