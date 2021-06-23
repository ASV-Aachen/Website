from faker import Faker
from arbeitsstunden.models import *
import random
from member.models import profile

'''
Erstellt die gewünschte Anzahl an fakeNews.
fakeNews sind dabei News müssen nicht zwangsläufig einen Sinn haben.

@return Array, bestehend aus Objekten mit Text, Titel
'''
def fakeNews(Anzahl: int) -> []:
    fake = Faker()
    Ergebnis = []
    for _ in range(0,Anzahl):
        newNews = {
            "Text": fake.text(max_nb_chars=500),
            "Titel": fake.sentence()
        }

        Ergebnis.append(newNews)

    return Ergebnis

'''
Erstellt die gewünschte Anzahl an Fake Nutzern. 

@return Array aus Objecten -> username, vorname, nachname, country, hometown, Email, HandyNummer
'''
def fakeNutzer(Anzahl: int) -> []:
    fake = Faker()
    Ergebnis = []

    for _ in range(0, Anzahl):
        newNews = {
            "username": fake.simple_profile().get("username"),
            "vorname": fake.first_name(),
            "nachname": fake.last_name(),
            "country": fake.country(),
            "hometown": fake.city(),
            "Email": fake.email(),
            "HandyNummer": fake.phone_number()
        }

        Ergebnis.append(newNews)

    return Ergebnis


def fakeArbeitsstunden(AnzahlProKostenstelle: int):
    # aktuelle Season eintragen, falls noch nicht existent
    season = getCurrentSeason()
    fake = Faker()

    Nutzer = profile.objects.all()

    Kostenstelen_namen = [
            "Etage",
            "AGIV",
            "Amme",
            "Rudolf",
            "Halle Eschweiler",
            "Halle Aachen"
        ]
    # Kostenstellen einfügen
    for i in Kostenstelen_namen:
        new = costCenter(name=i, description="----")
        new.save()

    # projekte erstellen (pro Kostenstelle AnzahlProKostenstelle)
    for kostenstelle in costCenter.objects.all():
        for _ in range(AnzahlProKostenstelle):
            newProject = project(
                    name=fake.text(max_nb_chars=60), 
                    description = fake.sentence(), 
                    season = getCurrentSeason(),
                    costCenter = kostenstelle,
                    aktiv = random.choice([True,False])
                )
            newProject.save()
            newProject.responsible.add(random.choice(Nutzer).user)
            for _ in range(random.randint(2,10)):
                # Work erstellen (zwischen 2 und 10 Pro Projekt)
                tempWork = work(
                    name = fake.text(max_nb_chars=40),
                    hours = random.randint(2, 30)
                )
                tempWork.save()
                for _ in range(random.randint(1,5)):
                    # zufällig accounts zuordnen
                    tempWork.employee.add(random.choice(Nutzer).workingHoursAccount)
                tempWork.save()
                newProject.parts.add(tempWork)
                pass    
            newProject.save()



    
    


    pass
