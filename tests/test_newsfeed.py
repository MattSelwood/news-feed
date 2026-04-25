"""Smoke tests for NewsFeed — no network access required."""

import sys
import os
import json
import tempfile
import time
from datetime import date
from unittest.mock import patch, MagicMock

# Ensure the package is importable from the repo root
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# ---------------------------------------------------------------------------
# concepts.py
# ---------------------------------------------------------------------------

def test_concepts_list_nonempty():
    from newsfeed.concepts import CONCEPTS
    assert len(CONCEPTS) >= 50, "Expected at least 50 concepts"


def test_concepts_all_have_required_fields():
    from newsfeed.concepts import CONCEPTS
    required = {"title", "category", "equation", "overview"}
    for c in CONCEPTS:
        missing = required - c.keys()
        assert not missing, f"Concept '{c.get('title')}' is missing fields: {missing}"


def test_get_daily_concept_returns_concept():
    from newsfeed.concepts import get_daily_concept, CONCEPTS
    concept = get_daily_concept()
    assert concept in CONCEPTS


def test_get_daily_concept_cycles():
    from newsfeed.concepts import get_daily_concept, CONCEPTS
    day = date.today().timetuple().tm_yday
    expected = CONCEPTS[day % len(CONCEPTS)]
    assert get_daily_concept() == expected


# ---------------------------------------------------------------------------
# config.py
# ---------------------------------------------------------------------------

def test_categories_defined():
    from newsfeed.config import CATEGORIES
    assert len(CATEGORIES) == 9


def test_each_category_has_feeds():
    from newsfeed.config import CATEGORIES
    for cat in CATEGORIES:
        assert "feeds" in cat
        assert "name" in cat and "short" in cat and "key" in cat
        # RSS-backed categories must have at least one feed defined;
        # special tabs (concepts_tab, weather_tab) are allowed to have none.
        is_special = cat.get("concepts_tab") or cat.get("weather_tab")
        if not is_special:
            assert len(cat["feeds"]) >= 1, (
                f"Category '{cat['name']}' has no feeds and no special-tab flag"
            )
            for feed in cat["feeds"]:
                assert "name" in feed and "url" in feed


def test_math_ai_category_exists():
    from newsfeed.config import CATEGORIES
    math_cats = [c for c in CATEGORIES if "Math" in c["name"] or "AI" in c["name"]]
    assert len(math_cats) >= 1


# ---------------------------------------------------------------------------
# fetcher.py — cache helpers
# ---------------------------------------------------------------------------

def test_cache_roundtrip():
    from newsfeed import fetcher
    items = [{"title": "Test", "url": "https://example.com", "summary": "s",
              "source": "Test", "date": "", "is_concept": False}]

    with tempfile.TemporaryDirectory() as tmpdir:
        with patch.object(fetcher, "CACHE_DIR", tmpdir):
            url = "https://example.com/feed"
            # Nothing in cache yet
            assert fetcher._load_cache(url) is None
            # Save, then load
            fetcher._save_cache(url, items)
            loaded = fetcher._load_cache(url)
            assert loaded == items


def test_cache_respects_ttl():
    from newsfeed import fetcher
    items = [{"title": "Old", "url": "u", "summary": "", "source": "S",
              "date": "", "is_concept": False}]

    with tempfile.TemporaryDirectory() as tmpdir:
        with patch.object(fetcher, "CACHE_DIR", tmpdir):
            url = "https://example.com/feed2"
            fetcher._save_cache(url, items)
            cache_path = fetcher._cache_path(url)
            # Backdate the cache timestamp
            with open(cache_path) as fh:
                data = json.load(fh)
            data["timestamp"] = time.time() - (fetcher.CACHE_TTL_HOURS + 1) * 3600
            with open(cache_path, "w") as fh:
                json.dump(data, fh)
            # Should be considered stale
            assert fetcher._load_cache(url) is None


def test_strip_html():
    from newsfeed.fetcher import _strip_html
    assert _strip_html("<p>Hello <b>world</b></p>") == "Hello world"
    assert _strip_html("Plain text") == "Plain text"
    assert _strip_html("") == ""
    assert _strip_html(None) == ""


def test_fetch_feed_handles_network_error():
    """fetch_feed should return an empty list on failure."""
    from newsfeed import fetcher

    with tempfile.TemporaryDirectory() as tmpdir:
        with patch.object(fetcher, "CACHE_DIR", tmpdir):
            with patch("feedparser.parse", side_effect=Exception("network error")):
                result = fetcher.fetch_feed(
                    {"name": "Test", "url": "https://example.com/bad"}
                )
                assert result == []


def test_fetch_category_deduplication():
    """fetch_category should not return duplicate URLs."""
    from newsfeed import fetcher

    duplicate_item = {
        "title": "Dup", "url": "https://dup.com/article",
        "summary": "", "source": "S", "date": "", "is_concept": False,
    }
    feeds = [
        {"name": "Feed A", "url": "https://a.com/rss"},
        {"name": "Feed B", "url": "https://b.com/rss"},
    ]

    with tempfile.TemporaryDirectory() as tmpdir:
        with patch.object(fetcher, "CACHE_DIR", tmpdir):
            with patch.object(fetcher, "fetch_feed", return_value=[duplicate_item]):
                result = fetcher.fetch_category(feeds)
                assert len(result) == 1  # deduplicated


def test_clear_cache():
    from newsfeed import fetcher
    with tempfile.TemporaryDirectory() as tmpdir:
        with patch.object(fetcher, "CACHE_DIR", tmpdir):
            fetcher._save_cache("https://example.com/feed", [])
            assert len(os.listdir(tmpdir)) == 1
            fetcher.clear_cache()
            assert len(os.listdir(tmpdir)) == 0


