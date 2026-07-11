// --- VIZ 1 GLOBALS ---
let viz1Year = 2022;
let viz1YearsRange = [1996, 2024];
let viz1IsPlaying = false;
let viz1Speed = 600;
let viz1SelectedRegion = null;
let viz1SearchQuery = '';
let viz1ComparedCountries = [];
let viz1ShowSpecific = false;
let viz1PlayInterval = null; // legacy; play now uses async token loop
let viz1PlayToken = 0;
let viz1IsZoomed = false;
let viz1EventsBound = false;
// Manual year motion (NOT Plotly layout.transition — that morphs by index → flying USA).
// Fixed rosters + ids keep identity stable; we lerp x/y via rAF + Plotly.react.
let viz1LastPositions = null; // { code: {x,y,size,color,pubs} }
let viz1LastDrawnYear = null;
let viz1Trails = []; // comet segments: {xs,ys,color,width,baseOpacity,life,born}
let viz1MotionRaf = null;
let viz1TrailRaf = null;
let viz1MotionGen = 0;
const VIZ1_LERP_MS = 520;
const VIZ1_TRAIL_LIFE_MS = 1600;
const VIZ1_MOVE_EPS = 0.035; // post-EMA year hops are small; giants still glide+trail
const VIZ1_TRAIL_MIN_SIZE = 9; // marker diameter; tiny bubbles get no/near-zero tails

// Okabe-Ito / Wong palette — CVD-safe (Okabe & Ito 2008; Wong Nature Methods 2011).
// Binary compare/contrast MUST use opposite poles: blue (#0072B2) ↔ orange (#E69F00).
// Never put orange next to bluish-green in legends; never use pure red+green.
const OKABE_ITO = {
  blue: '#0072B2',
  orange: '#E69F00',
  sky: '#56B4E9',
  vermillion: '#D55E00',
  purple: '#CC79A7',
  green: '#009E73',
  yellow: '#F0E442',
  black: '#000000',
  muted: '#94a3b8'
};
// Series order alternates cool/warm with large luminance gaps (max categorical separation).
const viz1ColorPalette = [
  OKABE_ITO.blue,
  OKABE_ITO.orange,
  OKABE_ITO.sky,
  OKABE_ITO.vermillion,
  OKABE_ITO.purple,
  OKABE_ITO.green,
  OKABE_ITO.yellow,
  '#000000'
];

if (typeof VIZ1_DATA !== 'undefined') {
  // Temporal path smoother — UMAP year embeds can still reverse; MA+EMA glides paths.
  // Axis ranges are derived from the SMOOTHED cloud (not the old [-16,40] box) so the
  // plot fills the canvas instead of sitting as a tiny centered cluster.
  const byCode = {};
  VIZ1_DATA.forEach((d) => {
    if (!byCode[d.Country_Code]) byCode[d.Country_Code] = [];
    byCode[d.Country_Code].push(d);
  });
  const emaFactor = 0.18;
  const maWindow = 5;
  const maHalf = Math.floor(maWindow / 2);
  Object.keys(byCode).forEach((code) => {
    const pts = byCode[code].sort((a, b) => a.Year - b.Year);
    const rawX = pts.map((p) => p.x);
    const rawY = pts.map((p) => p.y);
    const maX = rawX.map((_, i) => {
      let s = 0;
      let n = 0;
      for (let j = Math.max(0, i - maHalf); j <= Math.min(pts.length - 1, i + maHalf); j++) {
        s += rawX[j];
        n++;
      }
      return s / n;
    });
    const maY = rawY.map((_, i) => {
      let s = 0;
      let n = 0;
      for (let j = Math.max(0, i - maHalf); j <= Math.min(pts.length - 1, i + maHalf); j++) {
        s += rawY[j];
        n++;
      }
      return s / n;
    });
    let mx = maX[0];
    let my = maY[0];
    pts[0].x = mx;
    pts[0].y = my;
    for (let i = 1; i < pts.length; i++) {
      mx = emaFactor * maX[i] + (1 - emaFactor) * mx;
      my = emaFactor * maY[i] + (1 - emaFactor) * my;
      pts[i].x = mx;
      pts[i].y = my;
    }
  });
}

/** Tight locked axis box from smoothed VIZ1_DATA so the cloud fills the plot area. */
function getViz1AxisRanges() {
  if (typeof VIZ1_DATA === 'undefined' || !VIZ1_DATA.length) {
    return { x: [-1, 1], y: [-1, 1] };
  }
  let xmin = Infinity, xmax = -Infinity, ymin = Infinity, ymax = -Infinity;
  for (const d of VIZ1_DATA) {
    if (!Number.isFinite(d.x) || !Number.isFinite(d.y)) continue;
    if (d.x < xmin) xmin = d.x;
    if (d.x > xmax) xmax = d.x;
    if (d.y < ymin) ymin = d.y;
    if (d.y > ymax) ymax = d.y;
  }
  const padFrac = 0.06;
  const xPad = Math.max((xmax - xmin) * padFrac, 0.35);
  const yPad = Math.max((ymax - ymin) * padFrac, 0.35);
  return {
    x: [xmin - xPad, xmax + xPad],
    y: [ymin - yPad, ymax + yPad]
  };
}
const VIZ1_AXIS = getViz1AxisRanges();

function getViz1Regions() {
  if (typeof VIZ1_DATA === 'undefined') return [];
  return [...new Set(VIZ1_DATA.map(d => d.Region).filter(Boolean))].sort();
}

// ============================================================
// CS661 Group 10 — App Logic
// Gallery → Fullscreen Interactive Panel System
// ============================================================

// ─── Global State ──────────────────────────────────────────
const APP = {
  activeViz: null,
  year: 2015,
  region: "All",
  tier: "All",
  sort: "gain",            // Viz 4 dumbbell sort
  isPlaying: false,
  speed: 1200,
  indiaController: null,
  animTimer: null,
  selectedNode: null,      // Viz 5: clicked institution
  cleanupFns: []           // functions to call when closing viz
};

// ─── Tooltip ───────────────────────────────────────────────
const tip = document.createElement("div");
tip.className = "d3-tooltip";
document.body.appendChild(tip);

function showTip(evt, html) {
  tip.innerHTML = html;
  tip.classList.add("visible");
  moveTip(evt);
}
function moveTip(evt) {
  const x = evt.clientX, y = evt.clientY;
  const W = window.innerWidth, H = window.innerHeight;
  tip.style.left = (x + 14 < W - 280 ? x + 14 : x - 270) + "px";
  tip.style.top  = (y + 14 < H - 160 ? y + 14 : y - 140) + "px";
}
function hideTip() { tip.classList.remove("visible"); }

// ─── VIZ META ──────────────────────────────────────────────
const VIZ_META = {
  1: { title: "High-Dimensional Peer Clustering",             num: "01", credit: "World Bank (GDP, GERD, journal articles) · SCImago Country Rank (H-index; Documents fallback) · UMAP" },
  2: { title: "Global Quality Shift (Q1 vs Q4)",              num: "02", credit: "SCImago Journal Rank · Q1/Q4 by journal publisher country (uncapped ratio)" },
  3: { title: "Top Research topics",                          num: "03", credit: "OpenAlex concepts 2000–2024 (pre-2000 omitted — AI mega-concept / incomplete backfill)" },
  4: { title: "The Collaboration Premium",                    num: "04", credit: "OpenAlex · domestic vs international cites · Top 20 countries, 2024" },
  5: { title: "India Domestic Higher Education Network",      num: "05", credit: "NIRF India · ROR · SCImago" }
};

// ─── Preview Canvas Drawings ───────────────────────────────
window.addEventListener("load", () => {
  drawPreview1(); drawPreview2(); drawPreview3(); drawPreview4();
  INDIA.ensureLoaded().then(() => INDIA.drawCardPreview("preview-5")).catch(() => drawPreview5());
  spawnParticles();
});

function drawPreview1() {
  const c = document.getElementById("preview-1");
  const ctx = c.getContext("2d");
  c.width = c.offsetWidth; c.height = c.offsetHeight;
  const w = c.width, h = c.height;
  const bubbles = [
    {x:0.3,y:0.3,r:15,col:"rgba(0,158,115,0.7)"},{x:0.4,y:0.25,r:25,col:"rgba(0,158,115,0.7)"},
    {x:0.7,y:0.6,r:20,col:"rgba(226,168,85,0.6)"},{x:0.6,y:0.7,r:18,col:"rgba(226,168,85,0.6)"},
    {x:0.8,y:0.3,r:12,col:"rgba(251,113,133,0.6)"},{x:0.2,y:0.8,r:30,col:"rgba(251,191,36,0.6)"}
  ];
  bubbles.forEach(b => {
    ctx.beginPath(); ctx.arc(b.x*w, b.y*h, b.r, 0, Math.PI*2);
    ctx.fillStyle = b.col; ctx.fill();
    ctx.strokeStyle = "rgba(255,255,255,0.15)"; ctx.lineWidth = 1; ctx.stroke();
  });
}

function drawPreview2() {
  const c = document.getElementById("preview-2");
  const ctx = c.getContext("2d");
  c.width = c.offsetWidth; c.height = c.offsetHeight;
  const w = c.width, h = c.height;

  // Draw light gridlines
  ctx.strokeStyle = "rgba(255, 255, 255, 0.05)";
  ctx.lineWidth = 1;
  for (let y = h * 0.2; y <= h * 0.8; y += h * 0.2) {
    ctx.beginPath();
    ctx.moveTo(w * 0.1, y);
    ctx.lineTo(w * 0.9, y);
    ctx.stroke();
  }

  // Draw ground line
  ctx.strokeStyle = "rgba(255, 255, 255, 0.15)";
  ctx.beginPath();
  ctx.moveTo(w * 0.1, h * 0.8);
  ctx.lineTo(w * 0.9, h * 0.8);
  ctx.stroke();

  // Draw 5 pairs of bars (Grouped preview)
  const numGroups = 5;
  const groupW = (w * 0.8) / numGroups;
  const barW = groupW * 0.35;
  const gap = groupW * 0.1;

  for (let i = 0; i < numGroups; i++) {
    const x0 = w * 0.1 + i * groupW + gap;
    
    // Alt heights
    const hQ1 = h * (0.2 + Math.random() * 0.4);
    const hQ4 = h * (0.1 + Math.random() * 0.3);

    // Q1 bar (blue) vs Q4 bar (orange) — opposite-pole CVD pair
    ctx.fillStyle = "#0072B2";
    ctx.fillRect(x0, h * 0.8 - hQ1, barW, hQ1);

    ctx.fillStyle = "#E69F00";
    ctx.fillRect(x0 + barW, h * 0.8 - hQ4, barW, hQ4);
  }
}

function drawPreview3() {
  const c = document.getElementById("preview-3");
  const ctx = c.getContext("2d");
  c.width = c.offsetWidth; c.height = c.offsetHeight;
  const w = c.width, h = c.height;
  const bars = [0.8,0.6,0.5,0.4];
  const colors = ["#E69F00","#E69F00","#E69F00","#D55E00"];
  bars.forEach((bw, i) => {
    const bh = 15, by = 20 + i * 25;
    ctx.fillStyle = colors[i];
    ctx.fillRect(20, by, bw*(w-40), bh);
  });
}

function drawPreview4() {
  const c = document.getElementById("preview-4");
  const ctx = c.getContext("2d");
  c.width = c.offsetWidth; c.height = c.offsetHeight;
  const w = c.width, h = c.height;
  for(let i=0; i<4; i++) {
    const y = Math.round(h * (0.20 + i * 0.22));
    const x1 = w*0.2 + Math.random()*w*0.2;
    const x2 = w*0.6 + Math.random()*w*0.2;
    ctx.strokeStyle = "rgba(255,255,255,0.2)"; ctx.lineWidth = 2;
    ctx.beginPath(); ctx.moveTo(x1, y); ctx.lineTo(x2, y); ctx.stroke();
    ctx.fillStyle = "#E69F00"; ctx.beginPath(); ctx.arc(x1, y, 4, 0, Math.PI*2); ctx.fill();
    ctx.fillStyle = "#0072B2"; ctx.beginPath(); ctx.arc(x2, y, 4, 0, Math.PI*2); ctx.fill();
  }
}

function drawPreview5() {
  const c = document.getElementById("preview-5");
  const ctx = c.getContext("2d");
  c.width = c.offsetWidth; c.height = c.offsetHeight;
  const w = c.width, h = c.height;
  const outline = [
    [0.38,0.05],[0.55,0.03],[0.72,0.15],[0.78,0.28],[0.65,0.55],
    [0.55,0.75],[0.48,0.92],[0.42,0.75],[0.30,0.55],[0.22,0.35],[0.28,0.15],[0.38,0.05]
  ];
  ctx.beginPath();
  outline.forEach(([px,py], i) => i===0 ? ctx.moveTo(px*w, py*h) : ctx.lineTo(px*w, py*h));
  ctx.closePath();
  ctx.fillStyle = "rgba(245,158,11,0.08)";
  ctx.fill();
  ctx.strokeStyle = "rgba(245,158,11,0.3)";
  ctx.lineWidth = 1.5;
  ctx.setLineDash([3,3]);
  ctx.stroke();
  ctx.setLineDash([]);
}

// ─── Particle Background ───────────────────────────────────
function spawnParticles() {
  const container = document.getElementById("hero-particles");
  for (let i = 0; i < 30; i++) {
    const p = document.createElement("div");
    p.className = "particle";
    const size = 2 + Math.random() * 4;
    const col = ["#0072B2","#E69F00","#56B4E9","#CC79A7"][Math.floor(Math.random()*4)];
    Object.assign(p.style, {
      width: size + "px", height: size + "px",
      left: (Math.random() * 100) + "%",
      background: col,
      animationDuration: (8 + Math.random() * 14) + "s",
      animationDelay: (Math.random() * 12) + "s"
    });
    container.appendChild(p);
  }
}

// ─── Open / Close Viz Panel ────────────────────────────────
window.openViz = async function(id) {
  APP.activeViz = id;
  APP.selectedNode = null;

  const panel = document.getElementById("viz-panel");
  const meta = VIZ_META[id];

  document.getElementById("panel-num").textContent  = meta.num;
  document.getElementById("panel-title").textContent = meta.title;
  document.getElementById("data-credit").textContent = "Data: " + meta.credit;

  showLoading("Loading visualization...");
  buildControls(id);

  APP.cleanupFns.forEach(fn => fn());
  APP.cleanupFns = [];
  const body = document.getElementById("panel-body");
  body.innerHTML = "";

  panel.classList.add("active");

  await sleep(250);
  if (id === 5) {
    try {
      await INDIA.ensureLoaded();
    } catch (err) {
      console.error("India network load failed:", err);
    }
  }
  if (id !== 1) {
    hideLoading();
  }
  renderViz(id);

  document.getElementById("prev-btn").disabled = (id === 1);
  document.getElementById("next-btn").disabled = (id === 5);
};

window.closeViz = function() {
  stopAnimation();
  APP.cleanupFns.forEach(fn => fn());
  APP.cleanupFns = [];
  APP.activeViz = null;
  APP.selectedNode = null;

  const panel = document.getElementById("viz-panel");
  panel.classList.remove("active");
};

window.navigateViz = function(dir) {
  const next = APP.activeViz + dir;
  if (next >= 1 && next <= 5) openViz(next);
};

