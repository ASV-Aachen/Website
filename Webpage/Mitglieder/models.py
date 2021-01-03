from django.db import models

class Position(models.Model):
    Titel = models.CharField(max_length=70, null=False, primary_key=True)
    Beschreibung = models.TextField(null=True)
# ---------------------------------------------------------------
class Status(models.Model):
    Titel = models.CharField(max_length=70, null=False, primary_key=True)
    Beschreibung = models.TextField()
# ---------------------------------------------------------------

class Login(models.Model):
    Passwort = models.TextField()
    Salt = models.TextField()
    User = models.ForeignKey(User)

class User(models.Model):
    Vorname = models.CharField(max_length=45)
    Nachname = models.CharField(max_length=45)
    Heimatstadt = models.CharField(max_length=45)
    PLZ = models.IntegerField()
    Land = models.CharField(max_length=70)
    # Bild (TODO)
    PositionImVerein = models.models.ManyToManyField(Position, through="PositionImVerein")
    Status = models.ForeignKey(Status, null=False)
    Eintrittsdatum = models.DateField()
    # Konto (TODO)
    EMail = models.EmailField(null=False)
    HandyNummer = models.CharField(max_length=100)
    Darfbearbeiten = models.BooleanField()


class PositionImVerein(models.Model):
    ErnennungsDatum = models.date(null=False)
    Position = models.ForeignKey(Position)
    Mitglied = models.ForeignKey(User)