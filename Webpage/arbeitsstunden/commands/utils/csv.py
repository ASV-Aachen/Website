from pathlib import Path


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
    for i in files:
        current_path = path + "Arbeitsstunden/" + i + ".csv"
        my_file = Path(current_path)
        if my_file.is_file() is False:
            # file doesn't exists        
            files.remove(i)
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
    return files, listeIsThere
    

def importCSV():
        
    # Check which data file can be found
    importable_files, listeIsThere = checkForImport()
    
    # import Nutzer Liste
    if listeIsThere:
        # import Nutzerliste
        pass
    
    
    
    # All Files there?
    if len(importable_files) == 7:
        # import members, user, seasons, reduction, projects, project Items, project_item_hour
        
        # Wenn möglich, füge die Accounts zusammen
        pass
        
    # fehlen Projekte oder season, members und User sind aber da => lade nur die members und users. 
    if ("project" not in importable_files and "season" not in importable_files) and ( "members" not in importable_files and "user" not in importable_files):
        pass
    
    
    # Gib je nach Option eine Check Meldung raus.
    
    
        

        
        
    pass