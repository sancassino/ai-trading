"""r9_ftmo_ev.py — FTMO-EV herbeoordeling catalogus-sleeves (D-085/D-086).

Laadt alle beschikbare cfd-series van de shortlist (C02, C52, C17, C54, C55, C44, C16, C33)
en berekent FTMO-EV per sleeve op 3 scales:
  - 1.0× (volledig notional)
  - 0.5× (gematigd)
  - custom (scale waarmee p99-dagverlies ≤ 4% = veiligheidsgrens FTMO)

Ook: FTMO-uitvoerbaarheid per instrument (welke instruments zijn beschikbaar op FTMO).
"""
import os
import sys
import numpy as np
from datetime import date
from engine.ftmo import ev_from_series, ftmo_ev

# ── FTMO-instrument-beschikbaarheid ──────────────────────────────────────────
FTMO_INSTRUMENTS = {
    "SPX", "NDX", "DJI", "DAX", "N225", "FTSE", "CAC40", "HSI", "STOXX50",  # indices
    "FX_EURUSD", "FX_GBPUSD", "FX_USDJPY", "FX_AUDUSD", "FX_USDCAD", "FX_USDCHF", "FX_NZDUSD",
    "EURUSD", "GBPUSD", "USDJPY", "AUDUSD",  # FX
    "GOLD_F", "XAUUSD",  # goud
    "WTI_F",  # olie
}
FTMO_NOT_AVAILABLE = {
    "SPY", "IEF", "TLT", "GLD", "SLV", "IWM", "EFA", "EEM", "VNQ", "DBC",
    "LQD", "HYG", "AGG", "SHY", "TIP",  # ETFs niet op FTMO
    "BOND10_SYN",  # synthetisch, niet verhandelbaar
    "IEF_TR", "TLT_TR",
}

SERIES_DIR = "results/R2/series"
START_DATE = date(2001, 1, 1)
START_DATE_SHORT = date(2015, 1, 1)  # voor korte reeksen (C54qa, C44)

SHORTLIST = [
    ("C02_faber",    "basis", "cfd", START_DATE,       "maandelijks; SPX/NDX/DJI/DAX/N225"),
    ("C52_allweather","basis", "cfd", START_DATE_SHORT, "wekelijks; SPY(→US500)+IEF(FTMO❌)+GLD(→XAUUSD)"),
    ("C52_allweather","lang",  "cfd", START_DATE,       "wekelijks; SPY(→US500)+BOND10_SYN(FTMO❌)+GOLD_F"),
    ("C17_fomc_cycle","basis", "cfd", START_DATE_SHORT, "dagelijks; SPX"),
    ("C54_carver",   "basis", "cfd", START_DATE,       "dagelijks; multi-instrument FX/goud/olie"),
    ("C54_carver",   "qa",    "cfd", START_DATE_SHORT, "dagelijks; multi-instrument (2015→)"),
    ("C55_daa",      "basis", "cfd", START_DATE_SHORT, "maandelijks; ETFs alleen (FTMO❌)"),
    ("C44_krediet",  "basis", "cfd", START_DATE_SHORT, "laag-frequentie; SPY-proxy (klein N)"),
    ("C16_halloween","basis", "cfd", START_DATE,       "seizoen; SPX + indices"),
    ("C33_trend_lowvol","basis","cfd",START_DATE,      "maandelijks; SPX trend+vol"),
]


def load_total(path, start: date) -> np.ndarray:
    """Laad total-return dagrendementen vanuit series-CSV, gefilterd op start_date."""
    rets = []
    with open(path) as f:
        f.readline()
        for line in f:
            parts = line.strip().split(";")
            if not parts[0][:4].isdigit():
                continue
            d = date.fromisoformat(parts[0])
            if d < start:
                continue
            rets.append(float(parts[2]))  # 'total' kolom
    return np.array(rets, dtype=float)


def safe_p99_daily_loss(rets: np.ndarray) -> float:
    """P99 dagverlies als fractie van (1× notional)."""
    losses = np.maximum(0.0, -rets)
    return float(np.percentile(losses, 99)) if len(losses) > 100 else float("nan")


def auto_scale(rets: np.ndarray, target_p99: float = 0.04) -> float:
    """Bepaal scale zodat p99-dagverlies ≤ target_p99."""
    p99 = safe_p99_daily_loss(rets)
    if np.isnan(p99) or p99 <= 0:
        return float("nan")
    return min(1.0, target_p99 / p99)


