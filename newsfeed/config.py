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
                "name": "Reuters",
                "url": "https://news.google.com/rss/search?q=site%3Areuters.com&hl=en-US&gl=US&ceid=US%3Aen",
            },
            {
                "name": "Al Jazeera",
                "url": "https://www.aljazeera.com/xml/rss/all.xml",
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
                "name": "The Economist",
                "url": "https://www.economist.com/finance-and-economics/rss.xml",
            },
            {
                "name": "Bloomberg Markets",
                "url": "https://feeds.bloomberg.com/markets/news.rss",
            },
            {
                "name": "Bloomberg Wealth",
                "url": "https://feeds.bloomberg.com/wealth/news.rss",
            },
            {
                "name": "Bloomberg Economics",
                "url": "https://feeds.bloomberg.com/economics/news.rss",
            }
        ],
    },
    {
        "name": "Technology",
        "short": "Tech",
        "key": "3",
        "feeds": [
            {
                "name": "Bloomberg Technology",
                "url": "https://feeds.bloomberg.com/technology/news.rss",
            },
            {
                "name": "Towards Data Science",
                "url": "https://towardsdatascience.com/feed",
            },
            {
                "name": "Google Research",
                "url": "http://googleresearch.blogspot.com/atom.xml",
            },
        ],
    },
    {
        "name": "Math / Stats / AI",
        "short": "AI Research",
        "key": "4",
        "feeds": [
            {
                "name": "arXiv: ML",
                "url": "https://arxiv.org/rss/cs.LG",
            },
            {
                "name": "arXiv: AI",
                "url": "https://arxiv.org/rss/cs.AI",
            },
            {
                "name": "arXiv: Statistics",
                "url": "https://arxiv.org/rss/stat.ML",
            },
        ],
        "daily_concept": False,
    },
    {
        "name": "Astrophysics",
        "short": "Astro",
        "key": "5",
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
        "key": "6",
        "feeds": [
            {
                "name": "HLTV",
                "url": "https://www.hltv.org/rss/news",
                "max_items": 50,
            },
            {
                "name": "CS2 - Community Feed",
                "url": "https://raw.githubusercontent.com/IceQ1337/CS-RSS-Feed/master/feeds/news-feed-en.xml",
            }
        ],
    },
    {
        "name": "Science/Tech",
        "short": "Science",
        "key": "7",
        "feeds": [
            {
                "name": "Nature",
                "url": "http://www.nature.com/nature/current_issue/rss",
            },
            {
                "name": "The Verge",
                "url": "https://www.theverge.com/rss/index.xml",
            },
            {
                "name": "Hacker News",
                "url": "https://news.ycombinator.com/rss",
            },
            {
                "name": "Singularity Hub",
                "url": "https://singularityhub.com/feed/",
            },
            {
                "name": "Wired",
                "url": "https://www.wired.com/feed/category/security/latest/rss",
            }

        ],
    },
    {
        "name": "Daily Facts",
        "short": "Facts",
        "key": "8",
        "feeds": [],
        "concepts_tab": True,
    },
    {
        "name": "Weather",
        "short": "Weather",
        "key": "9",
        "feeds": [],
        "weather_tab": True,
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

# ---------------------------------------------------------------------------
# Weather settings
# ---------------------------------------------------------------------------

# Default location shown in the Weather tab.
# Change latitude / longitude (and name) to your preferred city.
WEATHER_LOCATION = {
    "name": "London",
    "latitude": 51.5074,
    "longitude": -0.1278,
}

# How long before weather data is considered stale (hours)
WEATHER_CACHE_TTL_HOURS = 1
