from pprint import pprint
from django.utils.translation import gettext_lazy as _
from django.db import models

# Create your models here.
from member.models import profile

class Sailor(models.Model):
    Member = models.OneToOneField(profile, on_delete=models.RESTRICT)
    Givenname = models.CharField(max_length=64)
    Sirname = models.CharField(max_length=64)

    SKIPPER = 'S'
    WATCH = 'W'
    CREW = 'C'
    PATENT_TYPE = [
        (SKIPPER, 'Schiffer'),
        (WATCH, 'Wachführer'),
        (CREW, 'Crew'),
    ]
    OwnsPatent = models.CharField(max_length=2, choices=PATENT_TYPE, default=CREW)
   
class Cruise(models.Model):
    CruiseName = models.CharField(max_length=128)
    CruiseDescription = models.TextField()
    StartDate = models.DateField(blank=True, null=False)
    EndDate = models.DateField(blank=True, null=False)
    StartPort = models.CharField(max_length=128)
    EndPort = models.CharField(max_length=128)
    MaxBerths = models.IntegerField()
    Sailors = models.ManyToManyField(Sailor, through="CruiseShare")
    
    def __str__(self):
        return self.CruiseName


class CruiseShare(models.Model):
    Cruise = models.ForeignKey(Cruise, on_delete=models.RESTRICT)
    Sailor = models.ForeignKey(Sailor, on_delete=models.RESTRICT)

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
        return str(self.Sailor) + " sailed at " + str(self.Cruise) + str(self.Distance) + " nm as " + str(self.SailAs)

class License(models.Model):
    Owner = models.ForeignKey(Sailor, on_delete=models.CASCADE)

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