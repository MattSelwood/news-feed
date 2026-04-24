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
    assert len(CATEGORIES) == 6


def test_each_category_has_feeds():
    from newsfeed.config import CATEGORIES
    for cat in CATEGORIES:
        assert "feeds" in cat and len(cat["feeds"]) >= 1
        assert "name" in cat and "short" in cat and "key" in cat
        for feed in cat["feeds"]:
            assert "name" in feed and "url" in feed


def test_math_ai_category_has_daily_concept_flag():
    from newsfeed.config import CATEGORIES
    math_cats = [c for c in CATEGORIES if c.get("daily_concept")]
    assert len(math_cats) == 1
    assert "Math" in math_cats[0]["name"] or "AI" in math_cats[0]["name"]


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
# Run
# ---------------------------------------------------------------------------

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