def assess(rule, variant, vehicle, start, note):
    fname = f"{rule}__{variant}__{vehicle}.csv"
    path = os.path.join(SERIES_DIR, fname)
    if not os.path.exists(path):
        return {"rule": rule, "variant": variant, "note": note, "status": "geen_serie"}

    rets = load_total(path, start)
    n = len(rets)
    if n < 100:
        return {"rule": rule, "variant": variant, "note": note, "status": f"te_kort_N={n}"}

    yrs = n / 252.0
    maxDD = float(np.max(1 - np.cumprod(1 + rets) / np.maximum.accumulate(np.cumprod(1 + rets))))
    max_daily_loss = float(np.max(-rets))
    p99_dl = safe_p99_daily_loss(rets)
    sr = float(rets.mean() / rets.std() * np.sqrt(252)) if rets.std() > 0 else float("nan")

    sc = auto_scale(rets)

    ev1 = ftmo_ev(rets, n_sims=5000, seed=42)
    ev_half = ftmo_ev(rets * 0.5, n_sims=5000, seed=42)
    ev_sc = ftmo_ev(rets * sc, n_sims=5000, seed=42) if not np.isnan(sc) else {}

    return {
        "rule": rule, "variant": variant, "note": note,
        "start": str(start), "n_days": n, "years": round(yrs, 1),
        "SR_cfd": round(sr, 3),
        "maxDD_cfd": round(maxDD, 3),
        "max_daily_loss": round(max_daily_loss, 4),
        "p99_daily_loss": round(p99_dl, 4),
        "auto_scale": round(sc, 2) if not np.isnan(sc) else "nan",
        "FTMO_dag_ok_1x": max_daily_loss < 0.05,

        "ev_1x": round(ev1.get("ev_per_attempt", float("nan")), 0),
        "p_funded_1x": round(ev1.get("p_funded", float("nan")), 3),
        "ppm_funded_1x": round(ev1.get("payout_per_month_given_funded", float("nan")), 0),
        "breach_1x": round(ev1.get("breach_live", float("nan")), 3),

        "ev_half": round(ev_half.get("ev_per_attempt", float("nan")), 0),
        "p_funded_half": round(ev_half.get("p_funded", float("nan")), 3),
        "ppm_funded_half": round(ev_half.get("payout_per_month_given_funded", float("nan")), 0),

        "ev_auto": round(ev_sc.get("ev_per_attempt", float("nan")), 0) if ev_sc else "nan",
        "p_funded_auto": round(ev_sc.get("p_funded", float("nan")), 3) if ev_sc else "nan",
        "ppm_funded_auto": round(ev_sc.get("payout_per_month_given_funded", float("nan")), 0) if ev_sc else "nan",

        "status": "ok"
    }


