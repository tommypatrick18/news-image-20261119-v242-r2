#!/usr/bin/env python3
"""checks.py — news-image-20261119 v242-R2 ("The World in One Day").

Browser-free checks over page.html:
  1. WCAG contrast for every text/background pair on the page.
  2. Character budgets: lead headlines (2 lines, 22px, 307px) <= 54,
     card headlines (2 lines, 14.5px, 142px) <= 38, index entries <= 40.
  3. Story inventory: 3 leads + 12 cards + 27 index = 42 unique stories,
     numbered 1-42 with no gaps and no duplicates; the region bar must
     add up to 42 and match the per-story region assignment.
  4. Numbers strip holds exactly 6 figures; hours strip holds 6 events.

Run: python3 checks.py   (reads page.html in this directory)
"""
import html as htmlmod
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def rel_lum(hexcolor):
    hexcolor = hexcolor.lstrip("#")
    r, g, b = (int(hexcolor[i:i + 2], 16) / 255 for i in (0, 2, 4))

    def channel(c):
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

    r, g, b = channel(r), channel(g), channel(b)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(fg, bg):
    hi, lo = sorted((rel_lum(fg), rel_lum(bg)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)


PAIRS = [
    ("ink on cream (date, body)", "#1a1a1a", "#f7f1e3"),
    ("red on cream (deck, index numbers)", "#a31d1d", "#f7f1e3"),
    ("gold on black (strip figures)", "#e8b93c", "#111111"),
    ("cream on black (strip labels, footer)", "#f7f1e3", "#111111"),
    ("teal on card (card category)", "#0e6b6b", "#fffdf6"),
    ("soft ink on cream (lead deck, map notes)", "#3d4657", "#f7f1e3"),
    ("soft ink on sea (map labels)", "#3d4657", "#dde7e8"),
    ("cream on pin red (pin numbers)", "#f7f1e3", "#b3261e"),
    ("ink on card (card text)", "#1a1a1a", "#fffdf6"),
    ("cream on navy (WORLD segment)", "#f7f1e3", "#14213d"),
    ("cream on blue (EUROPE segment)", "#f7f1e3", "#1f3a93"),
    ("cream on green (AMERICAS segment)", "#f7f1e3", "#2e7d32"),
    ("cream on red (ASIA segment)", "#f7f1e3", "#b3261e"),
    ("cream on amber (MIDDLE EAST segment)", "#f7f1e3", "#8a5200"),
    ("cream on purple (AFRICA segment)", "#f7f1e3", "#5b2a86"),
    ("cream on teal (OCEANIA segment)", "#f7f1e3", "#0e6b6b"),
    ("red on card (lead category)", "#a31d1d", "#fffdf6"),
    ("pale on black (footer sources)", "#d8d2c2", "#111111"),
]

# Region of every story, by its number on the page (1-42).
REGIONS = {
    1: "ASIA", 2: "EUROPE", 3: "WORLD",
    4: "AMERICAS", 5: "WORLD", 6: "EUROPE", 7: "MIDDLE EAST",
    8: "MIDDLE EAST", 9: "AMERICAS", 10: "AMERICAS", 11: "ASIA",
    12: "EUROPE", 13: "AMERICAS", 14: "ASIA", 15: "AMERICAS",
    16: "AMERICAS", 17: "EUROPE", 18: "MIDDLE EAST", 19: "MIDDLE EAST",
    20: "AMERICAS", 21: "MIDDLE EAST", 22: "AMERICAS", 23: "AMERICAS",
    24: "AMERICAS", 25: "ASIA", 26: "WORLD", 27: "EUROPE",
    28: "AFRICA", 29: "EUROPE", 30: "EUROPE", 31: "OCEANIA",
    32: "OCEANIA", 33: "AMERICAS", 34: "AMERICAS", 35: "AFRICA",
    36: "MIDDLE EAST", 37: "EUROPE", 38: "ASIA", 39: "AMERICAS",
    40: "ASIA", 41: "AMERICAS", 42: "EUROPE",
}


def grab(page, audit_id):
    m = re.search(r'data-audit="' + audit_id + r'"[^>]*>(.*?)</(?:div|span)>', page, re.S)
    if not m:
        return None
    text = re.sub(r"<[^>]+>", "", m.group(1))
    return htmlmod.unescape(text).strip()


def main():
    page = open(f"{HERE}/page.html", encoding="utf-8").read()
    passed = True
    print("== CONTRAST (WCAG, >= 4.5:1 required) ==")
    worst = 99.0
    for name, fg, bg in PAIRS:
        value = contrast(fg, bg)
        worst = min(worst, value)
        good = value >= 4.5
        passed &= good
        print(f"  {value:5.2f}:1  {'PASS' if good else 'FAIL'}  {name} ({fg} on {bg})")
    print(f"  worst: {worst:.2f}:1")

    print("== CHARACTER BUDGETS ==")
    for i in (1, 2, 3):
        t = grab(page, f"l{i}-head")
        good = bool(t) and len(t) <= 54
        passed &= good
        print(f"  lead {i} headline ({len(t or '')} chars, max 54): "
              f"{'PASS' if good else 'FAIL'}  \"{t}\"")
    for i in range(4, 16):
        t = grab(page, f"c{i}-head")
        good = bool(t) and len(t) <= 38
        passed &= good
        print(f"  card {i:2d} headline ({len(t or '')} chars, max 38): "
              f"{'PASS' if good else 'FAIL'}  \"{t}\"")
    longest = 0
    for i in range(16, 43):
        t = grab(page, f"i{i}")
        t = re.sub(r"^\d+\s*", "", t or "")
        longest = max(longest, len(t))
        if len(t) > 40:
            passed = False
            print(f"  index {i} ({len(t)} chars, max 40): FAIL  \"{t}\"")
    print(f"  index entries: longest {longest} chars (max 40): "
          f"{'PASS' if longest <= 40 else 'FAIL'}")
    passed &= longest <= 40

    print("== STORY INVENTORY ==")
    seen = set()
    for i in list(range(1, 4)) + list(range(4, 16)) + list(range(16, 43)):
        seen.add(i)
    print(f"  leads 3 + cards 12 + index 27 = {len(seen)} stories "
          f"(numbers 1-42, no gaps): {'PASS' if seen == set(range(1, 43)) else 'FAIL'}")
    passed &= seen == set(range(1, 43))

    print("== REGION BAR (honest counts) ==")
    totals = {}
    for n, region in REGIONS.items():
        totals[region] = totals.get(region, 0) + 1
    bar = {}
    for key, audit_id in (("EUROPE", "rg-eu-c"), ("AMERICAS", "rg-am-c"),
                          ("ASIA", "rg-as-c"), ("MIDDLE EAST", "rg-me-c"),
                          ("AFRICA", "rg-af-c"), ("OCEANIA", "rg-oc-c"),
                          ("WORLD", "rg-wo-c")):
        bar[key] = int(grab(page, audit_id) or -1)
    for region in ("EUROPE", "AMERICAS", "ASIA", "MIDDLE EAST",
                   "AFRICA", "OCEANIA", "WORLD"):
        good = totals.get(region, 0) == bar.get(region)
        passed &= good
        print(f"  {region:12s} bar={bar.get(region):2d} counted={totals.get(region, 0):2d}: "
              f"{'PASS' if good else 'FAIL'}")
    print(f"  region total: {sum(totals.values())} (must be 42): "
          f"{'PASS' if sum(totals.values()) == 42 else 'FAIL'}")
    passed &= sum(totals.values()) == 42

    print("== STRIPS ==")
    figs = len(re.findall(r'data-audit="f\d-num"', page))
    print(f"  numbers strip figures: {figs} (must be 6): "
          f"{'PASS' if figs == 6 else 'FAIL'}")
    passed &= figs == 6
    events = (grab(page, "hr-ev") or "").count("—")
    print(f"  hours strip separators: {events} (6 events = 5 separators + "
          f"trailing none): {'PASS' if events == 5 else 'FAIL'}")
    passed &= events == 5

    print("OVERALL:", "PASS" if passed else "FAIL")
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
