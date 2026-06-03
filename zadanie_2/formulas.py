import math

def sigmoida(x):
    return 1 / (1 + math.exp(-x))

def propagacja_w_przod(sygnaly_wejsciowe, wagi, biasy, czy_bias):
    aktywacje_wszystkich_warstw = [] 
    aktualne_wejscie = sygnaly_wejsciowe 
    for i in range(len(wagi)):
        wyjscia_tej_warstwy = []
        for j in range(len(wagi[i])):
            suma = 0
            for k in range(len(aktualne_wejscie)):
                suma += aktualne_wejscie[k] * wagi[i][j][k]
            if czy_bias:
                suma += biasy[i][j]
            aktywacja_neuronu = sigmoida(suma)
            wyjscia_tej_warstwy.append(aktywacja_neuronu)
        aktywacje_wszystkich_warstw.append(wyjscia_tej_warstwy)
        aktualne_wejscie = wyjscia_tej_warstwy 
    return aktywacje_wszystkich_warstw

def blad_pojedynczego_wzorca(oczekiwane_wyniki, rzeczywiste_wyniki):
    blad = 0
    for k in range(len(oczekiwane_wyniki)):
        blad += (oczekiwane_wyniki[k] - rzeczywiste_wyniki[k]) ** 2
    blad = 0.5 * blad
    return blad

def blad_globalny_mse(lista_bledow_wzorcow, liczba_neuronow_wyjsciowych):
    suma_wszystkich_bledow = sum(lista_bledow_wzorcow)
    blad_sredniokwadratowy = suma_wszystkich_bledow / (len(lista_bledow_wzorcow) * liczba_neuronow_wyjsciowych)
    return blad_sredniokwadratowy

def oblicz_precyzje(prawdziwie_pozytywne, falszywie_pozytywne):
    if prawdziwie_pozytywne == 0 and falszywie_pozytywne == 0:
        return 0.0
    return prawdziwie_pozytywne / (prawdziwie_pozytywne + falszywie_pozytywne)

def oblicz_czulosc(prawdziwie_pozytywne, falszywie_negatywne):
    if prawdziwie_pozytywne == 0 and falszywie_negatywne == 0:
        return 0.0
    return prawdziwie_pozytywne / (prawdziwie_pozytywne + falszywie_negatywne)

def oblicz_f1_score(precyzja, czulosc):
    if precyzja + czulosc == 0:
        return 0.0
    return 2 * (precyzja * czulosc) / (precyzja + czulosc)
def pochodna_sigmoidy(x):
    return x * (1 - x)

def propagacja_wsteczna(sygnaly_wejsciowe, aktywacje_warstw, oczekiwane_wyjscia, wagi, biasy, wspolczynnik_nauki, momentum, poprzednie_zmiany_wag, poprzednie_zmiany_biasow, czy_bias):
    delty_wyjsciowe = []
    for k in range(len(oczekiwane_wyjscia)):
        delta = (oczekiwane_wyjscia[k] - aktywacje_warstw[-1][k]) * pochodna_sigmoidy(aktywacje_warstw[-1][k])
        delty_wyjsciowe.append(delta)
    delty_wszystkich_warstw = []
    delty_wszystkich_warstw.insert(0, delty_wyjsciowe)
    
    for i in range(len(wagi) - 2, -1, -1):
        delty_tej_warstwy = []
        for j in range(len(wagi[i])):
            suma = 0
            for k in range(len(wagi[i + 1])):
                delta_nastepnej = delty_wszystkich_warstw[0][k]
                waga_polaczenia = wagi[i + 1][k][j]
                suma += delta_nastepnej * waga_polaczenia
            delta_neuronu = suma * pochodna_sigmoidy(aktywacje_warstw[i][j])
            delty_tej_warstwy.append(delta_neuronu)
        delty_wszystkich_warstw.insert(0, delty_tej_warstwy)
    for i in range(len(wagi)):
        if i == 0:
            wejscie_do_warstwy = sygnaly_wejsciowe
        else:
            wejscie_do_warstwy = aktywacje_warstw[i - 1]
        for j in range(len(wagi[i])):
            for k in range(len(wagi[i][j])):
                zmiana_wagi = (wspolczynnik_nauki * delty_wszystkich_warstw[i][j] * wejscie_do_warstwy[k]) + (momentum * poprzednie_zmiany_wag[i][j][k])
                wagi[i][j][k] += zmiana_wagi
                poprzednie_zmiany_wag[i][j][k] = zmiana_wagi
            if czy_bias:
                zmiana_biasu = (wspolczynnik_nauki * delty_wszystkich_warstw[i][j]) + (momentum * poprzednie_zmiany_biasow[i][j])
                biasy[i][j] += zmiana_biasu
                poprzednie_zmiany_biasow[i][j] = zmiana_biasu
    return wagi, biasy, poprzednie_zmiany_wag, poprzednie_zmiany_biasow