import json
from formulas import propagacja_w_przod
from neural_network import trenuj_siec
from data_tools import zapisz_model, wczytaj_model, wczytaj_plik_autoenkoder, wprowadzanie_danych_do_programu


def siec_autoenkoder():
    print("Podaj nazwe pliku z danymi wejściowymi (np. dane_autoenkoder.csv): ")
    nazwa_pliku = input("nazwa pliku: ")
    dane_wejsciowe, oczekiwane_wyjsciowe = wczytaj_plik_autoenkoder(nazwa_pliku)
    pomin_petle = False

    czy_wczytywanie_sieci_z_pliku = input("Czy chcesz wczytać sieć z pliku? (tak/nie): ").lower()

    if czy_wczytywanie_sieci_z_pliku == "tak":
        nazwa_pliku = input("Podaj nazwę pliku z modelem: ")
        wagi, biasy, czy_bias = wczytaj_model(nazwa_pliku)
    else:
        if czy_wczytywanie_sieci_z_pliku == "nie":
            rozmiary_warstw, epoki, docelowy_blad, wspolczynnik_nauki, momentum, czy_bias, losowa_kolejnosc, co_ile_zapis_log, nazwa_pliku_logu, nazwa_pliku_modelu = wprowadzanie_danych_do_programu()
        else:
            print("Wybrałeś niepoprawną opcję. Wyjście z zadania")
            pomin_petle = True

    if pomin_petle == False:
        while True:
            print("\nMenu:")
            print("1 - Uczenie z biasem (współczynnik uczenia = 0,6)")
            print("2 - Uczenie bez biasu (współczynnik uczenia = 0,6)")
            print("3 - Uczenie z różnymi kombinacjami")
            print("4 - Wczytaj sieć z pliku i przetestuj")
            print("6 - Wyjdź z zadania")

            wybor = input("wybór: ")

            match wybor:
                case "1":
                    print("\nUczenie z biasem:")

                    wagi, biasy, epoka, globalny_mse = trenuj_siec(rozmiary_warstw, dane_wejsciowe, oczekiwane_wyjsciowe, epoki, docelowy_blad, wspolczynnik_nauki, momentum, True, losowa_kolejnosc, co_ile_zapis_log, nazwa_pliku_logu)

                    zapisz_model(nazwa_pliku_modelu, True, wagi, biasy)
                    print("Zapisano nauczoną sieć do pliku '{nazwa_pliku_modelu}'")

                    print("Stan neuronów wyjściowych po nauce z biasem:")
                    for wejscie in dane_wejsciowe:
                        aktywacje = propagacja_w_przod(wejscie, wagi, biasy, czy_bias=True)
                        print(f"Wejście: {wejscie} daje wyjście na : [{aktywacje[1][0]:.4f}, {aktywacje[1][1]:.4f}, {aktywacje[1][2]:.4f}, {aktywacje[1][3]:.4f}]")

                    print("Stan neuronów ukrytych po nauce z biasem:")
                    for wejscie in dane_wejsciowe:
                        aktywacje = propagacja_w_przod(wejscie, wagi, biasy, czy_bias=True)
                        print(f"Wejście: {wejscie} daje wyjście na : [{aktywacje[0][0]:.4f}, {aktywacje[0][1]:.4f}]")

                case "2":
                    print("\nUczenie bez biasu: \n")

                    wagi, biasy, epoka, globalny_mse = trenuj_siec(rozmiary_warstw, dane_wejsciowe, oczekiwane_wyjsciowe, epoki, docelowy_blad, wspolczynnik_nauki, momentum, False, losowa_kolejnosc, co_ile_zapis_log, nazwa_pliku_logu)

                    zapisz_model(nazwa_pliku_modelu, False, wagi, biasy)
                    print("Zapisano nauczoną sieć do pliku '{nazwa_pliku_modelu}'")

                    print("Stan neuronów wyjściowych po nauce bez biasu:")
                    for wejscie in dane_wejsciowe:
                        aktywacje = propagacja_w_przod(wejscie, wagi, biasy, czy_bias=False)
                        print(f"Wejście: {wejscie} daje wyjście na : [{aktywacje[1][0]:.4f}, {aktywacje[1][1]:.4f}, {aktywacje[1][2]:.4f}, {aktywacje[1][3]:.4f}]")

                    print("Stan neuronów ukrytych po nauce bez biasu:")
                    for wejscie in dane_wejsciowe:
                        aktywacje = propagacja_w_przod(wejscie, wagi, biasy, czy_bias=False)
                        print(f"Wejście: {wejscie} daje wyjście na : [{aktywacje[0][0]:.4f}, {aktywacje[0][1]:.4f}]")

                case "3":
                    kombinacje = [(0.9, 0.0), (0.6, 0.0), (0.2, 0.0), (0.9, 0.6), (0.2, 0.9)]

                    for wsp_nauk, momentum in kombinacje:
                        print(f"\nTest kombinacji: Współczynnik nauki = {wsp_nauk}, Momentum = {momentum}")
                        wagi, biasy, epoka, globalny_mse = trenuj_siec(rozmiary_warstw, dane_wejsciowe, oczekiwane_wyjsciowe, epoki, docelowy_blad, wspolczynnik_nauki, momentum, True, losowa_kolejnosc, co_ile_zapis_log, f"autoenkoder_wsp_nauk{wsp_nauk}_momentum{momentum}.txt")
                        print(f"Osiągnięto próg docelowego błędu przy epoce: {epoka}")

                case "4":

                    for wejscie in dane_wejsciowe:
                        aktywacje = propagacja_w_przod(wejscie, wagi, biasy, czy_bias)
                        print(f"Wejście: {wejscie} daje wyjście na : [{aktywacje[1][0]:.4f}, {aktywacje[1][1]:.4f}, {aktywacje[1][2]:.4f}, {aktywacje[1][3]:.4f}]")

                    print("Stan neuronów ukrytych po nauce wczytanej z pliku:")
                    for wejscie in dane_wejsciowe:
                        aktywacje = propagacja_w_przod(wejscie, wagi, biasy, czy_bias)
                        print(f"Wejście: {wejscie} daje wyjście na : [{aktywacje[0][0]:.4f}, {aktywacje[0][1]:.4f}]")

                case "6":
                    break

                case _:
                    print("Wybrałeś niepoprawną opcję")