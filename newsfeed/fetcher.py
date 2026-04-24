"""RSS feed fetching with file-based daily caching."""

import hashlib  # SHA-256 used for cache key generation
import json
import os
import re
import time

import feedparser

from .config import CACHE_DIR, CACHE_TTL_HOURS, MAX_ITEMS_PER_FEED

# feedparser user-agent — be polite
feedparser.USER_AGENT = "NewsFeed/1.0 +https://github.com/MattSelwood/news-feed"

# ---------------------------------------------------------------------------
# HTML stripping helpers
# ---------------------------------------------------------------------------

_HTML_TAG_RE = re.compile(r"<[^>]+>")
_WHITESPACE_RE = re.compile(r"\s+")


def _strip_html(text: str) -> str:
    """Remove HTML tags and normalise whitespace."""
    if not text:
        return ""
    text = _HTML_TAG_RE.sub(" ", text)
    text = _WHITESPACE_RE.sub(" ", text)
    return text.strip()


# ---------------------------------------------------------------------------
# Cache helpers
# ---------------------------------------------------------------------------


def _cache_path(url: str) -> str:
    key = hashlib.sha256(url.encode()).hexdigest()
    return os.path.join(CACHE_DIR, f"{key}.json")


def _load_cache(url: str):
    """Return cached items if they are still fresh, else None."""
    path = _cache_path(url)
    if not os.path.exists(path):
        return None
    try:
        with open(path) as fh:
            data = json.load(fh)
        age_hours = (time.time() - data["timestamp"]) / 3600
        if age_hours < CACHE_TTL_HOURS:
            return data["items"]
    except Exception:
        pass
    return None


def _save_cache(url: str, items: list) -> None:
    os.makedirs(CACHE_DIR, exist_ok=True)
    path = _cache_path(url)
    with open(path, "w") as fh:
        json.dump({"timestamp": time.time(), "items": items}, fh)


def clear_cache() -> None:
    """Delete all cached feed data so feeds are refreshed on next load."""
    if not os.path.isdir(CACHE_DIR):
        return
    for fname in os.listdir(CACHE_DIR):
        if fname.endswith(".json"):
            try:
                os.remove(os.path.join(CACHE_DIR, fname))
            except OSError:
                pass


# ---------------------------------------------------------------------------
# Public fetch API
# ---------------------------------------------------------------------------


def fetch_feed(feed: dict) -> list:
    """Fetch a single RSS feed and return a list of article dicts.

    Falls back to an empty list on any network or parse error.
    Results are cached for CACHE_TTL_HOURS hours.
    """
    url = feed["url"]
    name = feed["name"]

    cached = _load_cache(url)
    if cached is not None:
        return cached

    try:
        parsed = feedparser.parse(url)
        items = []
        for entry in parsed.entries[:MAX_ITEMS_PER_FEED]:
            summary = _strip_html(
                entry.get("summary", "") or entry.get("description", "")
            )
            date_str = (
                entry.get("published", "")
                or entry.get("updated", "")
                or ""
            )
            items.append(
                {
                    "title": _strip_html(entry.get("title", "No title")),
                    "url": entry.get("link", ""),
                    "summary": summary[:500],
                    "source": name,
                    "date": date_str[:32],
                    "is_concept": False,
                }
            )
        _save_cache(url, items)
        return items
    except Exception:
        return []


def fetch_category(feeds: list, status_callback=None) -> list:
    """Fetch all feeds for a category and return a combined, de-duplicated list."""
    all_items: list = []
    seen_urls: set = set()

    for feed in feeds:
        if status_callback:
            status_callback(f"Fetching {feed['name']}…")
        for item in fetch_feed(feed):
            url = item.get("url", "")
            if url and url in seen_urls:
                continue
            if url:
                seen_urls.add(url)
            all_items.append(item)

    return all_items
