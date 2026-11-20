# OVERFLOW-REPORT-R2 — news-image-20261119 v242-R2

## Method

Same as R1: `render.js` dumps the DOM from headless Chromium and reads the
`<pre id="audit">` block the page builds on load. The audit measures:

- Every text node with `data-audit` (120 nodes): `scrollWidth`/`scrollHeight`
  vs `clientWidth`/`clientHeight`. Any excess = overflow.
- Every band (9): same test on the band element itself.
- Page: must be exactly 1024×1024.
- Map pins (9 incl. inset): each pin's bounding box must sit inside the map frame.

Overflow budget: **0px everywhere** (a 1px overflow is still an overflow).

## Run 1 (before fixes) — 8 text overflows, 4 band overflows

Text nodes overflowing:

| Element | dw | dh | Text |
|---|---|---|---|
| mh-date | 0 | 1 | "Thursday 19 November 2026" |
| f1-num | 0 | 1 | "$81.3BN" |
| f2-num | 0 | 1 | "730,000" |
| f3-num | 0 | 1 | "9–6" |
| f4-num | 0 | 1 | "€45BN" |
| f5-num | 0 | 1 | "162,5%" |
| f6-num | 0 | 1 | "5.400" |
| hr-ev | 82 | 0 | hours events line (too wide by 82px) |

Bands overflowing (clientHeight shrunk below design height):

| Band | design | clientHeight | scrollHeight |
|---|---|---|---|
| leads | 200 | 197 | 200 |
| cards | 230 | 227 | 230 |
| mapband | 150 | 148 | 150 |
| index | 108 | 107 | 108 |

Masthead clientHeight was 121 (design 122); hours 28 (design 30) — also shrunk,
but their content still fit, so they did not flag as overflowing.

## Root cause

Two independent causes:

1. **1px em-box overflows (mh-date, f1–f6).** Liberation Serif Bold 56px and
   Liberation Sans Bold 26px have an em-box 1px taller than the line box the
   CSS gave them (60px / 28px). Same class of issue R1 hit on its strip
   figures. Fix: give the line 1px more room (date 60→62px, figure numbers
   28→29px).
2. **Flex-shrink from a miscounted total (the 4 bands).** The sheet is a flex
   column with `gap: 6px`. Nine bands need EIGHT gaps = 48px, not 36px.
   Bands summed to 956px + 48px gutters = 1004px > 992px content height, so
   flexbox (default `flex-shrink: 1`) shrank the bands by 1–3px each and their
   content overflowed. The hours line (hr-ev, 82px too wide) is a separate
   width issue: the 6-event line at 10px was ~960px in an ~878px slot.
   Fix: cut 13px from the bands (masthead 122→116, hours 30→28, cards
   230→226 with rows 111→109px, index 108→107 with line 13.4→13.2px) and
   shrink the hours events font 10→9px. New total: 943 + 48 = 991 ≤ 992.

## Fixes applied (page.html, 5 edits)

1. `.top` height 122→116px; `.date` height/line-height 60→62px.
2. `.figures .num` height/line-height 28→29px.
3. `.hours` height 30→28px; `.hours .ev` font-size 10→9px.
4. `.cards` height 230→226px; grid rows 111→109px.
5. `.index` height 108→107px; `.idx-grid` 94→93px, margin-top 2→1px;
   `.idx-e` height/line-height 13.4→13.2px.

## Run 2 (after fixes) — 0 overflows

- Text nodes overflowing: **0 of 120**.
- Bands overflowing: **0 of 9**.
- Page: sw 1024 / cw 1024 / sh 1024 / ch 1024 — exact.
- Pins out of frame: **0 of 9**.
- Fonts: loaded.
- Determinism: raw-run1 sha256 == raw-run2 sha256
  (`d5362a6d32da016a2d3e888f62c9ee928a7e177d24509d6b7463cbf9788d8824`,
  261,446 bytes each).

## Contrast (checks.py, 18 pairs, WCAG ≥ 4.5:1)

Worst pair: **4.55:1** — cream text on the AMERICAS green segment
(#f7f1e3 on #2e7d32). It passes, but the margin is thin (0.05 above the
floor). All other pairs are 5.59:1 or better; the page worst overall is
4.55:1. Recorded here so a future revision knows the tightest pair first.
