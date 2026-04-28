/* ============================================================
   NewsFeed PWA — Vanilla JS SPA
   Handles: tab rendering, article list, detail panel,
            weather display, daily concept display,
            service worker registration.
============================================================ */

"use strict";

// ---------------------------------------------------------------------------
// Tab icon mapping
// ---------------------------------------------------------------------------
const TAB_ICONS = {
  "World News":      "🌍",
  "Finance":         "💹",
  "Technology":      "💻",
  "Math / Stats / AI": "🧮",
  "Astrophysics":    "🔭",
  "Counter-Strike 2":"🎮",
  "Science/Tech":    "🔬",
  "Daily Facts":     "💡",
  "Weather":         "🌤️",
};

// ---------------------------------------------------------------------------
// State
// ---------------------------------------------------------------------------
let categories = [];
let activeIndex = 0;

// ---------------------------------------------------------------------------
// DOM references
// ---------------------------------------------------------------------------
const contentEl       = document.getElementById("content");
const tabBarEl        = document.getElementById("tabBar");
const loadingSpinner  = document.getElementById("loadingSpinner");
const detailPanel     = document.getElementById("detailPanel");
const detailSource    = document.getElementById("detailSource");
const detailBody      = document.getElementById("detailBody");
const openLinkBtn     = document.getElementById("openLinkBtn");
const backBtn         = document.getElementById("backBtn");
const refreshBtn      = document.getElementById("refreshBtn");

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------
function showSpinner() {
  loadingSpinner.classList.remove("hidden");
}

function hideSpinner() {
  loadingSpinner.classList.add("hidden");
}

