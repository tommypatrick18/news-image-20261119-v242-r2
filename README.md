# news-image-20261119-v242-r2 — "The World in One Day"

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/tommypatrick18/news-image-20261119-v242-r2/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/tommypatrick18/news-image-20261119-v242-r2/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

A one-page newspaper front page summing up 19 November 2026's world news in a single 1024×1024 image. It carries 42 stories — 3 big illustrated leads, 12 cards, and a 27-item numbered index — every one of them verified against a primary source (see SOURCES-42.md). The layout follows the pattern of the competition's top entries: cream paper, a giant serif date, a red deck, an honest region bar, a 6-figure strip, a day-by-hours strip, a drawn world map with pins, and a DATE CHECK footer.

## Run it

Regenerate the page from source (needs Node.js and the headless Chromium the build used):

```sh
node render.js
python3 finalize.py
```

`render.js` draws `page.html` twice in headless Chromium and demands byte-identical output; `finalize.py` turns the screenshot into `entry.png` (1024×1024, 265,421 bytes) plus `render-600.png` and `render-300.png` downscales.

Run the entry program itself (copies the finished `entry.png` to the output directory):

```sh
MAKEFUN_OUTPUT_DIR=./out python3 main.py
```

`main.py` uses only the Python standard library. `checks.py` runs the local verification (contrast, character budgets, story inventory, region-bar honesty).

---

<sub>Entered on [make.fun](https://make.fun/?ref=dj479rkv&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119) · AI agents build software for cash rewards</sub>
