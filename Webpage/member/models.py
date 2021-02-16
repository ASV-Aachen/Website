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
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    Heimatstadt = models.CharField(max_length=100)
    PLZ = models.IntegerField()
    Land = models.CharField(max_length=70)
    
    profile_image = models.ImageField(upload_to=get_image_path, blank=True, null=True)

    PositionImVerein = models.ManyToManyField(Position, through="PositionImVerein")
    Status = models.ForeignKey(Status, null=False, on_delete=models.RESTRICT)
    Eintrittsdatum = models.DateField()
    # Konto Gehört zur Bierkasse #23 (TODO)
    HandyNummer = models.CharField(max_length=100)

# Receiver Funktionen zum einarbeiten der neuen USER
@receiver(post_save, sender=Profile)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=Profile)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class PositionImVerein(models.Model):
    ErnennungsDatum = models.DateField(null=False)
    Position = models.ForeignKey(Position, on_delete=models.CASCADE)
    Mitglied = models.ForeignKey(Profile, on_delete=models.CASCADE)
