from zadanie1_irysy import siec_irysy
from zadanie2_autoenkoder import siec_autoenkoder
from charts import rysuj_wykres_mse

def main():
    while(True):
        print("\nWybierz zadanie:")
        print("1 - Klasyfikacja irysów")
        print("2 - Autoenkoder")
        print("3 - Rysuj wykres MSE z logu")
        print("4 - Zakończ")

        wybor = input("\nWybór: ")

        match wybor:
            case "1":
                siec_irysy()
            case "2":
                siec_autoenkoder()
            case "3":
                nazwa_pliku_wejscia = input("Podaj nazwę pliku logu (np. 'log_irysy.txt'): ")
                nazwa_pliku_wyjsciowego = input("Podaj nazwę pliku wyjściowego dla wykresu (np. 'wykres_mse.png'): ")
                rysuj_wykres_mse(nazwa_pliku_wejscia, nazwa_pliku_wyjsciowego)
            case "4":
                print("Koniec programu")
                break
            case _:
                print("Wybrałeś niepoprawną opcję")

if __name__ == "__main__":
    main()