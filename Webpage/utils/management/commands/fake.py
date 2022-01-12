from django.core.management.base import BaseCommand

from utils.faker import fakeNews, fakeNutzer
from utils.member import newMember
from blog.models import blogPost
from member.models import profile
import random

class Command(BaseCommand):
    help = 'Creates Fake Infos and users for Testing'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        self.stdout.write("creating News", ending='\n')
        news = fakeNews(50)
        self.stdout.write("creating Users", ending='\n')
        fakeUsers = fakeNutzer(50)
        self.stdout.write("inserting into Database...", ending='\n')

        for i in fakeUsers:
            newMember(
                i['vorname'],
                i['nachname'],
                i['country'],
                i['hometown'],
                i['Email']
            )

        Editoren = profile.objects.all()

        for i in news:
            aktuellerUser = random.choice(Editoren).user
            new = blogPost(text = i['Text'], titel = i['Titel'], author = aktuellerUser, last_editor = "FAKENEWSTEST")
            new.save()
        
        # self.stdout.write("creating Arbeitsstunden", ending='\n')
        # fakeArbeitsstunden(10)

        self.stdout.write("SUCCESS", ending='\n')