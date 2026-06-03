import pandas as pd
import joblib
import os

def przewiduj_wynik(plik_drzewa, statystyki_meczowe):

    model = joblib.load(plik_drzewa)

    cechy = ['Gole_Polowa_Dom', 'Gole_Polowa_Gosc', 'Strzaly_Dom', 'Strzaly_Gosc', 'Celne_Dom', 'Celne_Gosc', 'Faule_Dom', 'Faule_Gosc', 'Rozne_Dom', 'Rozne_Gosc', 'Zolte_Dom', 'Zolte_Gosc', 'Czerwone_Dom', 'Czerwone_Gosc']
    
    df_wejscie = pd.DataFrame([statystyki_meczowe], columns=cechy)

    wynik_surowy = model.predict(df_wejscie)[0]
    slownik_wynikow = {'H': 'WYGRANA GOSPODARZY', 'D': 'REMIS', 'A': 'WYGRANA GOŚCI'}
    czytelny_wynik = slownik_wynikow.get(wynik_surowy, "Nieznany")

    sciezka_wezlow = model.decision_path(df_wejscie)
    indeksy_wezlow = sciezka_wezlow.indices
    
    print("Drzewo sprawdziło następujące reguły:")
    
    for i, wezel in enumerate(indeksy_wezlow):
        if model.tree_.children_left[wezel] == model.tree_.children_right[wezel]:
            print(f" -> KROK {i+1}: Koniec ścieżki - jest wynik")
            break
            
        cecha = cechy[model.tree_.feature[wezel]]
        prog = model.tree_.threshold[wezel]
        podana_wartosc = df_wejscie.iloc[0][cecha]
        
        if podana_wartosc <= prog:
            znak = "<="
        else:
            znak = ">"
        print(f" -> KROK {i+1}: Zbadano '{cecha}'. Twoja wartość ({podana_wartosc}) jest {znak} od progu ({prog:.2f})")

    print(f" OSTATECZNY WYNIK: *** {czytelny_wynik} ***")