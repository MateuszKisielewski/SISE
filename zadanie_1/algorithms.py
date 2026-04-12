import heapq
from collections import deque
from manager import koncowy_efekt_ukladanki, pobierz_sasiadow

def bfs(plansza_startowa, wiersze, kolumny, porzadek_sprawdzania):
    wzor = koncowy_efekt_ukladanki(wiersze, kolumny)

    stany_odwiedzone = 1
    stany_przetworzone = 0
    max_glebokosc = 0

    if plansza_startowa == wzor:
        return "", stany_odwiedzone, stany_przetworzone, max_glebokosc

    kolejka = deque([(plansza_startowa, "", 0)])
    odwiedzone = {plansza_startowa}

    while kolejka:
        aktualna_plansza, sciezka, glebokosc = kolejka.popleft()

        stany_przetworzone += 1

        if glebokosc > max_glebokosc:
            max_glebokosc = glebokosc

        if len(sciezka) > 0:
            ostatni_ruch = sciezka[-1]
        else:
            ostatni_ruch = ""

        sasiedzi = pobierz_sasiadow(aktualna_plansza, wiersze, kolumny, porzadek_sprawdzania, ostatni_ruch)

        for nowa_plansza, ruch in sasiedzi:
            if nowa_plansza == wzor:
                stany_odwiedzone += 1
                
                if glebokosc + 1 > max_glebokosc:
                    max_glebokosc = glebokosc + 1
                    
                return sciezka + ruch, stany_odwiedzone, stany_przetworzone, max_glebokosc

            if nowa_plansza not in odwiedzone:
                odwiedzone.add(nowa_plansza)
                stany_odwiedzone += 1
                kolejka.append((nowa_plansza, sciezka + ruch, glebokosc + 1))

    return None, stany_odwiedzone, stany_przetworzone, max_glebokosc

def dfs(plansza_startowa, wiersze, kolumny, porzadek_sprawdzania):
    wzor = koncowy_efekt_ukladanki(wiersze, kolumny)
    stany_odwiedzone = 1
    stany_przetworzone = 0
    max_glebokosc = 0

    MAX_GLEBOKOSC = 20;

    if plansza_startowa == wzor:
        return "", stany_odwiedzone, stany_przetworzone, max_glebokosc

    stos = deque([(plansza_startowa, "", 0)])
    odwiedzone = {plansza_startowa: 0}

    while stos:
        aktualna_plansza, sciezka, glebokosc = stos.pop()

        stany_przetworzone += 1

        if glebokosc > max_glebokosc:
            max_glebokosc = glebokosc

        if glebokosc >= MAX_GLEBOKOSC:
            continue

        if len(sciezka) > 0:
            ostatni_ruch = sciezka[-1]
        else:
            ostatni_ruch = ""

        sasiedzi = pobierz_sasiadow(aktualna_plansza, wiersze, kolumny, porzadek_sprawdzania, ostatni_ruch)

        for nowa_plansza, ruch in reversed(sasiedzi):
            if nowa_plansza == wzor:
                stany_odwiedzone += 1

                if glebokosc + 1 > max_glebokosc:
                    max_glebokosc = glebokosc + 1

                return sciezka + ruch, stany_odwiedzone, stany_przetworzone, max_glebokosc

            nowa_glebokosc = glebokosc + 1
            if nowa_plansza not in odwiedzone or nowa_glebokosc < odwiedzone[nowa_plansza]:
                odwiedzone[nowa_plansza] = nowa_glebokosc
                stany_odwiedzone += 1
                stos.append((nowa_plansza, sciezka + ruch, nowa_glebokosc))

    return None, stany_odwiedzone, stany_przetworzone, max_glebokosc


import heapq
from manager import koncowy_efekt_ukladanki, pobierz_sasiadow

def astar(plansza, wiersze, kolumny, parametr):
    def manhattan(plansza):
        odleglosc = 0
        for i, kafelek in enumerate(plansza):
            if kafelek == 0:
                continue
            cel = kafelek - 1
            wiersz_aktualny = i // kolumny
            kolumna_aktualna = i % kolumny
            wiersz_docelowy = cel // kolumny
            kolumna_docelowa = cel % kolumny
            odleglosc += abs(wiersz_aktualny - wiersz_docelowy) + abs(kolumna_aktualna - kolumna_docelowa)
        return odleglosc
    
    def hamming(plansza):
        odleglosc = 0
        for i, kafelek in enumerate(plansza):
            if kafelek == 0:
                continue
            if kafelek != i + 1:
                odleglosc += 1
        return odleglosc

    wzor = koncowy_efekt_ukladanki(wiersze, kolumny)
    stany_odwiedzone = 1
    stany_przetworzone = 0
    max_glebokosc = 0

    if parametr in ["manhattan", "manh"]:
        heurystyka = manhattan
    elif parametr in ["hamming", "hamm"]:
        heurystyka = hamming

    h = heurystyka(plansza)

    licznik_id = 0
    kolejka = [(h, 0, licznik_id, plansza, "")]
    licznik_id += 1
    
    odwiedzone = {plansza: 0}

    while kolejka:
        f, g, _, aktualna_plansza, sciezka = heapq.heappop(kolejka)
        
        if g > max_glebokosc:
            max_glebokosc = g
        
        if aktualna_plansza == wzor:
            return sciezka, stany_odwiedzone, stany_przetworzone, max_glebokosc

        stany_przetworzone += 1

        if len(sciezka) > 0:
            ostatni_ruch = sciezka[-1]
        else:
            ostatni_ruch = ""

        sasiedzi = pobierz_sasiadow(aktualna_plansza, wiersze, kolumny, "RDUL", ostatni_ruch)

        for nowa_plansza, ruch in sasiedzi:
            nowe_g = g + 1
            
            if nowa_plansza not in odwiedzone or nowe_g < odwiedzone[nowa_plansza]:
                odwiedzone[nowa_plansza] = nowe_g
                stany_odwiedzone += 1
                nowe_f = nowe_g + heurystyka(nowa_plansza)
                
                heapq.heappush(kolejka, (nowe_f, nowe_g, licznik_id, nowa_plansza, sciezka + ruch))
                licznik_id += 1

    return None, stany_odwiedzone, stany_przetworzone, max_glebokosc