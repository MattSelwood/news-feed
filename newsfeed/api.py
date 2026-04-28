"""FastAPI backend for the NewsFeed PWA."""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
import os

from .config import CATEGORIES, WEATHER_LOCATION
from .fetcher import fetch_category, fetch_weather
from .concepts import get_daily_concept

app = FastAPI(title="NewsFeed API", version="1.0.0")


@app.get("/api/categories")
def get_categories():
    """Return the list of category metadata (index, name, short, key, flags)."""
    result = []
    for idx, cat in enumerate(CATEGORIES):
        result.append(
            {
                "index": idx,
                "name": cat["name"],
                "short": cat["short"],
                "key": cat["key"],
                "concepts_tab": bool(cat.get("concepts_tab")),
                "weather_tab": bool(cat.get("weather_tab")),
            }
        )
    return result


@app.get("/api/feed/{index}")
def get_feed(index: int):
    """Fetch and return articles for the category at *index*."""
    if index < 0 or index >= len(CATEGORIES):
        raise HTTPException(status_code=404, detail="Category not found")

    cat = CATEGORIES[index]

    if cat.get("weather_tab"):
        raise HTTPException(
            status_code=400,
            detail="Use /api/weather for the weather tab",
        )

    if cat.get("concepts_tab"):
        raise HTTPException(
            status_code=400,
            detail="Use /api/concept for the concepts tab",
        )

    articles = fetch_category(cat["feeds"])
    return {"category": cat["name"], "articles": articles}


@app.get("/api/weather")
def get_weather():
    """Return current weather and 6-day forecast."""
    data = fetch_weather(WEATHER_LOCATION)
    if data is None:
        raise HTTPException(status_code=503, detail="Weather data unavailable")
    return data


@app.get("/api/concept")
def get_concept():
    """Return today's daily concept."""
    return get_daily_concept()


# ---------------------------------------------------------------------------
# Static files — must be mounted last so API routes take priority
# ---------------------------------------------------------------------------

_static_dir = os.path.join(os.path.dirname(__file__), "..", "static")
_static_dir = os.path.normpath(_static_dir)

if os.path.isdir(_static_dir):
    app.mount("/", StaticFiles(directory=_static_dir, html=True), name="static")
