"""Curses-based terminal UI for NewsFeed."""

import curses
import threading
import webbrowser
from datetime import datetime
from textwrap import wrap

from .config import CATEGORIES, WEATHER_LOCATION
from .concepts import get_daily_concept, get_daily_concepts_panel
from .fetcher import fetch_category, clear_cache, fetch_weather, wmo_description

# ---------------------------------------------------------------------------
# Colour pair indices
# ---------------------------------------------------------------------------
_C_HEADER = 1       # App title bar
_C_ACTIVE_TAB = 2   # Selected category tab
_C_INACTIVE_TAB = 3 # Unselected tab
_C_SELECTED = 4     # Highlighted article row
_C_SOURCE = 5       # Source name in article list (fallback)
_C_DATE = 6         # Date in article list
_C_CONCEPT_HDR = 7  # Daily Concept section header
_C_URL = 8          # URL in detail pane
_C_SEPARATOR = 9    # Separator lines
_C_FOOTER = 10      # Footer bar
_C_LOADING = 11     # Loading / status message
_C_ERROR = 12       # Error text

# Weather-specific colour pairs
_C_WEATHER_SUNNY  = 13   # Clear / sunny conditions
_C_WEATHER_CLOUDY = 14   # Cloudy / fog
_C_WEATHER_RAIN   = 15   # Rain / drizzle / showers
_C_WEATHER_SNOW   = 16   # Snow
_C_WEATHER_STORM  = 17   # Thunderstorm
_C_WEATHER_LABEL  = 18   # Weather section headers

# Source-specific colour pairs start at this index.
# We reserve _C_SRC_BASE … _C_SRC_BASE+_SRC_PALETTE_SIZE-1.
_C_SRC_BASE = 20
_SRC_PALETTE = [
    curses.COLOR_CYAN,
    curses.COLOR_GREEN,
    curses.COLOR_MAGENTA,
    curses.COLOR_YELLOW,
    curses.COLOR_RED,
    curses.COLOR_BLUE,
    curses.COLOR_WHITE,
]
_SRC_PALETTE_SIZE = len(_SRC_PALETTE)

# Map source name → assigned pair index (populated at draw time)
_source_pair_map: dict = {}
_src_pair_counter = [_C_SRC_BASE]   # mutable counter via list


def _source_color_pair(source: str, bg: int) -> int:
    """Return a stable curses color_pair number for *source*.

    Each unique source name gets one of the palette colours.  The mapping is
    deterministic within a session (first-seen order) and wraps around if
    there are more sources than palette entries.
    """
    if source not in _source_pair_map:
        pair_idx = _src_pair_counter[0]
        palette_fg = _SRC_PALETTE[(pair_idx - _C_SRC_BASE) % _SRC_PALETTE_SIZE]
        curses.init_pair(pair_idx, palette_fg, bg)
        _source_pair_map[source] = pair_idx
        _src_pair_counter[0] += 1
    return _source_pair_map[source]


def _safe_addstr(win, y: int, x: int, text: str, attr: int = 0) -> None:
    """Write text clipped to the window; silently ignore out-of-bounds errors."""
    max_y, max_x = win.getmaxyx()
    if y < 0 or y >= max_y or x < 0 or x >= max_x:
        return
    available = max_x - x - 1
    if available <= 0:
        return
    try:
        win.addstr(y, x, text[:available], attr)
    except curses.error:
        pass


def _hline(win, y: int, x: int, width: int, attr: int = 0) -> None:
    """Draw a horizontal line of dashes."""
    _safe_addstr(win, y, x, "─" * width, attr)


def _wmo_color_pair(code) -> int:
    """Return a curses attribute for a WMO weather interpretation code."""
    try:
        code = int(code)
    except (TypeError, ValueError):
        return curses.color_pair(_C_WEATHER_CLOUDY)
    if code <= 1:
        return curses.color_pair(_C_WEATHER_SUNNY)
    if code <= 3 or code in (45, 48):
        return curses.color_pair(_C_WEATHER_CLOUDY)
    if (51 <= code <= 67) or (80 <= code <= 82):
        return curses.color_pair(_C_WEATHER_RAIN)
    if (71 <= code <= 77) or (85 <= code <= 86):
        return curses.color_pair(_C_WEATHER_SNOW)
    if code >= 95:
        return curses.color_pair(_C_WEATHER_STORM)
    return curses.color_pair(_C_WEATHER_CLOUDY)


