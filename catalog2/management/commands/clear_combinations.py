from django.core.management.base import BaseCommand
from catalog2.models import Glassone, Glasstwo, Glassthree

class Command(BaseCommand):
    help = 'Usuwa pakiety okien w zależności od typu: jednoszybowy, dwuszybowy, trzyszybowy'

    def add_arguments(self, parser):
        # Dodajemy opcje do wybierania, który pakiet usunąć
        parser.add_argument(
            'pakiet',
            type=str,
            choices=['glassone', 'glasstwo', 'glassthree'],
            help='Typ pakietu do usunięcia (glassone, glasstwo, glassthree)'
        )

    def handle(self, *args, **kwargs):
        pakiet = kwargs['pakiet']

        if pakiet == 'glassone':
            self.usun_glassone()
        elif pakiet == 'glasstwo':
            self.usun_glasstwo()
        elif pakiet == 'glassthree':
            self.usun_glassthree()

    def usun_glassone(self):
        # Usuwanie wszystkich obiektów Glassone
        glassone_count, _ = Glassone.objects.all().delete()
        self.stdout.write(f'Usunięto {glassone_count} okien jednoszybowych')

    def usun_glasstwo(self):
        # Usuwanie wszystkich obiektów Glasstwo
        glasstwo_count, _ = Glasstwo.objects.all().delete()
        self.stdout.write(f'Usunięto {glasstwo_count} pakietów Glasstwo')

    def usun_glassthree(self):
        # Usuwanie wszystkich obiektów Glassthree
        glassthree_count, _ = Glassthree.objects.all().delete()
        self.stdout.write(f'Usunięto {glassthree_count} pakietów Glassthree')