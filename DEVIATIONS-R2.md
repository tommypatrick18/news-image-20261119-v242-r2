# DEVIATIONS-R2 — news-image-20261119 v242-R2

What R2 does differently from the frozen spec (SPEC-REVISED-V2.4.2),
from R1, and from the ni19 Top 3 it mirrors. Every deviation is deliberate
and recorded here — nothing is silent.

## vs SPEC-REVISED-V2.4.2 (frozen spec)

The spec describes a 4-hero layout (39 stories: 4 heroes + 12 cards + 5-figure
strip + 23 index). R2 replaces that layout with the ni19 Top 1–5 pattern,
per Tommy's order of 20 Nov 10:10 WIB ("Tiru pola top 1-5 build ulang r2"):

- **3 big leads instead of 4 heroes.** Leads are 307px wide with 92px-tall
  illustrations (trilateral skyline / ICJ courthouse / GTA VI sunset city),
  22px serif headlines, 2-line decks.
- **42 stories instead of 39.** 3 leads + 12 cards + 27 index.
- **Region bar (new).** 7 segments with honest per-story counts
  (EUROPE 9 / AMERICAS 14 / ASIA 6 / MIDDLE EAST 6 / AFRICA 2 / OCEANIA 2 /
  WORLD 3). The spec had no region bar.
- **Figures strip: 6 figures instead of 5.** Added 730,000 (Rohingya fled
  2017) and 9–6 (ICJ vote) — the two consensus figures present in 4–5 of the
  Top 5 strips and missing from R1.
- **Hours strip (new).** 6 timed events across the day.
- **Masthead: 116px instead of 122px** (date line 62px; see OVERFLOW-REPORT).
- **Index: 27 items instead of 23**, in 4 columns (7/7/7/6).
- **Map: 8 pins + inset**, same as the spec, but the panel is "ON THE MAP —
  8 PLACES" and the inset note reads "Inset shows pins 5–8 in true relative
  place; the main map marks with one ◆".
- **DATE CHECK footer kept**, updated to the R1 outcomes (trilateral ended in
  a 4-point pact; ICJ found Myanmar guilty 9–6; COP31 draft has no fossil
  fuels; GTA VI score per 18 Nov).
- Unchanged from the spec: canvas 1024×1024, cream paper, Chromium render,
  stdlib-only main.py, determinism + overflow + contrast gates.

## vs R1 (news-image-20261119-v242-r1, HEAD fbcc0f1)

- Layout rebuilt on the Top 1–5 pattern (above); R1's 4-hero layout retired.
- **C7 FIXED.** R1 card C7 read "Trump, Putin to meet in Shenzhen" while H1
  said the pact had ended — a contradiction. R2 card 11 reads "Trump, Putin
  meet in Shenzhen" (the meeting happened; the trilateral ended in a pact).
- **3 new stories (19 Nov, verified-primary in this session):**
  #40 Suneung, #41 Florida floods, #42 COP31 draft.
- Strip grows 5 → 6 figures; hours strip and region bar are new.
- Anthropic stays a card (card 4); the spec §9 double-count (Anthropic as
  both hero 4 and card 12) does not occur in R2 because there are only
  3 leads and Anthropic appears once.
- R1's "SINCE ALASKA 2025" subline is kept on card 11.

## vs ni19 Top 3 (sawitmen, the mirrored entry)

R2 mirrors Top 3's template and 40-story structure but is NOT the same entry:

- **Not the same file.** Every illustration was drawn fresh in this session;
  every headline/deck was written fresh; the code is a new file.
- **Named difference: "SOURCED NUMBERS".** The figures strip keeps Top 3's
  6 figures, each with a gold source tag underneath (PYMNTS · UNHRC · ICJ ·
  REUTERS · REUTERS · CDC).
- **42 stories vs Top 3's 40.** 12 stories Top 3 carried failed the hard
  date rule (event/first report on 17 Nov, not 19 Nov) and were replaced;
  3 new 19 Nov stories were added.
- **Region bar counts are honest** — R2's bar (9/14/6/6/2/2/3) reconciles
  with its own per-story regions; Top 3's bar does not reconcile with its
  own labels.
- **Hours strip is R2's own** (6 events, incl. Suneung 08:40 and the
  trilateral 14:30).
- **Map + inset + "ON THE MAP" panel** are R2's own drawing (integer
  coordinates, written fresh; coasts simplified, disclosed "NOT TO SCALE").
- Shared weakness, honestly noted: R2's illustrations are flat-vector and
  schematic, like V6's — Top 3's illustrations are livelier. That is the
  known gap, not a hidden one.

## Honesty notes

- The map is a **drawn, simplified world map** (coarse integer-coordinate
  polygons, written fresh in this session). It is labelled on the page:
  "DRAWN MAP — COASTS SIMPLIFIED, NOT TO SCALE".
- The Hormuz item is labelled **CLAIM** everywhere it appears (index 18,
  map pin 4, DATE CHECK footer) — it is an IRGC claim, not independently
  confirmed.
- The measles figure "5.400" is a rounding of CDC's 5,412 cases (2026,
  per 12 Nov).
- The Voyager crossing happened 18 Nov; it sits on the 19 Nov page because
  NASA's confirmation arrived 19 Nov (same reasoning as R1).
- PERM (index 23) is a **proposed** rule, not law in force; Prince Harry
  (index 30) "would rejoin" means the British Army, not the royal family;
  the Bayesian item (index 29) reports the MAIB finding only — the Italian
  prosecutors' experts concluded the opposite (crew error). All three
  nuances are carried over from SOURCES-39 §6.3 and noted in SOURCES-42.md.
