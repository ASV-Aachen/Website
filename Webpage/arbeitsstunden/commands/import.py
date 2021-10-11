from django.core.management.base import BaseCommand

class userStruct:
    pass


class Command(BaseCommand):
    help = "Import a given csv File and i"
    
    def add_arguments(self, parser: CommandParser) -> None:
        return super().add_arguments(parser)
    
    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        
        data = self.createData(self.importCSV)
        
        self.addToDatabase(data)
        
        return super().handle(*args, **options)
    

    
    
    def createData(self, data):
        pass
    
    def addToDatabase(self):
        
        
        
        pass