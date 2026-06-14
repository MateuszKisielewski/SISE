import pandas as pd
import joblib
import warnings
from sklearn.tree import plot_tree
import matplotlib.pyplot as plt

warnings.filterwarnings("ignore")

def przewiduj_wynik(plik_drzewa, plik_wykresu, statystyki_meczowe):

    model = joblib.load(plik_drzewa)

    cechy = ['Gole_Polowa_Dom', 'Gole_Polowa_Gosc', 'Strzaly_Dom', 'Strzaly_Gosc', 'Celne_Dom', 'Celne_Gosc', 'Faule_Dom', 'Faule_Gosc', 'Rozne_Dom', 'Rozne_Gosc', 'Zolte_Dom', 'Zolte_Gosc', 'Czerwone_Dom', 'Czerwone_Gosc']
    
    df_wejscie = pd.DataFrame([statystyki_meczowe], columns=cechy)

    wynik_surowy = model.predict(df_wejscie)[0]
    slownik_wynikow = {'H': 'WYGRANA GOSPODARZY', 'D': 'REMIS', 'A': 'WYGRANA GOŚCI'}
    czytelny_wynik = slownik_wynikow.get(wynik_surowy)

    prawdopodobienstwa = model.predict_proba(df_wejscie)[0]
    
    klasy = list(model.classes_)
    
    for klasa, prawdopodobienstwo in zip(klasy, prawdopodobienstwa):
        nazwa = slownik_wynikow.get(klasa)
        procent = prawdopodobienstwo * 100
        print(f"{nazwa}: {procent:.1f}% głosów")

    print(f"Wynik: {czytelny_wynik}")

    id_zwyciezcy = klasy.index(wynik_surowy)
    wybrane_drzewo = None

    for i, drzewo in enumerate(model.estimators_):
        prawdopodobienstwa_drzewa = drzewo.predict_proba(df_wejscie.values)[0]
        najlepsza_klasa_drzewa = prawdopodobienstwa_drzewa.argmax()
        
        if najlepsza_klasa_drzewa == id_zwyciezcy:
            wybrane_drzewo = drzewo
            break
            
    if wybrane_drzewo is not None:
        sciezka_wezlow = wybrane_drzewo.decision_path(df_wejscie.values)
        indeksy_wezlow = sciezka_wezlow.indices
        
        for i, wezel in enumerate(indeksy_wezlow):
            if wybrane_drzewo.tree_.children_left[wezel] == wybrane_drzewo.tree_.children_right[wezel]:
                break
                
            cecha_id = wybrane_drzewo.tree_.feature[wezel]
            cecha = cechy[cecha_id]
            prog = wybrane_drzewo.tree_.threshold[wezel]
            podana_wartosc = df_wejscie.iloc[0][cecha]
            
            if podana_wartosc <= prog:
                znak = "<="
            else:
                znak = ">"

            print(f"Krok: {i+1}: '{cecha}' ({podana_wartosc}) jest {znak} od progu ({prog:.2f})")
        
        plt.figure(figsize=(40, 20), dpi=300)
        plot_tree(wybrane_drzewo, feature_names=cechy, class_names=model.classes_, filled=True, fontsize=8)
        plt.title(f"Drzewo decyzyjne", fontsize=20)
        plt.savefig(plik_wykresu, bbox_inches='tight')
        plt.close()

def przewiduj_zbior(plik_drzewa, plik_danych_testowych):

    model = joblib.load(plik_drzewa)
    df = pd.read_csv(plik_danych_testowych)

    if 'Wynik' not in df.columns:
        print("Plik testowy musi zawierać kolumnę 'Wynik'")
        return

    y_prawdziwe = df['Wynik']
    x_testowe = df.drop(columns=['Wynik'])

    y_przewidziane = model.predict(x_testowe)

    skutecznosc = accuracy_score(y_prawdziwe, y_przewidziane)
    ilosc_meczow = len(y_prawdziwe)
    poprawne_trafienia = sum(y_prawdziwe == y_przewidziane)

    print(f" Przeanalizowano meczów : {ilosc_meczow}")
    print(f" Poprawnie wytypowane : {poprawne_trafienia}")
    print(f" Błędne wytypowanie : {ilosc_meczow - poprawne_trafienia}")
    print(f" Skuteczność : {skutecznosc * 100:.2f}%")