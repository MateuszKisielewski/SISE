import pandas as pd
import matplotlib.pyplot as plt

kolumny = ['Glebokosc', 'ID', 'Strategia', 'Parametr', 'Dlugosc', 'Odwiedzone', 'Przetworzone', 'MaxGlebokosc', 'Czas']

df = pd.read_csv('wyniki.csv', names=kolumny, encoding='utf-8')

if df.iloc[0]['Glebokosc'] == 'Glebokosc':
    df = df.iloc[1:]

kolumny_liczbowe = ['Glebokosc', 'Dlugosc', 'Odwiedzone', 'Przetworzone', 'MaxGlebokosc', 'Czas']
for col in kolumny_liczbowe:
    df[col] = pd.to_numeric(df[col])

kryteria = {
    'Dlugosc': ('Długość znalezionego rozwiązania', False),
    'Odwiedzone': ('Liczba stanów odwiedzonych', True),
    'Przetworzone': ('Liczba stanów przetworzonych', True),
    'MaxGlebokosc': ('Maksymalna głębokość rekursji', False),
    'Czas': ('Czas trwania [ms]', True)
}

id_png = 1

for kolumna, (tytul_osi_y, log_scale) in kryteria.items():

    dane_ogolem = df.groupby(['Glebokosc', 'Strategia'])[kolumna].mean().unstack()
    dane_astr = df[df['Strategia'] == 'astr'].groupby(['Glebokosc', 'Parametr'])[kolumna].mean().unstack()
    dane_bfs = df[df['Strategia'] == 'bfs'].groupby(['Glebokosc', 'Parametr'])[kolumna].mean().unstack()
    dane_dfs = df[df['Strategia'] == 'dfs'].groupby(['Glebokosc', 'Parametr'])[kolumna].mean().unstack()

    figure, axes = plt.subplots(figsize=(12, 10), nrows=2, ncols=2)
    plt.tight_layout(pad=3.5)

    dane_ogolem.plot(kind='bar', ax=axes[0, 0])
    axes[0, 0].set_title('Ogółem', fontsize=14)
    axes[0, 0].set_xlabel('Głębokość', fontsize=12)
    axes[0, 0].set_ylabel(tytul_osi_y, fontsize=12)
    axes[0, 0].tick_params(axis='x', labelsize=10)
    if log_scale:
        axes[0, 0].set_yscale('log')

    dane_astr.plot(kind='bar', ax=axes[0, 1])
    axes[0, 1].set_title('A*', fontsize=14)
    axes[0, 1].set_xlabel('Głębokość', fontsize=12)
    axes[0, 1].set_ylabel(tytul_osi_y, fontsize=12)
    axes[0, 1].tick_params(axis='x', labelsize=10)
    if log_scale:
        axes[0, 1].set_yscale('log')

    dane_bfs.plot(kind='bar', ax=axes[1, 0], colormap='tab10')
    axes[1, 0].set_title('BFS', fontsize=14)
    axes[1, 0].set_xlabel('Głębokość', fontsize=12)
    axes[1, 0].set_ylabel(tytul_osi_y, fontsize=12)
    axes[1, 0].tick_params(axis='x', labelsize=10)
    if log_scale:
        axes[1, 0].set_yscale('log')

    dane_dfs.plot(kind='bar', ax=axes[1, 1], colormap='tab10')
    axes[1, 1].set_title('DFS', fontsize=14)
    axes[1, 1].set_xlabel('Głębokość', fontsize=12)
    axes[1, 1].set_ylabel(tytul_osi_y, fontsize=12)
    axes[1, 1].tick_params(axis='x', labelsize=10)
    if log_scale:
        axes[1, 1].set_yscale('log')


    plt.savefig(f"{id_png}.png", bbox_inches='tight')
    id_png += 1

    plt.show()