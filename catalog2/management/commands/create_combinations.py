from django.core.management.base import BaseCommand
from catalog2.models import Szyba, Ramka, Glasstwo, Glassthree, Glassone
from itertools import permutations

class Command(BaseCommand):
    help = 'Tworzy wszystkie możliwe kombinacje pakietów szyba-ramka oraz okien jednoszybowych, pomijając istniejące'

    def handle(self, *args, **kwargs):

        szyby = Szyba.objects.all()
        ramki = Ramka.objects.all()


        self.create_glasstwo_combinations(szyby, ramki)


        self.create_glassthree_combinations(szyby, ramki)


        self.create_glassone_combinations(szyby)

    def create_glasstwo_combinations(self, szyby, ramki):

        for szyba1, szyba2 in permutations(szyby, 2):
            for ramka in ramki:

                glasstwo, created = Glasstwo.objects.get_or_create(
                    szyba1=szyba1, szyba2=szyba2, ramka1=ramka
                )
                if created:
                    self.stdout.write(f'Utworzono pakiet Glasstwo: {glasstwo}')
                else:
                    self.stdout.write(f'Pakiet Glasstwo już istnieje: {glasstwo}')

    def create_glassthree_combinations(self, szyby, ramki):

        for szyba1, szyba2, szyba3 in permutations(szyby, 3):
            for ramka1, ramka2 in permutations(ramki, 2):

                glassthree, created = Glassthree.objects.get_or_create(
                    szyba1=szyba1, szyba2=szyba2, szyba3=szyba3, ramka1=ramka1, ramka2=ramka2
                )
                if created:
                    self.stdout.write(f'Utworzono pakiet Glassthree: {glassthree}')
                else:
                    self.stdout.write(f'Pakiet Glassthree już istnieje: {glassthree}')

    def create_glassone_combinations(self, szyby):

        for szyba in szyby:

            glassone, created = Glassone.objects.get_or_create(
                szyba1=szyba
            )
            if created:
                self.stdout.write(f'Utworzono okno jednoszybowe: {glassone}')
            else:
                self.stdout.write(f'Okno jednoszybowe już istnieje: {glassone}')
