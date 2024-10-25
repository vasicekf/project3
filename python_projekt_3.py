"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie
author: Filip Vašíček
email: filda.vasicek@gmail.com
discord: vasicekf
"""

import requests
from bs4 import BeautifulSoup
import csv
import time
import sys


def fetch_url_content(url):
    response = requests.get(url)
    if response.status_code != 200:
        raise ConnectionError(f"Nepodařilo se načíst data z odkazu: {url}")
    return BeautifulSoup(response.text, 'html.parser')


def extract_kraj_vyber_from_url(url):
    try:
        kraj = url.split('xkraj=')[1].split('&')[0]
        vyber = url.split('xnumnuts=')[1].split('&')[0]
        return kraj, vyber
    except IndexError:
        raise ValueError("URL neobsahuje požadované parametry 'xkraj' a 'xnumnuts'.")


def extract_obce(soup):
    volebni_tabulka = soup.find('table', {'class': 'table'})
    if not volebni_tabulka:
        raise ValueError("Nepodařilo se najít volební tabulku.")

    obce = []
    rows = volebni_tabulka.find_all('tr')
    for row in rows:
        cells = row.find_all('td')
        if len(cells) > 0:
            obec_id = cells[0].get_text(strip=True)
            obec_nazev = cells[1].get_text(strip=True)
            obce.append([obec_id, obec_nazev])
    return obce


def scrap_data_for_obec(obec_id, obec_nazev, kraj, vyber):
    url = f'https://www.volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj={kraj}&xobec={obec_id}&xvyber={vyber}'
    soup = fetch_url_content(url)

    volebni_tabulka = soup.find_all('table')[0]
    if not volebni_tabulka:
        return []

    rows = volebni_tabulka.find_all('tr')
    data_row = rows[2].find_all('td')

    volici_v_seznamu = data_row[3].get_text(strip=True).replace('\xa0', '')
    vydane_obalky = data_row[4].get_text(strip=True).replace('\xa0', '')
    platne_hlasy = data_row[7].get_text(strip=True).replace('\xa0', '')

    strana_hlasy = {}
    for table_index in range(1, 3):
        tables = soup.find_all('table')
        if len(tables) > table_index:
            current_table = tables[table_index]
            for row in current_table.find_all('tr')[1:]:
                cols = row.find_all('td')
                if len(cols) >= 3:
                    strana_nazev = cols[1].text.strip()
                    platne_hlasy_strany = cols[2].text.strip()
                    strana_hlasy[strana_nazev] = platne_hlasy_strany

    return [obec_id, obec_nazev, volici_v_seznamu, vydane_obalky, platne_hlasy, strana_hlasy]


def collect_vysledky(obce, kraj, vyber):
    vysledky = []
    for obec_id, obec_nazev in obce:
        data = scrap_data_for_obec(obec_id, obec_nazev, kraj, vyber)
        if data:
            vysledky.append(data)
        time.sleep(1)
    return vysledky


def get_unique_party_names(vysledky):
    nazvy_stran = set()
    for result in vysledky:
        strana_hlasy = result[5]
        nazvy_stran.update(strana_hlasy.keys())
    return {strana for strana in nazvy_stran if any(result[5].get(strana) != '0' for result in vysledky)}


def prepare_final_data(vysledky, nazvy_stran):
    final_data = []
    for result in vysledky:
        obec_data = result[:5]
        strana_hlasy = result[5]
        final_row = list(obec_data)
        for strana in nazvy_stran:
            final_row.append(strana_hlasy.get(strana, '0'))
        final_data.append(final_row)
    return final_data


def save_to_csv(final_data, nazvy_stran, output_file):
    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')
        header = ['ID Obce', 'Název Obce', 'Voliči v seznamu', 'Vydané obálky', 'Platné hlasy'] + list(nazvy_stran)
        writer.writerow(header)
        writer.writerows(final_data)
    print(f"Volební data byla úspěšně uložena do {output_file}")


def main(url, output_file):
    try:
        soup = fetch_url_content(url)
        kraj, vyber = extract_kraj_vyber_from_url(url)
        obce = extract_obce(soup)
        vysledky = collect_vysledky(obce, kraj, vyber)
        nazvy_stran = get_unique_party_names(vysledky)
        final_data = prepare_final_data(vysledky, nazvy_stran)
        save_to_csv(final_data, nazvy_stran, output_file)
    except Exception as e:
        print(f"Chyba: {e}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Použití: python_projekt_3.py <url> <výstupní_soubor>")
        sys.exit(1)

    url = sys.argv[1]
    output_file = sys.argv[2]

    main(url, output_file)




