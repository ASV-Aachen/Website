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
Model für die Header Seiten
-> Haben Unterseiten in Form von InfoPages
'''
class HeadPage(models.Model):
    titel = models.CharField(max_length=50)
    text = HTMLField()

    description = models.TextField()
    image = models.ImageField()

    # subThema = models.ForeignKey(subThemen)
    name = models.CharField(max_length=200)

    history = models.ManyToManyField(infoPageHistory)

    def getFullUrl(self):
        return "/" + str(self.name)

    def __str__(self):
        return self.titel


'''
Model für die Infoseiten
'''
class infoPage(models.Model):
    headPage = models.ForeignKey(HeadPage, on_delete=models.CASCADE())

    titel = models.CharField(max_length=200)
    text = HTMLField()

    # subThema = models.ForeignKey(subThemen)
    name = models.CharField(max_length=200)

    history = models.ManyToManyField(infoPageHistory)

    def getFullUrl(self):
        return "/" + str(self.headPage.name) + "/" + str(self.name)

    def __str__(self):
        return self.titel

'''
MUSS BEIM ERSTEN STARTEN ANGELEGT WERDEN!!!!
'''
class frontHeader(models.Model):
    left = models.ForeignKey(HeadPage)
    right = models.ForeignKey(HeadPage)