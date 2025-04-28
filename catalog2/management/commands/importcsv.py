import csv
from django.core.management.base import BaseCommand
from catalog2.models import Glassone, Glasstwo, Glassthree, Szyba, Ramka


class Command(BaseCommand):
    help = 'Importer CSV do bazy danych dla modeli Glassone, Glasstwo i Glassthree'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Ścieżka do pliku CSV')

    def handle(self, *args, **options):
        csv_path = options['csv_file']

        try:
            with open(csv_path, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                rows = list(reader)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Nie udało się otworzyć pliku: {e}"))
            return

        if not rows:
            self.stdout.write(self.style.ERROR("Plik CSV jest pusty"))
            return

        # Przyjmujemy, że pierwszy wiersz to główny nagłówek
        main_header = rows.pop(0)
        self.stdout.write(f"Nagłówek główny: {main_header}")

        current_section = None
        for row in rows:
            # Pomijamy całkowicie puste wiersze
            if not any(cell.strip() for cell in row):
                continue

            # Jeżeli pierwszy element wiersza to nazwa sekcji, ustawiamy ją i przechodzimy do kolejnego wiersza
            if row[0] in ('Glassone', 'Glasstwo', 'Glassthree'):
                current_section = row[0]
                self.stdout.write(f"Rozpoczynamy sekcję: {current_section}")
                continue

            if current_section is None:
                self.stdout.write(self.style.WARNING("Nie ustawiono sekcji – pomijam wiersz"))
                continue

            # Przetwarzamy dane w zależności od bieżącej sekcji
            try:
                if current_section == 'Glassone':
                    # Format: [ID, szyba1_nazwa, "", "", "", "", szyba1_grubosc, ufactor, gfactor, rw]
                    # Zakładamy, że kolumna ID jest nieistotna przy imporcie
                    _, szyba1_name, _, _, _, _, szyba1_grubosc, ufactor, gfactor, rw = row
                    # Szukamy lub tworzymy obiekt szyby (pole 'grubosc' traktujemy jako tekst – rzutuj w razie potrzeby na Decimal)
                    szyba, created = Szyba.objects.get_or_create(
                        nazwa=szyba1_name,
                        defaults={'grubosc': szyba1_grubosc}
                    )
                    if created:
                        self.stdout.write(f"Utworzono szybę: {szyba}")
                    else:
                        self.stdout.write(f"Znaleziono istniejącą szybę: {szyba}")

                    glassone = Glassone.objects.create(
                        szyba1=szyba,
                        ufactor=ufactor,
                        gfactor=gfactor,
                        rw=rw
                    )
                    self.stdout.write(f"Zaimportowano Glassone: {glassone}")

                elif current_section == 'Glasstwo':
                    # Format: [ID, szyba1_nazwa, ramka1_nazwa, szyba2_nazwa, "", "", computed_grubosc, ufactor, gfactor, rw]
                    _, szyba1_name, ramka1_name, szyba2_name, _, _, _, ufactor, gfactor, rw = row

                    try:
                        szyba1 = Szyba.objects.get(nazwa=szyba1_name)
                    except Szyba.DoesNotExist:
                        self.stdout.write(
                            self.style.WARNING(f"Nie znaleziono szyby (szyba1): {szyba1_name}. Pomijam wiersz"))
                        continue

                    try:
                        szyba2 = Szyba.objects.get(nazwa=szyba2_name)
                    except Szyba.DoesNotExist:
                        self.stdout.write(
                            self.style.WARNING(f"Nie znaleziono szyby (szyba2): {szyba2_name}. Pomijam wiersz"))
                        continue

                    try:
                        ramka1 = Ramka.objects.get(nazwa=ramka1_name)
                    except Ramka.DoesNotExist:
                        self.stdout.write(self.style.WARNING(f"Nie znaleziono ramki: {ramka1_name}. Pomijam wiersz"))
                        continue

                    glasstwo = Glasstwo.objects.create(
                        szyba1=szyba1,
                        ramka1=ramka1,
                        szyba2=szyba2,
                        ufactor=ufactor,
                        gfactor=gfactor,
                        rw=rw
                    )
                    self.stdout.write(f"Zaimportowano Glasstwo: {glasstwo}")

                elif current_section == 'Glassthree':
                    # Format: [ID, szyba1_nazwa, ramka1_nazwa, szyba2_nazwa, ramka2_nazwa, szyba3_nazwa, computed_grubosc, ufactor, gfactor, rw]
                    _, szyba1_name, ramka1_name, szyba2_name, ramka2_name, szyba3_name, _, ufactor, gfactor, rw = row

                    try:
                        szyba1 = Szyba.objects.get(nazwa=szyba1_name)
                    except Szyba.DoesNotExist:
                        self.stdout.write(
                            self.style.WARNING(f"Nie znaleziono szyby (szyba1): {szyba1_name}. Pomijam wiersz"))
                        continue

                    try:
                        szyba2 = Szyba.objects.get(nazwa=szyba2_name)
                    except Szyba.DoesNotExist:
                        self.stdout.write(
                            self.style.WARNING(f"Nie znaleziono szyby (szyba2): {szyba2_name}. Pomijam wiersz"))
                        continue

                    try:
                        szyba3 = Szyba.objects.get(nazwa=szyba3_name)
                    except Szyba.DoesNotExist:
                        self.stdout.write(
                            self.style.WARNING(f"Nie znaleziono szyby (szyba3): {szyba3_name}. Pomijam wiersz"))
                        continue

                    try:
                        ramka1 = Ramka.objects.get(nazwa=ramka1_name)
                    except Ramka.DoesNotExist:
                        self.stdout.write(
                            self.style.WARNING(f"Nie znaleziono ramki (ramka1): {ramka1_name}. Pomijam wiersz"))
                        continue

                    try:
                        ramka2 = Ramka.objects.get(nazwa=ramka2_name)
                    except Ramka.DoesNotExist:
                        self.stdout.write(
                            self.style.WARNING(f"Nie znaleziono ramki (ramka2): {ramka2_name}. Pomijam wiersz"))
                        continue

                    glassthree = Glassthree.objects.create(
                        szyba1=szyba1,
                        ramka1=ramka1,
                        szyba2=szyba2,
                        ramka2=ramka2,
                        szyba3=szyba3,
                        ufactor=ufactor,
                        gfactor=gfactor,
                        rw=rw
                    )
                    self.stdout.write(f"Zaimportowano Glassthree: {glassthree}")

                else:
                    self.stdout.write(self.style.WARNING("Nieznana sekcja – pomijam wiersz"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Błąd podczas przetwarzania wiersza {row}: {e}"))
                continue

        self.stdout.write(self.style.SUCCESS("Import zakończony pomyślnie"))
