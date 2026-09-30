"""U1 kostenpoort (geen trial): mediane spread in het ORB-venster (eerste 30 min + slot) voor indices die nooit in de ORB-selectie zaten."""
import numpy as np

import b4_sim

NEW = {  # cash-sessies (lokale beurstijd); commissie indices 0
    "US2000cash": ("America/New_York", (9, 30), (16, 0), 0.0),
    "EU50cash": ("Europe/Berlin", (9, 0), (17, 30), 0.0),
    "FRA40cash": ("Europe/Paris", (9, 0), (17, 30), 0.0),
    "N25cash": ("Europe/Amsterdam", (9, 0), (17, 30), 0.0),
    "SPN35cash": ("Europe/Madrid", (9, 0), (17, 30), 0.0),
    "JP225cash": ("Asia/Tokyo", (9, 0), (15, 0), 0.0),
    "AUS200cash": ("Australia/Sydney", (10, 0), (16, 0), 0.0),
    "HK50cash": ("Asia/Hong_Kong", (9, 30), (16, 0), 0.0),
}
b4_sim.SYMS.update(NEW)


def main():
    print("symbool      sessies  spread OR-venster (bp)  spread slot (bp)  rondreis ORB ≈ (bp)  poort ≤ 1,0 bp")
    for s in NEW:
        try:
            sess = b4_sim.sessions(s)
        except FileNotFoundError:
            print(f"{s:<12} geen data"); continue
        sess = [(d, b) for d, b in sess if d.year >= 2021]
        if not sess:
            print(f"{s:<12} 0 volledige sessies (sessietijden controleren)"); continue
        orw = np.median([x[5] / x[4] for _, b in sess for x in b[6:12]]) * 1e4
        cl = np.median([b[-1][5] / b[-1][4] for _, b in sess]) * 1e4
        rt = (orw + cl) / 2  # instap in OR-venster (long) of uitstap aan slot (short)
        print(f"{s:<12} {len(sess):>7}  {orw:>22.2f}  {cl:>16.2f}  {rt:>19.2f}  {'DOOR' if rt <= 1.0 else 'nee'}")


if __name__ == "__main__":
    main()
