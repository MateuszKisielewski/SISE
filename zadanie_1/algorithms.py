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

    MAX_GLEBOKOSC = 7;

    if plansza_startowa == wzor:
        return "", stany_odwiedzone, stany_przetworzone, max_glebokosc

    stos = deque([(plansza_startowa, "", 0)])
    odwiedzone = {plansza_startowa}

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

        for nowa_plansza, ruch in sasiedzi:
            if nowa_plansza == wzor:
                stany_odwiedzone += 1
                return sciezka + ruch, stany_odwiedzone, stany_przetworzone, max_glebokosc

            if nowa_plansza not in odwiedzone:
                odwiedzone.add(nowa_plansza)
                stany_odwiedzone += 1
                stos.append((nowa_plansza, sciezka + ruch, glebokosc + 1))

    return None, stany_odwiedzone, stany_przetworzone, max_glebokosc



def astar(plansza, wiersze, kolumny, parametr):
    def manhattan(plansza):
        odleglosc = 0
        for i, kafelek in enumerate(plansza):
            if kafelek == 0:
                continue
            cel = kafelek - 1
            wiersz_aktualny = i //kolumny
            kolumna_aktualna = i % kolumny
            wiersz_docelowy = cel //kolumny
            kolumna_docelowa = cel % kolumny
            odleglosc += abs(wiersz_aktualny - wiersz_docelowy) + abs(kolumna_aktualna - kolumna_docelowa)
        return odleglosc

    def hamming(plansza):
        odleglosc = 0
        for i, kafelek in enumerate(plansza):
            if kafelek == 0:
                continue
            if kafelek != i+1:
                odleglosc += 1
        return odleglosc

    wzor = koncowy_efekt_ukladanki(wiersze, kolumny)
    stany_odwiedzone = 1
    stany_przetworzone = 0
    max_glebokosc = 0

    if parametr == "manhattan":
        heurystyka = manhattan
    elif parametr == "hamming":
        heurystyka = hamming

    if plansza == wzor:
        return "", stany_odwiedzone, stany_przetworzone, max_glebokosc

    h=heurystyka(plansza)
    kolejka=[(h, 0, plansza, "")]
    odwiedzone = {plansza}

    while kolejka:
        f, g, aktualna_plansza, sciezka = heapq.heappop(kolejka)

        stany_przetworzone += 1

        if g > max_glebokosc:
            max_glebokosc = g

        if len(sciezka) > 0:
            ostatni_ruch = sciezka[-1]
        else:
            ostatni_ruch = ""

        sasiedzi = pobierz_sasiadow(aktualna_plansza, wiersze, kolumny, "LRUD", ostatni_ruch)

        for nowa_plansza, ruch in sasiedzi:
            if nowa_plansza == wzor:
                stany_odwiedzone += 1
                return sciezka + ruch, stany_odwiedzone, stany_przetworzone, max_glebokosc

            if nowa_plansza not in odwiedzone:
                odwiedzone.add(nowa_plansza)
                stany_odwiedzone += 1
                nowe_g = g + 1
                nowe_f = nowe_g + heurystyka(nowa_plansza)
                heapq.heappush(kolejka, (nowe_f, nowe_g, nowa_plansza, sciezka + ruch))

    return None, stany_odwiedzone, stany_przetworzone, max_glebokosc