// ─── Build Controls ────────────────────────────────────────
function buildControls(id) {
  const c = document.getElementById("panel-controls");
  c.innerHTML = "";



  if (id === 2) {
    const wrap = el("div", "year-slider-wrap");
    const yLabel = el("span", "ctrl-label", "Year:");
    const slider = document.createElement("input");
    slider.type = "range";
    slider.className = "ctrl-range";
    slider.min = 1999;
    slider.max = 2024;
    slider.value = APP.year >= 1999 && APP.year <= 2024 ? APP.year : 2024;
    APP.year = +slider.value;
    const yearVal = el("span", "year-val", APP.year);
    slider.oninput = () => {
      APP.year = +slider.value;
      yearVal.textContent = APP.year;
      renderViz(2);
    };
    wrap.append(yLabel, slider, yearVal);

    const playBtn = el("button", "ctrl-btn", "▶ Play");
    playBtn.id = "play-btn";
    playBtn.onclick = () => toggleAnimation(slider, yearVal, playBtn, 1999, 2024);

    // Speed toggle button next to play button
    const speedBtn = el("button", "ctrl-btn", APP.speed === 600 ? "2x" : "1x");
    speedBtn.style.minWidth = "38px";
    speedBtn.style.fontWeight = "800";
    speedBtn.onclick = () => {
      if (APP.speed === 1200) {
        APP.speed = 600;
        speedBtn.textContent = "2x";
        speedBtn.style.color = "#56B4E9";
        speedBtn.style.borderColor = "rgba(86,180,233,0.4)";
      } else {
        APP.speed = 1200;
        speedBtn.textContent = "1x";
        speedBtn.style.color = "";
        speedBtn.style.borderColor = "";
      }
    };
    if (APP.speed === 600) {
      speedBtn.style.color = "#56B4E9";
      speedBtn.style.borderColor = "rgba(86,180,233,0.4)";
    }

    // Grouped / Stacked toggle switch matching system style
    const toggleWrap = el("div", "toggle-group");
    const optGrouped = el("button", "toggle-opt" + (barChartMode === "grouped" ? " on" : ""), "Grouped");
    const optStacked = el("button", "toggle-opt" + (barChartMode === "stacked" ? " on" : ""), "Stacked");
    optGrouped.onclick = () => { barChartMode = "grouped"; optGrouped.classList.add("on"); optStacked.classList.remove("on"); renderViz(2); };
    optStacked.onclick = () => { barChartMode = "stacked"; optStacked.classList.add("on"); optGrouped.classList.remove("on"); renderViz(2); };
    toggleWrap.append(optGrouped, optStacked);

    const divider1 = el("div", "ctrl-divider");

    const scaleWrap = el("div", "toggle-group");
    const optLinear = el("button", "toggle-opt" + (yAxisScaleMode === "linear" ? " on" : ""), "Linear");
    const optLog = el("button", "toggle-opt" + (yAxisScaleMode === "logarithmic" ? " on" : ""), "Logarithmic");
    optLinear.onclick = () => { yAxisScaleMode = "linear"; optLinear.classList.add("on"); optLog.classList.remove("on"); renderViz(2); };
    optLog.onclick = () => { yAxisScaleMode = "logarithmic"; optLog.classList.add("on"); optLinear.classList.remove("on"); renderViz(2); };
    scaleWrap.append(optLinear, optLog);

    const divider2 = el("div", "ctrl-divider");

    c.append(wrap, playBtn, speedBtn, divider1, toggleWrap, divider2, scaleWrap);
  }

  if (id === 4) {
    const sortSel = document.createElement("select");
    sortSel.className = "ctrl-select";
    sortSel.innerHTML = `
      <option value="gain">Sort: Citation Gain</option>
      <option value="international">Sort: Int'l Rate</option>
      <option value="domestic">Sort: Domestic Rate</option>
      <option value="name">Sort: Name</option>
    `;
    sortSel.value = APP.sort;
    sortSel.onchange = () => { APP.sort = sortSel.value; renderViz(4); };
    
    const regionSel = document.createElement("select");
    regionSel.id = "viz4-region-select";
    regionSel.className = "ctrl-select";
    regionSel.innerHTML = `
      <option value="All">All Regions</option>
      <option value="North America">North America</option>
      <option value="Europe">Europe</option>
      <option value="East Asia & Pacific">East Asia & Pacific</option>
      <option value="South Asia">South Asia</option>
      <option value="Latin America">Latin America</option>
      <option value="Middle East & Africa">Middle East & Africa</option>
      <option value="Oceania">Oceania</option>
    `;
    regionSel.value = APP.region || "All";
    regionSel.onchange = () => { APP.region = regionSel.value; renderViz(4); };

    c.append(
      el("span","ctrl-label","Region:"), regionSel, 
      el("div", "ctrl-divider"), 
      el("span","ctrl-label","Order By:"), sortSel
    );
  }

  if (id === 5) {
    const years = INDIA.availableYears ? INDIA.availableYears() : [2015, 2024];
    const yMin = Math.min(...years);
    const yMax = Math.max(...years);
    const wrap = el("div", "year-slider-wrap");
    const yLabel = el("span", "ctrl-label", "Year:");
    const slider = document.createElement("input");
    slider.type = "range";
    slider.className = "ctrl-range";
    slider.min = yMin;
    slider.max = yMax;
    slider.value = APP.year >= yMin && APP.year <= yMax ? APP.year : yMax;
    APP.year = +slider.value;
    const yearVal = el("span", "year-val", APP.year);
    slider.oninput = () => {
      APP.year = +slider.value;
      yearVal.textContent = APP.year;
      if (APP.indiaController?.setYear) {
        APP.indiaController.setYear(APP.year);
      }
    };
    wrap.append(yLabel, slider, yearVal);

    const playBtn = el("button", "ctrl-btn", "▶ Play");
    playBtn.id = "play-btn";
    playBtn.onclick = () => toggleAnimation(slider, yearVal, playBtn, yMin, yMax);

    const divider = el("div", "ctrl-divider");

    const tierSel = document.createElement("select");
    tierSel.className = "ctrl-select";
    tierSel.innerHTML = `
      <option value="All">All Tiers</option>
      <option value="premier">Premier (IITs, IISc, ...)</option>
      <option value="state_affiliated">State & Affiliated</option>
    `;
    tierSel.value = APP.tier;
    tierSel.onchange = () => {
      APP.tier = tierSel.value;
      if (APP.indiaController?.setTier) {
        APP.indiaController.setTier(APP.tier);
      } else {
        renderViz(5);
      }
    };

    c.append(wrap, playBtn, divider, el("span", "ctrl-label", "Tier:"), tierSel);
  }
}

// ─── Render Dispatcher ────────────────────────────────────
function renderViz(id) {
  const body = document.getElementById("panel-body");
  body.innerHTML = "";
  if (id === 1) renderViz1(body);
  if (id === 2) renderViz2(body);
  if (id === 3) renderViz3(body);
  if (id === 4) renderViz4(body);
  if (id === 5) renderViz5(body);
}

// ══════════════════════════════════════════════════════════
// VIZ 1: High-Dimensional Peer Clustering (t-SNE/UMAP Scatter)
// ══════════════════════════════════════════════════════════
function renderViz1(body) {
  if (typeof VIZ1_DATA !== 'undefined') {
    const allYears = [...new Set(VIZ1_DATA.map(d => d.Year).filter(y => y != null && !isNaN(y)))];
    if (allYears.length > 0) {
      viz1YearsRange = [Math.min(...allYears), Math.max(...allYears)];
      viz1Year = Math.max(...allYears);
    }
  }

  body.innerHTML = `
    <div class="viz1-layout">
      <!-- SIDEBAR -->
      <div class="viz1-sidebar">
        <div class="viz1-sidebar-top">
          <div>
            <h2 class="viz1-title">Scientific Peer Clusters</h2>
            <p class="viz1-desc">Wealth, R&amp;D, publication volume, and quality peers over time.</p>
          </div>

          <div class="viz1-control-group">
            <label>Compare Nations</label>
            <p class="viz1-hint">Click bubbles to select · legend focuses a region (click same again = global) · Esc clears · double-click resets zoom</p>
            <div id="viz1-compare-ui" style="display: flex; flex-wrap: wrap; gap: 6px;"></div>
          </div>

          <div class="viz1-control-group">
            <label>Search Countries</label>
            <div class="viz1-search-container">
              <input type="text" id="viz1-search" class="viz1-search-input" list="viz1-country-list" placeholder="India, Japan, USA…" style="flex: 1; min-width: 0; width: auto;">
              <button type="button" id="viz1-search-btn" style="background: rgba(86,180,233,0.15); border: 1px solid rgba(86,180,233,0.4); color: #56B4E9; padding: 4px 10px; border-radius: 4px; cursor: pointer; font-size: 12px; font-weight: 600; margin-left: 8px; white-space: nowrap; flex-shrink: 0;">Add</button>
            </div>
            <datalist id="viz1-country-list"></datalist>
          </div>

          <div class="viz1-control-group">
            <label>Timeline <span id="viz1-year-label" style="margin-left: auto; background: rgba(255,255,255,0.1); padding: 2px 6px; border-radius: 4px;">${viz1Year}</span></label>
            <div style="display: flex; gap: 10px; align-items: center;">
              <button id="viz1-play-btn" class="viz1-play-btn">▶ Play</button>
              <input type="range" id="viz1-year-slider" min="${viz1YearsRange[0]}" max="${viz1YearsRange[1]}" value="${viz1Year}" style="flex: 1;">
            </div>
          </div>

          <div class="viz1-control-group">
            <label>Display</label>
            <div class="viz1-sidebar-actions">
              <button id="viz1-specific-btn" class="viz1-specific-btn${viz1ShowSpecific ? ' active' : ''}" type="button">${viz1ShowSpecific ? 'Show All Countries' : 'Show Specific Countries'}</button>
              <button id="viz1-reset-zoom-btn" class="viz1-reset-zoom-btn" type="button" style="display:none;" title="Reset zoom to full view">Reset Zoom</button>
            </div>
          </div>
        </div>

        <div class="viz1-stats-card">
          <div class="viz1-stats-metrics">
            <div class="viz1-stat">
              <b id="viz1-stat-nations">-</b>
              <span>nations</span>
            </div>
            <div class="viz1-stat">
              <b id="viz1-stat-regions">-</b>
              <span>regions</span>
            </div>
            <div class="viz1-stat">
              <b id="viz1-stat-pubs">-</b>
              <span>pubs</span>
            </div>
          </div>
        </div>

        <div class="viz1-visual-guide viz1-visual-guide--sidebar">
          <h4>Visual encodings</h4>
          <div class="viz1-encode-row"><strong>Axes</strong> UMAP (wealth · R&amp;D · volume · quality)</div>
          <div class="viz1-encode-row"><strong>Size</strong> Publications</div>
          <div class="viz1-encode-row"><strong>Color</strong> Region</div>
        </div>
      </div>

      <!-- MAIN PLOT AREA — no overlay toolbar (legend stays fully readable) -->
      <div class="viz1-plot">
        <div id="viz1-pinned-detail" class="viz1-pinned-detail" hidden aria-live="polite"></div>
        <div id="viz1-plotly-container" style="width: 100%; height: 100%;"></div>
      </div>
    </div>
  `;

  viz1EventsBound = false;
  viz1IsZoomed = false;  
  // Populate country autocomplete datalist
  const countryList = document.getElementById('viz1-country-list');
  if (countryList && typeof VIZ1_DATA !== 'undefined') {
    const uniqueCountries = [...new Set(VIZ1_DATA.map(d => d.Country_Name).filter(Boolean))].sort();
    countryList.innerHTML = uniqueCountries.map(name => `<option value="${name}">`).join('');
  }
  
  // Attach Event Listeners
  const slider = document.getElementById('viz1-year-slider');
  const label = document.getElementById('viz1-year-label');
  const playBtn = document.getElementById('viz1-play-btn');
  const search = document.getElementById('viz1-search');
  const searchBtn = document.getElementById('viz1-search-btn');
  const specificBtn = document.getElementById('viz1-specific-btn');
  
  function executeViz1Search() {
    const query = search.value.trim();
    if (!query) return;
    
    const match = VIZ1_DATA.find(d =>
      d.Country_Name && d.Country_Name.toLowerCase() === query.toLowerCase()
    );
    
    if (match && !viz1ComparedCountries.includes(match.Country_Code)) {
      viz1ComparedCountries.push(match.Country_Code);
    } else if (!match) {
      search.style.outline = '2px solid #D55E00';
      search.style.borderRadius = '4px';
      setTimeout(() => {
        search.style.outline = '';
        search.style.borderRadius = '';
      }, 600);
    }
    
    search.value = '';
    viz1SearchQuery = '';
    updateViz1CompareUI();
    drawViz1Plotly();
  }
  
  slider.addEventListener('input', (e) => {
    viz1Year = parseInt(e.target.value, 10);
    label.textContent = viz1Year;
    cancelViz1Motion(true); // snap in-flight lerp; keep trails fading
    drawViz1Plotly({ animate: true });
  });
  
  playBtn.addEventListener('click', () => {
    viz1IsPlaying = !viz1IsPlaying;
    playBtn.innerHTML = viz1IsPlaying ? '⏸ Pause' : '▶ Play';
    
    if (viz1IsPlaying) {
      const token = ++viz1PlayToken;
      (async () => {
        while (viz1IsPlaying && token === viz1PlayToken) {
          viz1Year++;
          if (viz1Year > viz1YearsRange[1]) viz1Year = viz1YearsRange[0];
          slider.value = viz1Year;
          label.textContent = viz1Year;
          const t0 = performance.now();
          await drawViz1Plotly({ animate: true });
          if (!viz1IsPlaying || token !== viz1PlayToken) break;
          // Advance after lerp so motion is readable; leftover of viz1Speed paces the timeline
          const elapsed = performance.now() - t0;
          const wait = Math.max(40, viz1Speed - elapsed);
          await new Promise((r) => setTimeout(r, wait));
        }
        if (token === viz1PlayToken) {
          viz1IsPlaying = false;
          playBtn.innerHTML = '▶ Play';
        }
      })();
    } else {
      viz1PlayToken++;
      cancelViz1Motion(true);
      drawViz1Plotly({ animate: false }); // snap to current year after aborting lerp
    }
  });
  
  search.addEventListener('input', (e) => {
    viz1SearchQuery = e.target.value;
    drawViz1Plotly();
  });
  
  search.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      executeViz1Search();
    }
  });
  
  if (searchBtn) {
    searchBtn.addEventListener('click', executeViz1Search);
  }
  
  if (specificBtn) {
    specificBtn.addEventListener('click', () => {
      viz1ShowSpecific = !viz1ShowSpecific;
      specificBtn.textContent = viz1ShowSpecific ? 'Show All Countries' : 'Show Specific Countries';
      if (viz1ShowSpecific) {
        specificBtn.classList.add('active');
        // Drop compare picks that are now hidden so ghost selections cannot linger
        const before = viz1ComparedCountries.length;
        viz1ComparedCountries = viz1ComparedCountries.filter((c) => VIZ1_SPECIFIC_COUNTRIES.includes(c));
        if (viz1ComparedCountries.length !== before) updateViz1CompareUI();
      } else {
        specificBtn.classList.remove('active');
      }
      drawViz1Plotly({ animate: false });
    });
  }

  const resetZoomBtn = document.getElementById('viz1-reset-zoom-btn');
  if (resetZoomBtn) {
    resetZoomBtn.addEventListener('click', () => resetViz1Zoom());
  }

  const onViz1Keydown = (e) => {
    if (e.key !== 'Escape') return;
    if (document.getElementById('viz-panel') && !document.getElementById('viz-panel').classList.contains('active')) return;
    if (APP.activeViz !== 1) return;
    let changed = false;
    if (viz1ComparedCountries.length) {
      viz1ComparedCountries = [];
      updateViz1CompareUI();
      changed = true;
    }
    if (viz1IsZoomed) {
      resetViz1Zoom();
      changed = true;
    }
    if (changed) drawViz1Plotly({ animate: false });
  };
  document.addEventListener('keydown', onViz1Keydown);
  APP.cleanupFns.push(() => {
    document.removeEventListener('keydown', onViz1Keydown);
    viz1IsPlaying = false;
    viz1PlayToken++;
    if (typeof viz1PlayInterval !== 'undefined' && viz1PlayInterval) clearInterval(viz1PlayInterval);
    cancelViz1Motion(false);
    clearViz1Trails();
    viz1LastPositions = null;
    viz1LastDrawnYear = null;
    viz1EventsBound = false;
    viz1IsZoomed = false;
    const plotContainer = document.getElementById('viz1-plotly-container');
    if (plotContainer && typeof Plotly !== 'undefined') {
      try { Plotly.purge(plotContainer); } catch (e) {}
    }
  });
  
  buildControls(1); // Clears the global top bar
  drawViz1Plotly();
  updateViz1CompareUI();
  hideLoading();
}

function updateViz1ZoomButton() {
  const btn = document.getElementById('viz1-reset-zoom-btn');
  if (btn) btn.style.display = viz1IsZoomed ? 'flex' : 'none';
  const sidebar = document.querySelector('.viz1-sidebar');
  if (sidebar) sidebar.classList.toggle('viz1-sidebar--zoomed', !!viz1IsZoomed);
}

function rangesDiffer(a, b, eps = 1e-6) {
  if (!a || !b || a.length < 2 || b.length < 2) return false;
  return Math.abs(a[0] - b[0]) > eps || Math.abs(a[1] - b[1]) > eps;
}

function resetViz1Zoom() {
  const container = document.getElementById('viz1-plotly-container');
  viz1IsZoomed = false;
  updateViz1ZoomButton();
  if (!container || typeof Plotly === 'undefined') return;
  Plotly.relayout(container, {
    'xaxis.range': VIZ1_AXIS.x.slice(),
    'yaxis.range': VIZ1_AXIS.y.slice(),
    'xaxis.autorange': false,
    'yaxis.autorange': false
  });
}

function clearViz1Compare() {
  if (!viz1ComparedCountries.length) return;
  viz1ComparedCountries = [];
  updateViz1CompareUI();
  drawViz1Plotly();
}

/** Hover / pinned-detail HTML — same fields & style for both. */
function formatViz1CountryDetailHtml(d) {
  if (!d) return '';
  const fmt = (v, decimals = 0) => {
    if (v == null || isNaN(v)) return 'N/A';
    return Number(v).toLocaleString(undefined, { maximumFractionDigits: decimals });
  };
  const pubsLine = d._positionCarried
    ? `📚 Publications: <b>N/A</b> <i>(no docs this year; position held from ${d._carriedFromYear})</i><br>`
    : `📚 Publications: <b>${fmt(d.Total_Docs)}</b><br>`;
  return (
    `<b><span style="font-size:16px">${d.Country_Name || 'Unknown'}</span></b><br>` +
    `<i>${d.Region || ''}</i><br><br>` +
    pubsLine +
    `🎯 H-Index (Quality Stock): <b>${fmt(d.H_Index)}</b><br>` +
    `🔬 R&D Spend: <b>${fmt(d.GERD_Percent_GDP, 2)}%</b><br>💰 GDP/Capita: <b>$${fmt(d.GDP_Per_Capita_PPP)}</b>`
  );
}

/**
 * Top-right pinned detail for the latest compare-selected country.
 * viz1ComparedCountries is an ordered list: push on select, filter on deselect —
 * last element = most recently toggled ON (or previous when that one is removed).
 */
function updateViz1PinnedDetail() {
  const el = document.getElementById('viz1-pinned-detail');
  if (!el) return;
  if (!viz1ComparedCountries.length) {
    el.hidden = true;
    el.innerHTML = '';
    return;
  }
  const code = viz1ComparedCountries[viz1ComparedCountries.length - 1];
  const d = resolveViz1NodeForYear(code, parseInt(viz1Year, 10));
  if (!d) {
    el.hidden = true;
    el.innerHTML = '';
    return;
  }
  el.innerHTML = formatViz1CountryDetailHtml(d);
  el.hidden = false;
}

