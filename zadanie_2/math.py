import numpy as np

def sigmoida(x):
    return 1 / (1 + np.exp(-x))

def pochodna_sigmoidy(x):
    return x * (1 - x)

def blad_sredniokwadratowy(oczekiwane, wyjscie_sieci):
    return np.sum((oczekiwane - wyjscie_sieci) ** 2) / 2