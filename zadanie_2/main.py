import sys
import random
import pandas as pd
from data_tools import zapisz_model, wczytaj_model
from neural_network import trenuj_siec, testuj_siec
from formulas import propagacja_w_przod, oblicz_precyzje, oblicz_czulosc, oblicz_f1_score
from charts import rysuj_wykres_mse

def wczytaj_dane_uniwersalne(plik_csv, n_wejsc, n_wyjsc):
    dane = pd.read_csv(plik_csv, header=None)
    
    wycinek_x = dane.iloc[:, 0:n_wejsc]
    x = wycinek_x.values.tolist()
    
    kolumna_decyzyjna = dane.iloc[:, n_wejsc]
    pierwsza_wartosc = kolumna_decyzyjna.values[0]
    
    if isinstance(pierwsza_wartosc, str):
        lista_etykiet = kolumna_decyzyjna.values.tolist()
        zbiór_unikalny = set(lista_etykiet)
        unikalne_klasy = sorted(list(zbiór_unikalny))
        
        mapowanie = {}
        indeks_klasy = 0
        for klasa in unikalne_klasy:
            wektor = [0] * n_wyjsc
            
            if indeks_klasy < n_wyjsc:
                wektor[indeks_klasy] = 1
                
            mapowanie[klasa] = wektor
            indeks_klasy = indeks_klasy + 1
            
        y = []
        for klasa in lista_etykiet:
            odpowiedni_wektor = mapowanie[klasa]
            y.append(odpowiedni_wektor)
            
        nazwy_klas = unikalne_klasy
        
    else:
        indeks_koncowy = n_wejsc + n_wyjsc
        wycinek_y = dane.iloc[:, n_wejsc:indeks_koncowy]
        y = wycinek_y.values.tolist()
        
        nazwy_klas = []
        for i in range(n_wyjsc):
            nazwa = f"Wyjscie_{i}"
            nazwy_klas.append(nazwa)
            
    return x, y, nazwy_klas

def oblicz_macierz_pomylek(oczekiwane_wyjscia, rzeczywiste_wyjscia, liczba_klas):
    macierz = []

    for wiersz in range(liczba_klas):
        pusty_wiersz = []
        for kolumna in range(liczba_klas):
            pusty_wiersz.append(0)
        macierz.append(pusty_wiersz)

    poprawne_trafienia = 0

    for i in range(len(oczekiwane_wyjscia)):
        
        wektor_oczekiwany = oczekiwane_wyjscia[i]
        wektor_rzeczywisty = rzeczywiste_wyjscia[i]

        najwieksza_wartosc_oczekiwana = max(wektor_oczekiwany)
        indeks_oczekiwany = wektor_oczekiwany.index(najwieksza_wartosc_oczekiwana)

        najwieksza_wartosc_rzeczywista = max(wektor_rzeczywisty)
        indeks_rzeczywisty = wektor_rzeczywisty.index(najwieksza_wartosc_rzeczywista)

        macierz[indeks_oczekiwany][indeks_rzeczywisty] += 1

        if indeks_oczekiwany == indeks_rzeczywisty:
            poprawne_trafienia += 1

    return macierz, poprawne_trafienia

def wypisz_metryki_dokladnosci(macierz, nazwy_klas, liczba_klas, poprawne_trafienia, liczba_wszystkich_probek):
    skutecznosc = (poprawne_trafienia / liczba_wszystkich_probek) * 100
    print(f"Ogólna skuteczność: {skutecznosc:.2f}%\n")

    for indeks_klasy in range(liczba_klas):
        nazwa_obecnej_klasy = nazwy_klas[indeks_klasy]
        prawdziwie_pozytywne = macierz[indeks_klasy][indeks_klasy]
    
        falszywie_pozytywne = 0
        for wiersz in range(liczba_klas):
            if wiersz != indeks_klasy:
                falszywie_pozytywne += macierz[wiersz][indeks_klasy]
                
        falszywie_negatywne = 0
        for kolumna in range(liczba_klas):
            if kolumna != indeks_klasy:
                falszywie_negatywne += macierz[indeks_klasy][kolumna]
                
        precyzja = oblicz_precyzje(prawdziwie_pozytywne, falszywie_pozytywne)
        czulosc = oblicz_czulosc(prawdziwie_pozytywne, falszywie_negatywne)
        f1 = oblicz_f1_score(precyzja, czulosc)
        
        print(f"Klasa {nazwa_obecnej_klasy}:")
        print(f"Precyzja: {precyzja:.2f}")
        print(f"Czułość: {czulosc:.2f}")
        print(f"F1 Score: {f1:.2f}\n")

    print("Macierz pomyłek:")
    ramka_macierzy = pd.DataFrame(macierz, index=nazwy_klas, columns=nazwy_klas)
    print(ramka_macierzy)

def tryb_wykres():
    rysuj_wykres_mse(sys.argv[2], sys.argv[3])