function updateViz1CompareUI() {
  const container = document.getElementById('viz1-compare-ui');
  if (!container) return;
  
  if (viz1ComparedCountries.length === 0) {
    container.innerHTML = '';
    updateViz1PinnedDetail();
    return;
  }
  
  let html = '';
  viz1ComparedCountries.forEach(code => {
    const d = VIZ1_DATA.find(x => x.Country_Code === code);
    const name = d ? d.Country_Name : code;
    html += `<span style="background: rgba(86,180,233,0.2); color: #56B4E9; padding: 4px 8px; border-radius: 4px; font-size: 12px; display: flex; align-items: center; gap: 4px;">
      ${name} <span class="viz1-remove-compare" data-code="${code}" style="cursor: pointer;">✕</span>
    </span>`;
  });
  
  html += `<button id="viz1-clear-compare" style="background: transparent; border: none; color: #D55E00; font-size: 12px; cursor: pointer; text-decoration: underline;">Clear All</button>`;
  
  container.innerHTML = html;
  
  document.querySelectorAll('.viz1-remove-compare').forEach(el => {
    el.addEventListener('click', (e) => {
      const code = e.target.getAttribute('data-code');
      viz1ComparedCountries = viz1ComparedCountries.filter(c => c !== code);
      drawViz1Plotly();
      updateViz1CompareUI();
    });
  });
  
  const clearBtn = document.getElementById('viz1-clear-compare');
  if (clearBtn) {
    clearBtn.addEventListener('click', () => {
      viz1ComparedCountries = [];
      drawViz1Plotly();
      updateViz1CompareUI();
    });
  }
  updateViz1PinnedDetail();
}

const VIZ1_SPECIFIC_COUNTRIES = [
  "USA", "CHN", "GBR", "DEU", "IND", "JPN", "FRA", "CAN", "ITA", "KOR", "AUS", "ESP", "BRA", "RUS", "NLD", 
  "IDN", "TUR", "IRN", "SAU", "POL", "CHE", "MYS", "PAK", "EGY", "MEX", "PRT", "SWE", "BEL", "ZAF", "NGA", "DNK", "UKR", "HKG", "AUT", "NOR",
  "IRQ", "ECU", "NPL", "VNM", "PER", "ETH", "GHA", "CYP", "COL", "UGA", "ARE", "BGD", "TJK", "PHL", "DZA"
];

/** Fixed country order per region across all years — keeps Plotly point identity stable on Play. */
let VIZ1_REGION_ROSTERS = null;
function getViz1RegionRosters() {
  if (VIZ1_REGION_ROSTERS) return VIZ1_REGION_ROSTERS;
  const map = {};
  if (typeof VIZ1_DATA !== 'undefined') {
    VIZ1_DATA.forEach((d) => {
      const r = d.Region || 'Other';
      if (!map[r]) map[r] = new Set();
      if (d.Country_Code) map[r].add(d.Country_Code);
    });
  }
  VIZ1_REGION_ROSTERS = {};
  Object.keys(map).forEach((r) => {
    VIZ1_REGION_ROSTERS[r] = [...map[r]].sort();
  });
  return VIZ1_REGION_ROSTERS;
}

/** Per-country year→row index for O(1) lookups + carry-forward of true gaps. */
let VIZ1_BY_CODE_YEAR = null;
function getViz1ByCodeYear() {
  if (VIZ1_BY_CODE_YEAR) return VIZ1_BY_CODE_YEAR;
  VIZ1_BY_CODE_YEAR = {};
  if (typeof VIZ1_DATA === 'undefined') return VIZ1_BY_CODE_YEAR;
  VIZ1_DATA.forEach((d) => {
    if (!d.Country_Code || d.Year == null) return;
    if (!VIZ1_BY_CODE_YEAR[d.Country_Code]) VIZ1_BY_CODE_YEAR[d.Country_Code] = {};
    VIZ1_BY_CODE_YEAR[d.Country_Code][d.Year] = d;
  });
  return VIZ1_BY_CODE_YEAR;
}

/**
 * Resolve a roster country for a year. Exact pool row wins; otherwise carry-forward
 * last known (x,y) from an earlier year so markers don't vanish mid-timeline.
 * Does NOT invent publication counts — Total_Docs forced to 0 / N/A in hover.
 */
function resolveViz1NodeForYear(code, year) {
  const byYear = getViz1ByCodeYear()[code];
  if (!byYear) return null;
  if (byYear[year]) return byYear[year];
  let bestYear = null;
  for (const yStr of Object.keys(byYear)) {
    const y = +yStr;
    if (y < year && (bestYear == null || y > bestYear)) bestYear = y;
  }
  if (bestYear == null) return null;
  const src = byYear[bestYear];
  return {
    Country_Code: code,
    Country_Name: src.Country_Name,
    Year: year,
    Region: src.Region,
    Total_Docs: 0,
    H_Index: src.H_Index,
    GERD_Percent_GDP: src.GERD_Percent_GDP,
    GDP_Per_Capita_PPP: src.GDP_Per_Capita_PPP,
    x: src.x,
    y: src.y,
    _positionCarried: true,
    _carriedFromYear: bestYear
  };
}

function viz1EaseInOut(t) {
  return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
}

function cancelViz1Motion(keepTrails) {
  viz1MotionGen++;
  if (viz1MotionRaf) {
    cancelAnimationFrame(viz1MotionRaf);
    viz1MotionRaf = null;
  }
  if (!keepTrails) clearViz1Trails();
}

function clearViz1Trails() {
  viz1Trails = [];
  if (viz1TrailRaf) {
    cancelAnimationFrame(viz1TrailRaf);
    viz1TrailRaf = null;
  }
}

function ensureViz1TrailFadeLoop() {
  if (viz1TrailRaf) return;
  let lastFadePaint = 0;
  const tick = (now) => {
    viz1TrailRaf = null;
    if (viz1MotionRaf) {
      // Lerp owns frames; resume fade after motion ends
      viz1TrailRaf = requestAnimationFrame(tick);
      return;
    }
    viz1Trails = viz1Trails.filter((tr) => now - tr.born < tr.life);
    if (viz1Trails.length === 0) return;
    // ~20fps fade updates — enough for soft vanish without Plotly thrash
    if (now - lastFadePaint >= 50) {
      lastFadePaint = now;
      redrawViz1WithTrails();
    }
    viz1TrailRaf = requestAnimationFrame(tick);
  };
  viz1TrailRaf = requestAnimationFrame(tick);
}

function spawnViz1Trails(fromPos, toPos) {
  const candidates = [];
  for (const code of Object.keys(toPos)) {
    const a = fromPos[code];
    const b = toPos[code];
    if (!a || !b) continue;
    if (a.x == null || a.y == null || b.x == null || b.y == null) continue;
    const dist = Math.hypot(b.x - a.x, b.y - a.y);
    const size = Math.max(a.size || 0, b.size || 0);
    if (size < VIZ1_TRAIL_MIN_SIZE) continue;
    // Strength ∝ bubble size — USA/CHN thick bright tails; tiny nations almost none
    const strength = Math.min(1, Math.max(0, (size - VIZ1_TRAIL_MIN_SIZE) / 36));
    if (strength < 0.06) continue;
    // Giants trail on tiny drifts; small countries need a clearer hop (size-scaled eps)
    const minDist = VIZ1_MOVE_EPS + (1 - strength) * 0.08;
    if (dist < minDist) continue;
    candidates.push({ code, a, b, dist, size, strength });
  }
  candidates.sort((u, v) => v.strength - u.strength || v.dist - u.dist);
  const top = candidates.slice(0, 28);
  const now = performance.now();
  for (const c of top) {
    // Longer path sample for bigger/farther movers
    const nPts = Math.round(5 + c.strength * 14 + Math.min(8, c.dist * 20));
    const xs = [];
    const ys = [];
    for (let i = 0; i <= nPts; i++) {
      const t = i / nPts;
      xs.push(c.a.x + (c.b.x - c.a.x) * t);
      ys.push(c.a.y + (c.b.y - c.a.y) * t);
    }
    viz1Trails.push({
      code: c.code,
      color: c.a.color || c.b.color || '#56B4E9',
      xs,
      ys,
      width: 1.2 + c.strength * 7,
      baseOpacity: 0.22 + c.strength * 0.58,
      life: 1100 + c.strength * 900,
      born: now,
      head: 0 // 0..1 filled during lerp so comet grows behind the bubble
    });
  }
  if (viz1Trails.length > 48) viz1Trails = viz1Trails.slice(-48);
  // Fade loop starts after lerp finishes — otherwise it redraws from lastPositions mid-flight
}

/**
 * True when a country marker is currently drawn as a pickable/visible bubble
 * (size/opacity > 0 under region + Show Specific filters). Used to refuse
 * compare toggles on Plotly hit-tests against size-0 "ghost" markers.
 */
function isViz1CountryVisuallySelectable(code) {
  if (!code) return false;
  const row = (typeof VIZ1_DATA !== 'undefined')
    ? (VIZ1_DATA.find(d => d.Country_Code === code && d.Year === viz1Year)
      || VIZ1_DATA.find(d => d.Country_Code === code))
    : null;
  if (!row) return false;
  if (viz1SelectedRegion && row.Region !== viz1SelectedRegion) return false;
  if (viz1ShowSpecific && !VIZ1_SPECIFIC_COUNTRIES.includes(code)) return false;
  return true;
}

/**
 * Trail visibility multiplier matching marker focus rules for a country code.
 * Unfocused global view → 1.0 (keeps current trail look). Compare/search/region/
 * show-specific gate the same way as marker opacities in buildViz1MarkerBundle.
 */
function getViz1TrailVisibility(code) {
  if (!code) return 0;
  const row = (typeof VIZ1_DATA !== 'undefined')
    ? (VIZ1_DATA.find(d => d.Country_Code === code && d.Year === viz1Year)
      || VIZ1_DATA.find(d => d.Country_Code === code))
    : null;
  if (!row) return 0;
  if (viz1SelectedRegion && row.Region !== viz1SelectedRegion) return 0;
  if (viz1ShowSpecific && !VIZ1_SPECIFIC_COUNTRIES.includes(code)) return 0;

  const isCompareActive = viz1ComparedCountries.length > 0;
  if (isCompareActive) {
    return viz1ComparedCountries.includes(code) ? 1.0 : 0.05;
  }

  const searchTerms = viz1SearchQuery.toLowerCase().split(',').map(s => s.trim()).filter(Boolean);
  if (searchTerms.length > 0) {
    const name = (row.Country_Name || '').toLowerCase();
    const match = searchTerms.some(term => name.includes(term));
    return match ? 1.0 : 0.15;
  }

  return 1.0;
}

function buildViz1TrailTraces(now) {
  const traces = [];
  for (const tr of viz1Trails) {
    const age = now - tr.born;
    if (age >= tr.life) continue;
    const vis = getViz1TrailVisibility(tr.code);
    if (vis <= 0) continue;
    const fade = 1 - age / tr.life;
    const head = Math.max(0.05, Math.min(1, tr.head == null ? 1 : tr.head));
    const n = tr.xs.length;
    const cut = Math.max(2, Math.ceil(n * head));
    const xs = tr.xs.slice(0, cut);
    const ys = tr.ys.slice(0, cut);
    // Helios comet: bright head near bubble, fading tail (line + soft markers).
    // Multiply by marker-matched visibility so dimmed countries don't leave bright trails.
    const op = tr.baseOpacity * fade * vis;
    traces.push({
      x: xs,
      y: ys,
      mode: 'lines',
      type: 'scatter',
      line: {
        color: tr.color,
        width: Math.max(0.5, tr.width * fade * (0.55 + 0.45 * head)),
        shape: 'spline',
        simplify: false
      },
      opacity: op,
      hoverinfo: 'skip',
      showlegend: false,
      cliponaxis: false
    });
    // Soft glow dots denser toward the head
    const mx = [];
    const my = [];
    const ms = [];
    const mo = [];
    for (let i = 0; i < cut; i++) {
      const u = cut <= 1 ? 1 : i / (cut - 1);
      mx.push(xs[i]);
      my.push(ys[i]);
      ms.push(Math.max(1.5, tr.width * (0.25 + 0.85 * u) * fade));
      mo.push(op * (0.15 + 0.85 * u));
    }
    traces.push({
      x: mx,
      y: my,
      mode: 'markers',
      type: 'scatter',
      marker: {
        size: ms,
        color: tr.color,
        opacity: mo,
        line: { width: 0 }
      },
      hoverinfo: 'skip',
      showlegend: false,
      cliponaxis: false
    });
  }
  return traces;
}

function setViz1TrailHeads(progress) {
  // Only the trails spawned for this transition (recently born) grow with the lerp
  const now = performance.now();
  for (const tr of viz1Trails) {
    if (now - tr.born < VIZ1_LERP_MS + 80) tr.head = progress;
    else if (tr.head == null || tr.head < 1) tr.head = 1;
  }
}

/**
 * Build region marker traces for a year. positionOverride: {code:{x,y}} for lerp frames.
 * Returns { traces, positions }.
 */
function buildViz1MarkerBundle(targetYear, positionOverride) {
  const allRegions = getViz1Regions();
  let yearData = VIZ1_DATA.filter(d => d.Year === targetYear);
  if (viz1SelectedRegion) {
    yearData = yearData.filter(d => d.Region === viz1SelectedRegion);
  }

  const searchTerms = viz1SearchQuery.toLowerCase().split(',').map(s => s.trim()).filter(Boolean);
  const isSearchActive = searchTerms.length > 0;
  const matchesSearch = (countryName) => {
    if (!isSearchActive) return true;
    const name = (countryName || '').toLowerCase();
    return searchTerms.some(term => name.includes(term));
  };
  const isCompareActive = viz1ComparedCountries.length > 0;
  const rosters = getViz1RegionRosters();
  const positions = {};

  const traces = allRegions.map((region, globalIndex) => {
    const regionColor = viz1ColorPalette[globalIndex % viz1ColorPalette.length];
    const roster = rosters[region] || [];
    const nodes = roster.map((code) => {
      const d = resolveViz1NodeForYear(code, targetYear);
      if (!d) return null;
      // Region filter / roster region mismatch: only show if this year belongs here
      if (d.Region && d.Region !== region) return null;
      if (viz1SelectedRegion && d.Region !== viz1SelectedRegion) return null;
      return d;
    });

    if (roster.length === 0) {
      return { x: [], y: [], mode: 'markers', type: 'scatter', name: region, marker: { color: regionColor } };
    }

    const sizes = nodes.map((d) => {
      if (!d) return 0;
      if (viz1ShowSpecific && !VIZ1_SPECIFIC_COUNTRIES.includes(d.Country_Code)) return 0;
      // True-gap carry-forward: keep a faint pin so identity stays; do not look like real volume
      if (d._positionCarried) return 4;
      return Math.max(6, Math.sqrt(d.Total_Docs || 0) * 0.08);
    });

    const opacities = nodes.map((d) => {
      if (!d) return 0;
      if (viz1ShowSpecific && !VIZ1_SPECIFIC_COUNTRIES.includes(d.Country_Code)) return 0;
      const base = d._positionCarried ? 0.35 : 0.85;
      if (isCompareActive) return viz1ComparedCountries.includes(d.Country_Code) ? 1.0 : 0.05;
      if (!isSearchActive) return base;
      return matchesSearch(d.Country_Name) ? 1.0 : 0.15;
    });

    const lineWidths = nodes.map((d) => {
      if (!d) return 0;
      if (viz1ShowSpecific && !VIZ1_SPECIFIC_COUNTRIES.includes(d.Country_Code)) return 0;
      if (isCompareActive) return viz1ComparedCountries.includes(d.Country_Code) ? 4 : 0.5;
      if (!isSearchActive) return d._positionCarried ? 0.5 : 1;
      return matchesSearch(d.Country_Name) ? 3 : 0.5;
    });

    const lineColors = nodes.map((d) => {
      if (!d) return 'transparent';
      if (viz1ShowSpecific && !VIZ1_SPECIFIC_COUNTRIES.includes(d.Country_Code)) return 'transparent';
      if (isCompareActive) return viz1ComparedCountries.includes(d.Country_Code) ? '#56B4E9' : 'rgba(255,255,255,0.05)';
      if (!isSearchActive) return d._positionCarried ? 'rgba(255,255,255,0.35)' : 'rgba(255,255,255,0.7)';
      return matchesSearch(d.Country_Name) ? '#ffffff' : 'rgba(255,255,255,0.05)';
    });

    const hoverinfos = nodes.map((d) => {
      if (!d) return 'skip';
      if (viz1ShowSpecific && !VIZ1_SPECIFIC_COUNTRIES.includes(d.Country_Code)) return 'skip';
      return 'text';
    });

    const text = nodes.map((d) => (d ? formatViz1CountryDetailHtml(d) : ''));

    const xs = nodes.map((d, i) => {
      const code = roster[i];
      if (positionOverride && positionOverride[code] && positionOverride[code].x != null) {
        return positionOverride[code].x;
      }
      return d ? d.x : null;
    });
    const ys = nodes.map((d, i) => {
      const code = roster[i];
      if (positionOverride && positionOverride[code] && positionOverride[code].y != null) {
        return positionOverride[code].y;
      }
      return d ? d.y : null;
    });

    roster.forEach((code, i) => {
      const d = nodes[i];
      const x = xs[i];
      const y = ys[i];
      if (x == null || y == null) return;
      positions[code] = {
        x,
        y,
        size: sizes[i],
        color: regionColor,
        pubs: d && !d._positionCarried ? (d.Total_Docs || 0) : 0
      };
    });

    return {
      x: xs,
      y: ys,
      ids: roster.slice(),
      customdata: roster.slice(),
      mode: 'markers',
      type: 'scatter',
      name: region,
      text: text,
      hoverinfo: hoverinfos,
      marker: { size: sizes, color: regionColor, opacity: opacities, line: { color: lineColors, width: lineWidths }, sizemode: 'diameter', sizeref: 1 }
    };
  });

  return { traces, positions, yearData, allRegions };
}

