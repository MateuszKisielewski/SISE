import sys
import time
from unittest import case

def main():
    if len(sys.argv) != 6:
        print("Użycie: python main.py <strategia> <parametr> <plik_wej> <plik_roz> <plik_stat>")
        sys.exit(1)

strategia = sys.argv[1]
parametr = sys.argv[2]
plik_wejsciowy = sys.argv[3]
plik_rozwiazanie = sys.argv[4]
plik_statystyki = sys.argv[5]

plansza, w, k = wczytaj_plansze(plik_wejsciowy)

start_czas = time.perf_counter()

match strategia:
        case 'bfs':
            wynik = bfs(plansza, w, k, parametr)
        case 'dfs':
            wynik = dfs(plansza, w, k, parametr)
        case 'astr':
            wynik = astar(plansza, w, k, parametr)
        case _:
            print("Nieznana strategia!")
            sys.exit(1)


koniec_czas = time.perf_counter()
czas_obliczen = (koniec_czas - start_czas) * 1000 #milisekundy i chuj

sciezka, stany_odwiedzone, stany_przetworzone, max_glebokosc = wynik
zapisz_wyniki(plik_rozwiazanie, plik_statystyki, sciezka, stany_odwiedzone, stany_przetworzone, max_glebokosc, czas_obliczen)

main()