function escapeHtml(str) {
  if (!str) return "";
  return str
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

// ---------------------------------------------------------------------------
// Service worker registration
// ---------------------------------------------------------------------------
if ("serviceWorker" in navigator) {
  window.addEventListener("load", () => {
    navigator.serviceWorker
      .register("/sw.js")
      .catch((err) => console.warn("SW registration failed:", err));
  });
}

// ---------------------------------------------------------------------------
// Boot
// ---------------------------------------------------------------------------
async function init() {
  try {
    const res = await fetch("/api/categories");
    if (!res.ok) throw new Error("Failed to load categories");
    categories = await res.json();
    renderTabs();
    loadTab(0);
  } catch (err) {
    contentEl.innerHTML = `<div class="empty-state">
      <div class="icon">⚠️</div>
      <p>Could not connect to the NewsFeed server.<br>${escapeHtml(err.message)}</p>
    </div>`;
  }
}

// ---------------------------------------------------------------------------
// Tab bar
// ---------------------------------------------------------------------------
function renderTabs() {
  tabBarEl.innerHTML = "";
  categories.forEach((cat, idx) => {
    const btn = document.createElement("button");
    btn.className = "tab-btn" + (idx === activeIndex ? " active" : "");
    btn.dataset.index = idx;
    const icon = TAB_ICONS[cat.name] || "📄";
    btn.innerHTML = `<span class="tab-icon">${icon}</span><span>${escapeHtml(cat.short)}</span>`;
    btn.addEventListener("click", () => {
      if (idx !== activeIndex) loadTab(idx);
    });
    tabBarEl.appendChild(btn);
  });
}

function setActiveTab(idx) {
  activeIndex = idx;
  document.querySelectorAll(".tab-btn").forEach((btn) => {
    btn.classList.toggle("active", Number(btn.dataset.index) === idx);
  });
  // Scroll active tab into view
  const activeBtn = tabBarEl.querySelector(".tab-btn.active");
  if (activeBtn) activeBtn.scrollIntoView({ inline: "center", behavior: "smooth" });
}

// ---------------------------------------------------------------------------
// Load a tab
// ---------------------------------------------------------------------------
async function loadTab(idx) {
  setActiveTab(idx);
  showSpinner();
  contentEl.innerHTML = "";
  contentEl.appendChild(loadingSpinner);
  loadingSpinner.classList.remove("hidden");

  const cat = categories[idx];

  try {
    if (cat.weather_tab) {
      await loadWeather();
    } else if (cat.concepts_tab) {
      await loadConcept();
    } else {
      await loadFeed(idx, cat);
    }
  } catch (err) {
    hideSpinner();
    contentEl.innerHTML = `<div class="empty-state">
      <div class="icon">⚠️</div>
      <p>${escapeHtml(err.message)}</p>
    </div>`;
  }
}

// ---------------------------------------------------------------------------
// Article feed
// ---------------------------------------------------------------------------
async function loadFeed(idx) {
  const res = await fetch(`/api/feed/${idx}`);
  if (!res.ok) throw new Error(`Server error ${res.status}`);
  const data = await res.json();
  hideSpinner();

  if (!data.articles || data.articles.length === 0) {
    contentEl.innerHTML = `<div class="empty-state">
      <div class="icon">📭</div>
      <p>No articles found.</p>
    </div>`;
    return;
  }

  const list = document.createElement("div");
  list.className = "article-list";

  data.articles.forEach((article) => {
    const card = document.createElement("div");
    card.className = "article-card";
    card.innerHTML = `
      <div class="card-source">${escapeHtml(article.source)}</div>
      <div class="card-title">${escapeHtml(article.title)}</div>
      ${article.summary ? `<div class="card-summary">${escapeHtml(article.summary)}</div>` : ""}
      ${article.date ? `<div class="card-date">${escapeHtml(article.date)}</div>` : ""}
    `;
    card.addEventListener("click", () => openDetail(article));
    list.appendChild(card);
  });

  contentEl.innerHTML = "";
  contentEl.appendChild(list);
}

// ---------------------------------------------------------------------------
// Daily concept
// ---------------------------------------------------------------------------
async function loadConcept() {
  const res = await fetch("/api/concept");
  if (!res.ok) throw new Error(`Server error ${res.status}`);
  const concept = await res.json();
  hideSpinner();

  const card = document.createElement("div");
  card.className = "concept-card";
  card.innerHTML = `
    <div class="concept-category">${escapeHtml(concept.category)}</div>
    <div class="concept-title">${escapeHtml(concept.title)}</div>
    <pre class="concept-equation">${escapeHtml(concept.equation)}</pre>
    <div class="concept-overview">${escapeHtml(concept.overview)}</div>
  `;

  contentEl.innerHTML = "";
  contentEl.appendChild(card);
}

// ---------------------------------------------------------------------------
// Weather
// ---------------------------------------------------------------------------
async function loadWeather() {
  const res = await fetch("/api/weather");
  if (!res.ok) throw new Error(`Weather unavailable (${res.status})`);
  const data = await res.json();
  hideSpinner();

  const current = data.current || {};
  const daily   = data.daily   || {};

  const temp    = current.temperature_2m    !== undefined ? `${current.temperature_2m}°C` : "—";
  const feels   = current.apparent_temperature !== undefined ? `${current.apparent_temperature}°C` : "—";
  const humidity = current.relative_humidity_2m !== undefined ? `${current.relative_humidity_2m}%` : "—";
  const wind    = current.wind_speed_10m    !== undefined ? `${current.wind_speed_10m} km/h` : "—";
  const wCode   = current.weather_code;
  const wDesc   = wmoDescription(wCode);

  let html = `
    <div class="weather-location">${escapeHtml(data.location_name || "")}</div>
    <div class="weather-current">
      <div class="weather-temp">${temp}</div>
      <div class="weather-desc">${escapeHtml(wDesc)}</div>
      <div class="weather-meta">
        <span>Feels like ${escapeHtml(feels)}</span>
        <span>Humidity ${escapeHtml(humidity)}</span>
        <span>Wind ${escapeHtml(wind)}</span>
      </div>
    </div>
  `;

  // Forecast
  const times = daily.time || [];
  if (times.length > 0) {
    html += `<div class="weather-forecast">`;
    times.forEach((day, i) => {
      const code  = (daily.weather_code || [])[i];
      const tmax  = (daily.temperature_2m_max || [])[i];
      const tmin  = (daily.temperature_2m_min || [])[i];
      const desc  = wmoDescription(code);
      const label = formatDate(day);
      const temps = tmax !== undefined && tmin !== undefined
        ? `${tmax}° / ${tmin}°`
        : "—";
      html += `
        <div class="forecast-row">
          <span class="forecast-date">${escapeHtml(label)}</span>
          <span class="forecast-desc">${escapeHtml(desc)}</span>
          <span class="forecast-temps">${escapeHtml(temps)}</span>
        </div>`;
    });
    html += `</div>`;
  }

  contentEl.innerHTML = html;
}

function formatDate(dateStr) {
  if (!dateStr) return "";
  try {
    const d = new Date(dateStr + "T00:00:00");
    return d.toLocaleDateString(undefined, { weekday: "short", month: "short", day: "numeric" });
  } catch (_) {
    return dateStr;
  }
}

// Minimal WMO code → description (mirrors the Python side)
function wmoDescription(code) {
  const WMO = {
    0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
    45: "Fog", 48: "Rime fog",
    51: "Light drizzle", 53: "Moderate drizzle", 55: "Dense drizzle",
    61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
    71: "Slight snow", 73: "Moderate snow", 75: "Heavy snow", 77: "Snow grains",
    80: "Slight showers", 81: "Moderate showers", 82: "Violent showers",
    85: "Snow showers", 86: "Heavy snow showers",
    95: "Thunderstorm", 96: "Thunderstorm + hail", 99: "Thunderstorm + hail",
  };
  return WMO[code] || (code !== undefined ? `Code ${code}` : "—");
}

// ---------------------------------------------------------------------------
// Article detail panel
// ---------------------------------------------------------------------------
function openDetail(article) {
  detailSource.textContent = article.source || "";

  detailBody.innerHTML = `
    <div class="detail-title">${escapeHtml(article.title)}</div>
    ${article.date ? `<div class="card-date" style="margin-bottom:12px">${escapeHtml(article.date)}</div>` : ""}
    <div class="detail-summary">${escapeHtml(article.summary || "No summary available.")}</div>
  `;

  if (article.url) {
    openLinkBtn.href = article.url;
    openLinkBtn.classList.remove("hidden");
  } else {
    openLinkBtn.href = "#";
    openLinkBtn.classList.add("hidden");
  }

  detailPanel.classList.add("open");
  detailPanel.setAttribute("aria-hidden", "false");
}

function closeDetail() {
  detailPanel.classList.remove("open");
  detailPanel.setAttribute("aria-hidden", "true");
}

backBtn.addEventListener("click", closeDetail);

// Swipe-right to close detail panel
(function setupSwipe() {
  let startX = 0;
  detailPanel.addEventListener("touchstart", (e) => {
    startX = e.touches[0].clientX;
  }, { passive: true });
  detailPanel.addEventListener("touchend", (e) => {
    const dx = e.changedTouches[0].clientX - startX;
    if (dx > 60) closeDetail();
  }, { passive: true });
})();

// ---------------------------------------------------------------------------
// Refresh button
// ---------------------------------------------------------------------------
refreshBtn.addEventListener("click", () => {
  refreshBtn.classList.add("spinning");
  loadTab(activeIndex).finally(() => {
    setTimeout(() => refreshBtn.classList.remove("spinning"), 600);
  });
});

// ---------------------------------------------------------------------------
// Start
// ---------------------------------------------------------------------------
init();
