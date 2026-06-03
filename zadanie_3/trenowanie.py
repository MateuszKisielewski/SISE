import pandas as pd
import joblib
import os
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import accuracy_score
 komentarz_commit
def trenuj_model(plik_danych, test_rozmiar, max_glebokosc, ziarno, plik_drzewa, plik_wykresu):

    df = pd.read_csv(plik_danych)
    y = df['Wynik']
    x = df.drop(columns=['Wynik'])

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=test_rozmiar, random_state=ziarno)

    drzewo = DecisionTreeClassifier(max_depth=max_glebokosc, random_state=ziarno)
    drzewo.fit(x_train, y_train)

    y_pred = drzewo.predict(x_test)
    skutecznosc = accuracy_score(y_test, y_pred)
    print(f"Skuteczność na zbiorze testowym: {skutecznosc * 100:.2f}%")

    joblib.dump(drzewo, plik_drzewa)
    print(f"Model zapisany pomyślnie jako: {plik_drzewa}")

    plt.figure(figsize=(40, 20), dpi=300)
    plot_tree(drzewo, feature_names=x.columns, class_names=drzewo.classes_, filled=True, fontsize=8)
    plt.title(f"Drzewo Decyzyjne (max_depth={max_glebokosc})")
    plt.savefig(plik_wykresu, bbox_inches='tight')
    print(f" - Wykres zapisany pomyślnie jako: {plik_wykresu}\n")