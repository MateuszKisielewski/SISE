import argparse
from trenowanie import trenuj_model
from testowanie import przewiduj_wynik, przewiduj_zbior

def zdefiniuj_argumenty():
    parser = argparse.ArgumentParser()
    
    parser.add_argument('--tryb', type=str, required=True, choices=['model', 'test', 'test_zbior'], help="Wybierz tryb działania: 'model' do trenowania, 'test' do pojedynczego wyniku, 'test_zbior' do weryfikacji całego pliku")
    
    parser.add_argument('--dane', type=str, default='dane.csv')
    parser.add_argument('--dane_testowe', type=str, default='test.csv')
    parser.add_argument('--test_rozmiar', type=float, default=0.2)
    parser.add_argument('--max_glebokosc', type=int, default=4)
    parser.add_argument('--liczba_drzew', type=int, default=100)
    parser.add_argument('--ziarno', type=int, default=67)
    parser.add_argument('--plik_drzewa', type=str, default='wytrenowane_drzewo.pkl')
    parser.add_argument('--plik_wykresu', type=str, default='wykres_drzewa.png')

    parser.add_argument('--gole_polowa_dom', type=int, default=0)
    parser.add_argument('--gole_polowa_gosc', type=int, default=0)
    parser.add_argument('--strzaly_dom', type=int, default=0)
    parser.add_argument('--strzaly_gosc', type=int, default=0)
    parser.add_argument('--celne_dom', type=int, default=0)
    parser.add_argument('--celne_gosc', type=int, default=0)
    parser.add_argument('--faule_dom', type=int, default=0)
    parser.add_argument('--faule_gosc', type=int, default=0)
    parser.add_argument('--rozne_dom', type=int, default=0)
    parser.add_argument('--rozne_gosc', type=int, default=0)
    parser.add_argument('--zolte_dom', type=int, default=0)
    parser.add_argument('--zolte_gosc', type=int, default=0)
    parser.add_argument('--czerwone_dom', type=int, default=0)
    parser.add_argument('--czerwone_gosc', type=int, default=0)

    return parser.parse_args()


def main():
    args = zdefiniuj_argumenty()

    if args.tryb == 'model':
        trenuj_model(args.dane, args.test_rozmiar, args.max_glebokosc, args.liczba_drzew, args.ziarno, args.plik_drzewa)

    elif args.tryb == 'test':
        statystyki = {
            'Gole_Polowa_Dom': args.gole_polowa_dom,
            'Gole_Polowa_Gosc': args.gole_polowa_gosc,
            'Strzaly_Dom': args.strzaly_dom,
            'Strzaly_Gosc': args.strzaly_gosc,
            'Celne_Dom': args.celne_dom,
            'Celne_Gosc': args.celne_gosc,
            'Faule_Dom': args.faule_dom,
            'Faule_Gosc': args.faule_gosc,
            'Rozne_Dom': args.rozne_dom,
            'Rozne_Gosc': args.rozne_gosc,
            'Zolte_Dom': args.zolte_dom,
            'Zolte_Gosc': args.zolte_gosc,
            'Czerwone_Dom': args.czerwone_dom,
            'Czerwone_Gosc': args.czerwone_gosc
        }
        przewiduj_wynik(args.plik_drzewa, args.plik_wykresu, statystyki)

    elif args.tryb == 'test_zbior':
        przewiduj_zbior(args.plik_drzewa, args.dane_testowe)

if __name__ == "__main__":
    main()