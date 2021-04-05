from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User


# Infos über das aktuelle Jahr
from tinymce import HTMLField


class Jahresinfo(models.Model):
    Jahr = models.IntegerField(primary_key=True)
    ZuLeistendeArbeitsstunden = models.IntegerField()


class subThemen(models.Model):
    titel = models.CharField(max_length=200, unique=True )


'''
Model zur Speicherung der Historie der InfoPages
'''
class infoPageHistory(models.Model):

    user_Editor = models.CharField(max_length=200)

    titel = models.CharField(max_length=200)
    text = HTMLField()
    description = models.TextField()

    # subThema = models.ForeignKey(subThemen)
    name = models.CharField(max_length=200, unique=True)

    datum = models.DateField()

'''
Model für die Infoseiten
'''
class infoPage(models.Model):
    themen = (
        ("SL", "Segeln lernen"),
        ("V", "Der Verein"),
        ("See", "Seeschiff"),
        ("J", "Jollenpark"),
        ("A", "Aktivitäten")
    )

    status = models.CharField(choices=themen, default="SL", max_length=3)

    titel = models.CharField(max_length=200)
    text = HTMLField()
    description = models.TextField()

    # subThema = models.ForeignKey(subThemen)
    name = models.CharField(max_length=200, unique=True)

    history = models.ManyToManyField(infoPageHistory)

    def getFullUrl(self):
        return "/" + str(self.subThema) + "/" + str(self.name)

    def __str__(self):
        return self.titel
