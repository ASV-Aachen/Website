from django.core.management.base import BaseCommand

from utils.faker import fakeNews, fakeNutzer


class Command(BaseCommand):
    help = 'Creates Fake Infos and users for Testing'

    def handle(self):
        fakeNews(50)
        fakeNutzer(50)