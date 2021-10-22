from django.test import TestCase
from arbeitsstunden.models import costCenter, work

from utils.faker import fakeArbeitsstunden, fakeNews
from utils.member import getGender

class fakerTest(TestCase):
    def setUp(self) -> None:
        return super().setUp()
    
    def test_fakeNews(self):
        fakeArbeitsstunden(1)
        
        self.assertEqual(work.objects.all().count(), 6)

class memberTester(TestCase):
    def setUp(self) -> None:
        return super().setUp()
    
    def test_getGender(self):
        self.assertEquals(getGender("Nele"), "F")
        self.assertEquals(getGender("Selma"), "F")
        self.assertEquals(getGender("Yvonne"), "F")
        self.assertEquals(getGender("Inga"), "F")
        self.assertEquals(getGender("Janine"), "F")
        self.assertEquals(getGender("Rieke"), "F")
        self.assertEquals(getGender("Neele"), "F")
        
        self.assertEquals(getGender("Christian"), "M")
        self.assertEquals(getGender("Andreas"), "M")
        self.assertEquals(getGender("Thomas"), "M")
        self.assertEquals(getGender("Jan"), "M")
        self.assertEquals(getGender("Marc"), "M")
        self.assertEquals(getGender("Dirk"), "M")
        self.assertEquals(getGender("Jörg"), "M")