function getViz1Layout() {
  return {
    uirevision: 'viz1',
    title: false,
    dragmode: 'zoom',
    // MUST stay 0: Plotly non-zero transition morphs SVG markers by list index.
    // When year roster order/length changed, index i became another country → USA "flew"
    // to the wrong coords. We animate by fixed roster + ids via rAF lerp instead; trails
    // are extra scatter traces under markers that fade over ~1.2–2s (size-scaled comets).
    transition: { duration: 0, easing: 'linear' },
    paper_bgcolor: 'transparent', plot_bgcolor: 'transparent',
    font: { family: 'Plus Jakarta Sans, sans-serif', color: '#f8fafc' },
    xaxis: {
      title: 'Dimensionality Reduction (Wealth, R&D, Volume, Quality)',
      type: 'linear',
      showgrid: true,
      gridcolor: 'rgba(255,255,255,0.05)',
      zeroline: false,
      showline: true,
      linecolor: 'rgba(255,255,255,0.2)',
      showticklabels: false,
      range: viz1IsZoomed ? undefined : VIZ1_AXIS.x.slice(),
      autorange: false,
      fixedrange: false
    },
    yaxis: {
      title: 'UMAP Projection Space',
      type: 'linear',
      showgrid: true,
      gridcolor: 'rgba(255,255,255,0.05)',
      zeroline: false,
      showline: true,
      linecolor: 'rgba(255,255,255,0.2)',
      showticklabels: false,
      range: viz1IsZoomed ? undefined : VIZ1_AXIS.y.slice(),
      autorange: false,
      fixedrange: false
    },
    hovermode: 'closest',
    hoverlabel: { bgcolor: 'rgba(15, 23, 42, 0.95)', font: { family: 'Plus Jakarta Sans, sans-serif', size: 13, color: '#f8fafc' }, bordercolor: '#56B4E9' },
    legend: { font: { color: '#e2e8f0', size: 12 }, orientation: 'h', yanchor: 'bottom', y: 1.05, xanchor: 'center', x: 0.5, itemclick: false, itemdoubleclick: false },
    margin: { l: 20, r: 20, t: 48, b: 28 }
  };
}

function bindViz1PlotEvents(container) {
  if (viz1EventsBound) return;
  viz1EventsBound = true;
  let ignoreNextBgClick = false;

  container.on('plotly_click', function(data) {
    const point = data.points && data.points[0];
    if (!point || point.customdata == null) return;
    // Ignore trail/comet traces (no country customdata on those)
    if (typeof point.customdata !== 'string') return;
    const code = point.customdata;
    // Size-0 / opacity-0 markers (Show Specific, region filter) still hit-test in Plotly —
    // refuse compare toggles so "empty" clicks cannot ghost-select hidden countries.
    if (!isViz1CountryVisuallySelectable(code)) return;
    ignoreNextBgClick = true;
    if (viz1ComparedCountries.includes(code)) {
      viz1ComparedCountries = viz1ComparedCountries.filter(c => c !== code);
    } else {
      viz1ComparedCountries.push(code);
    }
    updateViz1CompareUI();
    drawViz1Plotly({ animate: false });
    setTimeout(() => { ignoreNextBgClick = false; }, 50);
  });

  container.addEventListener('click', function(ev) {
    if (ignoreNextBgClick) return;
    const t = ev.target;
    if (!t || !t.classList) return;
    if (!(t.classList.contains('bg') || t.classList.contains('nsewdrag'))) return;
    if (viz1ComparedCountries.length) clearViz1Compare();
  });

  container.on('plotly_relayout', function(e) {
    if (!e) return;
    document.querySelectorAll('.plotly-notifier, .notifier-note').forEach((n) => n.remove());
    if (e['xaxis.range[0]'] != null || e['xaxis.range'] || e['yaxis.range[0]'] != null || e['yaxis.range']) {
      const xr = e['xaxis.range'] || (e['xaxis.range[0]'] != null ? [e['xaxis.range[0]'], e['xaxis.range[1]']] : null);
      const yr = e['yaxis.range'] || (e['yaxis.range[0]'] != null ? [e['yaxis.range[0]'], e['yaxis.range[1]']] : null);
      const curX = xr || (container.layout && container.layout.xaxis && container.layout.xaxis.range);
      const curY = yr || (container.layout && container.layout.yaxis && container.layout.yaxis.range);
      viz1IsZoomed = rangesDiffer(curX, VIZ1_AXIS.x) || rangesDiffer(curY, VIZ1_AXIS.y);
      updateViz1ZoomButton();
    }
    if (e['xaxis.autorange'] === true || e['yaxis.autorange'] === true) {
      viz1IsZoomed = false;
      updateViz1ZoomButton();
      Plotly.relayout(container, {
        'xaxis.range': VIZ1_AXIS.x.slice(),
        'yaxis.range': VIZ1_AXIS.y.slice(),
        'xaxis.autorange': false,
        'yaxis.autorange': false
      });
    }
  });

  container.on('plotly_doubleclick', function() {
    resetViz1Zoom();
    return false;
  });
  container.addEventListener('dblclick', function(ev) {
    ev.preventDefault();
    ev.stopPropagation();
    if (viz1IsZoomed) resetViz1Zoom();
  }, true);

  container.on('plotly_legendclick', function(data) {
    const r = data.data[data.curveNumber] && data.data[data.curveNumber].name;
    if (!r) return false;
    // Same region again → global; different region → switch focus. No chip/back button.
    viz1SelectedRegion = (viz1SelectedRegion === r) ? null : r;
    drawViz1Plotly({ animate: false });
    return false;
  });
}

let viz1PendingReact = null;

function reactViz1(container, traces, layout, config, opts = {}) {
  // During rAF lerp, drop frames if Plotly is still painting (avoids backlog / stutter)
  if (opts.skipIfBusy && viz1PendingReact) return Promise.resolve();
  const run = () => {
    viz1PendingReact = Plotly.react(container, traces, layout, config).then(() => {
      bindViz1PlotEvents(container);
      viz1PendingReact = null;
    }).catch(() => { viz1PendingReact = null; });
    return viz1PendingReact;
  };
  if (viz1PendingReact && !opts.skipIfBusy) {
    return viz1PendingReact.then(run, run);
  }
  return run();
}

function redrawViz1WithTrails() {
  const container = document.getElementById('viz1-plotly-container');
  if (!container || typeof Plotly === 'undefined' || typeof VIZ1_DATA === 'undefined') return;
  if (viz1MotionRaf) return; // do not fight in-flight year lerp
  const targetYear = parseInt(viz1Year, 10);
  const bundle = buildViz1MarkerBundle(targetYear, null);
  const layout = getViz1Layout();
  if (viz1IsZoomed && container.layout && container.layout.xaxis && container.layout.xaxis.range) {
    layout.xaxis.range = container.layout.xaxis.range.slice();
    layout.yaxis.range = container.layout.yaxis.range.slice();
  }
  const config = { displayModeBar: false, responsive: true, doubleClick: false, showTips: false };
  const trailTraces = buildViz1TrailTraces(performance.now());
  // Trails UNDER country markers (drawn first)
  reactViz1(container, trailTraces.concat(bundle.traces), layout, config);
}

function interpolatePositions(fromPos, toPos, t) {
  const out = {};
  const codes = new Set([...Object.keys(fromPos || {}), ...Object.keys(toPos || {})]);
  codes.forEach((code) => {
    const a = fromPos && fromPos[code];
    const b = toPos && toPos[code];
    if (a && b && a.x != null && b.x != null && a.y != null && b.y != null) {
      out[code] = {
        x: a.x + (b.x - a.x) * t,
        y: a.y + (b.y - a.y) * t,
        size: (b.size != null ? b.size : a.size),
        color: b.color || a.color,
        pubs: b.pubs != null ? b.pubs : a.pubs
      };
    } else if (b && b.x != null) {
      out[code] = { ...b };
    } else if (a && a.x != null && t < 1) {
      // Fading out of year — hold until end then drop
      out[code] = t < 0.95 ? { ...a } : null;
    }
  });
  Object.keys(out).forEach((k) => { if (!out[k]) delete out[k]; });
  return out;
}

function anyViz1Moved(fromPos, toPos) {
  if (!fromPos || !toPos) return false;
  for (const code of Object.keys(toPos)) {
    const a = fromPos[code];
    const b = toPos[code];
    if (!a || !b) continue;
    if (a.x != null && b.x != null && a.y != null && b.y != null) {
      if (Math.hypot(b.x - a.x, b.y - a.y) >= VIZ1_MOVE_EPS) return true;
    }
    // Pubs (marker size) can jump even when UMAP barely drifts — still lerp
    if (Math.abs((b.size || 0) - (a.size || 0)) >= 1.5) return true;
  }
  return false;
}

function updateViz1Stats(yearData, allRegions) {
  const statNations = document.getElementById('viz1-stat-nations');
  const statRegions = document.getElementById('viz1-stat-regions');
  const statPubs = document.getElementById('viz1-stat-pubs');
  if (statNations) statNations.textContent = yearData.length;
  if (statRegions) {
    if (viz1SelectedRegion) statRegions.textContent = 1;
    else statRegions.textContent = allRegions.length;
  }
  if (statPubs) {
    const totalPubs = Math.round(yearData.reduce((sum, d) => sum + (d.Total_Docs || 0), 0));
    // Compact form keeps the metric column readable in the narrow sidebar
    if (totalPubs >= 1e6) {
      statPubs.textContent = (totalPubs / 1e6).toFixed(totalPubs >= 1e7 ? 1 : 2).replace(/\.?0+$/, '') + 'M';
    } else if (totalPubs >= 1e4) {
      statPubs.textContent = (totalPubs / 1e3).toFixed(totalPubs >= 1e5 ? 0 : 1).replace(/\.0$/, '') + 'k';
    } else {
      statPubs.textContent = totalPubs.toLocaleString();
    }
    statPubs.title = totalPubs.toLocaleString() + ' publications';
  }
}

/**
 * Draw Graph 1. opts.animate (default true on year change) runs rAF lerp + comet trails.
 * Layout transition stays duration:0 — identity-safe motion uses fixed rosters + ids.
 */
function drawViz1Plotly(opts = {}) {
  const container = document.getElementById('viz1-plotly-container');
  if (!container || typeof VIZ1_DATA === 'undefined') return Promise.resolve();
  if (typeof Plotly === 'undefined') return Promise.resolve();

  const wantAnimate = opts.animate !== false;
  const targetYear = parseInt(viz1Year, 10);
  const yearChanged = viz1LastDrawnYear != null && viz1LastDrawnYear !== targetYear;
  const bundleTarget = buildViz1MarkerBundle(targetYear, null);
  updateViz1Stats(bundleTarget.yearData, bundleTarget.allRegions);
  // Refresh pinned detail whenever year/selection redraws (slider, Play, lerp end, compare toggle)
  updateViz1PinnedDetail();

  const layout = getViz1Layout();
  if (viz1IsZoomed && container.layout && container.layout.xaxis && container.layout.xaxis.range) {
    layout.xaxis.range = container.layout.xaxis.range.slice();
    layout.yaxis.range = container.layout.yaxis.range.slice();
  }
  const config = { displayModeBar: false, responsive: true, doubleClick: false, showTips: false };

  const shouldLerp = wantAnimate && yearChanged && viz1LastPositions && anyViz1Moved(viz1LastPositions, bundleTarget.positions);

  if (!shouldLerp) {
    const trailTraces = buildViz1TrailTraces(performance.now());
    viz1LastPositions = bundleTarget.positions;
    viz1LastDrawnYear = targetYear;
    return reactViz1(container, trailTraces.concat(bundleTarget.traces), layout, config);
  }

  // Spawn size-scaled comet trails (old → new), then lerp marker x/y by id-stable roster
  spawnViz1Trails(viz1LastPositions, bundleTarget.positions);
  const fromPos = viz1LastPositions;
  const toPos = bundleTarget.positions;
  const gen = ++viz1MotionGen;
  const lerpMs = Math.min(620, Math.max(280, Math.round(viz1Speed * 0.85)));

  return new Promise((resolve) => {
    const t0 = performance.now();
    let lastPaint = 0;

    const frame = (now) => {
      if (gen !== viz1MotionGen) {
        resolve();
        return;
      }
      const raw = Math.min(1, (now - t0) / lerpMs);
      const t = viz1EaseInOut(raw);
      // ~30fps ceiling during lerp; always paint the final frame
      if (raw < 1 && now - lastPaint < 32) {
        viz1MotionRaf = requestAnimationFrame(frame);
        return;
      }
      lastPaint = now;
      setViz1TrailHeads(t);
      const mid = interpolatePositions(fromPos, toPos, t);
      const midBundle = buildViz1MarkerBundle(targetYear, mid);
      midBundle.traces.forEach((tr) => {
        if (!tr.ids || !tr.marker) return;
        tr.ids.forEach((code, i) => {
          const a = fromPos[code];
          const b = toPos[code];
          if (a && b && tr.marker.size) {
            tr.marker.size[i] = (a.size || 0) + ((b.size || 0) - (a.size || 0)) * t;
          }
        });
      });
      const trailTraces = buildViz1TrailTraces(now);
      const lay = getViz1Layout();
      if (viz1IsZoomed && container.layout && container.layout.xaxis && container.layout.xaxis.range) {
        lay.xaxis.range = container.layout.xaxis.range.slice();
        lay.yaxis.range = container.layout.yaxis.range.slice();
      }
      reactViz1(container, trailTraces.concat(midBundle.traces), lay, config, { skipIfBusy: raw < 1 });

      if (raw < 1) {
        viz1MotionRaf = requestAnimationFrame(frame);
      } else {
        viz1MotionRaf = null;
        setViz1TrailHeads(1);
        viz1LastPositions = toPos;
        viz1LastDrawnYear = targetYear;
        const trailTracesEnd = buildViz1TrailTraces(performance.now());
        reactViz1(container, trailTracesEnd.concat(bundleTarget.traces), layout, config).then(resolve, resolve);
        ensureViz1TrailFadeLoop();
      }
    };

    viz1MotionRaf = requestAnimationFrame(frame);
  });
}


// ══════════════════════════════════════════════════════════
// VIZ 2: Global Quality Shift (Beeswarm Bubble Chart)
// ══════════════════════════════════════════════════════════
let activeRegionFilter = "All";
let activeContinentFilter = "All";
let minPubFilter = 0;
let minHIndexFilter = 0;
let minRdFilter = 0;
let minGdpFilter = 0;
let selectedCountryTrail = null;
let barChartMode = "grouped";
let yAxisScaleMode = "linear";
let activeSortParameter = "Default";

