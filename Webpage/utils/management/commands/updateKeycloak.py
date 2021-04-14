from django.core.management.base import BaseCommand

from utils.keycloak import *


class Command(BaseCommand):
    help = 'Update from Keycloak'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        try:
            auto_Update_Roles()
        except:
            self.stdout.write("Error beim Update von Roles", ending='')
            pass
        try:
            auto_Update_Groups()
        except:
            self.stdout.write("Error beim Update der Groups", ending='')
            pass
        try:
            update_all_Users()
        except:
            self.stdout.write("Error beim Update der User", ending='')
            pass


