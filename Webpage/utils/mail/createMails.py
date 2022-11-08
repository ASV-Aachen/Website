

def createMail(password)->str:
    mail = """
    Moin Moin,

    mit dieser Mail erhälst du ein Temporäres-Passwort zur Website des ASV Aachen. 
    Das Password ist nur für deinen Account gültig und muss beim ersten anmelden geändert werden. 

    Mit diesem kann man sich bei allen Diensten wie der Arbeitsstundendatenbank, dem Wiki oder der Cloud anmelden.
    Der Nutzername ist dabei die eigene E-Mail-Adresse.
    Die neue Seite ist aktuell erreichbar unter: https://asv-aachen.de/

    Dein Passwort lautet: {}

    BITTE BEACHTEN: Services wie das Wiki oder die Cloud, haben aktuell noch kein vollständiges Zertifikat, weswegen es hier zu ein Warnmeldung im Browser kommt. 
    Dies ist korrekt und wird in Zukunft noch behoben.

    Bei Fragen oder Anmerkungen, melde dich gerne beim Dev Team unter der Mail Adresse: dev@asv-aachen.de

    Viele Grüße,
    Christian Baltzer
    - Das Dev Team
    """
    
    mail = mail.format(password)

    return mail
    