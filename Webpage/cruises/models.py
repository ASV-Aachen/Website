from pprint import pprint
from django.utils.translation import gettext_lazy as _
from django.db import models

# Create your models here.
import datetime
from django.contrib.auth.models import User

class sailor(models.Model):
    name = models.CharField(max_length=256, default="TESTNUTZER")

    def __str__(self):
        return self.name

class cruise(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(blank=True)
    startDate = models.DateField()
    endDate = models.DateField()
    startPort = models.CharField(max_length=128)
    endPort = models.CharField(max_length=128)
    maxBerths = models.IntegerField()
    sailors = models.ManyToManyField(sailor, blank=True, null=True, through="cruiseShare")
    
    def getCrewsize(self):
        size = 23
        size = cruiseShare.objects.all().filter(Cruise=self).count()
        return size


    def __str__(self):
        return self.name

class cruiseShare(models.Model):
    Cruise = models.ForeignKey(cruise, on_delete=models.RESTRICT)
    cosailor = models.ForeignKey(sailor, on_delete=models.RESTRICT)

    SKIPPER = 'S'
    WATCH = 'W'
    CREW = 'C'
    PATENT_TYPE = [
        (SKIPPER, 'Schiffer'),
        (WATCH, 'Wachführer'),
        (CREW, 'Crew'),
    ]
    SailAs = models.CharField(max_length=2, choices=PATENT_TYPE, default=CREW)
    Distance = models.FloatField(default=0.0)

    def __str__(self):
        return str(self.cosailor) + " sailed at " + str(self.Cruise) + str(self.Distance) + " nm as " + str(self.SailAs)

class patent(models.Model):
    Owner = models.ForeignKey(User, on_delete=models.CASCADE)

    SKIPPER = 'S'
    WATCH = 'W'
    PATENT_TYPE = [
        (SKIPPER, 'Schiffer'),
        (WATCH, 'Wachführer'),
    ]
    Type = models.CharField(max_length=1, choices=PATENT_TYPE)
    Since = models.DateField()

class license(models.Model):
    Owner = models.ForeignKey(User, on_delete=models.CASCADE)

    SHS = 'SHS'
    SSS = 'SSS'
    SKS = 'SKS'
    SBS = 'SBS'
    SBB = 'SBB'
    SRC = 'SRC'
    LRC = 'LRC'
    LICENSE_TYPE = [
        (SHS, 'Sporthochseeschifferschein'),
        (SSS, 'Sportseeschifferschein'),
        (SKS, 'Sportlüstenschifferschein'),
        (SBS, 'Sportbootführerschein See'),
        (SBB, 'Sportbootführerschein Binnen'),
        (SRC, 'Short Range Certificate'),
        (LRC, 'Long Range Certificate'),
    ]


    Type = models.CharField(max_length=3, choices=LICENSE_TYPE)
    Since = models.DateField()
    LicenseNumber = models.CharField(max_length=16)