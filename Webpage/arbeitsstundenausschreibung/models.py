from django.db import models


# Create your models here.
from Mitglieder.models import Profile


class Boot(models.Model):
    Name = models.CharField(max_length=256)

    def __str__(self):
        return self.Name


class Arbeitskategorie(models.Model):
    Name = models.CharField(max_length=256)

    def __str__(self):
        return self.Name


class Tag(models.Model):
    Name = models.CharField(max_length=256)

    def __str__(self):
        return self.Name


class Arbeitsstundenausschreibung(models.Model):
    Titel = models.CharField(max_length=512)
    Beschreibung = models.TextField()
    Boote = models.ManyToManyField(Boot)
    Kategorien = models.ManyToManyField(Arbeitskategorie)
    Tags = models.ManyToManyField(Tag, blank=True)
    Verantwortlich = models.ManyToManyField(Profile)

    def __str__(self):
        return self.Titel
