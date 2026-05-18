from zadanie1_irysy import siec_irysy
from zadanie2_autoenkoder import siec_autoenkoder

def main():
    while(True):
        print("\nWybierz zadanie:")
        print("1 - Klasyfikacja irysów")
        print("2 - Autoenkoder")
        print("3 - Zakończ")

        wybor = input("\nWybór: \n")

        match wybor:
            case "1":
                siec_irysy()
            case "2":
                siec_autoenkoder()
            case "3":
                print("Koniec programu")
                break
            case _:
                print("Wybrałeś niepoprawną opcję")

if __name__ == "__main__":
    main()