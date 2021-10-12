from django.core.management.base import BaseCommand

from Webpage.arbeitsstunden.commands.utils.csv import importCSV


class Command(BaseCommand):
    help = "Import the given csv Files (ONLY FOR GIVEN STRUCT)"
    
    def add_arguments(self, parser: CommandParser) -> None:
        return super().add_arguments(parser)
    
    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        
        importCSV()
        
        return super().handle(*args, **options)
    

    
    
    def createData(self, data):
        pass
    
    def addToDatabase(self):
        
        
        
        pass