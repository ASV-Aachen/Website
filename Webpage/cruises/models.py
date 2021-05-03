from pprint import pprint
from django.utils.translation import gettext_lazy as _
from django.db import models

# Create your models here.
from member.models import profile
   
class Cruise(models.Model):
    CruiseName = models.CharField(max_length=128)
    CruiseDescription = models.TextField(blank=True, null=False)
    StartDate = models.DateField()
    EndDate = models.DateField()
    StartPort = models.CharField(max_length=128)
    EndPort = models.CharField(max_length=128)
    MaxBerths = models.IntegerField()
    Sailors = models.ManyToManyField(profile, through="CruiseShare")
    
    def __str__(self):
        return self.CruiseName


class CruiseShare(models.Model):
    Cruise = models.ForeignKey(Cruise, on_delete=models.RESTRICT)
    profile = models.ForeignKey(profile, on_delete=models.RESTRICT)

    SKIPPER = 'S'
    WATCH = 'W'
    CREW = 'C'
    PATENT_TYPE = [
        (SKIPPER, 'Schiffer'),
        (WATCH, 'Wachführer'),
        (CREW, 'Crew'),
    ]
    SailAs = models.CharField(max_length=2, choices=PATENT_TYPE, default=CREW)
    Distance = models.FloatField()

    def __str__(self):
        return str(self.profile) + " sailed at " + str(self.Cruise) + str(self.Distance) + " nm as " + str(self.SailAs)

class Patent(models.Model):
    Owner = models.ForeignKey(profile, on_delete=models.CASCADE)

    SKIPPER = 'S'
    WATCH = 'W'
    PATENT_TYPE = [
        (SKIPPER, 'Schiffer'),
        (WATCH, 'Wachführer'),
    ]
    Type = models.CharField(max_length=1, choices=PATENT_TYPE)
    Since = models.DateField()

class License(models.Model):
    Owner = models.ForeignKey(profile, on_delete=models.CASCADE)

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