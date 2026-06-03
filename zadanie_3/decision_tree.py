import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import accuracy_score, classification_report

df = pd.read_csv("dane_oczyszczone.csv")

y = df['Wynik']
x = df.drop(columns=['Wynik'])

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=67)

drzewo = DecisionTreeClassifier(max_depth=5, random_state=67)
drzewo.fit(x_train, y_train)

y_pred = drzewo.predict(x_test)
skutecznosc = accuracy_score(y_test, y_pred)

print(f"Skuteczność (Accuracy): {skutecznosc * 100:.2f}%\n")
print(classification_report(y_test, y_pred))

plt.figure(figsize=(20, 10))
plot_tree(drzewo, x.columns, drzewo.classes_, filled=True, fontsize=10)

plt.title("Drzewo decyzyjne - przewidywanie wyniku meczu")
plt.savefig("drzewo_wykres.png")