def tryb_testuj():
    plik_wejsciowy = sys.argv[2]
    plik_modelu = sys.argv[3]

    if len(sys.argv) >= 5:
        plik_logu = sys.argv[4]
    else:
        plik_logu = None

    czy_bias, wagi, biasy = wczytaj_model(plik_modelu)
    n_wejsc = len(wagi[0][0])
    n_wyjsc = len(wagi[-1])

    x, y, nazwy_klas = wczytaj_dane_uniwersalne(plik_wejsciowy, n_wejsc, n_wyjsc)
    rzeczywiste_wyjscia = testuj_siec(x, y, wagi, biasy, czy_bias, plik_logu)

    dane_z_pliku = pd.read_csv(plik_wejsciowy, header=None)
    kolumna_etykiet = dane_z_pliku.iloc[:, n_wejsc].values

    czy_zawiera_tekst = False
    for wartosc in kolumna_etykiet:
        if isinstance(wartosc, str):
            czy_zawiera_tekst = True
            break
    
    if n_wyjsc > 1 and czy_zawiera_tekst == True:
        macierz, poprawne = oblicz_macierz_pomylek(y, rzeczywiste_wyjscia, n_wyjsc)
        print("Ogólna skuteczność klasyfikacji: ")
        wypisz_metryki_dokladnosci(macierz, nazwy_klas, n_wyjsc, poprawne, len(x))
        
    else:
        liczba_probek = len(x)
        for i in range(liczba_probek):
            
            wyjscie_zaokraglone = []
            for wartosc in rzeczywiste_wyjscia[i]:
                zaokraglona_liczba = round(wartosc, 4)
                wyjscie_zaokraglone.append(zaokraglona_liczba)
                
            print(f"Wejście: {x[i]} daje Wyjście: {wyjscie_zaokraglone} (Oczekiwane: {y[i]})")

def tryb_trenuj():
    komenda = sys.argv[1]
    plik_wejsc = sys.argv[2]
    struktura_str = sys.argv[3]
    epoki = int(sys.argv[4])
    docelowy_blad = float(sys.argv[5])
    wsp_nauki = float(sys.argv[6])
    momentum = float(sys.argv[7])
    czy_bias= bool(int(sys.argv[8]))
    losowa_kol = bool(int(sys.argv[9]))
    co_ile_epok = int(sys.argv[10])
    plik_logu = sys.argv[11]
    plik_modelu = sys.argv[12]

    lista_struktury = struktura_str.split('-')
    rozmiary_warstw = []
    for element in lista_struktury:
        liczba = int(element)
        rozmiary_warstw.append(liczba)

    n_wejsc = rozmiary_warstw[0]
    n_wyjsc = rozmiary_warstw[-1]

    x, y, nazwy_klas = wczytaj_dane_uniwersalne(plik_wejsc, n_wejsc, n_wyjsc)

    x_train = []
    y_train = []
    x_test  = []
    y_test  = []

    if komenda == "trenuj_podzial":
        liczba_wszystkich_probek = len(x)
        
        indeksy = list(range(liczba_wszystkich_probek))
        random.shuffle(indeksy)
        prog_podzialu = int(liczba_wszystkich_probek * 0.7)
        
        for i in range(liczba_wszystkich_probek):
            wylosowany_indeks = indeksy[i]
            
            if i < prog_podzialu:
                x_train.append(x[wylosowany_indeks])
                y_train.append(y[wylosowany_indeks])
            else:
                x_test.append(x[wylosowany_indeks])
                y_test.append(y[wylosowany_indeks])
                
    else:
        x_train = x
        y_train = y
        x_test  = x
        y_test  = y

    wagi, biasy, epoka, blad = trenuj_siec(rozmiary_warstw, x_train, y_train, epoki, docelowy_blad, wsp_nauki, momentum, czy_bias, losowa_kol, co_ile_epok, plik_logu)

    zapisz_model(plik_modelu, czy_bias, wagi, biasy)
    print(f"Koniec na epoce: {epoka}, błąd MSE: {blad:.6f}")

    rzeczywiste_wyjscia = testuj_siec(x_test, y_test, wagi, biasy, czy_bias, plik_logu)

    if komenda == "trenuj_podzial":
        macierz, poprawne = oblicz_macierz_pomylek(y_test, rzeczywiste_wyjscia, n_wyjsc)
        print("\nSkuteczność generalizacji (zbiór testowy):")
        wypisz_metryki_dokladnosci(macierz, nazwy_klas, n_wyjsc, poprawne, len(x_test))
        
    else:
        print("\nStany wyjściowe:")
        for i in range(len(x_test)):
            wyjscie_zaokraglone = []
            for wartosc in rzeczywiste_wyjscia[i]:
                wyjscie_zaokraglone.append(round(wartosc, 4))
                
            print(f"  Wejście: {x_test[i]} daje: Wyjście: {wyjscie_zaokraglone}")

        print("\nStany warstwy ukrytej:")
        for i in range(len(x_test)):
            aktywacje = propagacja_w_przod(x_test[i], wagi, biasy, czy_bias)
            
            ukryta_zaokraglona = []
            for wartosc in aktywacje[0]:
                ukryta_zaokraglona.append(round(wartosc, 4))
                
            print(f"  Wejście: {x_test[i]} daje: Stan ukryty: {ukryta_zaokraglona}")

def main():
    if len(sys.argv) < 2:
        print("Użycie:")
        print("trenuj: python main.py trenuj_pelny|trenuj_podzial <csv> <warstwy> <epoki> <cel_MSE> <wsp_nauki> <momentum> <bias: 0|1> <losowa_kolejnosc: 0|1> <co_ile_epok> <log.txt> <model.json>")
        print("testuj: python main.py testuj <csv> <model.json> <log.txt>")
        print("wykres: python main.py wykres <log.txt> <wykres.png>")
        sys.exit(1)

    komenda = sys.argv[1]

    if komenda == "wykres":
        tryb_wykres()
    elif komenda == "testuj":
        tryb_testuj()
    elif komenda in ("trenuj_pelny", "trenuj_podzial"):
        tryb_trenuj()
    else:
        print(f"Nieznana komenda: '{komenda}'")
        sys.exit(1)


if __name__ == "__main__":
    main()