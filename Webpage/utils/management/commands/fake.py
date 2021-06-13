from django.core.management.base import BaseCommand

from utils.faker import fakeNews, fakeNutzer


class Command(BaseCommand):
    help = 'Creates Fake Infos and users for Testing'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        self.stdout.write("creating News", ending='\n')
        fakeNews(50)
        self.stdout.write("creating Users", ending='\n')
        fakeNutzer(50)