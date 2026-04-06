import pandas as pd
import matplotlib.pyplot as plt

# 1. Wczytanie danych z CSV
kolumny = ['Glebokosc', 'ID', 'Strategia', 'Parametr', 'Dlugosc', 'Odwiedzone', 'Przetworzone', 'MaxGlebokosc', 'Czas']
df = pd.read_csv('wyniki.csv', names=kolumny)

# Usunięcie nagłówka tekstowego, jeśli istnieje w pliku
if df.iloc[0]['Glebokosc'] == 'Glebokosc':
    df = df.iloc[1:]

# Zamiana danych na liczby, żeby można było policzyć średnią
kolumny_liczbowe = ['Glebokosc', 'Dlugosc', 'Odwiedzone', 'Przetworzone', 'MaxGlebokosc', 'Czas']
for col in kolumny_liczbowe:
    df[col] = pd.to_numeric(df[col])

# Co chcemy narysować: Nazwa kolumny -> (Tytuł osi Y, czy włączyć skalę logarytmiczną)
kryteria = {
    'Dlugosc': ('Długość znalezionego rozwiązania', False),
    'Odwiedzone': ('Liczba stanów odwiedzonych', True),
    'Przetworzone': ('Liczba stanów przetworzonych', True),
    'MaxGlebokosc': ('Maksymalna głębokość rekursji', False),
    'Czas': ('Czas trwania [ms]', True)
}

# 2. Rysowanie wykresów - po jednym oknie na każde kryterium
for kolumna, (tytul_osi_y, log_scale) in kryteria.items():
    # Tworzymy jedno duże okno z 4 miejscami na wykresy (2x2)
    fig, axs = plt.subplots(2, 2, figsize=(10, 7))
    fig.suptitle(f'Kryterium: {tytul_osi_y}', fontsize=14, fontweight='bold')

    # Funkcja pomocnicza do ładnego wyglądu każdego z 4 wykresów
    def formatuj_wykres(ax, tytul):
        ax.set_title(tytul)
        ax.set_xlabel('Głębokość')
        ax.set_ylabel(tytul_osi_y)
        ax.grid(axis='y', linestyle='--', alpha=0.7)
        if log_scale:
            ax.set_yscale('log') # Włącza skalę logarytmiczną tam, gdzie trzeba

    # --- LEWY GÓRNY: Ogółem ---
    dane_ogolem = df.groupby(['Glebokosc', 'Strategia'])[kolumna].mean().unstack()
    if not dane_ogolem.empty:
        dane_ogolem.plot(kind='bar', ax=axs[0, 0])
    formatuj_wykres(axs[0, 0], 'Ogółem')

    # --- PRAWY GÓRNY: A* ---
    dane_astr = df[df['Strategia'] == 'astr'].groupby(['Glebokosc', 'Parametr'])[kolumna].mean().unstack()
    if not dane_astr.empty:
        dane_astr.plot(kind='bar', ax=axs[0, 1])
    formatuj_wykres(axs[0, 1], 'A*')

    # --- LEWY DOLNY: BFS ---
    dane_bfs = df[df['Strategia'] == 'bfs'].groupby(['Glebokosc', 'Parametr'])[kolumna].mean().unstack()
    if not dane_bfs.empty:
        dane_bfs.plot(kind='bar', ax=axs[1, 0], colormap='tab10')
    formatuj_wykres(axs[1, 0], 'BFS')

    # --- PRAWY DOLNY: DFS ---
    dane_dfs = df[df['Strategia'] == 'dfs'].groupby(['Glebokosc', 'Parametr'])[kolumna].mean().unstack()
    if not dane_dfs.empty:
        dane_dfs.plot(kind='bar', ax=axs[1, 1], colormap='tab10')
    formatuj_wykres(axs[1, 1], 'DFS')

    # Ułożenie wykresów, żeby na siebie nie wchodziły
    plt.tight_layout()
    
    # Wyświetlenie okienka na ekranie (skrypt zatrzyma się tutaj, dopóki nie zamkniesz okna)
    plt.show()