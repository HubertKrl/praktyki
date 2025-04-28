import requests
from bs4 import BeautifulSoup


def get_data_from_api_via_bs(api_url):
    """
    Pobiera stronę HTML z API i wyciąga dane tabelaryczne.

    Zakładamy, że HTML zawiera tabelę ze strukturą:
      <table>
        <tbody>
          <tr>
            <td>{{ pak2.szyba1 }}</td>
            <td>{{ pak2.ramka1 }}</td>
            <td>{{ pak2.szyba2 }}</td>
            <td>{{ pak2.grubosc_calkowita }}mm</td>
            <td>{{ pak2.gfactor }}</td>
            <td>{{ pak2.ufactor }}</td>
            <td>{{ pak2.rw }}</td>
          </tr>
          <!-- kolejne wiersze -->
        </tbody>
      </table>

    Funkcja zwraca listę słowników, gdzie każdy słownik reprezentuje jeden wiersz.
    """
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Podnosi wyjątek, jeśli status HTTP to błąd
    except requests.RequestException as e:
        print("Błąd przy pobieraniu danych z API:", e)
        return None

    # Pobieramy treść HTML
    html_content = response.text

    # Parsowanie HTML z BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Szukamy elementu <tbody>; jeśli go nie znajdziemy, możemy spróbować szukać całej tabeli
    tbody = soup.find('tbody')
    if not tbody:
        print("Nie znaleziono elementu <tbody> w otrzymanym HTMLu.")
        return []

    data_list = []
    rows = tbody.find_all("tr")
    for row in rows:
        cells = row.find_all("td")
        if len(cells) < 7:
            # Jeśli liczba komórek jest mniejsza niż oczekiwana – pomijamy wiersz.
            continue
        entry = {
            'szyba1': cells[0].get_text(strip=True),
            'ramka1': cells[1].get_text(strip=True),
            'szyba2': cells[2].get_text(strip=True),
            # Usuwamy końcówkę "mm" z wartości grubości, jeśli jest obecna
            'grubosc_calkowita': cells[3].get_text(strip=True).replace('mm', '').strip(),
            'gfactor': cells[4].get_text(strip=True),
            'ufactor': cells[5].get_text(strip=True),
            'rw': cells[6].get_text(strip=True)
        }
        data_list.append(entry)
    return data_list


if __name__ == '__main__':
    # Podmień poniższy URL na endpoint Twojego API, który zwraca stronę HTML z tabelą
    api_url = "http://example.com/api/tabela"  # <-- to powinien być poprawny URL
    data = get_data_from_api_via_bs(api_url)

    if data is None:
        print("Błąd przy pobieraniu danych.")
    elif len(data) == 0:
        print("Brak danych w tabeli.")
    else:
        print("Dane wyekstrahowane z API:")
        for item in data:
            print(item)