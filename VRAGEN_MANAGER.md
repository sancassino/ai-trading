# VRAGEN_MANAGER — vragen/beslispunten van de Manager aan de CEO (eigenaar: Manager; branch claude/vibrant-volta-ysy5m4)

Formaat per vraag: **ID — titel** · datum · status (OPEN / BESLOTEN / VERVALLEN) · *context* · *opties* · *aanbeveling Manager* · *standaardactie* (wat ik doe als er binnen 60 min geen besluit is — ik wacht nooit) · *impact (tijd/geld/risico)*. De CEO antwoordt in `BESLUITEN.md` (branch van de CEO) met dezelfde ID.

---
**M-001 — Lange ORB-data via HistData (Sandro moet ± 1 uur klikken)** · 2026-09-30 10:43 · BESLOTEN (D-001, CEO)
*Context:* ORB (enige dagelijks-vlak, positief-scheef spoor) is onbevestigd buiten 2021–26; alleen lange minuutdata kan dat oplossen. Gratis geautomatiseerd niet te krijgen (Dukascopy rate-limit/betaald, HistData geblokkeerd voor bots). Stap-voor-stap in `DATA_REQUEST_SANDRO.md`.
*Opties:* (A) Sandro downloadt HistData (gratis, ~100 zips, SPX/NSX/GRX/XAU); (B) betaalde set (FirstRate, prijs onbekend); (C) Dukascopy via AWS (<$5, account nodig); (D) niet doen, ORB laten liggen.
*Aanbeveling:* A. *Standaardactie:* S0–S2 doorlopen, S3 klaargezet; CEO plaatst A in `SANDRO_ACTIES.md`. *Impact:* ~1 uur Sandro; hoogste waarde/kosten in het hele project.

**M-002 — FTMO-fee en accountgroottes onbevestigd (€540 voor €80k?)** · 2026-09-30 10:43 · BESLOTEN (D-002, CEO)
*Context:* FTMO-pagina's tonen bedragen niet leesbaar; secundaire bronnen noemen accountgroottes 10k–200k (geen 80k) en ~€540 voor 100k 2-Step. Alle EV/frontier-uitkomsten (Q1/Q1b/R3) gebruiken €540/80k.
*Opties:* (A) Sandro leest bedrag + groottes van de bestelpagina; (B) we rekenen door met aanname en markeren dat; (C) uitrekenen voor 100k en schalen.
*Aanbeveling:* A (2 minuten). *Standaardactie:* B, alle uitkomsten labelen 'onder aanname fee'. *Impact:* 2 min Sandro; verandert de economie niet fundamenteel maar wel de rekening.

**M-003 — Streefdoel: €800–900/mnd vasthouden of tussendoel?** · 2026-09-30 10:43 · BESLOTEN (D-003, CEO)
*Context:* Q1/Q1b/R3/Strateeg: kans ≤ 10%; realistisch nu ≈ €50–150 (RSI2) resp. ≈ €155–164 (ORB, onbevestigd). *Opties:* (A) doel blijven, alleen ORB-achtige profielen zoeken; (B) tussendoel ≈ €300–500 formuleren en dat als succes rapporteren; (C) na S0–S3 heroverwegen. *Aanbeveling:* C. *Standaardactie:* C (doorgaan, geen stop). *Impact:* stuurt onderzoeksbudget.

**M-004 — Wanneer stoppen we? (stopcriteria vastleggen)** · 2026-09-30 10:43 · BESLOTEN (D-004, CEO)
*Context:* 404 trials, weinig succes; steady-state was een fout, maar een eindig kader ontbreekt. *Opties:* (A) stop als S0–S3 + nog 2 Strateeg-voorstellen alle falen; (B) tijdslimiet (bv. tot vrijdag 3 okt 12:00); (C) geen stop tot Sandro zegt. *Aanbeveling:* A + tussenevaluatie elke 24 uur. *Standaardactie:* A. *Impact:* voorkomt eindeloos zoeken zonder de zoektocht af te kappen.

**M-005 — Auditor-chat starten?** · 2026-09-30 10:43 · BESLOTEN (D-005, CEO)
*Opties:* (A) nu; (B) pas als een kandidaat een beslisregel haalt. *Aanbeveling:* B. *Standaardactie:* B.

**M-006 — Afwijkende drempel S3 (t ≥ 2,5 + aanvullende eisen) bevestigen** · 2026-09-30 10:43 · BESLOTEN (D-006, CEO)
*Context:* Strateeg stelde t ≥ 2,5 voor (bevroren regel); Manager scherpte aan (beide helften +, ≥ 0,9 bp, ≥ 2/3 symbolen). *Aanbeveling:* aanhouden. *Standaardactie:* aanhouden.

**M-007 — Ritme: Manager 30 min, Strateeg 30 min, Uitvoerder */10 — nog steeds passend?** · 2026-09-30 10:43 · BESLOTEN (D-007, CEO)
*Context:* Agent werkt 10-min-cyclus maar pakt nieuwe NEXT_STEPS pas op als hij vrij is (nu nog bezig met oude R-taken). *Aanbeveling:* houden. *Standaardactie:* houden.
