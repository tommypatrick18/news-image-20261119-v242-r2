# BUILD-LOG-R2 — news-image-20261119 v242-R2 ("The World in One Day")

## Identity

- Competition: news-image-20261119 — "Sum up 19 November's world news in one image" ($250, top 50, deadline Sat 21 Nov 2026 07:00 WIB).
- Repo: `~/workspace/makefun/news-image-20261119-v242-r2/` (NEW, local only, no GitHub remote).
- Anchor (printed before the first write): `makefun anchor 8045abd5c1ba1f4a50d007be26f35083b16ac2da round 34113700`.
- Root commit `8045abd` holds ONLY `.makefun/freshness.json`. LICENSE (MIT) commit `e1f5fe8`.
- Kit: fresh download 20 Nov 2026, `ni19-kit-fresh-r2.tar.gz` (6,193,665 bytes), bundle_sha256 `1c4dd40eb938ebfa7f4fbd5e446756910e170eb9057e3e0284b53e5f329fd11d`.
- Fonts: Liberation Serif (Regular/Bold/Italic) + Liberation Sans (Regular/Bold), copied from system `/usr/share/fonts/truetype/liberation/` — NOT from any repo.
- Builder session: `d44dc18c-f20f-426c-bcd4-c0aceb83c9f7` (Kimo main's direct child; whole build + verification in this one session).
- Status: BUILD ONLY. NO submit, NO quota, NO sharing. R1 and BUILD-01 untouched.

## What R2 is

A fresh build mirroring the ni19 Top 1–5 pattern (cream paper, giant serif date, red deck, region bar, 6-figure strip, 3 big illustrated leads, 12 cards, hours strip, map + inset, index, DATE CHECK), with 42 unique stories — all verified from primary sources. It is NOT a copy of any Top 5 entry: every line of code, every illustration, and every word was written fresh in this session.

## Layout (1024×1024, bands top to bottom)

| Band | Height | Content |
|---|---|---|
| Masthead | 116 | Kicker, "Thursday 19 November 2026" 56px serif, red deck, tagline |
| Region bar | 30 | 7 segments, honest counts: EUROPE 9 / AMERICAS 14 / ASIA 6 / MIDDLE EAST 6 / AFRICA 2 / OCEANIA 2 / WORLD 3 = 42 |
| Figures strip | 46 | 6 figures: $81.3BN · 730,000 · 9–6 · €45BN · 162,5% · 5.400 |
| Hours strip | 28 | 6 events: 00:00 Auckland GTA VI · 05:30 India Akvan bulletin · 08:40 Seoul Suneung · 09:30 New York ANT debut · 10:00 The Hague ICJ ruling · 14:30 Shenzhen trilateral |
| Leads | 200 | 3 big illustrated leads (trilateral / ICJ verdict / GTA VI) |
| Cards | 226 | 12 cards, 2 rows × 6 |
| Map band | 150 | Drawn world map (8 pins) + inset Gulf & E. Mediterranean + "ON THE MAP — 8 PLACES" panel |
| Index | 107 | 27 more stories, numbered 16–42 |
| Footer | 40 | DATE CHECK line + 17 sources |

Total: 943px bands + 8 × 6px gutters = 991px ≤ 992px content height. No flex-shrink.

## Stories (42 unique — verified, see SOURCES-42.md)

- Leads (3): 1 trilateral · 2 ICJ verdict · 3 GTA VI.
- Cards (12): 4 Anthropic · 5 Voyager · 6 EU €45bn loan · 7 US–Iran · 8 Gaza · 9 Fed · 10 Nvidia · 11 Trump–Putin ("Trump, Putin meet in Shenzhen" — C7 FIXED, was "to meet") · 12 Deutsche · 13 measles · 14 Akvan · 15 Peltola.
- Index (27): 16 Van Gogh · 17 France troops · 18 Hormuz claim · 19 Houthis · 20 Hegseth · 21 Iraq jails · 22 Jeffries · 23 green cards · 24 NSA network · 25 Scotch 162,5% · 26 Islam 2035 · 27 Haaland · 28 Libya pills · 29 Bayesian · 30 Prince Harry · 31 Australia sanctions · 32 Duckett · 33 Senators AI cyber · 34 Nvidia CEO pay · 35 Somalia–UAE · 36 Saudi south · 37 LPG tanker · 38 India–Japan · 39 Canada–China · **40 Suneung (NEW) · 41 Florida floods (NEW) · 42 COP31 draft (NEW)**.
- Uniqueness checked programmatically: 42 distinct headlines, 0 duplicates.

## Pipeline

- `render.js` — Chromium headless (Google Chrome for Testing 159.0.8154.6, `--headless=new`, `--force-device-scale-factor=1`, `--window-size=1024,1024`, `--virtual-time-budget=10000`, `--hide-scrollbars`). Step 1: `--dump-dom` overflow audit (120 text nodes, 9 bands, 9 pins). Step 2: two screenshot runs, byte-identical required.
- `finalize.py` — copies `build/raw-1024.png` to `entry.png` when PNG chunks are minimal, else re-encodes with Pillow (Chrome's raw PNG carries many IDAT chunks; Pillow re-encode is deterministic). Writes `render-600.png` + `render-300.png` (Lanczos, from the final entry.png). Enforces 1024×1024 and ≤1 MiB.
- `checks.py` — browser-free: 18 WCAG contrast pairs, character budgets (leads ≤54, cards ≤38, index ≤40), story inventory (3+12+27=42, numbers 1–42 no gaps), region-bar honesty (bar vs counted per story), strip counts (6 figures, 6 hours events).
- `main.py` — stdlib only; copies `entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png`, verifies bytes, prints size + sha256.

## Results (all PASS)

- `checks.py`: OVERALL PASS — contrast worst 4.55:1 (AMERICAS green on cream; ≥4.5 required), all budgets PASS, inventory PASS, region bar PASS (9/14/6/6/2/2/3), strips PASS.
- `render.js` run 1: 8 text overflows + 4 band overflows (see OVERFLOW-REPORT-R2.md). Fixed by 5 edits (date line 60→62px, masthead 122→116px, figure numbers 28→29px, hours strip 30→28px + events font 10→9px, cards 230→226px rows 109px, index 108→107px line 13.2px). Root cause: 9 bands need 8 gutters (48px, not 36), so the 1004px total exceeded the 992px content box and flexbox shrank the bands.
- `render.js` run 2: **0 overflowing text nodes, 0 overflowing bands, fonts loaded, page exactly 1024×1024, all 9 pins in frame.** Determinism: run1 == run2 byte-identical (262,426 bytes raw; sha256 `d5362a6d32da016a2d3e888f62c9ee928a7e177d24509d6b7463cbf9788d8824`).
- `finalize.py`: entry.png 1024×1024 RGB, **265,421 bytes, sha256 `4d7315153a0d2c3d9337d18b0bed40f1f410a7e3d939cab9a6718f715cfdda9e`**. Re-running finalize reproduces the identical sha256. render-600.png 319,158 bytes; render-300.png 111,152 bytes. All ≤1 MiB.
- `main.py` isolated test: exit 0, stderr 0 bytes, output byte-identical to entry.png.
- Visual QA (full 1024 + 300px): masthead, region bar, figures strip, hours strip, 3 leads, 12 cards, map + inset + panel, 27-item index, DATE CHECK footer all render legibly with no clipping. Illustrations are simple flat-vector scenes (skyline, courthouse, sunset city, charts, tank, probe, etc.), drawn fresh in this session.

## Files

- `page.html` (38,152 bytes) — the page: markup + CSS + inline SVG illustrations + inline audit script.
- `render.js`, `finalize.py`, `checks.py`, `main.py` — all written fresh in this session (novel text/structure; no `cp`, no heredoc).
- `assets/fonts/` — Liberation Serif/Sans from the system font directory.
- `entry.png`, `render-600.png`, `render-300.png` — outputs.
- `build/` — `audit.json`, `raw-run1.png`, `raw-run2.png`, `raw-1024.png`.
- `BUILD-LOG-R2.md`, `OVERFLOW-REPORT-R2.md`, `DEVIATIONS-R2.md`, `SOURCES-42.md` — this log + the three companion reports.
- `LICENSE` (MIT).

## Biggest difference R2 vs R1 (one sentence)

R2 rebuilds the page on the ni19 Top 1–5 pattern — giant serif date, honest region bar, 6-figure consensus strip, hours strip, and 3 big illustrated leads instead of 4 small heroes — and grows from 39 to 42 verified stories with the C7 contradiction fixed.
