from django.db import models
from ..Mitglieder.models import Profile

# Infos über das aktuelle Jahr
class Jahresinfo(models.Model):
    Jahr = models.IntegerField(primary_key=True)
    ZuLeistendeArbeitsstunden = models.IntegerField()


# Speicher für InfoSeiten welche wir gerne mal verändern
class InfoPage(models.Model):
    Titel = models.CharField(max_length=200, primary_key=True)
    Text = models.TextField(null=False)
    Beschreibung = models.TextField()


# Modell für alle Blogeinträge
class Blogeintrag(models.Model):
    Titel = models.CharField(max_length=200)
    Text = models.TextField()
    Autor = models.ForeignKey(Profile)
    Datum = models.DateField(auto_created=True)