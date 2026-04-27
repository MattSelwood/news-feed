# NewsFeed

A personal command-line news aggregator with keyboard navigation.  
Get a daily-refreshed feed of headlines, research papers, and a rotating **Math / Stats / AI concept of the day** — all in your terminal.

![NewsFeed UI](https://github.com/user-attachments/assets/9528254d-697c-49e4-b6f3-b4853cf42f4b)

---

## Features

- **6 curated categories** navigated with number keys or `←`/`→`:
  1. 🌍 **World News** — BBC World, Al Jazeera, Reuters
  2. 💰 **Finance** — CNBC, MarketWatch, Yahoo Finance
  3. 🔭 **Astrophysics** — arXiv (AGN / Galaxy Evolution, High-Energy), NASA News
  4. 🎮 **Counter-Strike 2** — HLTV, r/GlobalOffensive, r/cs2
  5. 💻 **Software Dev** — Hacker News, GitHub Blog, Lobsters
  6. 🧮 **Math / Stats / AI** — arXiv ML, arXiv Statistics, arXiv AI + **Daily Concept**
  7. 🔬 **Science/Tech** — Nature, The Verge, Hacker News, Wired
  8. 📚 **Daily Facts** — Rotating math / stats / AI concept panel
  9. 🌤️ **Weather** — Current conditions + 5-day forecast via Open-Meteo
- **Daily rotating concept** — 60+ in-depth overviews of equations and ideas (Normal distribution, Backpropagation, KL Divergence, Transformers, MCMC, Kalman Filter, …)
- **Weather tab** — current conditions (temperature, humidity, wind) plus a 5-day forecast powered by the free [Open-Meteo API](https://open-meteo.com/) (no API key required); location configured in `config.py`; refreshes every hour
- **Split-pane detail view** — press `Enter` to expand an article summary inline
- **Open in browser** — press `o` to open the selected article in your default browser
- **File-based caching** — feeds are cached for 6 hours in `~/.newsfeed/cache/` so startup is instant after the first load
- **Background loading** — feeds are fetched in threads; the UI stays responsive with a "Loading…" indicator
- **Force refresh** — press `r` to clear the cache and re-fetch everything

---

## Download (Windows — no Python needed)

1. Download **[newsfeed.exe](https://github.com/MattSelwood/news-feed/releases/download/v1.0.2/newsfeed.exe)** from the latest release
2. Double-click it to run
3. If Windows shows **"Windows protected your PC"**, click **More info → Run anyway** (the app is unsigned, not dangerous)

---

## Requirements (running from source)

- Python 3.8+
- `feedparser` and `requests` (see `requirements.txt`)

---

## Installation (from source)

```bash
git clone https://github.com/MattSelwood/news-feed.git
cd news-feed
pip install -r requirements.txt
```

---

## Usage

```bash
python -m newsfeed
```

---

## Keyboard shortcuts

| Key | Action |
|-----|--------|
| `↑` / `k` | Move up in article list |
| `↓` / `j` | Move down in article list |
| `←` / `Shift+Tab` | Previous category |
| `→` / `Tab` | Next category |
| `1` – `9` | Jump directly to a category |
| `Enter` | Toggle article detail pane |
| `o` | Open selected article URL in browser |
| `r` | Force refresh (clear cache + reload) |
| `PgUp` / `PgDn` | Scroll 10 articles at a time |
| `Home` / `End` | Jump to first / last article |
| `q` | Quit |

---

## Project layout

```
newsfeed/
├── __init__.py      version string
├── __main__.py      entry point  (python -m newsfeed)
├── config.py        feed definitions, cache settings, and weather location
├── fetcher.py       RSS fetching + Open-Meteo weather fetching, both with file-based caching
├── concepts.py      60+ daily math/stats/AI concept definitions
└── ui.py            curses-based terminal UI
tests/
└── test_newsfeed.py smoke tests (no network required)
requirements.txt
```

---

## Running tests

```bash
python tests/test_newsfeed.py
```