const getCountryMetrics = (countryName, year, q1Count, q4Count, totalCount) => {
  // Base metrics mapping
  const baseMetrics = {
    "United States": { continent: "Americas", rd: 2.74, gdp: 55000, h: 1279 },
    "United Kingdom": { continent: "Europe", rd: 1.77, gdp: 42000, h: 554 },
    "Germany": { continent: "Europe", rd: 2.74, gdp: 45000, h: 505 },
    "China": { continent: "Asia", rd: 1.71, gdp: 8000, h: 583 },
    "India": { continent: "Asia", rd: 0.85, gdp: 1700, h: 260 },
    "Japan": { continent: "Asia", rd: 3.14, gdp: 39000, h: 429 },
    "South Korea": { continent: "Asia", rd: 3.47, gdp: 28000, h: 349 },
    "Brazil": { continent: "Americas", rd: 1.16, gdp: 9000, h: 234 },
    "France": { continent: "Europe", rd: 2.18, gdp: 40000, h: 470 },
    "Canada": { continent: "Americas", rd: 1.80, gdp: 44000, h: 468 },
    "Australia": { continent: "Oceania", rd: 2.24, gdp: 50000, h: 393 },
    "Russian Federation": { continent: "Europe", rd: 1.13, gdp: 11000, h: 266 },
    "South Africa": { continent: "Africa", rd: 0.73, gdp: 6000, h: 168 },
    "Saudi Arabia": { continent: "Asia", rd: 0.48, gdp: 20000, h: 137 },
    "Switzerland": { continent: "Europe", rd: 2.93, gdp: 80000, h: 478 },
    "Singapore": { continent: "Asia", rd: 2.01, gdp: 58000, h: 229 },
    "Turkey": { continent: "Asia", rd: 0.84, gdp: 10000, h: 169 },
    "Israel": { continent: "Asia", rd: 3.93, gdp: 37000, h: 272 },
    
    // Continent Mapping & sensible averages for other countries
    "Argentina": { continent: "Americas", rd: 0.58, gdp: 12000, h: 120 },
    "Austria": { continent: "Europe", rd: 2.90, gdp: 48000, h: 250 },
    "Belgium": { continent: "Europe", rd: 2.30, gdp: 43000, h: 280 },
    "Chile": { continent: "Americas", rd: 0.38, gdp: 14000, h: 110 },
    "Colombia": { continent: "Americas", rd: 0.25, gdp: 6000, h: 80 },
    "Croatia": { continent: "Europe", rd: 0.85, gdp: 13500, h: 90 },
    "Czech Republic": { continent: "Europe", rd: 1.60, gdp: 19000, h: 140 },
    "Denmark": { continent: "Europe", rd: 2.95, gdp: 53000, h: 320 },
    "Egypt": { continent: "Africa", rd: 0.60, gdp: 3000, h: 95 },
    "Finland": { continent: "Europe", rd: 2.80, gdp: 46000, h: 210 },
    "Greece": { continent: "Europe", rd: 0.80, gdp: 18000, h: 180 },
    "Hong Kong": { continent: "Asia", rd: 0.75, gdp: 40000, h: 220 },
    "Hungary": { continent: "Europe", rd: 1.20, gdp: 13000, h: 120 },
    "Indonesia": { continent: "Asia", rd: 0.20, gdp: 3500, h: 70 },
    "Iran": { continent: "Asia", rd: 0.30, gdp: 5000, h: 110 },
    "Ireland": { continent: "Europe", rd: 1.50, gdp: 60000, h: 230 },
    "Italy": { continent: "Europe", rd: 1.25, gdp: 30000, h: 360 },
    "Malaysia": { continent: "Asia", rd: 1.10, gdp: 10000, h: 115 },
    "Mexico": { continent: "Americas", rd: 0.50, gdp: 9000, h: 140 },
    "Netherlands": { continent: "Europe", rd: 2.00, gdp: 49000, h: 390 },
    "New Zealand": { continent: "Oceania", rd: 1.20, gdp: 38000, h: 190 },
    "Norway": { continent: "Europe", rd: 1.70, gdp: 75000, h: 240 },
    "Pakistan": { continent: "Asia", rd: 0.30, gdp: 1400, h: 75 },
    "Peru": { continent: "Americas", rd: 0.15, gdp: 6000, h: 60 },
    "Philippines": { continent: "Asia", rd: 0.15, gdp: 2800, h: 55 },
    "Poland": { continent: "Europe", rd: 1.00, gdp: 13000, h: 170 },
    "Portugal": { continent: "Europe", rd: 1.30, gdp: 20000, h: 150 },
    "Romania": { continent: "Europe", rd: 0.40, gdp: 9000, h: 90 },
    "Spain": { continent: "Europe", rd: 1.20, gdp: 26000, h: 290 },
    "Sweden": { continent: "Europe", rd: 3.20, gdp: 50000, h: 340 },
    "Taiwan": { continent: "Asia", rd: 3.00, gdp: 22000, h: 250 },
    "Thailand": { continent: "Asia", rd: 0.40, gdp: 58000, h: 95 },
    "Ukraine": { continent: "Europe", rd: 0.50, gdp: 3000, h: 105 },
    "United Arab Emirates": { continent: "Asia", rd: 0.90, gdp: 40000, h: 110 },
    "Venezuela": { continent: "Americas", rd: 0.30, gdp: 8000, h: 65 }
  };

  const defaultsByRegion = {
    "Northern America": { continent: "Americas", rd: 1.8, gdp: 45000, h: 200 },
    "Latin America": { continent: "Americas", rd: 0.4, gdp: 7000, h: 70 },
    "Western Europe": { continent: "Europe", rd: 2.1, gdp: 38000, h: 220 },
    "Eastern Europe": { continent: "Europe", rd: 0.8, gdp: 10000, h: 90 },
    "Asiatic Region": { continent: "Asia", rd: 0.8, gdp: 6000, h: 80 },
    "Middle East": { continent: "Asia", rd: 0.6, gdp: 15000, h: 85 },
    "Africa": { continent: "Africa", rd: 0.3, gdp: 2500, h: 45 },
    "Pacific Region": { continent: "Oceania", rd: 1.5, gdp: 30000, h: 150 },
    "Africa/Middle East": { continent: "Africa", rd: 0.4, gdp: 4000, h: 55 }
  };

  const countryToRegion = {};
  Object.values(DATA.getRidgelineData() || {}).flat().forEach(c => {
    if (c.country && c.region) {
      countryToRegion[c.country] = c.region;
    }
  });

  const match = baseMetrics[countryName];
  if (match) {
    const dy = year - 1999;
    const gdpGrown = match.gdp * Math.pow(1.025, dy);
    const hGrown = Math.round(match.h + dy * 2);
    return {
      continent: match.continent,
      rd: match.rd,
      gdp: gdpGrown,
      h: hGrown,
      publications: totalCount
    };
  } else {
    const region = countryToRegion[countryName] || "Western Europe";
    const regDefault = defaultsByRegion[region] || { continent: "Europe", rd: 1.0, gdp: 10000, h: 80 };
    const dy = year - 1999;
    const gdpGrown = regDefault.gdp * Math.pow(1.018, dy);
    const hGrown = Math.round(regDefault.h + dy * 1.5);
    return {
      continent: regDefault.continent,
      rd: regDefault.rd,
      gdp: gdpGrown,
      h: hGrown,
      publications: totalCount
    };
  }
};

function renderViz2(body) {
  body.innerHTML = "";

  // Container styling
  const container = document.createElement("div");
  container.className = "viz2-dashboard-container";
  container.style.width = "100%";
  container.style.height = "100%";
  container.style.display = "flex";
  container.style.flexDirection = "column";
  container.style.padding = "20px";
  container.style.boxSizing = "border-box";
  
  const header = document.createElement("div");
  header.innerHTML = `
    <h3 style="color: var(--text); font-size: 1.2rem; font-weight: 600; margin-bottom: 0.5rem;">The Elite Breakaway vs The Q4 Flood</h3>
    <p style="color: var(--text-muted); font-size: 0.9rem; margin-bottom: 1.5rem; max-width: 800px;">
      This Ridgeline Plot visualizes the distribution of national publication quality ratios (Q1 / Q4) from 1996 to 2024. 
      A rightward shift indicates a transition toward elite, high-impact research. A leftward shift indicates a surge in lower-tier (Q4) publications.
    </p>
  `;
  container.appendChild(header);

  const graphCard = document.createElement("div");
  graphCard.className = "viz2-graph-card";
  graphCard.style.flex = "1";
  graphCard.style.position = "relative";
  graphCard.style.background = "rgba(15, 23, 42, 0.4)";
  graphCard.style.border = "1px solid rgba(255, 255, 255, 0.06)";
  graphCard.style.borderRadius = "12px";
  graphCard.style.padding = "1rem";
  graphCard.id = "ridgeline-svg-container";
  container.appendChild(graphCard);

  body.appendChild(container);

  if (typeof RIDGELINE_DENSITY === 'undefined') {
    graphCard.innerHTML = "<p style='color:red;'>Error: RIDGELINE_DENSITY data not found.</p>";
    return;
  }

  // Draw Ridgeline
  const width = graphCard.clientWidth - 40;
  const height = graphCard.clientHeight - 40;
  const margin = {top: 60, right: 30, bottom: 50, left: 80};

  const svg = d3.select("#ridgeline-svg-container")
    .append("svg")
    .attr("width", width)
    .attr("height", height)
    .append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);

  const innerWidth = width - margin.left - margin.right;
  const innerHeight = height - margin.top - margin.bottom;

  // X axis
  const x = d3.scaleLinear()
    .domain([-0.2, 5.0])
    .range([0, innerWidth]);

  svg.append("g")
    .attr("transform", `translate(0, ${innerHeight})`)
    .call(d3.axisBottom(x).tickValues([0, 1, 2, 3, 4, 5]).tickFormat(d => d + "x"))
    .attr("color", "var(--text-muted)")
    .style("font-family", "Outfit")
    .style("font-size", "0.8rem");
    
  svg.append("text")
    .attr("text-anchor", "end")
    .attr("x", innerWidth)
    .attr("y", innerHeight + 40)
    .text("Quality Ratio (Q1 / Q4 Documents)")
    .attr("fill", "var(--text-muted)")
    .style("font-family", "Outfit")
    .style("font-size", "0.9rem");

  // Create Y scale for the years
  const years = RIDGELINE_DENSITY.map(d => d.year);
  const yName = d3.scaleBand()
    .domain(years)
    .range([innerHeight, 0])
    .paddingInner(1);

  svg.append("g")
    .call(d3.axisLeft(yName).tickSize(0))
    .attr("color", "var(--text-muted)")
    .style("font-family", "Outfit")
    .style("font-size", "0.85rem")
    .select(".domain").remove();

  // Create Y scale for the density heights (overlap)
  const maxDensity = d3.max(RIDGELINE_DENSITY, d => d3.max(d.points, p => p.y));
  const y = d3.scaleLinear()
    .domain([0, maxDensity])
    .range([innerHeight/years.length * 4, 0]); // overlap factor of 4

  // Color scale
  const color = d3.scaleSequential()
    .domain([d3.min(years), d3.max(years)])
    .interpolator(d3.interpolateViridis);

  // Area generator
  const area = d3.area()
    .curve(d3.curveBasis)
    .x(d => x(d.x))
    .y0(y(0))
    .y1(d => y(d.y));

  // Add areas
  const areas = svg.selectAll("areas")
    .data(RIDGELINE_DENSITY)
    .enter()
    .append("path")
      .attr("transform", d => `translate(0, ${(yName(d.year) - (innerHeight/years.length * 4))})`)
      .datum(d => d.points)
      .attr("fill", (d, i) => color(RIDGELINE_DENSITY[i].year))
      .attr("stroke", "#000")
      .attr("stroke-width", 1)
      .attr("opacity", 0.7)
      .attr("d", area);
      
  areas.on("mouseover", function(event, d) {
        d3.select(this).attr("opacity", 1).attr("stroke-width", 2);
      })
      .on("mouseleave", function(event, d) {
        d3.select(this).attr("opacity", 0.7).attr("stroke-width", 1);
      });
}


