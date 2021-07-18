from django.core.management.base import BaseCommand

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


