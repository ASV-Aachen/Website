from django.test import TestCase

from arbeitsstunden.management.commands.utils.import_functions import getStatus

class importFunctons(TestCase):
    
    def setUp(self) -> None:
        return super().setUp()
    
    def Test_getStatus(self):
        self.assertEqual(getStatus("Anwärter"), "Anwärter")
    
    
