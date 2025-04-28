import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET

from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Pobiera HTML ze strony, parsuje dane tabeli i konwertuje je do XML."

    def add_arguments(self, parser):
        parser.add_argument(
            '--url',
            type=str,
            required=True,
            help="URL strony zawierającej HTML z tabelą do konwersji.",
        )

    def handle(self, *args, **options):
        url = options['url']

        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/110.0.0.0 Safari/537.36"
            ),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Referer": "http://127.0.0.1:8000/"  # Opcjonalnie, jeśli przydatny
        }

        self.stdout.write("Pobieranie HTML ze strony: {}".format(url))
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Wywoła wyjątek, jeśli status HTTP to błąd (np. 403 lub 404)
            html_content = response.text
        except requests.RequestException as e:
            raise CommandError("Błąd przy pobieraniu danych z strony: {}".format(e))

        # Parsowanie HTML przy użyciu BeautifulSoup
        soup = BeautifulSoup(html_content, "html.parser")
        tbody = soup.find("tbody")
        if not tbody:
            raise CommandError("Nie znaleziono elementu <tbody> w pobranym HTML.")

        data_list = []
        rows = tbody.find_all("tr")
        for row in rows:
            cells = row.find_all("td")
            if len(cells) < 7:
                continue  # Pomijamy wiersze z niekompletną liczbą komórek
            record = {
                "szyba1": cells[0].get_text(strip=True),
                "ramka1": cells[1].get_text(strip=True),
                "szyba2": cells[2].get_text(strip=True),
                "grubosc_calkowita": cells[3].get_text(strip=True).replace("mm", "").strip(),
                "gfactor": cells[4].get_text(strip=True),
                "ufactor": cells[5].get_text(strip=True),
                "rw": cells[6].get_text(strip=True)
            }
            data_list.append(record)

        if not data_list:
            raise CommandError("Nie udało się wyekstrahować danych tabelarycznych z HTML.")

        # Budujemy drzewo XML przy użyciu ElementTree
        root = ET.Element("data")
        for record in data_list:
            rec_elem = ET.SubElement(root, "record")
            for key, value in record.items():
                child = ET.SubElement(rec_elem, key)
                child.text = value

        # Konwertujemy drzewo XML na łańcuch bajtowy z deklaracją XML
        xml_str = ET.tostring(root, encoding="utf-8", method="xml")
        xml_declaration = b'<?xml version="1.0" encoding="utf-8"?>\n'
        final_xml = xml_declaration + xml_str

        # Wypisujemy wynik do konsoli (stdout)
        self.stdout.write("Wygenerowany XML:")
        self.stdout.write(final_xml.decode("utf-8"))