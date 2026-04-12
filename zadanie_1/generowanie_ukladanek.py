def generuj_ukladanki():
    w, k = 4, 4
    wzorzec = tuple(list(range(1, w * k)) + [0])
    odwrotny = {'U': 'D', 'D': 'U', 'L': 'R', 'R': 'L', None: None}

    odwiedzone = {wzorzec}
    biezaca_warstwa = [(wzorzec, None)]
    calkowita_liczba = 0

    for g in range(1, 8):
        nastepna_warstwa = []

        for plansza, ostatni_ruch in biezaca_warstwa:
            idx_zera = plansza.index(0)
            wz, kz = idx_zera // k, idx_zera % k

            mozliwosci = [
                (wz > 0,      idx_zera - k, 'U'),
                (wz < w - 1, idx_zera + k, 'D'),
                (kz > 0,      idx_zera - 1, 'L'),
                (kz < k - 1, idx_zera + 1, 'R')
            ]

            for mozliwy, nowy_idx, ruch in mozliwosci:
                if mozliwy and ruch != odwrotny[ostatni_ruch]:
                    nowa_p = list(plansza)
                    nowa_p[idx_zera], nowa_p[nowy_idx] = nowa_p[nowy_idx], nowa_p[idx_zera]
                    nowa_p_krotka = tuple(nowa_p)

                    if nowa_p_krotka not in odwiedzone:
                        odwiedzone.add(nowa_p_krotka)
                        nastepna_warstwa.append((nowa_p_krotka, ruch))

        for i, (p, _) in enumerate(nastepna_warstwa, 1):
            nazwa = f"{w}x{k}_{g:02d}_{i:04d}.txt"
            with open(nazwa, 'w') as f:
                f.write(f"{w} {k}\n")
                for r in range(w):
                    f.write(" ".join(map(str, p[r*k:(r+1)*k])) + "\n")
            calkowita_liczba += 1

        print(f"Głębokość {g:02d}: {len(nastepna_warstwa)} plansz")
        biezaca_warstwa = nastepna_warstwa

    print(f"Łącznie: {calkowita_liczba}")

if __name__ == "__main__":
    generuj_ukladanki()