# ---------------------------------------------------------------------------
# Main application class
# ---------------------------------------------------------------------------


class NewsFeedApp:
    """Terminal UI for the NewsFeed application."""

    def __init__(self, stdscr: curses.window) -> None:
        self.stdscr = stdscr
        self._init_colors()
        curses.curs_set(0)
        stdscr.timeout(200)  # non-blocking getch with 200 ms timeout

        # State
        self.cat_idx: int = 0           # active category index (0–5)
        self.article_idx: int = 0       # selected article within active category
        self.scroll_offset: int = 0     # first visible article row
        self.show_detail: bool = False  # toggle detail pane
        self.status: str = ""           # transient status message

        # Per-category article cache: index → list[dict]
        self._articles: dict = {}
        # Weather data cache: index → dict (from fetch_weather)
        self._weather_data: dict = {}
        # Per-category loading flag
        self._loading: dict = {i: False for i in range(len(CATEGORIES))}

        self.daily_concept = get_daily_concept()

        # Kick off loading the first category immediately
        self._load_category(self.cat_idx)

    # ------------------------------------------------------------------
    # Colour initialisation
    # ------------------------------------------------------------------

    def _init_colors(self) -> None:
        curses.start_color()
        # use_default_colors() enables transparent background (bg=-1).
        # Not all terminals/builds support it, so fall back to black.
        try:
            curses.use_default_colors()
            _bg = -1
        except curses.error:
            _bg = curses.COLOR_BLACK
        # Pairs: (fg, bg)
        curses.init_pair(_C_HEADER,       curses.COLOR_BLACK,   curses.COLOR_CYAN)
        curses.init_pair(_C_ACTIVE_TAB,   curses.COLOR_BLACK,   curses.COLOR_YELLOW)
        curses.init_pair(_C_INACTIVE_TAB, curses.COLOR_CYAN,    _bg)
        curses.init_pair(_C_SELECTED,     curses.COLOR_BLACK,   curses.COLOR_GREEN)
        curses.init_pair(_C_SOURCE,       curses.COLOR_CYAN,    _bg)
        curses.init_pair(_C_DATE,         curses.COLOR_YELLOW,  _bg)
        curses.init_pair(_C_CONCEPT_HDR,  curses.COLOR_MAGENTA, _bg)
        curses.init_pair(_C_URL,          curses.COLOR_BLUE,    _bg)
        curses.init_pair(_C_SEPARATOR,    curses.COLOR_WHITE,   _bg)
        curses.init_pair(_C_FOOTER,       curses.COLOR_BLACK,   curses.COLOR_WHITE)
        curses.init_pair(_C_LOADING,      curses.COLOR_YELLOW,  _bg)
        curses.init_pair(_C_ERROR,        curses.COLOR_RED,     _bg)
        # Weather colours
        curses.init_pair(_C_WEATHER_SUNNY,  curses.COLOR_YELLOW,  _bg)
        curses.init_pair(_C_WEATHER_CLOUDY, curses.COLOR_WHITE,   _bg)
        curses.init_pair(_C_WEATHER_RAIN,   curses.COLOR_CYAN,    _bg)
        curses.init_pair(_C_WEATHER_SNOW,   curses.COLOR_BLUE,    _bg)
        curses.init_pair(_C_WEATHER_STORM,  curses.COLOR_RED,     _bg)
        curses.init_pair(_C_WEATHER_LABEL,  curses.COLOR_GREEN,   _bg)
        # Store bg so _source_color_pair can use it at draw time
        self._bg = _bg

    # ------------------------------------------------------------------
    # Background article loading
    # ------------------------------------------------------------------

    def _load_category(self, idx: int, force: bool = False) -> None:
        """Spawn a background thread to fetch articles for category *idx*."""
        if self._loading.get(idx) and not force:
            return

        self._loading[idx] = True
        cat = CATEGORIES[idx]

        def _worker() -> None:
            # Concepts-only tab: show one fact per discipline, no RSS feeds
            if cat.get("concepts_tab"):
                today = datetime.today().strftime("%b %d")
                items = [
                    {
                        "title": f"★ {c['category']}: {c['title']}",
                        "source": c["category"],
                        "date": today,
                        "summary": f"{c['equation']}\n\n{c['overview']}",
                        "url": "",
                        "is_concept": True,
                    }
                    for c in get_daily_concepts_panel()
                ]
                self._articles[idx] = items
                self._loading[idx] = False
                self._set_status(f"Loaded {len(items)} daily facts")
                return

            # Weather tab: fetch from Open-Meteo API
            if cat.get("weather_tab"):
                self._set_status(f"Fetching weather for {WEATHER_LOCATION['name']}…")
                data = fetch_weather(WEATHER_LOCATION)
                self._weather_data[idx] = data
                self._loading[idx] = False
                if data is not None:
                    self._set_status(
                        f"Loaded weather for {WEATHER_LOCATION['name']}"
                    )
                else:
                    self._set_status("Weather fetch failed — check connection")
                return

            items = fetch_category(cat["feeds"], status_callback=self._set_status)

            # Prepend Daily Concept as a special article for the Math/AI category
            if cat.get("daily_concept"):
                concept = self.daily_concept
                items = [
                    {
                        "title": f"★ Daily Concept: {concept['title']}",
                        "source": concept["category"],
                        "date": datetime.today().strftime("%b %d"),
                        "summary": (
                            f"{concept['equation']}\n\n{concept['overview']}"
                        ),
                        "url": "",
                        "is_concept": True,
                    }
                ] + items

            self._articles[idx] = items
            self._loading[idx] = False
            self._set_status(
                f"Loaded {len(items)} items for {cat['name']}"
            )

        t = threading.Thread(target=_worker, daemon=True)
        t.start()

    def _set_status(self, msg: str) -> None:
        self.status = msg

    # ------------------------------------------------------------------
    # Article accessors
    # ------------------------------------------------------------------

    def _current_articles(self) -> list:
        return self._articles.get(self.cat_idx, [])

    def _current_article(self):
        articles = self._current_articles()
        if not articles:
            return None
        idx = min(self.article_idx, len(articles) - 1)
        return articles[idx]

    # ------------------------------------------------------------------
    # Drawing helpers
    # ------------------------------------------------------------------

    def _draw_header(self, max_y: int, max_x: int) -> int:
        """Draw title bar. Returns next row index."""
        date_str = datetime.today().strftime("%A, %d %B %Y")
        title = " NewsFeed"
        min_width = len(title) + len(date_str) + 3
        if max_x >= min_width:
            bar = title.ljust(max_x - len(date_str) - 2) + date_str + " "
        else:
            bar = title
        _safe_addstr(self.stdscr, 0, 0, bar[:max_x], curses.color_pair(_C_HEADER) | curses.A_BOLD)
        return 1

    def _draw_tabs(self, row: int, max_x: int) -> int:
        """Draw category tab bar. Returns next row index."""
        x = 0
        self.stdscr.move(row, 0)
        self.stdscr.clrtoeol()
        for i, cat in enumerate(CATEGORIES):
            label = f" [{cat['key']}] {cat['short']} "
            loading = self._loading.get(i, False)
            if loading:
                label = f" [{cat['key']}] {cat['short']}… "
            if i == self.cat_idx:
                attr = curses.color_pair(_C_ACTIVE_TAB) | curses.A_BOLD
            else:
                attr = curses.color_pair(_C_INACTIVE_TAB)
            _safe_addstr(self.stdscr, row, x, label, attr)
            x += len(label)
            if i < len(CATEGORIES) - 1:
                _safe_addstr(self.stdscr, row, x, " │", curses.color_pair(_C_SEPARATOR))
                x += 2
        return row + 1

    def _draw_separator(self, row: int, max_x: int) -> int:
        _safe_addstr(
            self.stdscr, row, 0,
            "─" * max_x,
            curses.color_pair(_C_SEPARATOR)
        )
        return row + 1

    def _format_date(self, raw: str) -> str:
        """Convert RSS date string to a short display form."""
        for fmt in (
            "%a, %d %b %Y %H:%M:%S %z",
            "%a, %d %b %Y %H:%M:%S %Z",
            "%Y-%m-%dT%H:%M:%S%z",
            "%Y-%m-%dT%H:%M:%SZ",
            "%d %b %Y",
        ):
            try:
                dt = datetime.strptime(raw.strip(), fmt)
                return dt.strftime("%b %d")
            except (ValueError, AttributeError):
                continue
        # If parsing fails, return up to first 6 chars as a fallback
        return raw[:6].strip() if raw else ""

    def _draw_article_list(self, start_row: int, end_row: int, max_x: int) -> None:
        """Render the scrollable article list between start_row and end_row."""
        articles = self._current_articles()
        visible_height = end_row - start_row

        # Nothing to show yet
        if not articles:
            if self._loading.get(self.cat_idx):
                msg = "  Loading feeds…"
                _safe_addstr(
                    self.stdscr, start_row, 0, msg,
                    curses.color_pair(_C_LOADING) | curses.A_BOLD
                )
            else:
                _safe_addstr(
                    self.stdscr, start_row, 0,
                    "  No articles — press r to refresh.",
                    curses.color_pair(_C_ERROR)
                )
            return

        # Clamp indices
        self.article_idx = max(0, min(self.article_idx, len(articles) - 1))

        # Adjust scroll offset so selected item is visible
        if self.article_idx < self.scroll_offset:
            self.scroll_offset = self.article_idx
        elif self.article_idx >= self.scroll_offset + visible_height:
            self.scroll_offset = self.article_idx - visible_height + 1

        # Source column width
        src_col = 16

        for row_offset in range(visible_height):
            art_idx = self.scroll_offset + row_offset
            screen_row = start_row + row_offset

            if art_idx >= len(articles):
                # Clear any stale content
                self.stdscr.move(screen_row, 0)
                self.stdscr.clrtoeol()
                continue

            art = articles[art_idx]
            is_selected = art_idx == self.article_idx

            # Date
            date_str = self._format_date(art.get("date", ""))
            date_col = 6  # "Mmm DD"
            # Source
            src = art.get("source", "")[:src_col - 1].ljust(src_col)
            # Title fills the rest
            title_width = max_x - src_col - date_col - 4
            title = art.get("title", "")[:title_width]

            if art.get("is_concept"):
                base_attr = curses.color_pair(_C_CONCEPT_HDR) | curses.A_BOLD
            else:
                base_attr = 0

            if is_selected:
                sel_attr = curses.color_pair(_C_SELECTED) | curses.A_BOLD
                _safe_addstr(self.stdscr, screen_row, 0, " ▶ ", sel_attr)
                _safe_addstr(self.stdscr, screen_row, 3, title.ljust(title_width), sel_attr)
                _safe_addstr(
                    self.stdscr, screen_row, 3 + title_width,
                    f"  {src[:src_col]}",
                    sel_attr
                )
                _safe_addstr(
                    self.stdscr, screen_row, 3 + title_width + 2 + src_col,
                    date_str,
                    sel_attr
                )
            else:
                src_name = art.get("source", "")
                src_pair = curses.color_pair(
                    _source_color_pair(src_name, self._bg)
                )
                _safe_addstr(self.stdscr, screen_row, 0, "   ", 0)
                _safe_addstr(self.stdscr, screen_row, 3, title.ljust(title_width), base_attr)
                _safe_addstr(
                    self.stdscr, screen_row, 3 + title_width,
                    f"  {src[:src_col]}",
                    src_pair
                )
                _safe_addstr(
                    self.stdscr, screen_row, 3 + title_width + 2 + src_col,
                    date_str,
                    curses.color_pair(_C_DATE)
                )

    def _draw_detail(self, start_row: int, end_row: int, max_x: int) -> None:
        """Render the article detail pane."""
        art = self._current_article()
        row = start_row

        if art is None:
            return

        is_concept = art.get("is_concept", False)

        # Clear pane
        for r in range(start_row, end_row):
            self.stdscr.move(r, 0)
            self.stdscr.clrtoeol()

        # Title
        title = art.get("title", "")
        title_attr = (
            curses.color_pair(_C_CONCEPT_HDR) | curses.A_BOLD
            if is_concept
            else curses.A_BOLD
        )
        for line in wrap(title, max_x - 2):
            if row >= end_row:
                break
            _safe_addstr(self.stdscr, row, 1, line, title_attr)
            row += 1

        # Source / date line
        src_name = art.get('source', '')
        meta = f"{src_name}  ·  {art.get('date', '')}"
        if row < end_row:
            src_pair = curses.color_pair(_source_color_pair(src_name, self._bg))
            _safe_addstr(self.stdscr, row, 1, meta, src_pair)
            row += 1

        if row < end_row:
            _safe_addstr(self.stdscr, row, 1, "─" * (max_x - 2), curses.color_pair(_C_SEPARATOR))
            row += 1

        # Summary / overview
        summary = art.get("summary", "")
        if summary:
            for line in wrap(summary, max_x - 2):
                if row >= end_row:
                    break
                _safe_addstr(self.stdscr, row, 1, line)
                row += 1
            row += 1  # blank line after summary

        # URL
        url = art.get("url", "")
        if url and row < end_row:
            url_label = f"URL: {url}"
            _safe_addstr(self.stdscr, row, 1, url_label[:max_x - 2],
                         curses.color_pair(_C_URL))
            row += 1
        if row < end_row:
            _safe_addstr(
                self.stdscr, row, 1,
                "Press 'o' to open in browser" if url else "(no URL — Daily Concept)",
                curses.color_pair(_C_DATE)
            )

    def _draw_footer(self, row: int, max_x: int) -> None:
        """Draw keyboard-shortcut footer."""
        shortcuts = (
            " ↑↓/jk: Navigate  ←→/Tab: Category  Enter: Detail  "
            "o: Open  r: Refresh  q: Quit "
        )
        bar = shortcuts.ljust(max_x)[:max_x]
        _safe_addstr(self.stdscr, row, 0, bar, curses.color_pair(_C_FOOTER) | curses.A_BOLD)

    def _draw_weather_tab(self, start_row: int, end_row: int, max_x: int) -> None:
        """Render the weather dashboard for the Weather tab."""
        row = start_row
        idx = self.cat_idx

        # Clear the area
        for r in range(start_row, end_row):
            self.stdscr.move(r, 0)
            self.stdscr.clrtoeol()

        # Loading state
        if self._loading.get(idx):
            _safe_addstr(
                self.stdscr, row, 0,
                f"  Fetching weather for {WEATHER_LOCATION['name']}…",
                curses.color_pair(_C_LOADING) | curses.A_BOLD,
            )
            return

        data = self._weather_data.get(idx)

        # Error / no data state
        if data is None:
            _safe_addstr(
                self.stdscr, row, 0,
                "  Could not fetch weather data. "
                "Check your connection and press r to retry.",
                curses.color_pair(_C_ERROR),
            )
            return

        current = data.get("current", {})
        daily = data.get("daily", {})
        location_name = data.get("location_name", "")

        # ── Current conditions ─────────────────────────────────────────
        code = current.get("weather_code", 0)
        desc = wmo_description(code)
        temp = current.get("temperature_2m")
        feels = current.get("apparent_temperature")
        humidity = current.get("relative_humidity_2m")
        wind = current.get("wind_speed_10m")

        def _fmt(val, unit="", decimals=1):
            if val is None:
                return "N/A"
            try:
                fmt = f"{float(val):.{decimals}f}{unit}"
                return fmt
            except (TypeError, ValueError):
                return str(val)

        # Location + condition headline
        headline = f"  {location_name.upper()}  —  {desc}  —  {_fmt(temp, '°C')}"
        if row < end_row:
            _safe_addstr(
                self.stdscr, row, 0,
                headline[:max_x - 1],
                curses.color_pair(_C_WEATHER_LABEL) | curses.A_BOLD,
            )
            row += 1

        if row < end_row:
            _hline(self.stdscr, row, 0, max_x, curses.color_pair(_C_SEPARATOR))
            row += 1

        label_w = 18
        details = [
            ("  Conditions:",    desc,                           _wmo_color_pair(code)),
            ("  Temperature:",   f"{_fmt(temp, '°C')}   "
                                 f"(feels like {_fmt(feels, '°C')})",
                                 _wmo_color_pair(code)),
            ("  Humidity:",      f"{_fmt(humidity, '%', 0)}",    curses.color_pair(_C_WEATHER_RAIN)),
            ("  Wind speed:",    f"{_fmt(wind, ' km/h', 1)}",    curses.color_pair(_C_WEATHER_CLOUDY)),
        ]
        for label, value, attr in details:
            if row >= end_row:
                break
            _safe_addstr(self.stdscr, row, 0, label.ljust(label_w), curses.A_BOLD)
            _safe_addstr(self.stdscr, row, label_w, value[:max_x - label_w - 1], attr)
            row += 1

        row += 1  # blank line

        # ── 5-Day Forecast ─────────────────────────────────────────────
        if row < end_row:
            _safe_addstr(
                self.stdscr, row, 0, "  5-DAY FORECAST",
                curses.color_pair(_C_WEATHER_LABEL) | curses.A_BOLD,
            )
            row += 1

        if row < end_row:
            _hline(self.stdscr, row, 0, max_x, curses.color_pair(_C_SEPARATOR))
            row += 1

        # Column headers
        if row < end_row:
            col_hdr = (
                f"  {'Date':<13}{'Condition':<18}"
                f"{'High':>7}{'Low':>7}{'Rain':>8}{'Wind':>11}"
            )
            _safe_addstr(
                self.stdscr, row, 0, col_hdr[:max_x - 1],
                curses.A_BOLD | curses.A_UNDERLINE,
            )
            row += 1

        times = daily.get("time", [])
        codes = daily.get("weather_code", [])
        maxts = daily.get("temperature_2m_max", [])
        mints = daily.get("temperature_2m_min", [])
        precs = daily.get("precipitation_sum", [])
        winds = daily.get("wind_speed_10m_max", [])

        # Index 0 is today — skip it (already shown in Current Conditions)
        for i in range(1, min(6, len(times))):
            if row >= end_row:
                break
            try:
                day_date = datetime.strptime(times[i], "%Y-%m-%d")
                day_str = day_date.strftime("%a %b %d")
            except (ValueError, IndexError):
                day_str = times[i] if i < len(times) else "?"

            day_code = codes[i] if i < len(codes) else 0
            day_desc = wmo_description(day_code)
            mx = f"{float(maxts[i]):.0f}°C" if i < len(maxts) and maxts[i] is not None else "N/A"
            mn = f"{float(mints[i]):.0f}°C" if i < len(mints) and mints[i] is not None else "N/A"
            pr = f"{float(precs[i]):.1f}mm" if i < len(precs) and precs[i] is not None else "N/A"
            wn = f"{float(winds[i]):.0f}km/h" if i < len(winds) and winds[i] is not None else "N/A"

            line = (
                f"  {day_str:<13}{day_desc:<18}"
                f"{mx:>7}{mn:>7}{pr:>8}{wn:>11}"
            )
            _safe_addstr(
                self.stdscr, row, 0, line[:max_x - 1],
                _wmo_color_pair(day_code),
            )
            row += 1

        if row < end_row:
            _hline(self.stdscr, row, 0, max_x, curses.color_pair(_C_SEPARATOR))
            row += 1

        if row < end_row:
            note = "  Data: Open-Meteo API (open-meteo.com) · Cached 1 hour · Press r to refresh"
            _safe_addstr(
                self.stdscr, row, 0, note[:max_x - 1],
                curses.color_pair(_C_DATE),
            )

    def _draw_status(self, row: int, max_x: int) -> None:
        """Draw transient status message row."""
        if self.status:
            msg = f" {self.status}"
            _safe_addstr(self.stdscr, row, 0, msg[:max_x - 1],
                         curses.color_pair(_C_LOADING))

    # ------------------------------------------------------------------
    # Full redraw
    # ------------------------------------------------------------------

    def draw(self) -> None:
        max_y, max_x = self.stdscr.getmaxyx()
        self.stdscr.erase()

        # ── Row 0 : Header ─────────────────────────────────────────────
        row = self._draw_header(max_y, max_x)
        # ── Row 1 : Category tabs ──────────────────────────────────────
        row = self._draw_tabs(row, max_x)
        # ── Row 2 : Separator ──────────────────────────────────────────
        row = self._draw_separator(row, max_x)

        # Footer is always the last row
        footer_row = max_y - 1
        # Status row sits just above the footer
        status_row = max_y - 2

        if CATEGORIES[self.cat_idx].get("weather_tab"):
            self._draw_weather_tab(row, status_row, max_x)
        elif self.show_detail:
            # Split: list takes top 55%, detail takes remaining space
            list_height = max(4, int((max_y - row - 2) * 0.55))
            list_end = row + list_height
            sep_row = list_end
            detail_start = sep_row + 1
            detail_end = status_row

            self._draw_article_list(row, list_end, max_x)
            self._draw_separator(sep_row, max_x)
            if detail_start < detail_end:
                self._draw_detail(detail_start, detail_end, max_x)
        else:
            list_end = status_row
            self._draw_article_list(row, list_end, max_x)

        self._draw_status(status_row, max_x)
        self._draw_footer(footer_row, max_x)

        self.stdscr.refresh()

    # ------------------------------------------------------------------
    # Input handling
    # ------------------------------------------------------------------

    def _handle_key(self, key: int) -> bool:
        """Process a single keystroke. Returns False to quit."""
        articles = self._current_articles()
        n = len(articles)

        # ── Quit ───────────────────────────────────────────────────────
        if key in (ord("q"), ord("Q")):
            return False

        # ── Category navigation ────────────────────────────────────────
        elif key in (curses.KEY_RIGHT, ord("\t"), ord("l")):
            self._switch_category((self.cat_idx + 1) % len(CATEGORIES))
        elif key in (curses.KEY_LEFT, curses.KEY_BTAB):
            self._switch_category((self.cat_idx - 1) % len(CATEGORIES))
        elif key in (ord("1"), ord("2"), ord("3"),
                     ord("4"), ord("5"), ord("6"),
                     ord("7"), ord("8"), ord("9")):
            self._switch_category(key - ord("1"))

        # ── Article navigation ─────────────────────────────────────────
        elif key in (curses.KEY_DOWN, ord("j")):
            if n:
                self.article_idx = min(self.article_idx + 1, n - 1)
        elif key in (curses.KEY_UP, ord("k")):
            if n:
                self.article_idx = max(self.article_idx - 1, 0)
        elif key == curses.KEY_PPAGE:   # Page Up
            if n:
                self.article_idx = max(self.article_idx - 10, 0)
        elif key == curses.KEY_NPAGE:   # Page Down
            if n:
                self.article_idx = min(self.article_idx + 10, n - 1)
        elif key == curses.KEY_HOME:
            self.article_idx = 0
            self.scroll_offset = 0
        elif key == curses.KEY_END:
            self.article_idx = max(0, n - 1)

        # ── Toggle detail pane ─────────────────────────────────────────
        elif key in (ord("\n"), ord("\r"), curses.KEY_ENTER):
            if n:
                self.show_detail = not self.show_detail

        # ── Open URL in browser ────────────────────────────────────────
        elif key in (ord("o"), ord("O")):
            art = self._current_article()
            if art:
                url = art.get("url", "")
                if url:
                    webbrowser.open(url)
                    self._set_status(f"Opening: {url[:60]}")

        # ── Refresh (force re-fetch) ───────────────────────────────────
        elif key in (ord("r"), ord("R")):
            clear_cache()
            self._articles.clear()
            self._weather_data.clear()
            self._set_status("Cache cleared — reloading all categories…")
            for i in range(len(CATEGORIES)):
                self._loading[i] = False
            self._load_category(self.cat_idx, force=True)
            self.article_idx = 0
            self.scroll_offset = 0
            self.show_detail = False

        return True

    def _switch_category(self, new_idx: int) -> None:
        """Switch to category *new_idx*, triggering a load if needed."""
        self.cat_idx = new_idx
        self.article_idx = 0
        self.scroll_offset = 0
        self.show_detail = False
        if new_idx not in self._articles:
            self._load_category(new_idx)

    # ------------------------------------------------------------------
    # Main event loop
    # ------------------------------------------------------------------

    def run(self) -> None:
        """Enter the main draw / input loop."""
        while True:
            self.draw()
            key = self.stdscr.getch()
            if key != curses.ERR and not self._handle_key(key):
                break


# ---------------------------------------------------------------------------
# Entry point helper
# ---------------------------------------------------------------------------


def launch() -> None:
    """Initialise curses and run the app, cleaning up on exit."""
    def _main(stdscr: curses.window) -> None:
        app = NewsFeedApp(stdscr)
        app.run()

    try:
        curses.wrapper(_main)
    except KeyboardInterrupt:
        pass
    except curses.error as exc:
        if "Redirection is not supported" in str(exc):
            import sys
            print(
                "\n[NewsFeed] curses error: cannot open a proper console window.\n"
                "  • In Git Bash / mintty, prefix the command with winpty:\n"
                "      winpty python -m newsfeed\n"
                "  • Or run in Windows Terminal, PowerShell, or cmd.exe instead.\n",
                file=sys.stderr,
            )
            sys.exit(1)
        raise
