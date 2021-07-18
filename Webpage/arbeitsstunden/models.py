
from pprint import pprint
from django.db import models
# Create your models here.
import datetime
from django.contrib.auth.models import User

# Returns the given Winter season of a year
def getCurrentSeason():
    Year = datetime.datetime.now().year
    temp = season.objects.get_or_create(
        year = Year,
        hours = 40
    )
    if temp[1]:
        for i in account.objects.all():
            try:
                test = customHours(season=temp[0], used_account = i, customHours = temp[0].hours)
                test.save()
            except Exception as e:
                print(e)
                pass
    return temp

class tag(models.Model):
    Name = models.CharField(max_length=256)

    def __str__(self):
        return self.Name

class season(models.Model):
    year = models.IntegerField(primary_key=True)  # Erstes Jahr der Saison, z.B. "2020" => Saison 2020/21
    hours = models.IntegerField()

    def __str__(self):
        return "Saison " + str(self.year) + "/" + str(self.year + 1)[-2:]
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
    
    def getAllHours(self):
        projectsOfthatSeason = project.objects.filter(season = self)
        counter = 0 
        for i in projectsOfthatSeason:
            for x in i.parts:
                counter += x.hours


        return counter

    def getAllDates(self):
        projectsOfthatSeason = project.objects.filter(season = self)
        projectsOfthatSeason = projectsOfthatSeason.filter(aktiv = True)

        time = []
        date = []

        for i in projectsOfthatSeason:
            for x in i.parts:
                time.append(x.hours)
                date.append(x.endDate)
        return [time, date]


class account(models.Model):
    isNew = models.BooleanField(default=False)
    hasShortenedHours = models.BooleanField(default=False)

    name = models.CharField(max_length=256, default="TESTNUTZER")

    def HowManyHoursDoesUserHaveToWork(self, season):
        hours = season.hours
        if self.hasShortenedHours:
            hours = hours / 2
        
        if self.isNew:
            hours = hours / 2
        return hours
    
    def workedHours(self, season):
        
        zahler = 0

        projects = project.objects.filter(season=season)
        for i in projects:
            zahler = zahler + sum(t.hours for t in i.parts.filter(employee = self))

        
        return zahler

    def __str__(self):
        return self.name

class costCenter(models.Model):
    name = models.CharField(max_length=256)
    description = models.CharField(max_length=500)

    def __str__(self) -> str:
        return self.name

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

    class Meta:
        unique_together = (("season", "used_account"),)

    def __str__(self) -> str:
        return self.used_account.name + " - " + str(self.season)
        

    def getCustomHours(self):
        # Prozentualer Anteil
        return self.customHours * self.percentege / 100
        pass

    pass
class work(models.Model):
        
    name = models.CharField(max_length=256)

    employee = models.ManyToManyField(account, blank=True, null=True)
    voluntary = models.BooleanField(default=False)
    hours = models.IntegerField(default = 0)
    
    startDate = models.DateField(blank=True, null=True)
    endDate = models.DateField(blank=True, null=True)

    setupDate = models.DateField(default=datetime.date.today())
    
    def __str__(self):
        return str(self.name)


    
    
class project(models.Model):
    name = models.CharField(max_length=256)
    description = models.CharField(max_length=500, blank=True)
    
    tags = models.ManyToManyField(tag, blank=True)
    responsible = models.ManyToManyField(User, blank=True)

    season = models.ForeignKey(season, on_delete=models.RESTRICT, null=True)
    costCenter = models.ForeignKey(costCenter, on_delete=models.RESTRICT)

    planedHours = models.IntegerField(blank=True, null = True)

    aktiv = models.BooleanField(default=True)

    parts = models.ManyToManyField(work, blank=True)


    def __str__(self) -> str:
        return self.name + "->" + "description"

    def hourDifferenz(self):
        return self.planedHours - self.workedHours()
    
    def workedHours(self):
        workingParts = self.parts
        return sum(i.hours for i in workingParts.all() if i in workingParts.all())


    
