"""Feed configurations and application settings."""

import os

# ---------------------------------------------------------------------------
# Category / feed definitions
# ---------------------------------------------------------------------------
# Each category has a list of RSS feed sources.
# The "daily_concept" flag on the last category causes the Daily Concept widget
# to be prepended to that category's article list.
# ---------------------------------------------------------------------------

CATEGORIES = [
    {
        "name": "World News",
        "short": "World",
        "key": "1",
        "feeds": [
            {
                "name": "BBC World",
                "url": "https://feeds.bbci.co.uk/news/world/rss.xml",
            },
            {
                "name": "Al Jazeera",
                "url": "https://www.aljazeera.com/xml/rss/all.xml",
            },
            {
                "name": "Reuters",
                "url": "https://feeds.reuters.com/reuters/worldNews",
            },
        ],
    },
    {
        "name": "Finance",
        "short": "Finance",
        "key": "2",
        "feeds": [
            {
                "name": "CNBC",
                "url": "https://www.cnbc.com/id/100003114/device/rss/rss.html",
            },
            {
                "name": "MarketWatch",
                "url": "http://feeds.marketwatch.com/marketwatch/topstories/",
            },
            {
                "name": "Yahoo Finance",
                "url": "https://finance.yahoo.com/news/rssindex",
            },
        ],
    },
    {
        "name": "Astrophysics",
        "short": "Astro",
        "key": "3",
        "feeds": [
            {
                "name": "arXiv: Galaxies",
                "url": "https://arxiv.org/rss/astro-ph.GA",
            },
            {
                "name": "arXiv: High Energy",
                "url": "https://arxiv.org/rss/astro-ph.HE",
            },
            {
                "name": "NASA News",
                "url": "https://www.nasa.gov/news-release/feed/",
            },
        ],
    },
    {
        "name": "Counter-Strike 2",
        "short": "CS2",
        "key": "4",
        "feeds": [
            {
                "name": "HLTV",
                "url": "https://www.hltv.org/rss/news",
            },
            {
                "name": "r/GlobalOffensive",
                "url": "https://www.reddit.com/r/GlobalOffensive/.rss?limit=20",
            },
            {
                "name": "r/cs2",
                "url": "https://www.reddit.com/r/cs2/.rss?limit=20",
            },
        ],
    },
    {
        "name": "Software Dev",
        "short": "Dev",
        "key": "5",
        "feeds": [
            {
                "name": "Hacker News",
                "url": "https://news.ycombinator.com/rss",
            },
            {
                "name": "GitHub Blog",
                "url": "https://github.blog/feed/",
            },
            {
                "name": "Lobsters",
                "url": "https://lobste.rs/rss",
            },
        ],
    },
    {
        "name": "Math / Stats / AI",
        "short": "Math/AI",
        "key": "6",
        "feeds": [
            {
                "name": "arXiv: ML",
                "url": "https://arxiv.org/rss/cs.LG",
            },
            {
                "name": "arXiv: Statistics",
                "url": "https://arxiv.org/rss/stat.ML",
            },
            {
                "name": "arXiv: AI",
                "url": "https://arxiv.org/rss/cs.AI",
            },
        ],
        "daily_concept": True,
    },
]

# ---------------------------------------------------------------------------
# Cache settings
# ---------------------------------------------------------------------------

# Cache directory — stored in the user's home directory
CACHE_DIR = os.path.expanduser("~/.newsfeed/cache")

# How long before cached results are considered stale (hours)
CACHE_TTL_HOURS = 6

# Maximum number of items to keep from each individual feed
MAX_ITEMS_PER_FEED = 20
