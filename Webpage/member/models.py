from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import os

class Position(models.Model):
    Titel = models.CharField(max_length=70, null=False, primary_key=True)
    Beschreibung = models.TextField(null=True)
# ---------------------------------------------------------------
class Status(models.Model):
    Titel = models.CharField(max_length=70, null=False, 
    primary_key=True)
    Beschreibung = models.TextField()
# ---------------------------------------------------------------
# Finde den Path zum Bild
def get_image_path(instance, filename):
    return os.path.join('photos', str(instance.id), filename)
class Profile(models.Model):
    Anwärter = 1
    Aktiv = 2
    Inaktiv = 3
    AlterHerr = 4
    Status = (
        (Anwärter, 'Anwärter'),        
        (Aktiv, 'Aktiv'),
        (Inaktiv, 'Inaktiv'),
        (AlterHerr, 'AlterHerr'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    Heimatstadt = models.CharField(max_length=100, null=True, default='Aachen')
    PLZ = models.IntegerField(null=True, default=00000)
    Land = models.CharField(max_length=70, null=True, default='Germany')
    
    profile_image = models.ImageField(upload_to=get_image_path, blank=True, null=True)

    PositionImVerein = models.ManyToManyField(Position, through="PositionImVerein")
    Status = models.PositiveSmallIntegerField(choices=Status, null=True, blank=True)
    
    Eintrittsdatum = models.DateField()
    # Konto Gehört zur Bierkasse #23 (TODO)
    HandyNummer = models.CharField(max_length=100, null=True, default='0000000')
    


# Receiver Funktionen zum einarbeiten der neuen USER


class PositionImVerein(models.Model):
    ErnennungsDatum = models.DateField(null=False)
    Position = models.ForeignKey(Position, on_delete=models.CASCADE)
    Mitglied = models.ForeignKey(Profile, on_delete=models.CASCADE)
