from django.core.management.base import BaseCommand

from arbeitsstunden.management.commands.utils.csv import importCSV


class Command(BaseCommand):
    help = "Import the given csv Files (ONLY FOR GIVEN STRUCT)"
    
    def add_arguments(self, parser):
        pass
    
    def handle(self, *args, **options):
        importCSV()
    