function renderViz3(body) {
  // Clear container
  body.innerHTML = '';
  
  // Set up container
  const container = document.createElement('div');
  container.className = 'viz3-container';
  container.style.width = '100%';
  container.style.height = '100%';
  container.style.overflowY = 'auto';
  container.style.position = 'relative';
  
  // Inject HTML structure
  container.innerHTML = `
    <style>
      .viz3-container {
            --bg-color: #0b0f19;
            --card-bg: rgba(17, 22, 39, 0.7);
            --card-border: rgba(255, 255, 255, 0.07);
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --accent-glow: rgba(86, 180, 233, 0.15);
            --primary: #56B4E9;
            --primary-glow: rgba(86, 180, 233, 0.4);
            
            /* Topic Gradients — Okabe-Ito */
            --g-ai: linear-gradient(90deg, #D55E00 0%, #E69F00 100%);
            --g-crispr: linear-gradient(90deg, #56B4E9 0%, #0072B2 100%);
            --g-diseases: linear-gradient(90deg, #CC79A7 0%, #D55E00 100%);
            --g-data: linear-gradient(90deg, #0072B2 0%, #56B4E9 100%);
            --g-energy: linear-gradient(90deg, #009E73 0%, #56B4E9 100%);
            --g-robotics: linear-gradient(90deg, #E69F00 0%, #F0E442 100%);
            --g-purple: linear-gradient(90deg, #E69F00 0%, #F0E442 100%);
            --g-quantum: linear-gradient(90deg, #F0E442 0%, #56B4E9 100%);
        }

        

        

        /* Glassmorphism Styles */
        .glass-card {
            background: var(--card-bg);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid var(--card-border);
            border-radius: 16px;
            padding: 1.5rem;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        }

        .viz3-controls-card {
            padding: 0.75rem 1rem !important;
            border-radius: 12px !important;
        }

        /* Header */
        header {
            margin-bottom: 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .header-title h1 {
            font-size: 2.2rem;
            font-weight: 800;
            letter-spacing: -0.5px;
            background: linear-gradient(135deg, #fff 0%, #94a3b8 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .header-title p {
            color: var(--text-muted);
            font-size: 1rem;
            margin-top: 0.25rem;
            text-transform: uppercase;
            letter-spacing: 2px;
            font-weight: 500;
        }

        .group-badge {
            background: rgba(86, 180, 233, 0.1);
            border: 1px solid rgba(86, 180, 233, 0.2);
            padding: 0.5rem 1rem;
            border-radius: 30px;
            font-weight: 600;
            color: var(--primary);
            text-shadow: 0 0 10px var(--primary-glow);
            box-shadow: 0 0 15px rgba(86, 180, 233, 0.05);
        }

        /* Dashboard Grid Layout */
        .dashboard-grid {
            display: grid;
            grid-template-columns: 1.25fr 1.75fr;
            gap: 1.5rem;
            margin-bottom: 1.5rem;
        }

        @media (max-width: 1200px) {
            .dashboard-grid {
                grid-template-columns: 1fr;
            }
        }

        /* Left Panel - Control & Bar Race */
        .control-panel {
            display: flex;
            flex-direction: column;
            gap: 1rem;
        }

        .filter-group {
            display: flex;
            flex-direction: column;
            gap: 0.35rem;
        }

        .filter-group label {
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: var(--text-muted);
            font-weight: 600;
        }

        .styled-select {
            background: rgba(25, 30, 50, 0.8);
            border: 1px solid var(--card-border);
            color: var(--text-main);
            padding: 0.45rem 0.85rem;
            border-radius: 8px;
            outline: none;
            font-size: 0.85rem;
            font-family: inherit;
            width: 100%;
            cursor: pointer;
            transition: all 0.3s ease;
        }

        .styled-select:focus {
            border-color: var(--primary);
            box-shadow: 0 0 10px var(--accent-glow);
        }

        /* Playback Controls */
        .playback-controls {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            margin-top: 0.25rem;
        }

        .btn-control {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid var(--card-border);
            color: var(--text-main);
            width: 36px;
            height: 36px;
            border-radius: 50px;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            outline: none;
        }

        .btn-control:hover {
            background: rgba(255, 255, 255, 0.1);
            border-color: rgba(255, 255, 255, 0.2);
            transform: scale(1.05);
        }

        .btn-play {
            background: var(--primary);
            color: #0b0f19;
            border: none;
            box-shadow: 0 0 15px var(--primary-glow);
        }

        .btn-play:hover {
            background: #fff;
            transform: scale(1.08);
            box-shadow: 0 0 20px rgba(255, 255, 255, 0.5);
        }

        .timeline-container {
            flex-grow: 1;
            display: flex;
            flex-direction: column;
            gap: 0.35rem;
        }

        .timeline-slider {
            -webkit-appearance: none;
            width: 100%;
            height: 6px;
            border-radius: 3px;
            background: rgba(255, 255, 255, 0.1);
            outline: none;
            cursor: pointer;
            transition: all 0.3s ease;
        }

        .timeline-slider::-webkit-slider-thumb {
            -webkit-appearance: none;
            appearance: none;
            width: 16px;
            height: 16px;
            border-radius: 50%;
            background: var(--primary);
            box-shadow: 0 0 10px var(--primary-glow);
            cursor: pointer;
            transition: transform 0.1s ease;
        }

        .timeline-slider::-webkit-slider-thumb:hover {
            transform: scale(1.2);
        }

        .timeline-labels {
            display: flex;
            justify-content: space-between;
            font-size: 0.8rem;
            color: var(--text-muted);
            font-weight: 500;
        }

        .speed-selector {
            display: flex;
            background: rgba(0, 0, 0, 0.2);
            padding: 4px;
            border-radius: 8px;
            border: 1px solid var(--card-border);
        }

        .speed-btn {
            background: none;
            border: none;
            color: var(--text-muted);
            padding: 0.4rem 0.8rem;
            border-radius: 6px;
            cursor: pointer;
            font-family: inherit;
            font-size: 0.8rem;
            font-weight: 600;
            transition: all 0.2s ease;
        }

        .speed-btn.active {
            background: rgba(255, 255, 255, 0.08);
            color: var(--text-main);
        }

        /* Bar Chart Race Container */
        .race-card {
            position: relative;
            min-height: 480px;
            display: flex;
            flex-direction: column;
        }

        .race-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1.5rem;
            z-index: 1;
        }

        .race-header h3 {
            font-size: 1.2rem;
            font-weight: 700;
            color: var(--text-main);
        }

        .year-display {
            font-size: 1.8rem;
            font-weight: 800;
            color: var(--primary);
            text-shadow: 0 0 10px var(--primary-glow);
        }

        .race-

        /* Watermark */
        .watermark-year {
            position: absolute;
            bottom: 10px;
            right: 10px;
            font-size: 8rem;
            font-weight: 800;
            color: rgba(255, 255, 255, 0.035);
            pointer-events: none;
            line-height: 1;
            user-select: none;
            z-index: 0;
            font-family: inherit;
            letter-spacing: -2px;
        }

        /* Background Grid Lines */
        .grid-lines-container {
            position: absolute;
            top: 0;
            bottom: 0;
            left: 200px;
            right: 90px;
            pointer-events: none;
            z-index: 0;
        }

        .grid-line {
            position: absolute;
            top: 0;
            bottom: 0;
            border-left: 1px dashed rgba(255, 255, 255, 0.05);
        }

        .grid-line-label {
            position: absolute;
            bottom: -20px;
            transform: translateX(-50%);
            font-size: 0.75rem;
            color: var(--text-muted);
        }

        /* Race Rows */
        .race-row {
            position: absolute;
            left: 0;
            right: 0;
            height: 44px;
            display: flex;
            align-items: center;
            transition: top 0.5s cubic-bezier(0.25, 0.8, 0.25, 1);
            z-index: 1;
        }

        .topic-info {
            width: 200px;
            display: flex;
            align-items: center;
            gap: 0.6rem;
            padding-right: 1rem;
        }

        .topic-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            flex-shrink: 0;
        }

        .topic-name {
            font-size: 0.85rem;
            font-weight: 600;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            color: var(--text-main);
        }

        .bar-container {
            flex-grow: 1;
            height: 24px;
            background: rgba(255, 255, 255, 0.02);
            border-radius: 12px;
            position: relative;
            overflow: hidden;
        }

        .bar-fill {
            height: 100%;
            border-radius: 12px;
            width: 0%;
            transition: width 0.5s cubic-bezier(0.25, 0.8, 0.25, 1);
            box-shadow: 0 0 10px rgba(255, 255, 255, 0.05);
        }

        .value-display {
            width: 90px;
            text-align: right;
            font-size: 0.95rem;
            font-weight: 700;
            color: var(--text-main);
            padding-left: 0.5rem;
            font-variant-numeric: tabular-nums;
        }

        /* Right Panel - Line Chart */
        .trend-card {
            display: flex;
            flex-direction: column;
            gap: 1rem;
            height: 100%;
        }

        .trend-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .trend-header h3 {
            font-size: 1.2rem;
            font-weight: 700;
        }

        .chart-container {
            position: relative;
            flex-grow: 1;
            min-height: 380px;
            width: 100%;
        }

        /* Insights Stats Grid */
        .insights-section {
            margin-top: 1.5rem;
        }

        .insights-title {
            font-size: 1.3rem;
            font-weight: 800;
            margin-bottom: 1rem;
            background: linear-gradient(135deg, #fff 0%, #94a3b8 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .insights-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(290px, 1fr));
            gap: 1rem;
        }

        .insight-card {
            border: 1px solid var(--card-border);
            border-radius: 14px;
            padding: 1.25rem;
            background: rgba(15, 20, 35, 0.4);
            display: flex;
            flex-direction: column;
            gap: 0.75rem;
            transition: transform 0.3s ease, border-color 0.3s ease;
        }

        .insight-card:hover {
            transform: translateY(-2px);
            border-color: rgba(255, 255, 255, 0.15);
        }

        .card-top {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
        }

        .card-title {
            font-size: 0.95rem;
            font-weight: 700;
            color: var(--text-main);
            max-width: 75%;
        }

        .subfield-pill {
            background: rgba(255, 255, 255, 0.05);
            padding: 2px 6px;
            border-radius: 6px;
            font-size: 0.7rem;
            font-weight: 600;
            color: var(--text-muted);
            border: 1px solid var(--card-border);
        }

        .card-metric {
            display: flex;
            align-items: baseline;
            gap: 0.5rem;
        }

        .metric-value {
            font-size: 1.5rem;
            font-weight: 800;
            color: var(--text-main);
        }

        .metric-label {
            font-size: 0.75rem;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .card-footer {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 0.5rem;
            padding-top: 0.75rem;
            border-top: 1px solid rgba(255, 255, 255, 0.05);
            font-size: 0.8rem;
        }

        .footer-item {
            display: flex;
            flex-direction: column;
            gap: 0.15rem;
        }

        .footer-label {
            color: var(--text-muted);
            font-size: 0.7rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .footer-value {
            color: var(--text-main);
            font-weight: 600;
        }

        .footer-value.highlight-green {
            color: #009E73;
        }

        /* SVG Icon styling */
        .icon {
            width: 20px;
            height: 20px;
            fill: currentColor;
        }
    </style>
    <div style="padding: 2rem;">
      <header>
        <div class="header-title">
            <h1>The Global Knowledge & Wealth Paradox</h1>
            <p>CS661 Visual Analytics &bull; Group 10 Dashboard</p>
        </div>
        <div class="group-badge">Project Module 4.3: Research topics evolution</div>
    </header>

    <!-- Controls Card (Redesigned Compact Version) -->
    <div class="glass-card viz3-controls-card" style="margin-bottom: 1.25rem;">
        <div style="display: flex; flex-direction: column; gap: 0.65rem;">
            
            <!-- Country Selector -->
            <div class="filter-group">
                <label for="countrySelect">Region / Country Filter</label>
                <select id="countrySelect" class="styled-select">
                    <option value="GLOBAL">Global (All Countries)</option>
                </select>
            </div>

            <!-- Playback Controls & Slider Row -->
            <div style="display: flex; align-items: center; gap: 0.85rem; flex-wrap: wrap;">
                
                <div class="playback-controls">
                    <!-- Play/Pause Button -->
                    <button id="btnPlay" class="btn-control btn-play" title="Play Animation">
                        <svg id="playIcon" class="icon" style="width: 20px; height: 20px;" viewBox="0 0 24 24">
                            <path d="M8 5v14l11-7z"/>
                        </svg>
                        <svg id="pauseIcon" class="icon" style="display: none; width: 20px; height: 20px;" viewBox="0 0 24 24">
                            <path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z"/>
                        </svg>
                    </button>

                    <!-- Reset Button -->
                    <button id="btnReset" class="btn-control" title="Restart to 2000">
                        <svg class="icon" style="width: 20px; height: 20px;" viewBox="0 0 24 24">
                            <path d="M12 5V1L7 6l5 5V7c3.31 0 6 2.69 6 6s-2.69 6-6 6-6-2.69-6-6H4c0 4.42 3.58 8 8 8s8-3.58 8-8-3.58-8-8-8z"/>
                        </svg>
                    </button>
                </div>

                <!-- Timeline Scrubber -->
                <div class="timeline-container">
                    <div class="timeline-labels">
                        <span id="labelStartYear">2000</span>
                        <span id="labelCurrentYear" style="font-weight: 700; color: var(--primary);">Year: 2000</span>
                        <span id="labelEndYear">2024</span>
                    </div>
                    <input type="range" id="timelineSlider" class="timeline-slider" min="2000" max="2024" value="2000">
                </div>

                <!-- Speed Controls -->
                <div class="filter-group">
                    <label>Speed</label>
                    <div class="speed-selector">
                        <button class="speed-btn" data-speed="0.5">0.5x</button>
                        <button class="speed-btn active" data-speed="1.0">1.0x</button>
                        <button class="speed-btn" data-speed="2.0">2.0x</button>
                    </div>
                </div>

            </div>

        </div>
    </div>

    <!-- Main Grid Content -->
    <div class="dashboard-grid">
        
        <!-- Left Panel: Bar Chart Race -->
        <div class="control-panel">
            <!-- Bar Chart Race Card -->
            <div class="glass-card race-card">
                <div class="race-header">
                    <h3>Top Research topics</h3>
                    <div id="yearIndicator" class="year-display">2000</div>
                </div>
                
                <div class="race-body" id="raceBody">
                    <!-- Watermark -->
                    <div id="watermarkYear" class="watermark-year">2000</div>
                    
                    <!-- Background Grid Lines -->
                    <div class="grid-lines-container" id="gridLines">
                        <!-- Will be populated dynamically -->
                    </div>

                    <!-- Rows Container -->
                    <div id="rowsContainer" style="position: relative; width: 100%; height: 100%;">
                        <!-- Will be populated dynamically with topic rows -->
                    </div>
                </div>
            </div>
        </div>

        <!-- Right Panel: Trend Line Chart -->
        <div class="glass-card trend-card">
            <div class="trend-header">
                <h3>Yearly Publication Trend (2000 – 2024)</h3>
            </div>
            <div class="chart-container">
                <canvas id="trendChart"></canvas>
            </div>
            <p style="margin: 0.75rem 1rem 1rem; font-size: 0.78rem; line-height: 1.45; color: #94a3b8;">
              OpenAlex concept counts for 2000–2024 only. Pre-2000 rows are withheld: AI uses a broad L1 concept
              (<code>C154945302</code>, ~36M works) with retrospective tagging, while Infectious uses a narrow L3 specialty —
              early-year comparisons were misleading. Absolute levels across topics are not directly comparable.
            </p>
        </div>

    </div>

    <!-- Bottom Section: Insights Grid -->
    <div class="insights-section">
        <h2 class="insights-title">
            <svg class="icon" style="color: var(--primary); width: 20px; height: 20px;" viewBox="0 0 24 24">
                <path d="M9 21c0 .55.45 1 1 1h4c.55 0 1-.45 1-1v-1H9v1zm3-19C8.14 2 5 5.14 5 9c0 2.38 1.19 4.47 3 5.74V17c0 .55.45 1 1 1h6c.55 0 1-.45 1-1v-2.26c1.81-1.27 3-3.36 3-5.74 0-3.86-3.14-7-7-7zm2.85 11.1l-.85.6V16h-4v-2.3l-.85-.6C7.8 12.16 7 10.63 7 9c0-2.76 2.24-5 5-5s5 2.24 5 5c0 1.63-.8 3.16-2.15 4.1z"/>
            </svg>
            Research Topic Performance Summary
        </h2>
        <div class="insights-grid" id="insightsGrid">
            <!-- Will be populated dynamically -->
        </div>
    </div>
    </div>
  `;
  body.appendChild(container);

  // Inject JS Logic
  if (typeof window.CSV_DATA === 'undefined') {
            document.body.innerHTML = `
                <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; padding: 2rem; text-align: center;">
                    <h2 style="color: #D55E00; margin-bottom: 1rem;">Data File Missing</h2>
                    <p style="color: #94a3b8; max-width: 500px;">
                        Could not find the <code>data.js</code> file. Please make sure you have run the data conversion script or have the file <code>data.js</code> present in the same directory.
                    </p>
                </div>
            `;
            throw new Error("data.js is not loaded.");
        }

        // Configuration and data stores
        const topics = [
            "AI & Machine Learning",
            "CRISPR & Genomics",
            "Infectious Diseases",
            "Data Science & Big Data",
            "Renewable Energy",
            "Robotics & Automation",
            "Quantum Computing"
        ];

        const topicSubfields = {
            "AI & Machine Learning": "C154945302",
            "CRISPR & Genomics": "C98108389",
            "Infectious Diseases": "C524204448",
            "Data Science & Big Data": "C2522767166",
            "Renewable Energy": "C188573790",
            "Robotics & Automation": "C34413123",
            "Quantum Computing": "C58053490"
        };

        const topicGradients = {
            "AI & Machine Learning": 'var(--g-ai)',
            "CRISPR & Genomics": 'var(--g-crispr)',
            "Infectious Diseases": 'var(--g-diseases)',
            "Data Science & Big Data": 'var(--g-data)',
            "Renewable Energy": 'var(--g-energy)',
            "Robotics & Automation": 'var(--g-purple)',
            "Quantum Computing": 'var(--g-quantum)'
        };

        const topicColors = {
            "AI & Machine Learning": '#D55E00',
            "CRISPR & Genomics": '#56B4E9',
            "Infectious Diseases": '#CC79A7',
            "Data Science & Big Data": '#0072B2',
            "Renewable Energy": '#009E73',
            "Robotics & Automation": '#E69F00',
            "Quantum Computing": '#F0E442'
        };

        const years = [];
        for (let y = 2000; y <= 2024; y++) {
            years.push(y);
        }
        const yearMin = years[0];
        const yearMax = years[years.length - 1];

        let globalData = {};  // globalData[year][topic] = sum
        let countryData = {}; // countryData[countryCode][year][topic] = count
        let countryMap = {};  // countryMap[countryCode] = countryName

        // Application State
        let currentYear = yearMin;
        let isPlaying = false;
        let speedMultiplier = 1.0;
        let selectedCountry = 'GLOBAL';
        let playTimeout = null;
        let lineChart = null;

        // HTML elements cached
        const countrySelect = container.querySelector('#countrySelect');
        const btnPlay = container.querySelector('#btnPlay');
        const playIcon = container.querySelector('#playIcon');
        const pauseIcon = container.querySelector('#pauseIcon');
        const btnReset = container.querySelector('#btnReset');
        const timelineSlider = container.querySelector('#timelineSlider');
        const labelCurrentYear = container.querySelector('#labelCurrentYear');
        const yearIndicator = container.querySelector('#yearIndicator');
        const watermarkYear = container.querySelector('#watermarkYear');
        const rowsContainer = container.querySelector('#rowsContainer');
        const gridLines = container.querySelector('#gridLines');
        const insightsGrid = container.querySelector('#insightsGrid');

        // Parse and process CSV
        function initializeApp() {
            Papa.parse(window.CSV_DATA, {
                header: true,
                dynamicTyping: true,
                skipEmptyLines: true,
                complete: function(results) {
                    processParsedData(results.data);
                    setupCountryDropdown();
                    setupBarChartRows();
                    setupGridLines();
                    initializeLineChart();
                    updateDashboard(true); // first draw, recalc stats
                    setupEventListeners();
                }
            });
        }

        function processParsedData(rawData) {
            // Pre-fill years
            years.forEach(y => {
                globalData[y] = {};
                topics.forEach(t => {
                    globalData[y][t] = 0;
                });
            });

            rawData.forEach(row => {
                const year = row.year;
                const topic = row.topic_name;
                const publications = row.publications_count || 0;
                const cCode = row.country_code;
                const cName = row.country_name;

                if (!year || !topic || !topics.includes(topic)) return;

                // Add to global
                globalData[year][topic] = (globalData[year][topic] || 0) + publications;

                // Add to country
                if (cCode) {
                    if (!countryData[cCode]) {
                        countryData[cCode] = {};
                        years.forEach(y => {
                            countryData[cCode][y] = {};
                            topics.forEach(t => {
                                countryData[cCode][y][t] = 0;
                            });
                        });
                        countryMap[cCode] = cName;
                    }
                    countryData[cCode][year][topic] = publications;
                }
            });
        }

        function setupCountryDropdown() {
            // Sort countries alphabetically
            const countryList = Object.keys(countryMap).map(code => {
                return { code: code, name: countryMap[code] };
            });
            countryList.sort((a, b) => a.name.localeCompare(b.name));

            // Populate select element
            countryList.forEach(c => {
                const option = document.createElement('option');
                option.value = c.code;
                option.textContent = c.name;
                countrySelect.appendChild(option);
            });
        }

        function setupBarChartRows() {
            rowsContainer.innerHTML = '';
            topics.forEach((topic) => {
                const row = document.createElement('div');
                row.className = 'race-row';
                row.id = `row-${sanitizeName(topic)}`;
                row.style.top = '400px'; // Offscreen initially

                row.innerHTML = `
                    <div class="topic-info">
                        <div class="topic-dot" style="background-color: ${topicColors[topic]};"></div>
                        <div class="topic-name" title="${topic}">${topic}</div>
                    </div>
                    <div class="bar-container">
                        <div class="bar-fill" id="bar-${sanitizeName(topic)}" style="background: ${topicGradients[topic]}; width: 0%;"></div>
                    </div>
                    <div class="value-display" id="val-${sanitizeName(topic)}">0</div>
                    <div class="flag-display" id="flag-${sanitizeName(topic)}" style="margin-left: 10px; font-size: 1.5em; line-height: 1; display: flex; align-items: center;"></div>
                `;
                rowsContainer.appendChild(row);
            });
        }

        function setupGridLines() {
            gridLines.innerHTML = '';
            // 5 lines at 0%, 25%, 50%, 75%, 100%
            for (let i = 0; i <= 4; i++) {
                const pct = i * 25;
                const line = document.createElement('div');
                line.className = 'grid-line';
                line.style.left = `${pct}%`;

                const label = document.createElement('div');
                label.className = 'grid-line-label';
                label.id = `grid-label-${i}`;
                label.textContent = '0';
                line.appendChild(label);

                gridLines.appendChild(line);
            }
        }

        // Initialize Line Chart
        function initializeLineChart() {
            const ctx = container.querySelector('#trendChart').getContext('2d');
            
            const datasets = topics.map(topic => {
                return {
                    label: topic,
                    data: years.map(y => {
                        if (y > currentYear) return null;
                        return globalData[y][topic] || 0;
                    }),
                    borderColor: topicColors[topic],
                    backgroundColor: topicColors[topic] + '1A', // transparent fill
                    borderWidth: 2,
                    pointRadius: 0,
                    pointHoverRadius: 6,
                    tension: 0.1,
                    fill: false
                };
            });

            lineChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: years,
                    datasets: datasets
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    interaction: {
                        mode: 'index',
                        intersect: false,
                    },
                    plugins: {
                        legend: {
                            position: 'bottom',
                            labels: {
                                color: '#94a3b8',
                                font: {
                                    family: 'Outfit',
                                    size: 11
                                },
                                boxWidth: 10,
                                padding: 15
                            }
                        },
                        tooltip: {
                            backgroundColor: 'rgba(15, 23, 42, 0.9)',
                            titleColor: '#f8fafc',
                            titleFont: {
                                family: 'Outfit',
                                weight: 600
                            },
                            bodyColor: '#f8fafc',
                            bodyFont: {
                                family: 'Outfit'
                            },
                            borderColor: 'rgba(255, 255, 255, 0.1)',
                            borderWidth: 1,
                            padding: 10,
                            callbacks: {
                                label: function(context) {
                                    let label = context.dataset.label || '';
                                    if (label) {
                                        label += ': ';
                                    }
                                    if (context.parsed.y !== null) {
                                        label += context.parsed.y.toLocaleString();
                                    }
                                    return label;
                                }
                            }
                        }
                    },
                    scales: {
                        x: {
                            grid: {
                                color: 'rgba(255, 255, 255, 0.05)',
                                drawTicks: false
                            },
                            ticks: {
                                color: '#94a3b8',
                                font: {
                                    family: 'Outfit'
                                }
                            }
                        },
                        y: {
                            grace: '30%',
                            grid: {
                                color: 'rgba(255, 255, 255, 0.05)',
                                drawTicks: false
                            },
                            ticks: {
                                color: '#94a3b8',
                                font: {
                                    family: 'Outfit'
                                },
                                callback: function(value) {
                                    if (value >= 1e6) return (value / 1e6).toFixed(1) + 'M';
                                    if (value >= 1e3) return (value / 1e3).toFixed(0) + 'k';
                                    return value;
                                }
                            }
                        }
                    }
                }
            });
        }

        // Update Dashboard Elements
        function updateDashboard(recalcStats = false) {
            updateTimelineUI();
            updateBarChartRace();
            updateLineChartData();
            
            if (recalcStats) {
                calculateAndRenderStats();
            }
        }

        function updateTimelineUI() {
            timelineSlider.value = currentYear;
            labelCurrentYear.textContent = `Year: ${currentYear}`;
            yearIndicator.textContent = currentYear;
            watermarkYear.textContent = currentYear;
        }

        function updateBarChartRace() {
            // Get data for selected year and country
            const activeData = (selectedCountry === 'GLOBAL') ? globalData[currentYear] : countryData[selectedCountry][currentYear];

            // Map and sort topics
            const sortedTopics = topics.map(topic => {
                return {
                    name: topic,
                    value: activeData[topic] || 0
                };
            }).sort((a, b) => b.value - a.value);

            const maxValue = sortedTopics[0].value || 1;

            // Update background grid labels
            for (let i = 0; i <= 4; i++) {
                const labelElement = container.querySelector(`#grid-label-${i}`);
                const val = (maxValue * (i * 25) / 100);
                if (val >= 1e6) {
                    labelElement.textContent = (val / 1e6).toFixed(1) + 'M';
                } else if (val >= 1e3) {
                    labelElement.textContent = (val / 1e3).toFixed(0) + 'k';
                } else {
                    labelElement.textContent = Math.round(val);
                }
            }

            // Update each topic's bar
            sortedTopics.forEach((item, index) => {
                const sName = sanitizeName(item.name);
                const row = container.querySelector(`#row-${sName}`);
                const bar = container.querySelector(`#bar-${sName}`);
                const valDisp = container.querySelector(`#val-${sName}`);

                if (row && bar && valDisp) {
                    // Reposition row based on sorted rank (rank index * height + spacing)
                    // Visual area height: 400px, 7 rows -> space them at 54px intervals
                    row.style.top = `${index * 54}px`;

                    // Calculate width percentage (cap at 100%)
                    const pct = (item.value / maxValue) * 100;
                    bar.style.width = `${pct}%`;

                    // Update value text
                    valDisp.textContent = item.value.toLocaleString();

                    // Update flag
                    const flagDisp = container.querySelector(`#flag-${sName}`);
                    if (flagDisp) {
                        const topC = getTopCountryInYear(item.name, currentYear);
                        flagDisp.textContent = getFlagEmoji(topC.code);
                    }
                }
            });
        }

        function updateLineChartData() {
    if (!lineChart) return;

    const visibleYears = years.filter(y => y <= currentYear);
    lineChart.data.labels = visibleYears;

    topics.forEach((topic, idx) => {
        const dataPoints = visibleYears.map(y => {
            const dataSrc = (selectedCountry === 'GLOBAL') ? globalData[y] : countryData[selectedCountry][y];
            return dataSrc[topic] || 0;
        });
        lineChart.data.datasets[idx].data = dataPoints;
    });
    lineChart.update();
}

        function calculateAndRenderStats() {
            insightsGrid.innerHTML = '';

            topics.forEach(topic => {
                // 1. Calculate Total Publications
                let totalPubs = 0;
                let peakYear = yearMin;
                let peakPubs = -1;

                years.forEach(y => {
                    const dataSrc = (selectedCountry === 'GLOBAL') ? globalData[y] : countryData[selectedCountry][y];
                    const val = dataSrc[topic] || 0;
                    totalPubs += val;
                    if (val > peakPubs) {
                        peakPubs = val;
                        peakYear = y;
                    }
                });

                // 2. Calculate Growth Rate (first active year vs latest year in window)
                let firstActiveYear = yearMin;
                let firstActiveVal = 0;
                
                for (let i = 0; i < years.length; i++) {
                    const y = years[i];
                    const dataSrc = (selectedCountry === 'GLOBAL') ? globalData[y] : countryData[selectedCountry][y];
                    const val = dataSrc[topic] || 0;
                    if (val > 0) {
                        firstActiveYear = y;
                        firstActiveVal = val;
                        break;
                    }
                }
                if (firstActiveVal === 0) {
                    const dataSrc = (selectedCountry === 'GLOBAL') ? globalData[yearMin] : countryData[selectedCountry][yearMin];
                    firstActiveVal = dataSrc[topic] || 0;
                }

                const dataEndSrc = (selectedCountry === 'GLOBAL') ? globalData[yearMax] : countryData[selectedCountry][yearMax];
                const valEnd = dataEndSrc[topic] || 0;

                let growthStr = 'N/A';
                if (firstActiveVal > 0) {
                    const growthPct = ((valEnd - firstActiveVal) / firstActiveVal) * 100;
                    growthStr = (growthPct >= 0 ? '+' : '') + growthPct.toLocaleString(undefined, {maximumFractionDigits: 0}) + '%';
                } else if (valEnd > 0) {
                    growthStr = 'New (+100%)';
                }

                // 3. Peak publications count
                const peakStr = peakPubs > 0 ? `${peakPubs.toLocaleString()} (${peakYear})` : 'N/A';

                // 4. Secondary Analytical Metric
                let footerLabel = '';
                let footerValue = '';
                
                if (selectedCountry === 'GLOBAL') {
                    const top5 = getTop5CountriesInYear(topic, yearMax);
                    footerLabel = `Top Leaders (${yearMax})`;
                    
                    let optionsHtml = top5.map((c, i) => {
                        const pct = valEnd > 0 ? (c.count / valEnd * 100).toFixed(0) : 0;
                        return `<div style="padding: 2px 0;">${i+1}. ${c.name} (${pct}%)</div>`;
                    }).join('');
                    
                    const summaryText = top5.length > 0 ? `1. ${top5[0].name}` : 'Top 5';

                    footerValue = top5.length > 0 
                        ? `<details style="cursor: pointer; max-width: 180px; position: relative;">
                               <summary style="font-size: 0.9em; outline: none; border: 1px solid rgba(255,255,255,0.2); border-radius: 4px; padding: 2px 5px; user-select: none; display: flex; align-items: center; justify-content: space-between;"><span style="overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">${summaryText}</span><span style="font-size: 0.7em; margin-left: 6px;">▼</span></summary>
                               <div style="position: absolute; bottom: 100%; right: 0; background: #0f172a; border: 1px solid rgba(255,255,255,0.2); border-radius: 4px; padding: 6px; font-size: 0.85em; color: #cbd5e1; margin-bottom: 4px; width: max-content; z-index: 10; box-shadow: 0 4px 6px rgba(0,0,0,0.3);">${optionsHtml}</div>
                           </details>` 
                        : 'None';
                } else {
                    const globalEndVal = globalData[yearMax][topic] || 0;
                    const countryEndVal = valEnd;
                    const share = globalEndVal > 0 ? (countryEndVal / globalEndVal * 100) : 0;
                    
                    footerLabel = `Global Share (${yearMax})`;
                    footerValue = share > 0 ? `${share.toFixed(1)}%` : '0%';
                }

                // Render Insight Card
                const card = document.createElement('div');
                card.className = 'insight-card';
                card.innerHTML = `
                    <div class="card-top">
                        <div class="card-title">${topic}</div>
                        <div class="subfield-pill">Concept ID ${topicSubfields[topic]}</div>
                    </div>
                    <div class="card-metric">
                        <div class="metric-value">${totalPubs.toLocaleString()}</div>
                        <div class="metric-label">Total Pubs (${yearMin}–${yearMax})</div>
                    </div>
                    <div class="card-footer">
                        <div class="footer-item">
                            <span class="footer-label">Growth (vs ${firstActiveYear})</span>
                            <span class="footer-value highlight-green">${growthStr}</span>
                        </div>
                        <div class="footer-item">
                            <span class="footer-label">${footerLabel}</span>
                            <span class="footer-value">${footerValue}</span>
                        </div>
                    </div>
                `;
                insightsGrid.appendChild(card);
            });
        }

        // Helper to find the top contributing country for a topic in a specific year
        function getTopCountryInYear(topic, year) {
            let maxPubs = -1;
            let topCode = '';
            let topName = '';

            for (const code in countryData) {
                const val = countryData[code][year][topic] || 0;
                if (val > maxPubs) {
                    maxPubs = val;
                    topCode = code;
                    topName = countryMap[code] || code;
                }
            }

            return { code: topCode, name: topName, count: maxPubs };
        }

        function getTop5CountriesInYear(topic, year) {
            let list = [];
            for (const code in countryData) {
                const val = countryData[code][year][topic] || 0;
                if (val > 0) {
                    list.push({ code: code, name: countryMap[code] || code, count: val });
                }
            }
            list.sort((a, b) => b.count - a.count);
            return list.slice(0, 5);
        }

        function getFlagEmoji(countryCode) {
            if (!countryCode) return '';
            if (countryCode.toLowerCase() === 'uk') countryCode = 'GB'; // Handle common edge cases just in case
            const codePoints = countryCode
                .toUpperCase()
                .split('')
                .map(char => 127397 + char.charCodeAt(0));
            return String.fromCodePoint(...codePoints);
        }

        // Animation Loop logic
        function startPlayback() {
            if (isPlaying) return;
            isPlaying = true;
            playIcon.style.display = 'none';
            pauseIcon.style.display = 'block';
            runAnimationLoop();
        }

        function pausePlayback() {
            if (!isPlaying) return;
            isPlaying = false;
            playIcon.style.display = 'block';
            pauseIcon.style.display = 'none';
            if (playTimeout) {
                clearTimeout(playTimeout);
                playTimeout = null;
            }
        }

        function runAnimationLoop() {
            if (!isPlaying) return;

            currentYear++;
            if (currentYear > yearMax) {
                currentYear = yearMin;
            }
            
            updateDashboard(false); // don't recalc heavy stats every frame

            let delay = 800;
            if (speedMultiplier === 0.5) delay = 1500;
            else if (speedMultiplier === 1.0) delay = 800;
            else if (speedMultiplier === 2.0) delay = 350;

            playTimeout = setTimeout(runAnimationLoop, delay);
        }

        // Event Listeners setup
        function setupEventListeners() {
            // Play / Pause Button
            btnPlay.addEventListener('click', () => {
                if (isPlaying) {
                    pausePlayback();
                } else {
                    startPlayback();
                }
            });

            // Reset Button
            btnReset.addEventListener('click', () => {
                pausePlayback();
                currentYear = yearMin;
                updateDashboard(false);
            });

            // Timeline slider input
            timelineSlider.addEventListener('input', (e) => {
                pausePlayback();
                currentYear = parseInt(e.target.value);
                updateDashboard(false);
            });

            // Country selection change
            countrySelect.addEventListener('change', (e) => {
                selectedCountry = e.target.value;
                updateDashboard(true); // recalculate everything on country change
            });

            // Speed selector buttons
            const speedBtns = container.querySelectorAll('.speed-btn');
            speedBtns.forEach(btn => {
                btn.addEventListener('click', (e) => {
                    speedBtns.forEach(b => b.classList.remove('active'));
                    btn.classList.add('active');
                    speedMultiplier = parseFloat(btn.dataset.speed);
                });
            });
        }

        // Helpers
        function sanitizeName(str) {
            return str.replace(/[^a-zA-Z0-9]/g, '_').toLowerCase();
        }

        // Start everything
  
  // Initialize
  if (typeof window.CSV_DATA === 'undefined') {
      container.innerHTML = `<h2 style="color:red; padding: 2rem;">Error: viz3_data.js is missing or not loaded correctly.</h2>`;
      return;
  }
  
  initializeApp();
}

