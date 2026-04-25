"""RSS feed fetching with file-based daily caching."""

import hashlib  # SHA-256 used for cache key generation
import json
import os
import re
import time

import feedparser
import requests

from .config import CACHE_DIR, CACHE_TTL_HOURS, MAX_ITEMS_PER_FEED, WEATHER_CACHE_TTL_HOURS

# feedparser user-agent — be polite
feedparser.USER_AGENT = "NewsFeed/1.0 +https://github.com/MattSelwood/news-feed"

# ---------------------------------------------------------------------------
# HTML stripping helpers
# ---------------------------------------------------------------------------

_HTML_TAG_RE = re.compile(r"<[^>]+>")
_WHITESPACE_RE = re.compile(r"\s+")


_ARXIV_PREAMBLE_RE = re.compile(
    r"^arXiv:\S+\s+Announce\s+Type:\s+\S+\s+Abstract:\s*", re.IGNORECASE
)


def _clean_summary(text: str) -> str:
    """Remove arXiv announce preamble and return the cleaned summary."""
    return _ARXIV_PREAMBLE_RE.sub("", text).strip()


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
        limit = feed.get("max_items", MAX_ITEMS_PER_FEED)
        items = []
        for entry in parsed.entries[:limit]:
            summary = _clean_summary(_strip_html(
                entry.get("summary", "") or entry.get("description", "")
            ))
            date_str = (
                entry.get("published", "")
                or entry.get("updated", "")
                or ""
            )
            # Use the pre-parsed time struct when available for reliable sorting
            parsed_time = (
                entry.get("published_parsed")
                or entry.get("updated_parsed")
            )
            pub_timestamp = time.mktime(parsed_time) if parsed_time else 0.0
            items.append(
                {
                    "title": _strip_html(entry.get("title", "No title")),
                    "url": entry.get("link", ""),
                    "summary": summary,
                    "source": name,
                    "date": date_str[:32],
                    "pub_timestamp": pub_timestamp,
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

    # Sort newest-first; items with no timestamp (0.0) sink to the bottom
    all_items.sort(key=lambda x: x.get("pub_timestamp", 0.0), reverse=True)

    return all_items


# ---------------------------------------------------------------------------
# Weather fetch (Open-Meteo)
# ---------------------------------------------------------------------------

# WMO weather interpretation code → human-readable description
_WMO_DESC: dict = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    71: "Slight snow",
    73: "Moderate snow",
    75: "Heavy snow",
    77: "Snow grains",
    80: "Slight showers",
    81: "Moderate showers",
    82: "Violent showers",
    85: "Snow showers",
    86: "Heavy snow showers",
    95: "Thunderstorm",
    96: "Thunderstorm + hail",
    99: "Thunderstorm + hail",
}


def wmo_description(code) -> str:
    """Return a human-readable string for a WMO weather code."""
    try:
        return _WMO_DESC.get(int(code), "Unknown")
    except (TypeError, ValueError):
        return "Unknown"


def _weather_cache_path(lat: float, lon: float) -> str:
    key = f"weather_{lat}_{lon}"
    return os.path.join(CACHE_DIR, f"{hashlib.sha256(key.encode()).hexdigest()}.json")


def fetch_weather(location: dict):
    """Fetch current conditions and a 6-day forecast from Open-Meteo.

    Args:
        location: dict with ``name``, ``latitude``, and ``longitude`` keys.

    Returns:
        A dict with ``location_name``, ``current``, and ``daily`` sub-dicts,
        or ``None`` on any network / parse error.  Results are cached for
        ``WEATHER_CACHE_TTL_HOURS`` hours.
    """
    lat = location["latitude"]
    lon = location["longitude"]
    cache_path = _weather_cache_path(lat, lon)

    # Return cached data if still fresh
    if os.path.exists(cache_path):
        try:
            with open(cache_path) as fh:
                cached = json.load(fh)
            age_hours = (time.time() - cached["timestamp"]) / 3600
            if age_hours < WEATHER_CACHE_TTL_HOURS:
                return cached["data"]
        except Exception:
            pass

    # Fetch from Open-Meteo (no API key required)
    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}"
        "&current=temperature_2m,relative_humidity_2m,apparent_temperature,"
        "weather_code,wind_speed_10m"
        "&hourly=temperature_2m,weather_code,precipitation_probability,wind_speed_10m"
        "&daily=weather_code,temperature_2m_max,temperature_2m_min,"
        "precipitation_sum,wind_speed_10m_max"
        "&timezone=auto&forecast_days=6"
    )
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        raw = resp.json()
        data = {
            "location_name": location.get("name", ""),
            "current": raw.get("current", {}),
            "hourly": raw.get("hourly", {}),
            "daily": raw.get("daily", {}),
        }
        os.makedirs(CACHE_DIR, exist_ok=True)
        with open(cache_path, "w") as fh:
            json.dump({"timestamp": time.time(), "data": data}, fh)
        return data
    except Exception:
        return None
