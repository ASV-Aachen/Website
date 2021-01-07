from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


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
    User = models.ForeignKey(Profile)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Heimatstadt = models.CharField(max_length=45)
    PLZ = models.IntegerField()
    Land = models.CharField(max_length=70)
    # Bild (TODO)
    PositionImVerein = models.models.ManyToManyField(Position, through="PositionImVerein")
    Status = models.ForeignKey(Status, null=False)
    Eintrittsdatum = models.DateField()
    # Konto Gehört zur Bierkasse #23 (TODO)
    EMail = models.EmailField(null=False)
    HandyNummer = models.CharField(max_length=100)


    Darfbearbeiten = models.BooleanField()

# Receiver Funktionen zum einarbeiten der neuen USER
@receiver(post_save, sender=Profile)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=Profile)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class PositionImVerein(models.Model):
    ErnennungsDatum = models.date(null=False)
    Position = models.ForeignKey(Position)
    Mitglied = models.ForeignKey(Profile)