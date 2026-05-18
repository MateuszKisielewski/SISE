import random
import pandas as pd
from data_tools import wczytaj_plik_irysy, zapisz_model, wczytaj_model, wprowadzanie_danych_do_programu
from neural_network import trenuj_siec, testuj_siec
from formulas import oblicz_precyzje, oblicz_czulosc, oblicz_f1_score

def siec_irysy():
    print("Podaj nazwe pliku z danymi wejściowymi (np. irysy.csv): ")
    nazwa_pliku = input("nazwa pliku: ")
    dane_wejsciowe, oczekiwane_wyjscia = wczytaj_plik_irysy(nazwa_pliku)

    indeksy = list(range(len(dane_wejsciowe)))
    random.shuffle(indeksy)

    prog = int(len(dane_wejsciowe) * 0.7)

    indeksy_treningowe = indeksy[:prog]
    indeksy_testowe = indeksy[prog:]

    X_train = [dane_wejsciowe[i] for i in indeksy_treningowe]
    y_train = [oczekiwane_wyjscia[i] for i in indeksy_treningowe]

    X_test = [dane_wejsciowe[i] for i in indeksy_testowe]
    y_test = [oczekiwane_wyjscia[i] for i in indeksy_testowe]

    wagi = None
    biasy = None

    while True:
        print("\nMenu:")
        print("1 - Wczytaj gotowy model i testuj")
        print("2 - Trenuj nowy model i testuj")
        print("3 - Wyjdź z zadania")
        
        wybor = input("wybór: ")
        
        match wybor:
            case "1":
                nazwa_pliku_modelu = input("Podaj nazwę pliku z modelem (np. model_irysy.json): ")
                nazwa_pliku_logu = input("Podaj nazwę pliku do zapisu logu testowego (np. log_testowy_irysy.txt): ")
                wagi, biasy, czy_bias = wczytaj_model(nazwa_pliku_modelu)
                wyniki_testu = testuj_siec(X_test, y_test, wagi, biasy, czy_bias, nazwa_pliku_logu)
                
                macierz_pomylek = []
                for i in range(3):
                    macierz_pomylek.append([0, 0, 0])
                nazwy_klas = ["Setosa", "Versicolor", "Virginica"]
                poprawne = 0

                for i in range(len(y_test)):
                    faktyczny_wynik = y_test[i].index(max(y_test[i]))
                    przewidywany_wynik = wyniki_testu[i].index(max(wyniki_testu[i]))
                    
                    macierz_pomylek[faktyczny_wynik][przewidywany_wynik] += 1
                    
                    if przewidywany_wynik == faktyczny_wynik:
                        poprawne += 1

                dokladnosc = (poprawne / len(y_test)) * 100
                print(f"\nPoprawnie sklasyfikowano {poprawne} z {len(y_test)} irysów")
                print(f"Dokładność: {dokladnosc:.2f}%")
                
                print("\nSkuteczność w rozbiciu na klasy")
                for gatunek in range(3):
                    prawdziwie_pozytywne = macierz_pomylek[gatunek][gatunek]
                    
                    falszywie_pozytywne = 0
                    for wiersz in range(3):
                        if wiersz != gatunek:
                            falszywie_pozytywne += macierz_pomylek[wiersz][gatunek]
                            
                    falszywie_negatywne = 0
                    for kolumna in range(3):
                        if kolumna != gatunek:
                            falszywie_negatywne += macierz_pomylek[gatunek][kolumna]

                    precyzja = oblicz_precyzje(prawdziwie_pozytywne, falszywie_pozytywne)
                    czulosc = oblicz_czulosc(prawdziwie_pozytywne, falszywie_negatywne)
                    f1 = oblicz_f1_score(precyzja, czulosc)

                    print(f"Klasa {nazwy_klas[gatunek]}: Prawdziwie Pozytywne = {prawdziwie_pozytywne}, Precyzja = {precyzja:.2f}, Czułość = {czulosc:.2f}, F1 = {f1:.2f}")

                print("\nMacierz pomyłek")
                df_macierz = pd.DataFrame(macierz_pomylek, index=nazwy_klas, columns=nazwy_klas)
                df_macierz.insert(0, 'Faktyczna klasa', nazwy_klas)
                print(df_macierz.to_string(index=False))
                
            case "2":
                rozmiary_warstw, epoki, docelowy_blad, wspolczynnik_nauki, momentum, czy_bias, losowa_kolejnosc, co_ile_zapis_log, nazwa_pliku_logu, nazwa_pliku_modelu = wprowadzanie_danych_do_programu()
                if losowa_kolejnosc:
                    random.shuffle(indeksy)
                
                wagi, biasy, epoka_koncowa, glob_mse = trenuj_siec(rozmiary_warstw, X_train, y_train, epoki, docelowy_blad, wspolczynnik_nauki, momentum, czy_bias, losowa_kolejnosc, co_ile_zapis_log, nazwa_pliku_logu)
                
                zapisz_model(nazwa_pliku_modelu, czy_bias, wagi, biasy)
                wyniki_testu = testuj_siec(X_test, y_test, wagi, biasy, czy_bias, nazwa_pliku_logu)
                
                macierz_pomylek = []
                for i in range(3):
                    macierz_pomylek.append([0, 0, 0])
                nazwy_klas = ["Setosa", "Versicolor", "Virginica"]
                poprawne = 0

                for i in range(len(y_test)):
                    faktyczny_wynik = y_test[i].index(max(y_test[i]))
                    przewidywany_wynik = wyniki_testu[i].index(max(wyniki_testu[i]))
                    
                    macierz_pomylek[faktyczny_wynik][przewidywany_wynik] += 1
                    
                    if przewidywany_wynik == faktyczny_wynik:
                        poprawne += 1

                dokladnosc = (poprawne / len(y_test)) * 100
                print(f"\nPoprawnie sklasyfikowano {poprawne} z {len(y_test)} irysów.")
                print(f"Dokładność: {dokladnosc:.2f}%")
                
                print("\nSkuteczność w rozbiciu na klasy")
                for gatunek in range(3):
                    prawdziwie_pozytywne = macierz_pomylek[gatunek][gatunek]
                    
                    falszywie_pozytywne = 0
                    for wiersz in range(3):
                        if wiersz != gatunek:
                            falszywie_pozytywne += macierz_pomylek[wiersz][gatunek]
                            
                    falszywie_negatywne = 0
                    for kolumna in range(3):
                        if kolumna != gatunek:
                            falszywie_negatywne += macierz_pomylek[gatunek][kolumna]

                    precyzja = oblicz_precyzje(prawdziwie_pozytywne, falszywie_pozytywne)
                    czulosc = oblicz_czulosc(prawdziwie_pozytywne, falszywie_negatywne)
                    f1 = oblicz_f1_score(precyzja, czulosc)

                    print(f"Klasa {nazwy_klas[gatunek]}: Prawdziwie Pozytywne = {prawdziwie_pozytywne}, Precyzja = {precyzja:.2f}, Czułość = {czulosc:.2f}, F1 = {f1:.2f}")

                print("\nMacierz pomyłek")
                df_macierz = pd.DataFrame(macierz_pomylek, index=nazwy_klas, columns=nazwy_klas)
                df_macierz.insert(0, 'Faktyczna klasa', nazwy_klas)
                print(df_macierz.to_string(index=False))
            
            case "3":
                break
                
            case _:
                print("Wybrałeś niepoprawną opcję")