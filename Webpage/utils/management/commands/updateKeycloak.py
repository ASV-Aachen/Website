from django.core.management.base import BaseCommand

from utils.keycloak import *


class Command(BaseCommand):
    help = 'Update from Keycloak'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        auto_Update_Roles()
        auto_Update_Groups()
        update_all_Users()


