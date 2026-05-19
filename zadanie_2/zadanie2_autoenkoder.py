from formulas import propagacja_w_przod
from neural_network import trenuj_siec, testuj_siec
from data_tools import zapisz_model, wczytaj_model, wczytaj_plik_autoenkoder, wprowadzanie_danych_do_programu

def siec_autoenkoder():
    print("Podaj nazwe pliku z danymi wejściowymi (np. autoenkoder.csv): ")
    nazwa_pliku = input("nazwa pliku: ")
    dane_wejsciowe, oczekiwane_wyjsciowe = wczytaj_plik_autoenkoder(nazwa_pliku)
    pomin_petle = False
    
    wagi = None
    biasy = None
    czy_bias = None
    rozmiary_warstw, epoki, docelowy_blad, wspolczynnik_nauki, momentum, czy_bias_input = None, None, None, None, None, None
    losowa_kolejnosc, co_ile_zapis_log, nazwa_pliku_logu, nazwa_pliku_modelu = None, None, "domyslny_log.txt", "domyslny_model.json"

    czy_wczytywanie_sieci_z_pliku = input("Czy chcesz wczytać sieć z pliku? (tak/nie): ").lower()

    if czy_wczytywanie_sieci_z_pliku == "tak":
        nazwa_pliku_modelu = input("Podaj nazwę pliku z modelem: ")
        wagi, biasy, czy_bias = wczytaj_model(nazwa_pliku_modelu)
    elif czy_wczytywanie_sieci_z_pliku == "nie":
        rozmiary_warstw, epoki, docelowy_blad, wspolczynnik_nauki, momentum, czy_bias_input, losowa_kolejnosc, co_ile_zapis_log, nazwa_pliku_logu, nazwa_pliku_modelu = wprowadzanie_danych_do_programu()
    else:
        print("Wybrałeś niepoprawną opcję. Wyjście z zadania")
        pomin_petle = True

    if not pomin_petle:
        while True:
            print("\nMenu:")
            print("1 - Uczenie z biasem (parametry podane z klawiatury)")
            print("2 - Uczenie bez biasu (parametry podane z klawiatury)")
            print("3 - Uczenie z różnymi kombinacjami z polecenia (tylko z biasem)")
            print("4 - Przetestuj aktualny model (wczytany lub wytrenowany)")
            print("5 - Zmień nazwę pliku modelu i pliku logu")
            print("6 - Wyjdź z zadania")

            wybor = input("wybór: ")

            match wybor:
                case "1":
                    if rozmiary_warstw is None:
                        print("\nBłąd: Brak parametrów treningowych. Zrestartuj tryb i wybierz 'nie' przy wczytywaniu modelu z pliku, aby je podać.")
                        continue
                        
                    print("\nUczenie z biasem:")
                    wagi, biasy, epoka, globalny_mse = trenuj_siec(rozmiary_warstw, dane_wejsciowe, oczekiwane_wyjsciowe, epoki, docelowy_blad, wspolczynnik_nauki, momentum, True, losowa_kolejnosc, co_ile_zapis_log, nazwa_pliku_logu)
                    czy_bias = True

                    zapisz_model(nazwa_pliku_modelu, czy_bias, wagi, biasy)
                    print(f"Zapisano nauczoną sieć do pliku '{nazwa_pliku_modelu}'")

                    print(f"Osiągnięto próg docelowego błędu przy epoce: {epoka}, globalny MSE: {globalny_mse:.6f}")
                    rzeczywiste_wyjscie = testuj_siec(dane_wejsciowe, oczekiwane_wyjsciowe, wagi, biasy, czy_bias, nazwa_pliku_logu)

                    print("Stan neuronów wyjściowych po nauce z biasem:")
                    for wejscie in dane_wejsciowe:
                        aktywacje = propagacja_w_przod(wejscie, wagi, biasy, czy_bias)
                        print(f"Wejście: {wejscie} daje wyjście na : [{aktywacje[1][0]:.4f}, {aktywacje[1][1]:.4f}, {aktywacje[1][2]:.4f}, {aktywacje[1][3]:.4f}]")

                    print("Stan neuronów ukrytych po nauce z biasem:")
                    for wejscie in dane_wejsciowe:
                        aktywacje = propagacja_w_przod(wejscie, wagi, biasy, czy_bias)
                        print(f"Wejście: {wejscie} daje wyjście na : [{aktywacje[0][0]:.4f}, {aktywacje[0][1]:.4f}]")

                case "2":
                    if rozmiary_warstw is None:
                        print("\nBłąd: Brak parametrów treningowych. Zrestartuj tryb i wybierz 'nie' przy wczytywaniu modelu z pliku, aby je podać.")
                        continue
                        
                    print("\nUczenie bez biasu: \n")
                    wagi, biasy, epoka, globalny_mse = trenuj_siec(rozmiary_warstw, dane_wejsciowe, oczekiwane_wyjsciowe, epoki, docelowy_blad, wspolczynnik_nauki, momentum, False, losowa_kolejnosc, co_ile_zapis_log, nazwa_pliku_logu)
                    czy_bias = False

                    zapisz_model(nazwa_pliku_modelu, czy_bias, wagi, biasy)
                    print(f"Zapisano nauczoną sieć do pliku '{nazwa_pliku_modelu}'")

                    print(f"Osiągnięto próg docelowego błędu przy epoce: {epoka}, globalny MSE: {globalny_mse:.6f}")
                    rzeczywiste_wyjscie = testuj_siec(dane_wejsciowe, oczekiwane_wyjsciowe, wagi, biasy, czy_bias, nazwa_pliku_logu)

                    print("Stan neuronów wyjściowych po nauce bez biasu:")
                    for wejscie in dane_wejsciowe:
                        aktywacje = propagacja_w_przod(wejscie, wagi, biasy, czy_bias)
                        print(f"Wejście: {wejscie} daje wyjście na : [{aktywacje[1][0]:.4f}, {aktywacje[1][1]:.4f}, {aktywacje[1][2]:.4f}, {aktywacje[1][3]:.4f}]")

                    print("Stan neuronów ukrytych po nauce bez biasu:")
                    for wejscie in dane_wejsciowe:
                        aktywacje = propagacja_w_przod(wejscie, wagi, biasy, czy_bias)
                        print(f"Wejście: {wejscie} daje wyjście na : [{aktywacje[0][0]:.4f}, {aktywacje[0][1]:.4f}]")

                case "3":
                    if rozmiary_warstw is None:
                        print("\nBłąd: Brak parametrów treningowych. Zrestartuj tryb i wybierz 'nie' przy wczytywaniu modelu z pliku, aby je podać.")
                        continue
                        
                    kombinacje = [(0.9, 0.0), (0.6, 0.0), (0.2, 0.0), (0.9, 0.6), (0.2, 0.9)]

                    for wsp_nauk, momentum_kombinacji in kombinacje:
                        print(f"\nTest kombinacji: Współczynnik nauki = {wsp_nauk}, Momentum = {momentum_kombinacji}")
                        wagi_temp, biasy_temp, epoka, globalny_mse = trenuj_siec(rozmiary_warstw, dane_wejsciowe, oczekiwane_wyjsciowe, epoki, docelowy_blad, wsp_nauk, momentum_kombinacji, czy_bias_input, losowa_kolejnosc, co_ile_zapis_log, f"autoenkoder_wsp_nauk{wsp_nauk}_momentum{momentum_kombinacji}.txt")
                        rzeczywiste_wyjscie = testuj_siec(dane_wejsciowe, oczekiwane_wyjsciowe, wagi, biasy, czy_bias, f"autoenkoder_wsp_nauk{wsp_nauk}_momentum{momentum_kombinacji}.txt")
                        zapisz_model(f"model_autoenkoder_wsp_nauk{wsp_nauk}_momentum{momentum_kombinacji}.json", czy_bias_input, wagi_temp, biasy_temp)
                        print(f"Osiągnięto próg docelowego błędu przy epoce: {epoka}")

                case "4":
                    if wagi is None:
                        print("\nBłąd: Najpierw wytrenuj sieć (opcja 1, 2 lub 3) albo wczytaj z pliku podczas startu")

                    else:
                        rzeczywiste_wyjscie = testuj_siec(dane_wejsciowe, oczekiwane_wyjsciowe, wagi, biasy, czy_bias, nazwa_pliku_logu)

                        print("\nStan neuronów wyjściowych aktualnego modelu:")
                        for wejscie in dane_wejsciowe:
                            aktywacje = propagacja_w_przod(wejscie, wagi, biasy, czy_bias)
                            print(f"Wejście: {wejscie} daje wyjście na : [{aktywacje[1][0]:.4f}, {aktywacje[1][1]:.4f}, {aktywacje[1][2]:.4f}, {aktywacje[1][3]:.4f}]")

                        print("Stan neuronów ukrytych aktualnego modelu:")
                        for wejscie in dane_wejsciowe:
                            aktywacje = propagacja_w_przod(wejscie, wagi, biasy, czy_bias)
                            print(f"Wejście: {wejscie} daje wyjście na : [{aktywacje[0][0]:.4f}, {aktywacje[0][1]:.4f}]")

                case "5":
                    nazwa_pliku_modelu = input("Podaj nową nazwę pliku modelu: ")
                    wczytaj_model(nazwa_pliku_modelu)
                    nazwa_pliku_logu = input("Podaj nową nazwę pliku logu: ")
                    print(f"Zmieniono nazwę pliku modelu na '{nazwa_pliku_modelu}' i pliku logu na '{nazwa_pliku_logu}'")
                
                case "6":
                    break

                case _:
                    print("Wybrałeś niepoprawną opcję")