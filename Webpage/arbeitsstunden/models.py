from django.db import models

# Create your models here.
from Mitglieder.models import Profile


class Saison(models.Model):
    Jahr = models.IntegerField(primary_key=True)  # Erstes Jahr der Saison, z.B. "2020" => Saison 2020/21

    def __str__(self):
        return "Saison " + str(self.Jahr) + "/" + str(self.Jahr + 1)[-2:]


class Tag(models.Model):
    Name = models.CharField(max_length=256)

    def __str__(self):
        return self.Name

class Projekt(models.Model):
    Saison = models.ForeignKey(Saison, on_delete=models.RESTRICT)
    Name = models.CharField(max_length=256)
    Beschreibung = models.TextField(blank=True)
    Verantwortlich = models.ManyToManyField(Profile)

    def __str__(self):
        return str(self.Saison) + ": " + self.Name


class Arbeitsstundenausschreibung(models.Model):
    Titel = models.CharField(max_length=512)
    Beschreibung = models.TextField()
    Projekt = models.ForeignKey(Projekt, on_delete=models.RESTRICT)
    Tags = models.ManyToManyField(Tag, blank=True)
    Umfang = models.CharField(max_length=512, blank=True)
    Fertigstellungstermin = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.Titel


class Arbeitseinheit(models.Model):
    Projekt = models.ForeignKey(Projekt, on_delete=models.RESTRICT)
    Beschreibung = models.CharField(max_length=1024)
    Beteiligte = models.ManyToManyField(Profile, through="Arbeitsbeteiligung")
    Ausschreibung = models.ForeignKey(Arbeitsstundenausschreibung, on_delete=models.SET_NULL, blank=True, null=True)


class Arbeitsbeteiligung(models.Model):
    Arbeitseinheit = models.ForeignKey(Arbeitseinheit, on_delete=models.RESTRICT)
    Arbeitsleistender = models.ForeignKey(Profile, on_delete=models.RESTRICT)
    Arbeitszeit = models.FloatField()

