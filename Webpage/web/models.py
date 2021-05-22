from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User


# Infos über das aktuelle Jahr
from django_resized import ResizedImageField
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
    name = models.CharField(max_length=200)

    datum = models.DateField()


'''
Model für die Header Seiten
-> Haben Unterseiten in Form von InfoPages
'''
class HeadPage(models.Model):
    titel = models.CharField(max_length=50)
    text = HTMLField()

    description = models.TextField()

    # image = models.ImageField()
    image = ResizedImageField(size=[166, 233], upload_to='frontPage', crop=['middle', 'center'], keep_meta=False, quality=100, blank=True, null=True)

    # subThema = models.ForeignKey(subThemen)
    name = models.CharField(max_length=200)

    history = models.ManyToManyField(infoPageHistory, blank=True)

    def getFullUrl(self):
        return "/" + str(self.name)

    def __str__(self):
        return self.titel


'''
Model für die Infoseiten
'''
class infoPage(models.Model):
    headPage = models.ForeignKey(HeadPage, on_delete=models.CASCADE)

    titel = models.CharField(max_length=200)
    text = HTMLField()

    # subThema = models.ForeignKey(subThemen)
    name = models.CharField(max_length=200)

    history = models.ManyToManyField(infoPageHistory, blank=True)

    def getFullUrl(self):
        return "/" + str(self.headPage.name) + "/" + str(self.name)

    def __str__(self):
        return self.titel

'''
MUSS BEIM ERSTEN STARTEN ANGELEGT WERDEN!!!!
'''
class frontHeader(models.Model):
    left = models.ForeignKey(HeadPage, on_delete=models.SET_NULL, null=True, related_name="left")
    right = models.ForeignKey(HeadPage, on_delete=models.SET_NULL, null=True, related_name="right")


class standartPages(models.Model):
    titel = models.CharField(max_length=200)
    text = HTMLField()

    def __str__(self):
        return self.titel



class sponsoren(models.Model):
    name = models.CharField(max_length=200)
    text = models.CharField(max_length=500)
    link = models.CharField(max_length=200)

    sponsorenBild   = ResizedImageField(size=[549,240], upload_to="sponsoren", crop=['middle', 'center'], keep_meta=False, quality=100, blank=True, null=True)
    logo            = ResizedImageField(size=[549,240], upload_to="sponsoren", crop=['middle', 'center'], keep_meta=False, quality=100, blank=True, null=True)
    
    def __str__(self) -> str:
        return self.name