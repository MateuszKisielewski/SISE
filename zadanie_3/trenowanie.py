import pandas as pd
import joblib
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

def trenuj_model(plik_danych, test_rozmiar, max_glebokosc, liczba_drzew, ziarno, plik_drzewa, plik_wykresu):

    df = pd.read_csv(plik_danych)
    y = df['Wynik']
    x = df.drop(columns=['Wynik'])

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=test_rozmiar, random_state=ziarno)

    las = RandomForestClassifier(n_estimators=liczba_drzew, max_depth=max_glebokosc, random_state=ziarno)
    las.fit(x_train, y_train)

    y_pred = las.predict(x_test)
    skutecznosc = accuracy_score(y_test, y_pred)
    print(f"Skuteczność na zbiorze testowym: {skutecznosc * 100:.2f}%")

    joblib.dump(las, plik_drzewa)
    print(f"Model zapisany pomyślnie jako: {plik_drzewa}")