# ---------------------------------------------------------------------------
# fetcher.py — weather
# ---------------------------------------------------------------------------

def test_weather_location_config():
    """WEATHER_LOCATION must have name, latitude, and longitude."""
    from newsfeed.config import WEATHER_LOCATION
    for key in ("name", "latitude", "longitude"):
        assert key in WEATHER_LOCATION, f"WEATHER_LOCATION missing '{key}'"
    assert isinstance(WEATHER_LOCATION["latitude"], float)
    assert isinstance(WEATHER_LOCATION["longitude"], float)


def test_weather_cache_ttl_config():
    from newsfeed.config import WEATHER_CACHE_TTL_HOURS
    assert 0 < WEATHER_CACHE_TTL_HOURS <= 24


def test_wmo_description_known_codes():
    from newsfeed.fetcher import wmo_description
    assert wmo_description(0) == "Clear sky"
    assert wmo_description(63) == "Moderate rain"
    assert wmo_description(95) == "Thunderstorm"


def test_wmo_description_unknown_code():
    from newsfeed.fetcher import wmo_description
    assert wmo_description(999) == "Unknown"
    assert wmo_description(None) == "Unknown"


def test_fetch_weather_handles_network_error():
    """fetch_weather should return None on any network failure."""
    from newsfeed import fetcher
    location = {"name": "Test", "latitude": 0.0, "longitude": 0.0}
    with tempfile.TemporaryDirectory() as tmpdir:
        with patch.object(fetcher, "CACHE_DIR", tmpdir):
            with patch.object(fetcher.requests, "get",
                              side_effect=Exception("network error")):
                result = fetcher.fetch_weather(location)
                assert result is None


def test_fetch_weather_caches_result():
    """fetch_weather should cache the response and return it on second call."""
    from newsfeed import fetcher

    fake_response = {
        "current": {
            "temperature_2m": 20.0,
            "relative_humidity_2m": 55,
            "apparent_temperature": 19.0,
            "weather_code": 0,
            "wind_speed_10m": 10.0,
        },
        "daily": {
            "time": ["2026-04-25", "2026-04-26", "2026-04-27"],
            "weather_code": [0, 2, 63],
            "temperature_2m_max": [22.0, 19.0, 15.0],
            "temperature_2m_min": [12.0, 10.0, 9.0],
            "precipitation_sum": [0.0, 0.5, 8.2],
            "wind_speed_10m_max": [12.0, 15.0, 25.0],
        },
    }

    mock_resp = MagicMock()
    mock_resp.json.return_value = fake_response
    mock_resp.raise_for_status.return_value = None

    location = {"name": "TestCity", "latitude": 51.0, "longitude": -0.1}

    with tempfile.TemporaryDirectory() as tmpdir:
        with patch.object(fetcher, "CACHE_DIR", tmpdir):
            with patch.object(fetcher.requests, "get", return_value=mock_resp) as mock_get:
                # First call — hits the network
                result1 = fetcher.fetch_weather(location)
                assert result1 is not None
                assert result1["location_name"] == "TestCity"
                assert mock_get.call_count == 1

                # Second call — should come from cache, no new network call
                result2 = fetcher.fetch_weather(location)
                assert result2 == result1
                assert mock_get.call_count == 1  # still 1


def test_fetch_weather_cache_ttl_respected():
    """Stale weather cache should be re-fetched."""
    from newsfeed import fetcher

    fake_response = {
        "current": {"temperature_2m": 15.0, "weather_code": 1,
                    "relative_humidity_2m": 60, "apparent_temperature": 14.0,
                    "wind_speed_10m": 8.0},
        "daily": {},
    }
    mock_resp = MagicMock()
    mock_resp.json.return_value = fake_response
    mock_resp.raise_for_status.return_value = None

    location = {"name": "StaleCity", "latitude": 52.0, "longitude": 0.1}

    with tempfile.TemporaryDirectory() as tmpdir:
        with patch.object(fetcher, "CACHE_DIR", tmpdir):
            with patch.object(fetcher.requests, "get", return_value=mock_resp):
                fetcher.fetch_weather(location)

            # Backdate the weather cache timestamp beyond TTL
            cache_file = fetcher._weather_cache_path(52.0, 0.1)
            with open(cache_file) as fh:
                cached = json.load(fh)
            cached["timestamp"] = (
                time.time() - (fetcher.WEATHER_CACHE_TTL_HOURS + 1) * 3600
            )
            with open(cache_file, "w") as fh:
                json.dump(cached, fh)

            with patch.object(fetcher.requests, "get",
                              return_value=mock_resp) as mock_get2:
                fetcher.fetch_weather(location)
                assert mock_get2.call_count == 1  # fetched again


# ---------------------------------------------------------------------------
# config.py — weather tab present
# ---------------------------------------------------------------------------

def test_weather_category_in_categories():
    from newsfeed.config import CATEGORIES
    weather_cats = [c for c in CATEGORIES if c.get("weather_tab")]
    assert len(weather_cats) == 1
    cat = weather_cats[0]
    assert cat["key"] == "9"
    assert cat["feeds"] == []

if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    passed = failed = 0
    for t in tests:
        try:
            t()
            print(f"  PASS  {t.__name__}")
            passed += 1
        except Exception as exc:
            print(f"  FAIL  {t.__name__}: {exc}")
            failed += 1
    print(f"\n{passed} passed, {failed} failed")
    if failed:
        sys.exit(1)
