

def createMail(password)->str:
    mail = """
    Moin Moin,

    mit dieser Mail erhälst du ein Temporäres-Passwort zur Website des ASV Aachen. 
    Das Password ist nur für deinen Account gültig und muss beim ersten anmelden geändert werden. 

    Mit diesem kann man sich bei allen Diensten wie der Arbeitsstundendatenbank, dem Wiki oder der Cloud anmelden.
    Der Nutzername ist dabei die eigene E-Mail-Adresse.
    Die neue Seite ist aktuell erreichbar unter: https://neu.asv-aachen.de/

    Dein Passwort lautet: {}

    BITTE BEACHTEN: Die Website hat aktuell noch nicht das endgültige Zertifikat, weswegen es zu einer Warnung im Browser kommt. 
    Dies ist korrekt und wird in Zukunft noch behoben.

    Sollten dir Fehler auffallen, so melde diese gerne an einen der Admins oder trage diese ins folgende Formular ein:
    https://docs.google.com/forms/d/18ddftQjyX_WWSp2K2tNO9UoosWLea-X2v96AQSA0oCg

    Viele Grüße,
    Christian Baltzer
    - Das Dev Team
    """
    
    mail = mail.format(password)

    return mail
    