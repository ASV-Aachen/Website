from unicodedata import name
from django.db import models
from django.db.models.base import Model
from tinymce import HTMLField
from phonenumber_field.modelfields import PhoneNumberField
from django_resized import ResizedImageField
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.utils import timezone

class bootsklasse(models.Model):
    name = models.CharField(max_length=100, null=False)
    def __str__(self) -> str:
        return self.name

def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]

class nachricht_historie(models.Model):
    text = models.CharField(max_length=800, null=False)
    autor = models.ForeignKey(User, on_delete=models.SET(get_sentinel_user))
    date = models.DateTimeField(auto_created=True, default=timezone.now)

class nachricht(models.Model):
    # Status
    segelbar = 1
    eingeschränkt_segelbar = 2
    nicht_segelbar = 3
    fertig_für_die_Indienststellung = 4
    status_info = (
        (segelbar, 'segelbar'),        
        (eingeschränkt_segelbar, 'eingeschränkt segelbar'),
        (nicht_segelbar, 'nicht segelbar'),
        (fertig_für_die_Indienststellung, 'Fertig für die Indienststellung'),
    )
        # Segelbar
    Rursee = 1
    Eschweiler = 3
    Aachen = 4
    Segellager = 5
    unterwegs = 6
    position_info = (
        (Rursee, 'Rursee'),
        (Eschweiler, 'Eschweiler'),
        (Aachen, 'Aachen'),
        (Segellager, 'Segellager'),
        (unterwegs, 'unterwegs')
    )

    status = models.PositiveSmallIntegerField(choices=status_info, null=False, default=3)
    standort = models.PositiveSmallIntegerField(choices=position_info, null=False, default=3)

    text = models.CharField(max_length=800, null=False)
    autor = models.ForeignKey(User, on_delete=models.SET(get_sentinel_user))
    date = models.DateTimeField(auto_created=True, default=timezone.now)


class boot(models.Model):    

    # ------------------------------------------
    name = models.CharField(max_length=100, null=False)

    klasse = models.ForeignKey(bootsklasse, on_delete=models.SET_NULL, null=True)
    description = HTMLField()
    image = ResizedImageField(size=[166,233], upload_to='boats', crop=['middle', 'center'], keep_meta=False, quality=100, blank=True, null=True)
    obman = models.ManyToManyField(User, blank=True)

    isboat = models.BooleanField(default=True)
    
    message = models.OneToOneField(nachricht, on_delete=models.SET_NULL, null=True,  blank=True)
    history = models.ManyToManyField(nachricht_historie, blank=True)

    def __str__(self) -> str:
        return self.name
