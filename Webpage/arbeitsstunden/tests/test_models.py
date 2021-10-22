

from datetime import datetime
from django.test.testcases import TestCase
from django.test.utils import tag

from arbeitsstunden.models import *


class TestFunctions(TestCase):
    def setUp(self) -> None:
        return super().setUp()
    
    def test_getCurrentSeason_withoutExistingYear(self):
        self.assertEqual(getCurrentSeason().year, datetime.datetime.now().year)
    
    def test_getCurrentSeason_withExistingYear(self):
        temp = season.objects.get_or_create(
            year = datetime.datetime.now().year
        )
        self.assertEqual(getCurrentSeason()[0].year, datetime.datetime.now().year)
    
class ModelTests(TestCase):
    def setUp(self) -> None:
        return super().setUp()
    
    def test_tag(self):
        newtag = tag(
            Name = "TESTTAG"
        ) 
        newtag.save()
        
        self.assertEqual(tag.objects.all()[0].Name, "TESTTAG")
        

class TestFullSeason(TestCase):
    def setUp(self) -> None:
        # season
        NewSeason = getCurrentSeason()[0]
        NewSeason.save()
        
        NewAccount = account()
        NewAccount.save()
        
        NewCostCenter = costCenter(
            name = "TESTCENTER",
            description = ""
        )
        NewCostCenter.save()
        
        NewCustomHours = customHours(
            season = NewSeason,
            used_account = NewAccount
        )
        NewCustomHours.save()
        
        NewWork = work(
            name="TESTWORK",
            hours = 3
        )
        NewWork.employee.add(NewAccount)
        NewWork.save()
        
        newProjekt = project(
            name="TESTPROJECT",
            season = NewSeason,
            costCenter = NewCostCenter
        )
        newProjekt.parts.add(NewWork)
        newProjekt.save()
        
        return super().setUp()
    
    def test_Project_workedHours(self):
        newProjekt = project.objects.get(name="TESTPROJECT")
        self.assertEqual(newProjekt.workedHours(), 3)
    
    def test_customHours(self):
        NewCustomHours = customHours.objects.all()[0]
        self.assertEqual(NewCustomHours.getCustomHours(), 40)
        
    def test_costCenter(self):
        NewCostCenter = costCenter.objects.get(name = "TESTCENTER")
        self.assertEqual(NewCostCenter.workedHours(), 3)
        self.assertEqual(NewCostCenter.workedHoursinSeason(), 3)
        
    def test_account(self):
        newAccount = account.objects.all()[0]
        self.assertEqual(newAccount.workedHours(), 3)
    
    def test_season(self):
        NewSeason = getCurrentSeason()[0]
        
        self.assertEqual(NewSeason.getAllHours(), 3)
        
    
    
    