from django.core.management.base import BaseCommand

from arbeitsstunden.models import Saison
from web.models import HeadPage, infoPage, frontHeader


class Command(BaseCommand):
    help = 'Creates the init Data'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        self.headerAndInfoPages()
        self.arbeitsstundenSeason()

    def headerAndInfoPages(self):
        self.stdout.write("Starting Headers", ending='')
        text = "Diese Seite ist in Arbeit"

        right = HeadPage(titel="Segeln lernen", text=text, description=text, name="SL" )
        right.save()
        temp2 = infoPage(titel="Segeln lernen", text=text, headPage=right, name="SL")
        temp2.save()

        left = HeadPage(titel="Der Verein", text=text, description=text, name="DV")
        left.save()
        temp2 = infoPage(titel="Mitglied werden", text=text, headPage=left, name="MitgliedWerden")
        temp2.save()
        temp2 = infoPage(titel="Personalia", text=text, headPage=left, name="Personalia")
        temp2.save()
        temp2 = infoPage(titel="Ausbildung", text=text, headPage=left, name="Ausbildung")
        temp2.save()

        temp = HeadPage(titel="Seeschiff", text=text, description=text, name="SEE")
        temp.save()
        temp2 = infoPage(titel="Aquis Granus IV", text=text, headPage=temp, name="AquisGranusIV")
        temp2.save()
        temp2 = infoPage(titel="Position", text=text, headPage=temp, name="Position")
        temp2.save()

        temp = HeadPage(titel="Jollenpark", text=text, description=text, name="JP")
        temp.save()

        temp = HeadPage(titel="Aktivitäten", text=text, description=text, name="AK")
        temp.save()
        temp2 = infoPage(titel="Regatta", text=text, headPage=temp, name="Regatta")
        temp2.save()

        self.stdout.write("Finished", ending='')
        # FrontPage init
        temp = frontHeader(left=left, right=right)
        temp.save()
        pass


    def arbeitsstundenSeason(self):
        self.stdout.write("Season init", ending='')
        Saison(Jahr=2019).save()
        Saison(Jahr=2020).save()
