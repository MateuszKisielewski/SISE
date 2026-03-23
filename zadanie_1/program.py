import sys
import time

from manager import wczytaj_tekst_z_pliku, zbuduj_plansze_z_tekstu,zapisz_wyniki
from algorithms import bfs, dfs, astar

def main():
    if len(sys.argv) != 6:
        print("Użycie: python main.py <strategia> <parametr> <plik_wej> <plik_roz> <plik_stat>")
        sys.exit(1)

strategia = sys.argv[1]
parametr = sys.argv[2]
plik_wejsciowy = sys.argv[3]
plik_rozwiazanie = sys.argv[4]
plik_statystyki = sys.argv[5]

tekst = wczytaj_tekst_z_pliku(plik_wejsciowy)
plansza, wiersze, kolumny = zbuduj_plansze_z_tekstu(tekst)

poczatek_czas = time.perf_counter()

match strategia:
        case 'bfs':
            wynik = bfs(plansza, wiersze, kolumny, parametr)
        case 'dfs':
            wynik = dfs(plansza, wiersze, kolumny, parametr)
        case 'astr':
            wynik = astar(plansza, wiersze, kolumny, parametr)
        case _:
            print("Nieznana strategia. Dostępne: bfs, dfs, astr")
            sys.exit(1)


koniec_czas = time.perf_counter()
czas_obliczen = (koniec_czas - poczatek_czas) * 1000

sciezka, stany_odwiedzone, stany_przetworzone, max_glebokosc = wynik
zapisz_wyniki(plik_rozwiazanie, plik_statystyki, sciezka, stany_odwiedzone, stany_przetworzone, max_glebokosc, czas_obliczen)

main()