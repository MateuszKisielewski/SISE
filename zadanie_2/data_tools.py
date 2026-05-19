import json
import pandas as pd

def zapisz_model(nazwa_pliku, czy_bias, wagi, biasy):
    model = {
        "czy_bias": czy_bias,
        "wagi": wagi,
        "biasy": biasy
    }
    with open(nazwa_pliku, 'w') as f:
        json.dump(model, f, indent=4)
    print(f"Zapisano model do pliku: '{nazwa_pliku}'")

def wczytaj_model(nazwa_pliku):
    with open(nazwa_pliku, 'r') as f:
        model = json.load(f)
    return model["czy_bias"], model["wagi"], model["biasy"]

def zapisz_historie_nauki(nazwa_pliku, historia_bledow):
    with open(nazwa_pliku, 'w') as f:
        f.write("Epoka , blad_glowny \n")
        for log in historia_bledow:
            f.write(f"{log[0]} , {log[1]}\n")
    print(f"Zapisano historię błędu do pliku: '{nazwa_pliku}'")

def zapisz_log_testowy(nazwa_pliku, log, wzorzec_we, oczekiwane_wy, blad_wzorca, bledy_wyjsciowe, wartosci_wyjsciowe_warstw, wagi):
    if nazwa_pliku is None:
        return

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