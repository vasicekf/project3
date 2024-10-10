# project3
Třetí projekt do Engeto Online Python Akademie

**Popis Projektu**  

Tento projekt slouží k extrahování výsledků z parlamentních voleb v roce 2017. Odkaz k prohlédnutí najdete [zde](https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ).

**Instalace knihoven** 

Knihovny, které jsou použity v kódu jsou uložené v souboru [requirements.txt](https://github.com/vasicekf/project3/blob/main/requirements.txt). Po instalaci doporučuji použít nové virtuální prostředí a s nainstalovaný manažerem spustit následovně:

$ pip3 --version                     # kontrola verze manažeru

$ pip3 install -r requierements.txt  # instalace knihovny

**Spuštění projektu** 

Spuštění souboru [python_projekt_3](https://github.com/vasicekf/project3/blob/main/python_projekt_3.py) v rámci příkazového řádku požaduje dva povinné argumenty.

python_projekt_3 <odkaz-uzemniho-celku> <vysledny-soubor>

Následně se vám stáhnou výsledky jako soubour s příponou .csv.

**Ukázka projektu** 

Výsledky hlasování pro okres Uherskjé Hradiště:

1. argument: https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=13&xnumnuts=7202
2. argument: vysledky_uherske_hradiste.csv

**Spuštění programu:**

python python_projekt_3.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=13&xnumnuts=7202" "vysledky_uherske_hradiste.csv"

**Průběh stahování:**

python python_projekt_3.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=13&xnumnuts=7202" "vysledky_uherske_hradiste.csv"

Volební data byla úspěšně uložena do vysledky_uherske_hradiste.csv

**Částečný výstup:**

ID Obce;Název Obce;Voliči v seznamu;Vydané obálky;Platné hlasy;...

592013;Babice;1452;873;866;...

592021;Bánov;1707;1070;1063;...

592030;Bílovice;1473;1018;1008;...

...
