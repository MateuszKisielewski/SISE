import pandas as pd
import matplotlib.pyplot as plt
import io

def rysuj_wykres_mse(plik_wejsciowy, plik_wyjsciowy):
    with open(plik_wejsciowy, 'r') as f:
        linie = f.readlines()
        
    czyste_dane = []
    for linia in linie:
        if linia.strip() == '' or linia.startswith('Log:'):
            break
        czyste_dane.append(linia.strip())
        
    dane_jako_tekst = '\n'.join(czyste_dane)
    df = pd.read_csv(io.StringIO(dane_jako_tekst), sep=r'\s*,\s*', engine='python')

    plt.figure(figsize=(10, 6))
    plt.plot(df['Epoka'], df['blad_glowny'], marker='o', linestyle='-', color='b', markersize=4)
    
    plt.xlim(left=0, right = 20000)
    plt.ylim(bottom=0, top = 0.6)
    
    plt.title('Spadek błędu globalnego (MSE) w procesie nauki')
    plt.xlabel('Epoka')
    plt.ylabel('Błąd globalny (MSE)')
    plt.grid(True)
    plt.tight_layout()
    
    plt.savefig(plik_wyjsciowy)
    plt.show()