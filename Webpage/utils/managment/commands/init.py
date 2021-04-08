from django.core.management.base import BaseCommand

from arbeitsstunden.models import Saison
from web.models import HeadPage, infoPage, frontHeader


class Command(BaseCommand):
    help = 'Creates the init Data'

    def handle(self):
        self.headerAndInfoPages()
        self.arbeitsstundenSeason()

    def headerAndInfoPages(self):
        text = "Diese Seite ist in Arbeit"

        right = HeadPage(titel="Segeln lernen", text=text, description=text, name="SL" )
        right.save()
        infoPage(titel="Segeln lernen", text=text, headPage=right, name="SL").save()

        left = HeadPage(titel="Der Verein", text=text, description=text, name="DV")
        left.save()
        infoPage(titel="Mitglied werden", text=text, headPage=left, name="MitgliedWerden").save()
        infoPage(titel="Personalia", text=text, headPage=left, name="Personalia").save()
        infoPage(titel="Ausbildung", text=text, headPage=left, name="Ausbildung").save()

        temp = HeadPage(titel="Seeschiff", text=text, description=text, name="SEE")
        temp.save()
        infoPage(titel="Aquis Granus IV", text=text, headPage=temp, name="AquisGranusIV").save()
        infoPage(titel="Position", text=text, headPage=temp, name="Position").save()

        temp = HeadPage(titel="Jollenpark", text=text, description=text, name="JP").save()
        temp.save()

        temp = HeadPage(titel="Aktivitäten", text=text, description=text, name="AK").save()
        temp.save()
        infoPage(titel="Regatta", text=text, headPage=temp, name="Regatta").save()

        # FrontPage init
        frontHeader(left=left, right=right).save()
        pass


    def arbeitsstundenSeason(self):
        Saison(Jahr=2019).save()
        Saison(Jahr=2020).save()
