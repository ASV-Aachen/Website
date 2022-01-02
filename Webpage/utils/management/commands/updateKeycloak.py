from django.core.management.base import BaseCommand

from arbeitsstunden.models import account, customHours, getCurrentSeason
from cruises.models import sailor

from utils.keycloak import *


class Command(BaseCommand):
    help = 'Update from Keycloak'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        try:
            auto_Update_Roles() 
        except Exception as e:
            self.stdout.write("Error beim Update von Roles " + str(e), ending='\n')
            pass
        try:
            auto_Update_Groups()
        except Exception as e:
            self.stdout.write("Error beim Update der Groups: " + str(e), ending='\n')
            pass
        try:
            update_all_Users()
        except Exception as e:
            self.stdout.write("Error beim Update der User: " + str(e), ending='\n')
            pass

        # Account anlegen
        for user in profile.objects.all():
            if user.workingHoursAccount is None:
                temp, _ = account.objects.get_or_create(name=user.user.first_name + user.user.last_name)
                user.workingHoursAccount = temp
        season = getCurrentSeason()

        # Custom Hours anlegen
        for i in account.objects.all():
            try:
                test = customHours(season=season[0], used_account = i, customHours = season[0].hours)
                test.save()
            except Exception as e:
                print(e)
                pass

        # Sailor anlegen
        for user in profile.objects.all():
            if user.sailorID is None:
                temp, _ = sailor.objects.get_or_create(name=user.user.first_name + " " + user.user.last_name)
                user.sailorID = temp