import random
from data_tools import wczytaj_plik_irysy, zapisz_model, wczytaj_model
from neural_network import trenuj_siec, testuj_siec

def siec_irysy():
    dane_wejsciowe, oczekiwane_wyjscia = wczytaj_plik_irysy("irysy_nazwy.csv")

    indeksy = list(range(len(dane_wejsciowe)))
    random.shuffle(indeksy)

    prog = int(len(dane_wejsciowe) * 0.8)

    indeksy_treningowe = indeksy[:prog]
    indeksy_testowe = indeksy[prog:]

    X_train = [dane_wejsciowe[i] for i in indeksy_treningowe]
    y_train = [oczekiwane_wyjscia[i] for i in indeksy_treningowe]

    X_test = [dane_wejsciowe[i] for i in indeksy_testowe]
    y_test = [oczekiwane_wyjscia[i] for i in indeksy_testowe]

    rozmiary_warstw = [4, 5, 3]
    epoki = 1000
    docelowy_blad = 0.01
    wspolczynnik_nauki = 0.3
    momentum = 0.0
    czy_bias = True
    losowa_kolejnosc = True
    co_ile_zapis_log = 50
    nazwa_pliku_logu = "historia_irysy.txt"
    wagi = None
    biasy = None

    while True:
        print("\nmenu:")
        print("1 - Wczytaj gotowy model i testuj")
        print("2 - Trenuj nowy model i testuj")
        print("3 - Zakończ")
        
        wybor = input("wybór: ")
        
        match wybor:
            case "1":
                nazwa_pliku_modelu = input("Podaj nazwę pliku z modelem (np. model_irysy.json): ")
                wagi, biasy = wczytaj_model(nazwa_pliku_modelu)
                wyniki_testu = testuj_siec(X_test, y_test, wagi, biasy, czy_bias, "log_testowy_irysy.txt")
                
                poprawne = 0
                for i in range(len(y_test)):
                    faktyczny_wynik = y_test[i].index(max(y_test[i]))
                    przewidywany_wynik = wyniki_testu[i].index(max(wyniki_testu[i]))
                    if przewidywany_wynik == faktyczny_wynik:
                        poprawne += 1
                print(f"Poprawnie sklasyfikowano {poprawne} z {len(y_test)} irysów.")
                
            case "2":
                wagi, biasy = trenuj_siec(rozmiary_warstw, X_train, y_train, epoki, docelowy_blad, wspolczynnik_nauki, momentum, czy_bias, losowa_kolejnosc, co_ile_zapis_log, nazwa_pliku_logu)
                zapisz_model("model_irysy.json", czy_bias, wagi, biasy)
                wyniki_testu = testuj_siec(X_test, y_test, wagi, biasy, czy_bias, "log_testowy_irysy.txt")
                
                poprawne = 0
                for i in range(len(y_test)):
                    faktyczny_wynik = y_test[i].index(max(y_test[i]))
                    przewidywany_wynik = wyniki_testu[i].index(max(wyniki_testu[i]))
                    if przewidywany_wynik == faktyczny_wynik:
                        poprawne += 1
                print(f"Poprawnie sklasyfikowano {poprawne} z {len(y_test)} irysów.")
            case "3":
                print("Koniec programu")
                break
                
            case _:
                print("Wybrałeś niepoprawną opcję")
