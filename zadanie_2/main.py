import sys
import time
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


# ---------------------------------------------------------------------------
# Wyświetlanie wyników klasyfikacji
# ---------------------------------------------------------------------------

def wyswietl_macierz_i_metryki(y_true, y_pred, nazwy_klas, n_wyjsc):
    macierz = [[0] * n_wyjsc for _ in range(n_wyjsc)]
    poprawne = 0

    for i in range(len(y_true)):
        idx_oczekiwana = y_true[i].index(max(y_true[i]))
        idx_rzeczywista = y_pred[i].index(max(y_pred[i]))
        macierz[idx_oczekiwana][idx_rzeczywista] += 1
        if idx_oczekiwana == idx_rzeczywista:
            poprawne += 1

    return macierz, poprawne


def drukuj_metryki(macierz, nazwy_klas, n_wyjsc, poprawne, n_prob):
    print(f"Skuteczność: {(poprawne / n_prob) * 100:.2f}% ({poprawne}/{n_prob})\n")
    for g in range(n_wyjsc):
        tp = macierz[g][g]
        fp = sum(macierz[w][g] for w in range(n_wyjsc) if w != g)
        fn = sum(macierz[g][k] for k in range(n_wyjsc) if k != g)
        prec = oblicz_precyzje(tp, fp)
        rec  = oblicz_czulosc(tp, fn)
        f1   = oblicz_f1_score(prec, rec)
        print(f"  Klasa {nazwy_klas[g]}: Precyzja = {prec:.2f}, Czułość = {rec:.2f}, F1 = {f1:.2f}")

    print("\nMacierz pomyłek:")
    print(pd.DataFrame(macierz, index=nazwy_klas, columns=nazwy_klas))


# ---------------------------------------------------------------------------
# Tryb: wykres
# ---------------------------------------------------------------------------

def tryb_wykres():
    rysuj_wykres_mse(sys.argv[2], sys.argv[3])


# ---------------------------------------------------------------------------
# Tryb: testuj
# ---------------------------------------------------------------------------

def tryb_testuj():
    plik_wejsciowy = sys.argv[2]
    plik_modelu    = sys.argv[3]
    plik_logu      = sys.argv[4] if len(sys.argv) >= 5 else None

    czy_bias, wagi, biasy = wczytaj_model(plik_modelu)
    n_wejsc = len(wagi[0][0])
    n_wyjsc = len(wagi[-1])

    X, y, nazwy_klas = wczytaj_dane_uniwersalne(plik_wejsciowy, n_wejsc, n_wyjsc)
    rzeczywiste_wyjscia = testuj_siec(X, y, wagi, biasy, czy_bias, plik_logu)

    print("\n--- REZULTATY TESTOWANIA MODELU ---")

    kolumna_etykiet = pd.read_csv(plik_wejsciowy, header=None).iloc[:, n_wejsc].values
    klasyfikacja = n_wyjsc > 1 and any(isinstance(v, str) for v in kolumna_etykiet)

    if klasyfikacja:
        macierz, poprawne = wyswietl_macierz_i_metryki(y, rzeczywiste_wyjscia, nazwy_klas, n_wyjsc)
        print(f"Ogólna skuteczność klasyfikacji: ", end="")
        drukuj_metryki(macierz, nazwy_klas, n_wyjsc, poprawne, len(X))
    else:
        for i in range(len(X)):
            wyjscie = [round(v, 4) for v in rzeczywiste_wyjscia[i]]
            print(f"  Wejście: {X[i]} -> Wyjście: {wyjscie} (Oczekiwane: {y[i]})")

def tryb_trenuj():
    komenda       = sys.argv[1]
    plik_wejsc    = sys.argv[2]
    struktura_str = sys.argv[3]
    epoki         = int(sys.argv[4])
    docelowy_blad = float(sys.argv[5])
    wsp_nauki     = float(sys.argv[6])
    momentum      = float(sys.argv[7])
    czy_bias      = bool(int(sys.argv[8]))
    losowa_kol    = bool(int(sys.argv[9]))
    co_ile_epok   = int(sys.argv[10])
    plik_logu     = sys.argv[11]
    plik_modelu   = sys.argv[12]

    lista_tekstowa = struktura_str.split('-')

    rozmiary_warstw = []
    for element in lista_tekstowa:
        liczba = int(element)
        rozmiary_warstw.append(liczba)

    n_wejsc = rozmiary_warstw[0]
    n_wyjsc = rozmiary_warstw[-1]

    x, y, nazwy_klas = wczytaj_dane_uniwersalne(plik_wejsc, n_wejsc, n_wyjsc)

    if komenda == "trenuj_podzial":
        indeksy = list(range(len(x)))
        random.shuffle(indeksy)
        prog = int(len(x) * 0.7)
        x_train = [x[i] for i in indeksy[:prog]]
        y_train = [y[i] for i in indeksy[:prog]]
        x_test  = [x[i] for i in indeksy[prog:]]
        y_test  = [y[i] for i in indeksy[prog:]]
    else:
        x_train, y_train = x, y
        x_test,  y_test  = x, y

    poczatek = time.perf_counter()
    wagi, biasy, epoka, blad = trenuj_siec(
        rozmiary_warstw, x_train, y_train,
        epoki, docelowy_blad, wsp_nauki, momentum,
        czy_bias, losowa_kol, co_ile_epok, plik_logu
    )
    koniec = time.perf_counter()

    zapisz_model(plik_modelu, czy_bias, wagi, biasy)
    print(f"\nUczenie zakończone w czasie: {koniec - poczatek:.4f} s")
    print(f"Koniec na epoce: {epoka}, błąd MSE: {blad:.6f}")

    print("\n--- TEST PO ZAKOŃCZENIU NAUKI ---")
    rzeczywiste_wyjscia = testuj_siec(x_test, y_test, wagi, biasy, czy_bias, plik_logu)

    if komenda == "trenuj_podzial":
        macierz, poprawne = wyswietl_macierz_i_metryki(y_test, rzeczywiste_wyjscia, nazwy_klas, n_wyjsc)
        print("Skuteczność generalizacji (zbiór testowy):")
        drukuj_metryki(macierz, nazwy_klas, n_wyjsc, poprawne, len(x_test))
    else:
        print("\nStany wyjściowe:")
        for i in range(len(x_test)):
            wyjscie = [round(v, 4) for v in rzeczywiste_wyjscia[i]]
            print(f"  Wejście: {x_test[i]} -> Wyjście: {wyjscie}")

        print("\nStany warstwy ukrytej:")
        for i in range(len(x_test)):
            aktywacje = propagacja_w_przod(x_test[i], wagi, biasy, czy_bias)
            ukryta = [round(v, 4) for v in aktywacje[0]]
            print(f"  Wejście: {x_test[i]} -> Stan ukryty: {ukryta}")

def main():
    if len(sys.argv) < 2:
        print("Użycie:")
        print("trenuj:  python main.py trenuj_pelny|trenuj_podzial <csv> <warstwy> <epoki> <cel_MSE> <wsp_nauki> <momentum> <bias: 0|1> <losowa_kolejnosc: 0|1> <co_ile_epok> <log.txt> <model.json>")
        print("testuj:  python main.py testuj <csv> <model.json> <log.txt>")
        print("wykres:  python main.py wykres <log.txt> <wykres.png>")
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