def wczytaj_tekst_z_pliku(nazwa_pliku):
    with open(nazwa_pliku, 'r') as plik_in:
        return plik_in.readlines()

def zbuduj_plansze_z_tekstu(linie_tekstu):
    liczba_wierszy = int(linie_tekstu[0].split()[0])
    liczba_kolumn = int(linie_tekstu[0].split()[1])

    plansza = []
    for linia in linie_tekstu[1:]:
        for znak in linia.split():
            plansza.append(int(znak))

    return tuple(plansza), liczba_wierszy, liczba_kolumn   

def koncowy_efekt_ukladanki(liczba_wierszy, liczba_kolumn):
    return tuple(list(range(1, liczba_wierszy * liczba_kolumn)) + [0])

def pobierz_sasiadow(plansza, liczba_wierszy, liczba_kolumn, porzadek_sprawdzania, ostatni_ruch):
    sasiedzi = []   
    stara_pozycja_zera = plansza.index(0)
    wiersz = stara_pozycja_zera // liczba_kolumn
    kolumna = stara_pozycja_zera % liczba_kolumn

    ruchy = {
        'L': (kolumna > 0, stara_pozycja_zera - 1),
        'R': (kolumna < liczba_kolumn - 1, stara_pozycja_zera + 1),
        'U': (wiersz > 0, stara_pozycja_zera - liczba_kolumn),
        'D': (wiersz < liczba_wierszy - 1, stara_pozycja_zera + liczba_kolumn)
    }

    przeciwne_ruchy = {'L': 'R', 'R': 'L', 'U': 'D', 'D': 'U'}
    zakazany_ruch = przeciwne_ruchy.get(ostatni_ruch)

    for ruch in porzadek_sprawdzania:
        if ruch == zakazany_ruch:
            continue

        mozliwy, nowa_pozycja_zero = ruchy[ruch]
        if mozliwy:
            nowa_plansza = list(plansza)

            nowa_plansza[stara_pozycja_zera], nowa_plansza[nowa_pozycja_zero] = nowa_plansza[nowa_pozycja_zero], nowa_plansza[stara_pozycja_zera]
            sasiedzi.append((tuple(nowa_plansza), ruch))
            
    return sasiedzi

def zapisz_wyniki(plik_rozwiazanie, plik_statystyki, sciezka, stany_odwiedzone, stany_przetworzone, max_glebokosc, czas_obliczen):
    if sciezka is None:
        dlugosc = -1
    else:
        dlugosc = len(sciezka)

    with open(plik_rozwiazanie, 'w') as plik_out:
        plik_out.write(f"{dlugosc}\n")
        if sciezka is not None:
            plik_out.write(f"{sciezka}")

    with open(plik_statystyki, 'w') as plik_stat:
        plik_stat.write(f"{dlugosc}\n")
        plik_stat.write(f"{stany_odwiedzone}\n")
        plik_stat.write(f"{stany_przetworzone}\n")
        plik_stat.write(f"{max_glebokosc}\n")
        plik_stat.write(f"{czas_obliczen:.3f}\n")