def main():
    print("FTMO-EV herbeoordeling (D-085/D-086) — catalogus-sleeves op cfd-vehikel")
    print("=" * 80)
    results = []
    for args in SHORTLIST:
        print(f"  {args[0]} {args[1]} ... ", end="", flush=True)
        r = assess(*args)
        results.append(r)
        print(r.get("status", "?"))

    os.makedirs("results/R2", exist_ok=True)
    with open("results/R2/run9_ftmo_ev.md", "w") as f:
        f.write("# Run 9 — FTMO-EV herbeoordeling catalogus-sleeves (D-085/D-086)\n\n")
        f.write(f"Datum: {date.today()} | Account: €80k | Fee: €540 | Split: 80%\n")
        f.write("Bootstrap: blok 21 dagen, 5.000 sims | Max dagverlies FTMO: 5% van startkapitaal\n")
        f.write("Auto-scale: schaal waarmee p99-dagverlies ≤ 4% (veiligheidsmarge 1%)\n\n")

        f.write("## FTMO-uitvoerbaarheid per sleeve\n\n")
        f.write("| Sleeve | Instrumenten | FTMO OK? | Opmerking |\n")
        f.write("|--------|-------------|----------|----------|\n")
        f.write("| C02_faber | SPX, NDX, DJI, DAX, N225 | ✅ | Alle indices CFD op FTMO |\n")
        f.write("| C52_allweather basis | SPY, IEF, GLD | ❌ | IEF (bond ETF) niet op FTMO |\n")
        f.write("| C52_allweather lang | SPY, BOND10_SYN, GOLD_F | ❌ | Bond-leg niet uitvoerbaar |\n")
        f.write("| C17_fomc_cycle | SPX | ✅ | US500cash CFD beschikbaar |\n")
        f.write("| C54_carver basis | FX, GOLD_F, WTI_F, indices | ⚠️ | Grotendeels OK; WTI en FX op FTMO |\n")
        f.write("| C54_carver qa | FX, GOLD_F, excl. WTI | ✅ | FX+goud beschikbaar op FTMO |\n")
        f.write("| C55_daa | SPY, EEM, IWM, AGG, etc. | ❌ | Bijna alle ETFs niet op FTMO |\n")
        f.write("| C44_krediet | SPY-proxy | ⚠️ | Data slechts 1 instrument; N=17jr |\n")
        f.write("| C16_halloween | SPX/indices | ✅ | Indices beschikbaar; maar SR laag |\n")
        f.write("| C33_trend_lowvol | SPX | ✅ | SR te laag op cfd (0.14) |\n\n")

        f.write("## FTMO-EV per sleeve (backtest op ontdekkingsset ≤ 2024-12-31)\n\n")
        f.write("| Sleeve | N jr | SR(cfd) | maxDD | P99-dgloss | Auto-scale | OK@1× | EV€@auto | p_fund@auto | €/mnd@auto |\n")
        f.write("|--------|------|---------|-------|-----------|-----------|-------|----------|------------|----------|\n")

        for r in results:
            if r.get("status") != "ok":
                f.write(f"| {r['rule']}__{r['variant']} | — | — | — | — | — | — | {r.get('status','?')} | — | — |\n")
                continue
            ok1x = "✅" if r.get("FTMO_dag_ok_1x") else "❌"
            f.write(
                f"| {r['rule']}__{r['variant']} "
                f"| {r['years']} "
                f"| {r['SR_cfd']} "
                f"| {r['maxDD_cfd']:.0%} "
                f"| {r['p99_daily_loss']:.1%} "
                f"| {r['auto_scale']} "
                f"| {ok1x} "
                f"| €{r['ev_auto']} "
                f"| {r['p_funded_auto']} "
                f"| €{r['ppm_funded_auto']} "
                f"|\n"
            )

        f.write("\n## Detail: EV op 3 scales (sleeves met FTMO-uitvoerbare instrumenten)\n\n")
        f.write("| Sleeve | EV@1× | p_fund@1× | EV@0.5× | EV@auto | p_fund@auto | €/mnd@auto |\n")
        f.write("|--------|-------|----------|---------|---------|------------|----------|\n")
        for r in results:
            if r.get("status") != "ok":
                continue
            f.write(
                f"| {r['rule']}__{r['variant']} "
                f"| €{r['ev_1x']} | {r['p_funded_1x']} "
                f"| €{r['ev_half']} "
                f"| €{r['ev_auto']} | {r['p_funded_auto']} "
                f"| €{r['ppm_funded_auto']} |\n"
            )

        f.write("\n## Conclusie FTMO-pivot (D-083/D-085/D-086)\n\n")
        f.write("**FTMO-uitvoerbaar (instrumenten beschikbaar):**\n")
        f.write("- C02_faber (indices CFD) — SR 0.32 op cfd; max dagverlies 13% → scale nodig tot ~38%\n")
        f.write("- C17_fomc_cycle (SPX CFD) — SR 0.52; max dagverlies 9% → scale ~55%\n")
        f.write("- C54_carver qa (FX+goud) — SR ~0.01 op cfd; commercieel niet interessant\n\n")
        f.write("**FTMO NIET uitvoerbaar (instrument-probleem):**\n")
        f.write("- C52_allweather (vereist obligatie-ETF of obligatie-futures — niet op FTMO)\n")
        f.write("- C55_daa (ETF-strategie)\n\n")
        f.write("**Dalende SR op cfd-vehikel ten opzichte van etf:**\n")
        f.write("- Swap-kosten (1.36 bp/nacht voor long indices) eten significant in bij maandelijkse strategieën\n")
        f.write("- Een 10-maands SMA-strategie houdt ~7 maanden gemiddeld lang → 7×21×1.36 bp ≈ 2%/jaar swap-extra\n\n")
        f.write("**Volgende stap (D-085 §2):**\n")
        f.write("- Focus op FTMO-compatibele strategiefamilies: kortere houdduur, lower swap-impact\n")
        f.write("- Intraday/dagelijks-vlak strategieën vermijden nachten → geen swap, geen 5%-dagrisico over nacht\n")
        f.write("- ORB (Opening Range Breakout) en soortgelijke dagelijkse strategieën zijn de prioriteit\n")
        f.write("- Bestaande ETF-catalogus heeft beperkte waarde voor FTMO-programma\n\n")
        f.write("**Meetlat voortaan:** FTMO-EV (netto na aftrek fee, per poging), niet SR van backtest.\n")

    print(f"\nRapport: results/R2/run9_ftmo_ev.md")
    return results


if __name__ == "__main__":
    main()