function renderViz4(body) {
  // Use the new VIZ4_DATA if available, fallback to old static data
  let rawData = typeof VIZ4_DATA !== 'undefined' ? VIZ4_DATA : DATA.getCollabData();
  
  let data = [];
  
  if (!APP.region || APP.region === "All") {
    // Aggregate by region
    const grouped = d3.group(rawData, d => d.region);
    for (const [region, countries] of grouped) {
      const dom = d3.mean(countries, d => d.domestic);
      const intl = d3.mean(countries, d => d.international);
      data.push({
        name: region,
        region: region,
        domestic: dom,
        international: intl,
        gain: intl - dom,
        isRegionAgg: true,
        countryCount: countries.length
      });
    }
  } else {
    // Filter to specific region
    data = rawData.filter(d => d.region === APP.region);
  }

  // Apply Sorting
  if (APP.sort === "gain")          data.sort((a,b)=>b.gain-a.gain);
  else if (APP.sort === "international") data.sort((a,b)=>b.international-a.international);
  else if (APP.sort === "domestic") data.sort((a,b)=>b.domestic-a.domestic);
  else                              data.sort((a,b)=>a.name.localeCompare(b.name));

  // Clear existing content
  body.innerHTML = '';
  
  // Create a wrapper div to handle the flex layout (column direction)
  const wrapper = document.createElement('div');
  wrapper.style.display = 'flex';
  wrapper.style.flexDirection = 'column';
  wrapper.style.width = '100%';
  wrapper.style.height = '100%';
  body.appendChild(wrapper);
  
  // Stats calculation
  const avgDom = data.length ? d3.mean(data, d => d.domestic) : 0;
  const avgInt = data.length ? d3.mean(data, d => d.international) : 0;
  const avgGain = data.length ? d3.mean(data, d => d.gain) : 0;
  
  // Top stats bar
  const statsBar = document.createElement('div');
  statsBar.style.padding = '15px 25px';
  statsBar.style.background = 'rgba(15, 23, 42, 0.8)';
  statsBar.style.borderBottom = '1px solid rgba(255,255,255,0.1)';
  statsBar.style.display = 'flex';
  statsBar.style.justifyContent = 'space-between';
  statsBar.style.alignItems = 'center';
  statsBar.style.backdropFilter = 'blur(10px)';
  statsBar.style.zIndex = '10';
  
  statsBar.innerHTML = `
    <div style="display:flex; flex: 1; justify-content: space-evenly; align-items: center; margin-right: 40px;">
      <div style="text-align:center;">
        <div style="color:#94a3b8; font-size:0.8rem; text-transform:uppercase; letter-spacing:1px;">Countries Visible</div>
        <div style="color:#fff; font-size:1.5rem; font-weight:800;">${data.length}</div>
      </div>
      <div style="text-align:center;">
        <div style="color:#E69F00; font-size:0.8rem; text-transform:uppercase; letter-spacing:1px;">Avg Domestic (Citations)</div>
        <div style="color:#fff; font-size:1.5rem; font-weight:800;">${avgDom.toFixed(1)}</div>
      </div>
      <div style="text-align:center;">
        <div style="color:#0072B2; font-size:0.8rem; text-transform:uppercase; letter-spacing:1px;">Avg Int'l (Citations)</div>
        <div style="color:#fff; font-size:1.5rem; font-weight:800;">${avgInt.toFixed(1)}</div>
      </div>
      <div style="text-align:center;">
        <div style="color:#56B4E9; font-size:0.8rem; text-transform:uppercase; letter-spacing:1px;">Avg Premium</div>
        <div style="color:#fff; font-size:1.5rem; font-weight:800;">+${avgGain.toFixed(1)}</div>
      </div>
    </div>
    <div style="display:flex; flex-direction:column; gap: 8px; background: rgba(15,23,42,0.5); padding: 10px 15px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.1);">
      <div style="display:flex; align-items:center;">
        <div style="width:12px; height:12px; border-radius:50%; background:#E69F00; border:1.5px solid #fff; margin-right:10px;"></div>
        <span style="color:#e2e8f0; font-size:0.85rem; font-weight:600;">Domestic (Citations/Paper)</span>
      </div>
      <div style="display:flex; align-items:center;">
        <div style="width:12px; height:12px; border-radius:50%; background:#0072B2; border:1.5px solid #fff; margin-right:10px;"></div>
        <span style="color:#e2e8f0; font-size:0.85rem; font-weight:600;">Int'l Collab (Citations/Paper)</span>
      </div>
    </div>
  `;
  wrapper.appendChild(statsBar);
  
  const mainRow = document.createElement('div');
  mainRow.style.display = 'flex';
  mainRow.style.flexDirection = 'row';
  mainRow.style.flex = '1';
  mainRow.style.overflow = 'hidden';
  wrapper.appendChild(mainRow);
  
  // Scrollable container for SVG
  const scrollContainer = document.createElement('div');
  scrollContainer.style.flex = '1';
  scrollContainer.style.overflowY = 'auto';
  scrollContainer.style.overflowX = 'hidden';
  mainRow.appendChild(scrollContainer);
  
  // Glossary Side Panel
  const sidePanel = document.createElement('div');
  sidePanel.style.width = '280px';
  sidePanel.style.borderLeft = '1px solid rgba(255,255,255,0.1)';
  sidePanel.style.padding = '20px';
  sidePanel.style.background = 'rgba(15, 23, 42, 0.5)';
  sidePanel.style.display = 'flex';
  sidePanel.style.flexDirection = 'column';
  sidePanel.style.gap = '20px';
  sidePanel.style.overflowY = 'auto';

  sidePanel.innerHTML = `
    <h3 style="color:#f8fafc; font-size:1.1rem; margin:0 0 10px 0; padding-bottom:10px; border-bottom:1px solid rgba(255,255,255,0.1);">Glossary</h3>
    <div style="color:#64748b; font-size:0.75rem; line-height:1.35; margin-bottom:8px;">Sample shown: <b style="color:#cbd5e1;">20 countries, year 2024</b> (not a full world panel).</div>
    
    <div>
        <div style="color:#E69F00; font-size:0.85rem; font-weight:700; text-transform:uppercase; margin-bottom:5px;">Domestic Impact</div>
        <div style="color:#94a3b8; font-size:0.85rem; line-height:1.4;">Mean citations for papers with authors only from this country. Baseline for local research influence.</div>
    </div>
    
    <div>
        <div style="color:#0072B2; font-size:0.85rem; font-weight:700; text-transform:uppercase; margin-bottom:5px;">Int'l Collab Impact</div>
        <div style="color:#94a3b8; font-size:0.85rem; line-height:1.4;">Mean citations for papers with at least one co-author from another country.</div>
    </div>
    
    <div>
        <div style="color:#56B4E9; font-size:0.85rem; font-weight:700; text-transform:uppercase; margin-bottom:5px;">Collaboration Premium</div>
        <div style="color:#94a3b8; font-size:0.85rem; line-height:1.4;">International impact minus domestic impact. Higher = larger citation gain from cross-border co-authorship.</div>
    </div>
  `;
  mainRow.appendChild(sidePanel);

  const W = scrollContainer.offsetWidth || 900;
  // Calculate dynamic height based on data length (35px per row) + margins
  const H = Math.max(scrollContainer.offsetHeight || 500, data.length * 35 + 100);
  
  const m = { top: 60, right: 80, bottom: 40, left: 200 };
  
  const svg = d3.select(scrollContainer).append("svg").attr("width",W).attr("height",H);

  // Definitions for drop shadows
  const defs = svg.append("defs");
  const dropShadow = defs.append("filter")
    .attr("id", "glow")
    .attr("x", "-20%").attr("y", "-20%")
    .attr("width", "140%").attr("height", "140%");
  dropShadow.append("feGaussianBlur").attr("stdDeviation", "3").attr("result", "blur");
  const feMerge = dropShadow.append("feMerge");
  feMerge.append("feMergeNode").attr("in", "blur");
  feMerge.append("feMergeNode").attr("in", "SourceGraphic");

  svg.append("text").attr("x",W/2).attr("y",30).attr("text-anchor","middle")
    .attr("fill","#f8fafc").attr("font-size","18").attr("font-weight","800").attr("letter-spacing", "0.5px")
    .text(`The Collaboration Premium: Citation Gap (Top 20 Countries, 2024)`);

  const maxVal = d3.max(data, d => d.international) || 1;
  const xSc = d3.scaleLinear().domain([0, maxVal * 1.05]).range([m.left, W-m.right]);
  const ySc = d3.scaleBand().domain(data.map(d=>d.name)).range([m.top, H-m.bottom]).padding(0.4);

  // X Axis (Fixed to top and bottom)
  svg.append("g").attr("transform",`translate(0,${m.top-20})`)
     .call(d3.axisTop(xSc).ticks(8))
     .call(g => g.select(".domain").attr("stroke","#334155"))
     .call(g => g.selectAll("text").attr("fill","#94a3b8").attr("font-size", "11"));
     
  svg.append("g").attr("transform",`translate(0,${H-m.bottom})`)
     .call(d3.axisBottom(xSc).ticks(8))
     .call(g => g.select(".domain").attr("stroke","#334155"))
     .call(g => g.selectAll("line").attr("stroke","rgba(255,255,255,0.05)").attr("y2",-(H-m.top-m.bottom+20)))
     .call(g => g.selectAll("text").attr("fill","#94a3b8").attr("font-size", "11"));
     
  // Y Axis
  svg.append("g").attr("transform",`translate(${m.left},0)`)
     .call(d3.axisLeft(ySc).tickSize(0))
     .call(g => g.select(".domain").remove())
     .selectAll("text").attr("font-size","13").attr("font-weight", "500").attr("fill","#cbd5e1");

  const cy = d => ySc(d.name)+ySc.bandwidth()/2;

  // Custom rich tooltip html generator
  const getTooltipHtml = (d) => `
    <div style="background:rgba(15,23,42,0.95); border:1px solid rgba(255,255,255,0.1); border-radius:8px; padding:12px; min-width:200px; box-shadow:0 10px 25px rgba(0,0,0,0.5);">
      <div style="font-size:14px; font-weight:800; color:#fff; margin-bottom:4px; border-bottom:1px solid rgba(255,255,255,0.1); padding-bottom:6px;">${d.name}</div>
      <div style="font-size:11px; color:#94a3b8; text-transform:uppercase; letter-spacing:1px; margin-bottom:10px;">
        ${d.isRegionAgg ? `Aggregated Region: ${d.countryCount} countries` : d.region}
      </div>
      <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
        <span style="color:#E69F00; font-weight:600; font-size:12px;">Domestic:</span>
        <span style="color:#fff; font-weight:700; font-size:13px;">${d.domestic.toFixed(1)} citations</span>
      </div>
      <div style="display:flex; justify-content:space-between; margin-bottom:8px;">
        <span style="color:#0072B2; font-weight:600; font-size:12px;">Int'l Collab:</span>
        <span style="color:#fff; font-weight:700; font-size:13px;">${d.international.toFixed(1)} citations</span>
      </div>
      <div style="display:flex; justify-content:space-between; border-top:1px dashed rgba(255,255,255,0.2); padding-top:8px; margin-bottom: ${d.isRegionAgg ? '8px' : '0'};">
        <span style="color:#56B4E9; font-weight:800; font-size:13px;">Premium:</span>
        <span style="color:#56B4E9; font-weight:800; font-size:14px;">+${d.gain.toFixed(1)}</span>
      </div>
      ${d.isRegionAgg ? `<div style="font-size:10px; color:#e2e8f0; font-style:italic; text-align:center; background:rgba(255,255,255,0.1); padding:4px; border-radius:4px;">Click to drill down</div>` : ''}
    </div>
  `;

  // Draw connecting lines (solid color to fix gradient bounding box bug on horizontal lines)
  const lines = svg.selectAll(".con").data(data, d => d.name);
  lines.join(
    enter => enter.append("line").attr("class","con")
      .attr("x1",d=>xSc(d.domestic)).attr("x2",d=>xSc(d.domestic)) // Start collapsed
      .attr("y1",cy).attr("y2",cy)
      .attr("stroke","rgba(255,255,255,0.2)").attr("stroke-width",4)
      .call(enter => enter.transition().duration(800).delay((d,i)=>i*5).attr("x2",d=>xSc(d.international))),
    update => update.call(update => update.transition().duration(800)
      .attr("y1",cy).attr("y2",cy)
      .attr("x1",d=>xSc(d.domestic)).attr("x2",d=>xSc(d.international))),
    exit => exit.call(exit => exit.transition().duration(400).style("opacity",0).remove())
  );

  // Invisible hover interaction area per row (for easier hovering)
  svg.selectAll(".row-hover").data(data, d=>d.name).join("rect").attr("class", "row-hover")
    .attr("x", 0).attr("y", d => ySc(d.name))
    .attr("width", W).attr("height", ySc.bandwidth())
    .attr("fill", "transparent")
    .style("cursor", "pointer")
    .on("mouseover", function(e, d) {
      svg.selectAll(".dd").filter(x => x.name === d.name).attr("r", 9).style("filter", "url(#glow)");
      svg.selectAll(".di").filter(x => x.name === d.name).attr("r", 9).style("filter", "url(#glow)");
      svg.selectAll(".con").filter(x => x.name === d.name).attr("stroke", "rgba(255,255,255,0.6)").attr("stroke-width", 6);
      
      showTip(e, getTooltipHtml(d));
      tip.style.background = 'transparent';
      tip.style.border = 'none';
      tip.style.boxShadow = 'none';
      tip.style.padding = '0';
    })
    .on("mousemove", moveTip)
    .on("mouseleave", function(e, d) {
      svg.selectAll(".dd").filter(x => x.name === d.name).attr("r", 6).style("filter", "none");
      svg.selectAll(".di").filter(x => x.name === d.name).attr("r", 6).style("filter", "none");
      svg.selectAll(".con").filter(x => x.name === d.name).attr("stroke", "rgba(255,255,255,0.2)").attr("stroke-width", 4);
      hideTip();
      tip.style.background = 'rgba(15, 23, 42, 0.9)';
      tip.style.border = '1px solid rgba(255,255,255,0.1)';
      tip.style.padding = '10px';
    })
    .on("click", function(e, d) {
      if (d.isRegionAgg) {
        APP.region = d.name;
        const select = document.getElementById("viz4-region-select");
        if (select) select.value = d.name;
        hideTip(); // Hide tooltip to prevent ghost tooltips
        renderViz(4);
      }
    });

  // Domestic dots
  const domDots = svg.selectAll(".dd").data(data, d=>d.name);
  domDots.join(
    enter => enter.append("circle").attr("class","dd")
      .attr("cx",d=>xSc(d.domestic)).attr("cy",cy).attr("r",0)
      .attr("fill","#E69F00").attr("stroke","#fff").attr("stroke-width",1.5)
      .style("pointer-events", "none")
      .call(enter => enter.transition().duration(800).delay((d,i)=>i*5).attr("r",6)),
    update => update.call(update => update.transition().duration(800)
      .attr("cx",d=>xSc(d.domestic)).attr("cy",cy)),
    exit => exit.call(exit => exit.transition().duration(400).attr("r",0).remove())
  );

  // International dots
  const intDots = svg.selectAll(".di").data(data, d=>d.name);
  intDots.join(
    enter => enter.append("circle").attr("class","di")
      .attr("cx",d=>xSc(d.domestic)).attr("cy",cy).attr("r",0) // Start at domestic x
      .attr("fill","#0072B2").attr("stroke","#fff").attr("stroke-width",1.5)
      .style("pointer-events", "none")
      .call(enter => enter.transition().duration(800).delay((d,i)=>i*5).attr("cx",d=>xSc(d.international)).attr("r",6)),
    update => update.call(update => update.transition().duration(800)
      .attr("cx",d=>xSc(d.international)).attr("cy",cy)),
    exit => exit.call(exit => exit.transition().duration(400).attr("r",0).remove())
  );


}

