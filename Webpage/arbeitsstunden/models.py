from pprint import pprint

from django.db import models

# Create your models here.
from member.models import profile


class season(models.Model):
    year = models.IntegerField(primary_key=True)  # Erstes Jahr der Saison, z.B. "2020" => Saison 2020/21

    def __str__(self):
        return "Saison " + str(self.Jahr) + "/" + str(self.Jahr + 1)[-2:]


class tag(models.Model):
    Name = models.CharField(max_length=256)

    def __str__(self):
        return self.Name

class costCenter(models.Model):
    name = models.CharField(max_length=256)
    description = models.CharField(max_length=500)

    def workedHours(self):
        allProjects = project.objects.filter(costCenter=self)

    def workedHoursinSeason(self, season):
        allProjects = project.objects.filter(costCenter=self)
        allProjects = allProjects.filter(season = season)

class project(models.Model):
    name = models.CharField(max_length=256)
    description = models.CharField(max_length=500, blank=True)
    
    tags = models.ManyToManyField(tag, blank=True)
    responsible = models.ManyToManyField(User)

    season = models.ForeignKey(season, on_delete=models.RESTRICT)
    costCenter = models.ForeignKey(costCenter, on_delete=models.RESTRICT)

    planedHours = models.IntegerField(blank=True)

    def hourDifferenz(self):
        return self.planedHours - self.workedHours()
    
    def workedHours(self):
        subprojects = subproject.objects.filter(project = self)
        return sum(i.workedHours() for i in subprojects)

class subproject(models.Model):
    name = models.CharField(max_length=256)
    description = models.CharField(max_length=500)

    project = models.ForeignKey(project, on_delete=models.RESTRICT)

    voluntary = models.BooleanField(default=False)
    parts = models.ManyToManyField(work, blank=True)

    planed = models.BooleanField(default=True)
    endDate = models.DateField(blank=True, null=True)

    planedHours = models.IntegerField(blank=True)

    def hourDifferenz(self):
        return self.planedHours - self.workedHours()

    def workedHours(self):
        workingParts = self.parts
        return sum(i.hours for i in workingParts)
    
    
        
class work(models.Model):
    employee = models.ManyToManyField(User, blank=True)
    hours = models.IntegerField(default = 0)
    description = models.CharField(max_length=500)
    date = models.DateField
