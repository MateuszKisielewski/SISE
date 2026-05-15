import json

import pandas as pd

def wczytaj_plik_irysy (plik_csv):
    df = pd.read_csv(plik_csv, header=None, sep=';')
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

def zapisz_model(nazwa_pliku, czy_bias, wagi, biasy):
    stan_sieci = {
        "czy_bias": czy_bias,
        "wagi": wagi,
        "biasy": biasy
    }

    with open(nazwa_pliku, 'w') as plik:
        json.dump(stan_sieci, plik, indent=4)

zapisz_model("chuj1.txt", "true", 2, 1)


def zapisz_historie_nauki(nazwa_pliku, historia_bledow):
    with open(nazwa_pliku, 'w') as plik:
        plik.write("Epoka , blad_glowny \n")

        for dane in historia_bledow:
            epoka = dane[0]
            blad = dane[1]
            plik.write(f"{epoka} , {blad}\n")

historia_bledow = [[1,0.23],[2,0.15]]
zapisz_historie_nauki("chuj2.txt", historia_bledow)


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


nazwa_pliku = "chuj3.txt"
log = "3"
wzorzec_we = [1.0, 0.0]
oczekiwane_wy = [1.0]
blad_wzorca = 0.045
bledy_wyjsciowe = [0.212]

wartosci_wyjsciowe_warstw = [
    [0.65, 0.42, 0.88],
    [0.788]
]

wagi = [
    [ [0.15, -0.22], [0.44, 0.51], [-0.31, 0.85] ],
    [ [0.55, -0.41, 0.92] ]
]

zapisz_log_testowy(nazwa_pliku, log, wzorzec_we, oczekiwane_wy, blad_wzorca, bledy_wyjsciowe, wartosci_wyjsciowe_warstw, wagi)