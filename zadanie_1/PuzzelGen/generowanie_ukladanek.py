import os
from collections import deque

def generuj_zbiory_testowe():
    w, k = 4, 4
    # Generujemy układ wzorcowy: (1, 2, 3, ..., 15, 0)
    wzorzec = tuple(list(range(1, w * k)) + [0])
    
    # Kolejka do przeszukiwania BFS: przechowuje (plansza, głębokość)
    kolejka = deque([(wzorzec, 0)])
    odwiedzone = {wzorzec}
    
    # Słownik do liczenia, ile plików wygenerowaliśmy dla danej głębokości
    liczniki = {i: 0 for i in range(1, 8)}
    
    print("Rozpoczynam generowanie 413 plików testowych...")
    
    while kolejka:
        plansza, glebokosc = kolejka.popleft()
        
        # Zapisujemy pliki tylko dla głębokości od 1 do 7 (pomijamy głębokość 0, czyli sam wzorzec)
        if 1 <= glebokosc <= 7:
            liczniki[glebokosc] += 1
            id_pliku = liczniki[glebokosc]
            
            # Formatowanie nazwy pliku, np. 4x4_01_00001.txt
            nazwa_pliku = f"{w}x{k}_{glebokosc:02d}_{id_pliku:05d}.txt"
            
            with open(nazwa_pliku, 'w') as f:
                f.write(f"{w} {k}\n")
                for i in range(w):
                    wiersz = plansza[i*k : (i+1)*k]
                    f.write(" ".join(map(str, wiersz)) + "\n")
                    
        # Jeśli dotarliśmy do głębokości 7, nie szukamy już kolejnych sąsiadów
        if glebokosc == 7:
            continue
            
        # Generowanie wszystkich możliwych ruchów dla pustego pola (0)
        idx_zera = plansza.index(0)
        wiersz_zera, kolumna_zera = idx_zera // k, idx_zera % k
        
        mozliwe_ruchy = []
        if wiersz_zera > 0: mozliwe_ruchy.append(idx_zera - k)     # Ruch w górę
        if wiersz_zera < w - 1: mozliwe_ruchy.append(idx_zera + k) # Ruch w dół
        if kolumna_zera > 0: mozliwe_ruchy.append(idx_zera - 1)    # Ruch w lewo
        if kolumna_zera < k - 1: mozliwe_ruchy.append(idx_zera + 1)# Ruch w prawo
        
        for nowy_idx in mozliwe_ruchy:
            nowa_plansza = list(plansza)
            # Zamiana zera z kafelkiem
            nowa_plansza[idx_zera], nowa_plansza[nowy_idx] = nowa_plansza[nowy_idx], nowa_plansza[idx_zera]
            nowa_plansza_krotka = tuple(nowa_plansza)
            
            if nowa_plansza_krotka not in odwiedzone:
                odwiedzone.add(nowa_plansza_krotka)
                kolejka.append((nowa_plansza_krotka, glebokosc + 1))
                
    # Podsumowanie procesu
    print("-" * 30)
    print("Zakończono generowanie!")
    suma = 0
    for g, ile in liczniki.items():
        print(f"Głębokość {g}: wygenerowano {ile} układów")
        suma += ile
    print("-" * 30)
    print(f"Suma wygenerowanych plików: {suma} (Zgodnie z zadaniem powinno być 413).")

if __name__ == '__main__':
    generuj_zbiory_testowe()