from faker import Faker

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
            "Text": fake.text(),
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
