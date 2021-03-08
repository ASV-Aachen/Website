from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User


# Infos über das aktuelle Jahr

class Jahresinfo(models.Model):
    Jahr = models.IntegerField(primary_key=True)
    ZuLeistendeArbeitsstunden = models.IntegerField()


# Speicher für InfoSeiten welche wir gerne mal verändern
class InfoPage(models.Model):
    Titel = models.CharField(max_length=200, primary_key=True)
    Text = models.TextField(null=False)
    Beschreibung = models.TextField()


#def get_sentinel_user():
#    return get_user_model().objects.get_or_create(username='deleted')[0]


# Modell für alle Blogeinträge
#class BlogEintrag(models.Model):
#    Titel = models.CharField(max_length=200)
#    Inhalt = HTMLField()
#    Autor = models.ForeignKey(User, on_delete=models.SET(get_sentinel_user))
#    DatumErstellt = models.DateTimeField(auto_created=True, default=timezone.now)
