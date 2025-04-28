import csv
import io
from catalog2.models import Glassone, Glasstwo, Glassthree

def generate_csv():
    """
    Funkcja generuje plik CSV (w pamięci) zawierający dane z modeli:
      - Glassone (pakiety jednoszybowe)
      - Glasstwo (pakiety dwuszybowe)
      - Glassthree (pakiety trzyszybowe)
    Dane z każdej sekcji są poprzedzone nagłówkiem (np. "Glassone")
    oraz głównym nagłówkiem z kolumnami. Ostateczny plik jest przefiltrowany,
    aby nie zawierał pustych wierszy.
    """
    # Używamy StringIO z newline='' oraz podajemy lineterminator dla pewności
    output = io.StringIO(newline='')
    writer = csv.writer(output, delimiter=',', lineterminator='\n')

    main_header = [
        "ID", "Szyba1", "Ramka1", "Szyba2", "Ramka2",
        "Szyba3", "Grubość całkowita", "Ufactor", "Gfactor", "rw"
    ]
    writer.writerow(main_header)

    # --- Sekcja dla Glassone ---
    writer.writerow(["Glassone"] + [""] * (len(main_header) - 1))
    for obj in Glassone.objects.all():
        writer.writerow([
            obj.id,
            obj.szyba1.nazwa,
            "",   # brak danych dla Ramka1
            "",   # brak danych dla Szyba2
            "",   # brak danych dla Ramka2
            "",   # brak danych dla Szyba3
            obj.szyba1.grubosc,
            obj.ufactor,
            obj.gfactor,
            obj.rw
        ])

    # --- Sekcja dla Glasstwo ---
    writer.writerow(["Glasstwo"] + [""] * (len(main_header) - 1))
    for obj in Glasstwo.objects.all():
        writer.writerow([
            obj.id,
            obj.szyba1.nazwa,
            obj.ramka1.nazwa,
            obj.szyba2.nazwa,
            "",   # brak danych dla Ramka2
            "",   # brak danych dla Szyba3
            obj.grubosc_calkowita(),  # metoda zwracająca grubość całkowitą
            obj.ufactor,
            obj.gfactor,
            obj.rw
        ])

    # --- Sekcja dla Glassthree ---
    writer.writerow(["Glassthree"] + [""] * (len(main_header) - 1))
    for obj in Glassthree.objects.all():
        writer.writerow([
            obj.id,
            obj.szyba1.nazwa,
            obj.ramka1.nazwa,
            obj.szyba2.nazwa,
            obj.ramka2.nazwa,
            obj.szyba3.nazwa,
            obj.grubosc_calkowita,  # właściwość, więc bez nawiasów
            obj.ufactor,
            obj.gfactor,
            obj.rw
        ])

    # Pobieramy zawartość bufora i usuwamy całkowicie puste linie
    data = output.getvalue()
    lines = data.splitlines()
    # Zachowujemy linie, które nie są puste (dla każdej linii sprawdzamy, czy po usunięciu białych znaków nie jest pusta)
    filtered_lines = [line for line in lines if line.strip() != ""]
    final_data = "\n".join(filtered_lines)

    # Zwracamy czysty CSV jako StringIO
    return io.StringIO(final_data)
