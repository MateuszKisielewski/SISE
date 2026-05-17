from zadanie_2.formulas import propagacja_w_przod
from zadanie_2.neural_network import trenuj_siec


def siec_autoenkoder():
    rozmiary_warstw = [4, 2, 4]

    dane_wejsciowe = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
    oczekiwane_wyjsciowe = dane_wejsciowe

    epoki_max = 1000
    docelowy_blad = 0.01

    while True:
        print("\nmenu:")
        print("1 - Uczenie z biasem (współczynnik uczenia = 0,6)")
        print("2 - Uczenie bez biasu (współczynnik uczenia = 0,6)")
        print("3 - Eksperyment kombinacji")
        print("4 - Zakończ")

        wybor = input("wybór: ")

        match wybor:
            case "1":
                print("\nUczenie z biasem (współczynnik uczenia = 0,6):")

                wagi_z_biasem, biasy_z_biasem, epoka_z_biasem, globalny_mse_z_biasem = trenuj_siec(rozmiary_warstw, dane_wejsciowe, oczekiwane_wyjsciowe, epoki_max, docelowy_blad, 0.6, 0.0, True, True, 10, "autoenkoder_z_biasem.txt")

                print("Stan neuronów wyjściowych po nauce z biasem:")
                for wejscie in dane_wejsciowe:
                    aktywacje = propagacja_w_przod(wejscie, wagi_z_biasem, biasy_z_biasem, czy_bias=True)
                    print(
                        f"Wejście: {wejscie} daje wyjście na : [{aktywacje[1][0]:.4f}, {aktywacje[1][1]:.4f}, {aktywacje[1][2]:.4f}, {aktywacje[1][3]:.4f}]")

                print("Stan neuronów ukrytych po nauce z biasem:")
                for wejscie in dane_wejsciowe:
                    aktywacje = propagacja_w_przod(wejscie, wagi_z_biasem, biasy_z_biasem, czy_bias=True)
                    print(f"Wejście: {wejscie} daje wyjście na : [{aktywacje[0][0]:.4f}, {aktywacje[0][1]:.4f}]")

            case "2":
                print("\nUczenie bez biasu (współczynnik uczenia = 0,6) \n")

                wagi_bez_biasu, biasy_bez_biasu, epoka_bez_biasu, globalny_mse_bez_biasu = trenuj_siec(rozmiary_warstw, dane_wejsciowe, oczekiwane_wyjsciowe, epoki_max, docelowy_blad, 0.6, 0.0, False, True, 100, "autoenkoder_bez_biasu.txt")

                print("Stan neuronów wyjściowych po nauce bez biasu:")
                for wejscie in dane_wejsciowe:
                    aktywacje = propagacja_w_przod(wejscie, wagi_bez_biasu, biasy_bez_biasu, czy_bias=False)
                    print(
                        f"Wejście: {wejscie} daje wyjście na : [{aktywacje[1][0]:.4f}, {aktywacje[1][1]:.4f}, {aktywacje[1][2]:.4f}, {aktywacje[1][3]:.4f}]")

                print("Stan neuronów ukrytych po nauce bez biasu:")
                for wejscie in dane_wejsciowe:
                    aktywacje = propagacja_w_przod(wejscie, wagi_bez_biasu, biasy_bez_biasu, czy_bias=False)
                    print(f"Wejście: {wejscie} daje wyjście na : [{aktywacje[0][0]:.4f}, {aktywacje[0][1]:.4f}]")

            case "3":
                kombinacje = [(0.9, 0.0), (0.6, 0.0), (0.2, 0.0), (0.9, 0.6), (0.2, 0.9)]

                for wsp_nauk, momentum in kombinacje:
                    print(f"\nTest kombinacji: Współczynnik nauki = {wsp_nauk}, Momentum = {momentum}")
                    waga, bias, epoka, globalny_mse = trenuj_siec(rozmiary_warstw, dane_wejsciowe, oczekiwane_wyjsciowe, epoki_max, docelowy_blad, wsp_nauk, momentum, True, True, 100, f"autoenkoder_wsp_nauk{wsp_nauk}_momentum{momentum}.txt")
                    print(f"Osiągnięto próg docelowego błędu przy epoce: {epoka}")

            case "4":
                print("Koniec programu")
                break

            case _:
                print("Wybrałeś niepoprawną opcję")


if __name__ == "__main__":
    siec_autoenkoder()