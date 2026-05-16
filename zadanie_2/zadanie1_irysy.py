import random
from zadanie_2.data_tools import wczytaj_plik_irysy, zapisz_model
from zadanie_2.neural_network import trenuj_siec, testuj_siec

dane_wejsciowe, oczekiwane_wyjscia = wczytaj_plik_irysy("zadanie_2/irysy_nazwy.csv")

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

wagi, biasy = trenuj_siec(rozmiary_warstw, X_train, y_train, epoki, docelowy_blad, wspolczynnik_nauki, momentum, czy_bias, losowa_kolejnosc, co_ile_zapis_log, nazwa_pliku_logu)

nazwa_pliku_modelu = "model_irysy.json"
zapisz_model(nazwa_pliku_modelu, czy_bias, wagi, biasy)

nazwa_pliku_logu_test = "log_testowy_irysy.txt"
testuj_siec(X_test, y_test, wagi, biasy, czy_bias, nazwa_pliku_logu_test)