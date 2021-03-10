from PIL import Image
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import os
from phonenumber_field.modelfields import PhoneNumberField
from django_resized import ResizedImageField

class Position(models.Model):
    titel = models.CharField(max_length=70, null=False, primary_key=True)
    description = models.TextField(null=True)

# ---------------------------------------------------------------
# Finde den Path zum Bild
def get_image_path(instance, filename):
    return os.path.join('photos', str(instance.id), filename)

class profile(models.Model):
    Anwärter = 1
    Aktiv = 2
    Inaktiv = 3
    AlterHerr = 4
    Außerordentliches_Mitglied = 5
    Ehrenmitglied = 6
    status_info = (
        (Anwärter, 'Anwärter'),        
        (Aktiv, 'Aktiv'),
        (Inaktiv, 'Inaktiv'),
        (AlterHerr, 'Alter Herr'),
        (Außerordentliches_Mitglied, "Außerordentliches Mitglied"),
        (Ehrenmitglied, 'Ehrenmitglied'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    hometown = models.CharField(max_length=100, null=True, default='Aachen')
    plz = models.IntegerField(null=True, default=52062)
    country = models.CharField(max_length=70, null=True, default='Deutschland')
    
    # profile_image = models.ImageField(upload_to='profile', blank=True, null=True)
    profile_image = ResizedImageField(size=[166,233], upload_to='profile', crop=['middle', 'center'], keep_meta=False, quality=100, blank=True, null=True)
    
    status = models.PositiveSmallIntegerField(choices=status_info, null=True, blank=True)
    
    entry_date = models.DateField()
    # Konto Gehört zur Bierkasse #23 (TODO)

    # Pluggin: https://github.com/stefanfoulis/django-phonenumber-field
    phone = PhoneNumberField(null=True, blank=True, unique=False)
    mobile = PhoneNumberField(null=True, blank=True, unique=False)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name


class position_in_the_club(models.Model):
    ErnennungsDatum = models.DateField(null=False)
    Position = models.ForeignKey(Position, on_delete=models.CASCADE)
    Mitglied = models.ForeignKey(profile, on_delete=models.CASCADE)
