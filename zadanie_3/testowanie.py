import pandas as pd
import joblib
import warnings

warnings.filterwarnings("ignore")

def przewiduj_wynik(plik_drzewa, statystyki_meczowe):

    model = joblib.load(plik_drzewa)

    cechy = ['Gole_Polowa_Dom', 'Gole_Polowa_Gosc', 'Strzaly_Dom', 'Strzaly_Gosc', 'Celne_Dom', 'Celne_Gosc', 'Faule_Dom', 'Faule_Gosc', 'Rozne_Dom', 'Rozne_Gosc', 'Zolte_Dom', 'Zolte_Gosc', 'Czerwone_Dom', 'Czerwone_Gosc']
    
    df_wejscie = pd.DataFrame([statystyki_meczowe], columns=cechy)

    wynik_surowy = model.predict(df_wejscie)[0]
    slownik_wynikow = {'H': 'WYGRANA GOSPODARZY', 'D': 'REMIS', 'A': 'WYGRANA GOŚCI'}
    czytelny_wynik = slownik_wynikow.get(wynik_surowy)

    prawdopodobienstwa = model.predict_proba(df_wejscie)[0]
    klasy = model.classes_
    
    for klasa, prawdopodobienstwo in zip(klasy, prawdopodobienstwa):
        nazwa = slownik_wynikow.get(klasa)
        procent = prawdopodobienstwo * 100
        print(f"{nazwa}: {procent:.1f}% głosów")

    print(f"Wynik: {czytelny_wynik}")