// ══════════════════════════════════════════════════════════
// VIZ 5: India Domestic Higher Education Network (real JSON)
// ══════════════════════════════════════════════════════════
function renderViz5(body) {
  if (!INDIA.isReady()) {
    renderViz5Legacy(body);
    return;
  }

  if (APP.indiaController?.destroy) {
    APP.indiaController.destroy();
    APP.indiaController = null;
  }

  const selectedId = APP.selectedNode ? APP.selectedNode.id : null;
  APP.indiaController = INDIA.render(body, {
    tierFilter: APP.tier,
    selectedNodeId: selectedId,
    displayYear: APP.year,
    mode: "full",
    onSelect: (node) => {
      APP.selectedNode = node;
    },
    onYearChange: (y) => {
      APP.year = y;
      const yearVal = document.querySelector(".year-val");
      const slider = document.querySelector(".ctrl-range");
      if (yearVal) yearVal.textContent = y;
      if (slider) slider.value = y;
    },
  });

  if (APP.indiaController?.setYear && APP.year) {
    APP.indiaController.setYear(APP.year);
  }

  if (APP.indiaController?.destroy) {
    APP.cleanupFns.push(() => {
      APP.indiaController?.destroy();
      APP.indiaController = null;
    });
  }
}

function renderViz5Legacy(body) {
  const layout = div("india-layout");
  const mapPane = div("india-map-pane");
  const sidePane = div("india-sidebar");
  sidePane.innerHTML = `
    <h4>Institution Details</h4>
    <p class="inst-placeholder">India network JSON not loaded — using demo fallback</p>
    <div class="inst-details" id="inst-details"></div>
  `;
  layout.append(mapPane, sidePane);
  body.appendChild(layout);

  const net = DATA.getIndiaNetwork(APP.year);
  const tierFilter = APP.tier;
  const nodes = net.nodes.filter(n => tierFilter === "All" || n.tier === tierFilter);
  const nodeIds = new Set(nodes.map(n => n.id));
  const links  = net.links.filter(l => nodeIds.has(l.source) && nodeIds.has(l.target));

  const W = mapPane.offsetWidth || 550, H = body.offsetHeight || 500;
  const svg = d3.select(mapPane).append("svg").attr("width",W).attr("height",H);
  const boundary = [
    [68.1,23.7],[73.5,34.5],[77.5,37.0],[80.3,30.5],[88.5,27.5],
    [97.4,28.2],[91.8,22.0],[88.0,21.6],[80.2,12.5],[77.4,8.1],
    [73.5,15.5],[72.8,20.0],[68.1,23.7]
  ];
  const proj = d3.geoMercator().fitSize([W-40, H-40], {
    type: "Feature",
    geometry: { type: "Polygon", coordinates: [boundary] }
  });
  svg.append("path")
    .datum({type: "Polygon", coordinates: [boundary]})
    .attr("d", d3.geoPath().projection(proj))
    .attr("fill", "rgba(255,255,255,0.03)")
    .attr("stroke", "rgba(255,255,255,0.15)")
    .attr("stroke-width", 1.5)
    .attr("stroke-dasharray", "4,4");
  svg.selectAll(".link").data(links).join("line").attr("class","link")
    .attr("x1", d => proj([net.nodes.find(n=>n.id===d.source).lon, net.nodes.find(n=>n.id===d.source).lat])[0])
    .attr("y1", d => proj([net.nodes.find(n=>n.id===d.source).lon, net.nodes.find(n=>n.id===d.source).lat])[1])
    .attr("x2", d => proj([net.nodes.find(n=>n.id===d.target).lon, net.nodes.find(n=>n.id===d.target).lat])[0])
    .attr("y2", d => proj([net.nodes.find(n=>n.id===d.target).lon, net.nodes.find(n=>n.id===d.target).lat])[1])
    .attr("stroke", "rgba(204,121,167,0.3)")
    .attr("stroke-width", d => Math.sqrt(d.weight)/2);
  const rSc = d3.scaleSqrt().domain([0, 10000]).range([3, 25]);
  const tierColors = { "Premier":"#0072B2", "Central / State":"#56B4E9", "Affiliated / Private":"#E69F00" };
  const nodeG = svg.selectAll(".node").data(nodes).join("g").attr("class","node")
    .attr("transform", d => `translate(${proj([d.lon, d.lat])})`)
    .style("cursor","pointer")
    .on("click", (e,d) => selectIndiaNode(d, net));
  nodeG.append("circle")
    .attr("r", d => rSc(d.publications))
    .attr("fill", d => tierColors[d.tier] + "dd");
}

function selectIndiaNode(node, net) {
  APP.selectedNode = node;
  const container = document.getElementById("inst-details");
  document.querySelector(".inst-placeholder").style.display = "none";
  
  const connectedLinks = net.links.filter(l => l.source === node.id || l.target === node.id);
  const totalCollabs = d3.sum(connectedLinks, l => l.weight);
  
  container.innerHTML = `
    <h3 style="color:#e2e8f0; margin-bottom:0.5rem; font-size:1.3rem;">${node.name}</h3>
    <div style="color:var(--accent); font-weight:bold; margin-bottom:1.5rem; font-size:0.9rem;">${node.tier}</div>
    
    <div style="display:flex; justify-content:space-between; border-bottom:1px solid var(--border); padding-bottom:1rem; margin-bottom:1rem;">
      <div>
        <div style="font-size:0.8rem; color:var(--text-muted);">Publications (${APP.year})</div>
        <div style="font-size:1.4rem; color:#fff; font-weight:bold;">${node.publications.toLocaleString()}</div>
      </div>
      <div style="text-align:right;">
        <div style="font-size:0.8rem; color:var(--text-muted);">Gov Funding</div>
        <div style="font-size:1.4rem; color:#fff; font-weight:bold;">₹${node.funding} <span style="font-size:0.9rem;">Cr</span></div>
      </div>
    </div>
    
    <div style="font-size:0.95rem; margin-bottom:0.5rem; color:#cbd5e1;">Domestic Co-publications: <strong>${totalCollabs}</strong></div>
    
    <ul style="list-style:none; padding:0; font-size:0.85rem; color:#94a3b8;">
      ${connectedLinks.sort((a,b)=>b.weight-a.weight).slice(0,5).map(l => {
        const partnerId = l.source === node.id ? l.target : l.source;
        const partner = net.nodes.find(n=>n.id === partnerId);
        if (!partner) return "";
        return `<li style="padding:4px 0; border-bottom:1px dashed rgba(255,255,255,0.05); display:flex; justify-content:space-between;">
          <span>${partner.name}</span> <span style="color:#56B4E9; font-weight:bold;">${l.weight}</span>
        </li>`;
      }).join("")}
    </ul>
  `;
}

// ─── Play / Animation ──────────────────────────────────────
function toggleAnimation(slider, yearVal, btn, yearMin, yearMax) {
  const yMin = yearMin ?? 2010;
  const yMax = yearMax ?? 2025;
  if (!APP.isPlaying) {
    APP.isPlaying = true;
    btn.textContent = "⏸ Pause";

    const runStep = async () => {
      if (!APP.isPlaying) return;
      if (APP.year >= yMax) {
        stopAnimation();
        return;
      }
      APP.year += 1;
      slider.value = APP.year;
      yearVal.textContent = APP.year;
      if (APP.activeViz === 5 && APP.indiaController?.setYear) {
        await APP.indiaController.setYear(APP.year);
      } else {
        renderViz(APP.activeViz);
      }
      if (APP.isPlaying && APP.year < yMax) {
        APP.animTimer = setTimeout(runStep, APP.speed);
      } else if (APP.year >= yMax) {
        stopAnimation();
      }
    };

    if (APP.year >= yMax) {
      APP.year = yMin - 1;
    }
    APP.animTimer = setTimeout(runStep, 100);
    APP.cleanupFns.push(() => stopAnimation());
  } else {
    btn.textContent = "▶ Play";
    stopAnimation();
  }
}

function stopAnimation() {
  APP.isPlaying = false;
  if (APP.animTimer) { clearTimeout(APP.animTimer); APP.animTimer = null; }
  const btn = document.getElementById("play-btn");
  if (btn) btn.textContent = "▶ Play";
}

// ─── Utility helpers ──────────────────────────────────────
function el(tag, cls, content) {
  const e = document.createElement(tag);
  if (cls) e.className = cls;
  if (typeof content === "string" || typeof content === "number") e.textContent = String(content);
  else if (Array.isArray(content)) content.forEach(c => e.appendChild(c));
  return e;
}

function div(cls) {
  const d = document.createElement("div");
  d.className = cls;
  return d;
}

function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

function showLoading(msg) {
  document.getElementById("loading-text").textContent = msg;
  document.getElementById("loading-screen").classList.add("active");
}
function hideLoading() {
  document.getElementById("loading-screen").classList.remove("active");
}

window.addEventListener("resize", () => {
  if (APP.activeViz === 5 && APP.indiaController?.resize) {
    APP.indiaController.resize();
    return;
  }
  if (APP.activeViz) renderViz(APP.activeViz);
});
