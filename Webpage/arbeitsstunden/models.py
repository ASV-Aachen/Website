
from pprint import pprint
from django.db import models
# Create your models here.
import datetime
from django.contrib.auth.models import User

# Returns the given Winter season of a year
def getCurrentSeason():
    Year = datetime.date.year
    return season.objects.get(year=Year)

class tag(models.Model):
    Name = models.CharField(max_length=256)

    def __str__(self):
        return self.Name

class season(models.Model):
    year = models.IntegerField(primary_key=True)  # Erstes Jahr der Saison, z.B. "2020" => Saison 2020/21
    hours = models.IntegerField()

    def __str__(self):
        return "Saison " + str(self.Jahr) + "/" + str(self.Jahr + 1)[-2:]
    
    def save(self, *args, **kwargs):
        hours = customHours.objects.filter(season = self)

        for i in hours:
            i.customHours = self.hours

        super().save(*args, **kwargs)


class account(models.Model):
    isNew = models.BooleanField(default=False)
    hasShortenedHours = models.BooleanField(default=False)

    name = models.CharField(max_length=256, default="TESTNUTZER")

    def HowManyHoursDoesUserHaveToWork(self, season):
        if(self.customHours != null):
            return self.customHours
        else:
            hours = season.hours
            if self.hasShortenedHours:
                hours = hours / 2
            
            if self.isNew:
                hours = hours / 2
            return hours
    
    def workedHours(self):
        projects = work.objects.filter(employe = self)

    def __str__(self):
        return self.id

class costCenter(models.Model):
    name = models.CharField(max_length=256)
    description = models.CharField(max_length=500)

    def workedHours(self):
        allProjects = project.objects.filter(costCenter=self)
        return sum(i.workedHour() for i in allProjects)

    def workedHoursinSeason(self, season):
        allProjects = project.objects.filter(costCenter=self)
        allProjects = allProjects.filter(season = season)
        return sum(i.workedHour() for i in allProjects)

class customHours(models.Model):
    season = models.ForeignKey(season, on_delete=models.CASCADE)
    used_account = models.ForeignKey(account, on_delete=models.CASCADE)

    customHours = models.IntegerField(null=True)
    percentege = models.IntegerField(default=100)


    def getCustomHours(self):
        # Prozentualer Anteil
        return self.customHours * self.percentege / 100
        pass

    pass
class work(models.Model):
    name = models.CharField(max_length=256)
    description = models.CharField(max_length=500)

    employee = models.ManyToManyField(account, blank=True)
    voluntary = models.BooleanField(default=False)
    hours = models.IntegerField(default = 0)
    
    startDate = models.DateField(blank=True, null=True)
    endDate = models.DateField(blank=True, null=True)

    setupDate = models.DateField(default=datetime.date.today)
    
class project(models.Model):
    name = models.CharField(max_length=256)
    description = models.CharField(max_length=500, blank=True)
    
    tags = models.ManyToManyField(tag, blank=True)
    responsible = models.ManyToManyField(User)

    season = models.ForeignKey(season, on_delete=models.RESTRICT)
    costCenter = models.ForeignKey(costCenter, on_delete=models.RESTRICT)

    planedHours = models.IntegerField(blank=True)

    aktiv = models.BooleanField(default=True)

    parts = models.ManyToManyField(work, blank=True)

    def hourDifferenz(self):
        return self.planedHours - self.workedHours()
    
    def workedHours(self):
        workingParts = self.parts
        return sum(i.hours for i in workingParts)


    
