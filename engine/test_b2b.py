"""Regressietest engine: B2b-replicatie (RSI(2) boven SMA200) moet t(NW) ≈ 3,21 en SR ≈ 0,52 geven (cfd, ontdekking ≤ 2024).
Schrijft NIET naar catalogus/TRIALS.csv (tijdelijke kopie). Gebruik: python -m engine.test_b2b"""
import os, shutil, tempfile
import engine.run_rule as E

tmp = tempfile.mkdtemp()
try:
    E.TRIALS = os.path.join(tmp, "TRIALS.csv")
    open(E.TRIALS, "w").write("datum;regel_id;variant;dataset;fase;netto_SR;t_geclusterd;p;FDR_q;beslissing\n")
    import io, contextlib
    with contextlib.redirect_stdout(io.StringIO()):
        rows = E.run("rep_b2b_rsi2")
    r = rows[0]
    ok = abs(r["t_NW"] - 3.21) < 0.05 and abs(r["SR"] - 0.52) < 0.02
    print(f"B2b-replicatie: t_NW {r['t_NW']:.2f} (verwacht 3,21), SR {r['SR']:.2f} (verwacht 0,52) → {'OK' if ok else 'AFWIJKING'}")
finally:
    shutil.rmtree(tmp)
