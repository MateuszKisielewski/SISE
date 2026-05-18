import json

import pandas as pd

def wczytaj_plik_irysy (plik_csv):
    df = pd.read_csv(plik_csv, header=None, sep=',')
    dane_wejsciowe = df.iloc[:,0:4].values.tolist()
    etykiety = df.iloc[:,4].values.tolist()

    oczekiwane_dane_wyjsciowe = []
    for etykieta in etykiety:
        if etykieta == "setosa":
            oczekiwane_dane_wyjsciowe.append([1,0,0])
        if etykieta == "versicolor":
            oczekiwane_dane_wyjsciowe.append([0,1,0])
        if etykieta == "virginica":
            oczekiwane_dane_wyjsciowe.append([0,0,1])

    return dane_wejsciowe, oczekiwane_dane_wyjsciowe

def wczytaj_plik_autoenkoder(plik_csv):
    df = pd.read_csv(plik_csv, header=None, sep=',')
    dane_wejsciowe = df.iloc[:,0:4].values.tolist()
    oczekiwane_dane_wyjsciowe = df.iloc[:,4:8].values.tolist()

    return dane_wejsciowe, oczekiwane_dane_wyjsciowe

def zapisz_model(nazwa_pliku, czy_bias, wagi, biasy):
    stan_sieci = {
        "czy_bias": czy_bias,
        "wagi": wagi,
        "biasy": biasy
    }

    with open(nazwa_pliku, 'w') as plik:
        json.dump(stan_sieci, plik, indent=4)


def wczytaj_model(nazwa_pliku):
    with open(nazwa_pliku, 'r') as plik:
        stan_sieci = json.load(plik)

    czy_bias = stan_sieci["czy_bias"]
    wagi = stan_sieci["wagi"]
    biasy = stan_sieci["biasy"]

    return wagi, biasy, czy_bias


def zapisz_historie_nauki(nazwa_pliku, historia_bledow):
    with open(nazwa_pliku, 'w') as plik:
        plik.write("Epoka , blad_glowny \n")

        for dane in historia_bledow:
            epoka = dane[0]
            blad = dane[1]
            plik.write(f"{epoka} , {blad}\n")


def zapisz_log_testowy(nazwa_pliku, log, wzorzec_we, oczekiwane_wy, blad_wzorca, bledy_wyjsciowe, wartosci_wyjsciowe_warstw, wagi):

    with open(nazwa_pliku, 'a') as plik:
        plik.write(f"Log: {log}\n")
        plik.write(f"Wzorzec wejsciowy: {wzorzec_we}\n")
        plik.write(f"Oczekiwana odpowiedz: {oczekiwane_wy}\n")
        plik.write(f"Blad calkowity: {blad_wzorca}\n")
        plik.write(f"Bledy na wyjsciach: {bledy_wyjsciowe}\n\n")

        plik.write(f"Wartosci wyjsciowe: {wartosci_wyjsciowe_warstw[-1]}\n")
        plik.write(f"Wagi: {wagi[-1]}\n\n")

        for i in range(len(wagi) - 2, -1, -1):
            plik.write(f"Warstwa ukryta (nr {i})\n")
            plik.write(f"Wartosci wyjsciowe: {wartosci_wyjsciowe_warstw[i]}\n")
            plik.write(f"Wagi: {wagi[i]}\n\n")

        plik.write("\n")

def wprowadzanie_danych_do_programu ():
    print("Wprowadź dane do programu:")

    print("Podaj liczbę neuronów w wartwie wejściowej (np. 4): ")
    liczba_neuronow_wejsciowych = int(input("Wybór: "))

    print("Podaj liczbę neuronów w warstwie ukrytej (np. 5): ")
    liczba_neuronow_ukrytych = int(input("Wybór: "))

    print("Podaj liczbę neuronów w warstwie wyjściowej (np. 3): ")
    liczba_neuronow_wyjsciowych = int(input("Wybór: "))

    rozmiary_warstw = [liczba_neuronow_wejsciowych, liczba_neuronow_ukrytych, liczba_neuronow_wyjsciowych]

    print("Podaj maksymalną liczbę epok (np. 2000): ")
    epoki = int(input("Wybór: "))

    print("Podaj docelowy błąd (np. 0.01): ")
    docelowy_blad = float(input("Wybór: "))

    print("Podaj współczynnik uczenia (np. 0.3): ")
    wspolczynnik_nauki = float(input("Wybór: "))

    print("Podaj momentum (np. 0.1): ") 
    momentum = float(input("Wybór: "))

    print("Czy używać biasu? (tak/nie): ")
    czy_bias = input("Wybór: ").lower()
    if czy_bias == "tak":
        czy_bias = True 
    if czy_bias == "nie":    
        czy_bias = False

    print("Czy losować kolejność danych podczas nauki? (tak/nie): ")
    losowa_kolejnosc = input("Wybór: ").lower()
    if losowa_kolejnosc == "tak":
        losowa_kolejnosc = True
    if losowa_kolejnosc == "nie":
        losowa_kolejnosc = False

    print("Podaj co ile epok zapisywać logi (np. 50): ")
    co_ile_zapis_log = int(input("Wybór: "))

    print("Podaj nazwę pliku do zapisu historii nauki (np. historia.txt): ")
    nazwa_pliku_logu = input("Wybór: ")

    print("Podaj nazwę pliku do zapisu modelu (np. model.json): ")
    nazwa_pliku_modelu = input("Wybór: ")

    return rozmiary_warstw, epoki, docelowy_blad, wspolczynnik_nauki, momentum, czy_bias, losowa_kolejnosc, co_ile_zapis_log, nazwa_pliku_logu, nazwa_pliku_modelu
