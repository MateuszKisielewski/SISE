import random

from data_tools import zapisz_historie_nauki, zapisz_log_testowy
from formulas import propagacja_w_przod, blad_pojedynczego_wzorca, propagacja_wsteczna, blad_globalny_mse


def inicjalizuj_siec(rozmiary_warstw, czy_bias):
    wagi = []
    biasy = []
    poprzednie_zmiany_wag =[]
    poprzednie_zmiany_biasow=[]

    for i in range(len(rozmiary_warstw) - 1):
        liczba_wejsc_do_neuronu = rozmiary_warstw[i]
        liczba_neuronow_w_warstwie = rozmiary_warstw[i + 1]

        wagi_warstwy = []
        biasy_warstwy = []
        zmiany_wag_warstwy = []
        zmiany_biasow_warstwy = []

        for j in range(liczba_neuronow_w_warstwie):
            wagi_neuronu = []
            zmiany_wag_neuronu = []

            for k in range(liczba_wejsc_do_neuronu):
                wylosowana_waga = random.uniform(-1.0,1.0)
                wagi_neuronu.append(wylosowana_waga)
                zmiany_wag_neuronu.append(0.0)

            wagi_warstwy.append(wagi_neuronu)
            zmiany_wag_warstwy.append(zmiany_wag_neuronu)

            if czy_bias:
                biasy_warstwy.append(random.uniform(-1.0, 1.0))
            else:
                biasy_warstwy.append(0.0)

            zmiany_biasow_warstwy.append(0.0)

        wagi.append(wagi_warstwy)
        biasy.append(biasy_warstwy)
        poprzednie_zmiany_wag.append(zmiany_wag_warstwy)
        poprzednie_zmiany_biasow.append(zmiany_biasow_warstwy)

    return wagi, biasy, poprzednie_zmiany_wag, poprzednie_zmiany_biasow

def trenuj_siec(rozmiary_warstw, dane_wejsciowe, oczekiwane_wyjscia, epoki, docelowy_blad, wspolczynnik_nauki, momentum, czy_bias, losowa_kolejnosc, co_ile_zapis_log, nazwa_pliku_logu):

    if rozmiary_warstw[-1] != len(oczekiwane_wyjscia[0]):
        print("Błąd: Liczba neuronów wyjściowych nie zgadza się z rozmiarem wektora odpowiedzi. Ponownie uruchom program i podaj poprawne dane")
        return

    wagi, biasy, poprzednie_zmiany_wag, poprzednie_zmiany_biasow = inicjalizuj_siec(rozmiary_warstw, czy_bias)
    historia_bledow = []

    for epoka in range(1, epoki + 1):
        indeksy = list(range(len(dane_wejsciowe)))

        if losowa_kolejnosc:
            random.shuffle(indeksy)

        bledy_wzorcow_w_epoce = []

        for i in indeksy:
            wejscie = dane_wejsciowe[i]
            oczekiwane_wyjscie = oczekiwane_wyjscia[i]

            aktywacje_wartsw = propagacja_w_przod(wejscie, wagi, biasy, czy_bias)
            otrzymane_wyjscie = aktywacje_wartsw[-1]

            pojedynczy_blad_wzorca = blad_pojedynczego_wzorca(oczekiwane_wyjscie, otrzymane_wyjscie)
            bledy_wzorcow_w_epoce.append(pojedynczy_blad_wzorca)

            wagi, biasy, poprzednie_zmiany_wag, poprzednie_zmiany_biasow = propagacja_wsteczna(wejscie, aktywacje_wartsw, oczekiwane_wyjscie, wagi, biasy, wspolczynnik_nauki, momentum, poprzednie_zmiany_wag, poprzednie_zmiany_biasow, czy_bias)

        globalny_mse = blad_globalny_mse(bledy_wzorcow_w_epoce)

        if epoka == 1 or epoka % co_ile_zapis_log == 0:
            historia_bledow.append([epoka, globalny_mse])

        if globalny_mse <= docelowy_blad:
            if epoka % co_ile_zapis_log != 0 and epoka != 1:
                historia_bledow.append([epoka, globalny_mse])
            break

    zapisz_historie_nauki(nazwa_pliku_logu, historia_bledow)

    return wagi, biasy, epoka, globalny_mse

def testuj_siec(dane_wejsciowe, oczekiwane_wyjscia, wagi, biasy, czy_bias, nazwa_pliku_logu):
    rzeczywiste_wyjscia_sieci = []
    for i in range(len(dane_wejsciowe)):
        wejscie = dane_wejsciowe[i]
        oczekiwane_wyjscie = oczekiwane_wyjscia[i]

        aktywacje = propagacja_w_przod(wejscie, wagi, biasy, czy_bias)
        otrzymane_wyjscie = aktywacje[-1]

        pojedynczy_blad_wzorca = blad_pojedynczego_wzorca(oczekiwane_wyjscie, otrzymane_wyjscie)

        bledy_wyjsciowe = []
        for k in range(len(oczekiwane_wyjscie)):
            bledy_wyjsciowe.append(oczekiwane_wyjscie[k] - otrzymane_wyjscie[k])

        zapisz_log_testowy(nazwa_pliku_logu, str(i + 1), wejscie, oczekiwane_wyjscie, pojedynczy_blad_wzorca, bledy_wyjsciowe, aktywacje, wagi )

        rzeczywiste_wyjscia_sieci.append(otrzymane_wyjscie)

    return rzeczywiste_wyjscia_sieci