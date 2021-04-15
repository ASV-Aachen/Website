from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from tinymce import HTMLField
from simple_history.models import HistoricalRecords

# Infos über das aktuelle Jahr

#class Jahresinfo(models.Model):
#    Jahr = models.IntegerField(primary_key=True)
#    ZuLeistendeArbeitsstunden = models.IntegerField()


# Speicher für InfoSeiten welche wir gerne mal verändern
#class infoPage(models.Model):
#    Titel = models.CharField(max_length=200, primary_key=True)
#    Text = models.TextField(null=False)
#    Beschreibung = models.TextField()


def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]

class blogPostHistory(models.Model):
    titel = models.CharField(max_length=200)
    text = HTMLField()
    editor = models.CharField(max_length=300)

    date = models.DateTimeField(auto_created=True, default=timezone.now)

    def __str__(self):
        return self.date.__str__() + " - " + self.editor

# Modell für alle Blogeinträge
class blogPost(models.Model):
    titel = models.CharField(max_length=200)
    text = HTMLField()
    author = models.ForeignKey(User, on_delete=models.SET(get_sentinel_user))
    date_Created = models.DateTimeField(auto_created=True, default=timezone.now)

    last_editor = models.CharField(max_length=300)

    history = models.ManyToManyField(blogPostHistory, blank=True)

    def __str__(self):
        return self.titel
