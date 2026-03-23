import time
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

        sasiedzi = pobierz_sasiadow(aktualna_plansza, wiersze, kolumny, porzadek_sprawdzania)
        
        for nowa_plansza, ruch in sasiedzi:
            if nowa_plansza == wzor:
                stany_odwiedzone += 1
                return sciezka + ruch, stany_odwiedzone, stany_przetworzone, max_glebokosc
            
            if nowa_plansza not in odwiedzone:
                odwiedzone.add(nowa_plansza)
                stany_odwiedzone += 1
                kolejka.append((nowa_plansza, sciezka + ruch, glebokosc + 1))
                
    return None, stany_odwiedzone, stany_przetworzone, max_glebokosc

def dfs(plansza, wiersze, kolumny, porzadek_sprawdzania):
    wzor = koncowy_efekt_ukladanki(wiersze, kolumny)
    stany_odwiedzone = 1
    stany_przetworzone = 0
    

def astar(plansza, wiersze, kolumny, parametr):
    pass

