import random

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

def trenuj_siec():

def testuj_siec():