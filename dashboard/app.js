// --- VIZ 1 GLOBALS ---
let viz1Year = 2022;
let viz1YearsRange = [1996, 2024];
let viz1IsPlaying = false;
let viz1Speed = 600;
let viz1SelectedRegion = null;
let viz1SearchQuery = '';
let viz1ComparedCountries = [];
let viz1ShowSpecific = false;
let viz1PlayInterval = null;

const viz1ColorPalette = ['#00f2fe','#ff0844','#c471ed','#00ff87','#f6d365','#ff758c','#4facfe','#d4fc79'];

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
  1: { title: "High-Dimensional Peer Clustering",             num: "01", credit: "World Bank API · OpenAlex (t-SNE/UMAP Projection)" },
  2: { title: "Global Quality Shift (Q1 vs Q4)",              num: "02", credit: "SCImago SJR · Density Estimates" },
  3: { title: "Top Research topics",                          num: "03", credit: "OpenAlex (1950-2025)" },
  4: { title: "The Collaboration Premium",                    num: "04", credit: "OpenAlex Citation Networks" },
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
  
  // Draw subtle grid lines
  ctx.strokeStyle = "rgba(255,255,255,0.03)";
  ctx.lineWidth = 1;
  for (let x = w * 0.15; x < w; x += w * 0.15) {
    ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, h); ctx.stroke();
  }
  for (let y = h * 0.2; y < h; y += h * 0.2) {
    ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(w, y); ctx.stroke();
  }

  // Draw axis stubs
  ctx.strokeStyle = "rgba(255,255,255,0.1)";
  ctx.lineWidth = 1.5;
  ctx.beginPath(); ctx.moveTo(w * 0.08, h * 0.9); ctx.lineTo(w * 0.95, h * 0.9); ctx.stroke();
  ctx.beginPath(); ctx.moveTo(w * 0.08, h * 0.95); ctx.lineTo(w * 0.08, h * 0.05); ctx.stroke();

  // Draw clustered bubbles
  const bubbles = [
    {x:0.3, y:0.4, r:12, col:"rgba(34,211,238,0.75)"},
    {x:0.42, y:0.28, r:22, col:"rgba(34,211,238,0.55)"},
    {x:0.35, y:0.55, r:16, col:"rgba(34,211,238,0.65)"},
    
    {x:0.75, y:0.65, r:18, col:"rgba(168,85,247,0.75)"},
    {x:0.82, y:0.5, r:14, col:"rgba(168,85,247,0.55)"},
    
    {x:0.65, y:0.3, r:26, col:"rgba(244,63,94,0.65)"},
    {x:0.2, y:0.75, r:28, col:"rgba(251,191,36,0.6)"}
  ];
  
  bubbles.forEach(b => {
    ctx.beginPath(); ctx.arc(b.x*w, b.y*h, b.r, 0, Math.PI*2);
    ctx.fillStyle = b.col; ctx.fill();
    ctx.strokeStyle = "rgba(255,255,255,0.2)"; ctx.lineWidth = 1.2; ctx.stroke();
  });
}

function drawPreview2() {
  const c = document.getElementById("preview-2");
  const ctx = c.getContext("2d");
  c.width = c.offsetWidth; c.height = c.offsetHeight;
  const w = c.width, h = c.height;

  // Draw gridlines
  ctx.strokeStyle = "rgba(255, 255, 255, 0.03)";
  ctx.lineWidth = 1;
  for (let y = h * 0.25; y < h; y += h * 0.25) {
    ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(w, y); ctx.stroke();
  }

  // Draw 3 overlapping joyplot waves
  const drawJoyWave = (yBase, amp, shift, col1, col2) => {
    ctx.beginPath();
    ctx.moveTo(0, yBase);
    for (let x = 0; x <= w; x++) {
      const distFromMean = (x - (w * 0.5 + shift)) / (w * 0.22);
      const yValue = yBase - amp * Math.exp(-0.5 * distFromMean * distFromMean);
      ctx.lineTo(x, yValue);
    }
    ctx.lineTo(w, yBase);
    ctx.closePath();

    // Create gradient fill
    const grad = ctx.createLinearGradient(0, yBase - amp, 0, yBase);
    grad.addColorStop(0, col1);
    grad.addColorStop(1, col2);
    ctx.fillStyle = grad;
    ctx.fill();

    ctx.strokeStyle = "rgba(255,255,255,0.25)";
    ctx.lineWidth = 1.5;
    ctx.stroke();
  };

  // Draw background waves first (bottom to top layout style)
  drawJoyWave(h * 0.85, h * 0.55, w * 0.1, "rgba(244,63,94,0.45)", "rgba(244,63,94,0.01)");
  drawJoyWave(h * 0.6, h * 0.45, -w * 0.15, "rgba(56,189,248,0.45)", "rgba(56,189,248,0.01)");
  drawJoyWave(h * 0.35, h * 0.25, w * 0.05, "rgba(168,85,247,0.45)", "rgba(168,85,247,0.01)");
}

function drawPreview3() {
  const c = document.getElementById("preview-3");
  const ctx = c.getContext("2d");
  c.width = c.offsetWidth; c.height = c.offsetHeight;
  const w = c.width, h = c.height;

  const barData = [
    { label: "#1", width: 0.85, color: "#6366f1" },
    { label: "#2", width: 0.72, color: "#22d3ee" },
    { label: "#3", width: 0.58, color: "#f59e0b" },
    { label: "#4", width: 0.44, color: "#f43f5e" }
  ];

  barData.forEach((bar, i) => {
    const barHeight = 16;
    const y = 30 + i * 36;
    
    // Draw bar background track
    ctx.fillStyle = "rgba(255,255,255,0.03)";
    ctx.fillRect(40, y, w - 80, barHeight);

    // Draw active bar
    ctx.fillStyle = bar.color;
    ctx.fillRect(40, y, bar.width * (w - 80), barHeight);

    // Label
    ctx.fillStyle = "rgba(255,255,255,0.4)";
    ctx.font = "bold 9px sans-serif";
    ctx.textAlign = "right";
    ctx.fillText(bar.label, 30, y + 12);
  });
}

function drawPreview4() {
  const c = document.getElementById("preview-4");
  const ctx = c.getContext("2d");
  c.width = c.offsetWidth; c.height = c.offsetHeight;
  const w = c.width, h = c.height;

  // Draw central parity vertical line
  ctx.strokeStyle = "rgba(255,255,255,0.05)";
  ctx.setLineDash([4, 4]);
  ctx.beginPath(); ctx.moveTo(w * 0.45, 10); ctx.lineTo(w * 0.45, h - 10); ctx.stroke();
  ctx.setLineDash([]);

  // Dumbbells
  const dumbbells = [
    { y: 35, d: w * 0.25, i: w * 0.75, colD: "#f43f5e", colI: "#10b981" },
    { y: 65, d: w * 0.38, i: w * 0.65, colD: "#f43f5e", colI: "#10b981" },
    { y: 95, d: w * 0.15, i: w * 0.58, colD: "#f43f5e", colI: "#10b981" },
    { y: 125, d: w * 0.45, i: w * 0.85, colD: "#f43f5e", colI: "#10b981" }
  ];

  dumbbells.forEach(db => {
    // Line connector
    ctx.strokeStyle = "rgba(255,255,255,0.12)";
    ctx.lineWidth = 2.5;
    ctx.beginPath(); ctx.moveTo(db.d, db.y); ctx.lineTo(db.i, db.y); ctx.stroke();

    // Domestic dot (Red/Orange)
    ctx.fillStyle = db.colD;
    ctx.beginPath(); ctx.arc(db.d, db.y, 5, 0, Math.PI * 2); ctx.fill();
    ctx.strokeStyle = "rgba(255,255,255,0.2)"; ctx.lineWidth = 1; ctx.stroke();

    // International dot (Green)
    ctx.fillStyle = db.colI;
    ctx.beginPath(); ctx.arc(db.i, db.y, 5, 0, Math.PI * 2); ctx.fill();
    ctx.strokeStyle = "rgba(255,255,255,0.2)"; ctx.lineWidth = 1; ctx.stroke();
  });
}

function drawPreview5() {
  const c = document.getElementById("preview-5");
  const ctx = c.getContext("2d");
  c.width = c.offsetWidth; c.height = c.offsetHeight;
  const w = c.width, h = c.height;

  // Clean India Outline shape
  const outline = [
    [0.38,0.08],[0.55,0.05],[0.72,0.18],[0.78,0.3],[0.68,0.52],
    [0.55,0.72],[0.48,0.9],[0.42,0.72],[0.32,0.52],[0.24,0.32],[0.28,0.18],[0.38,0.08]
  ];
  ctx.beginPath();
  outline.forEach(([px,py], i) => i===0 ? ctx.moveTo(px*w, py*h) : ctx.lineTo(px*w, py*h));
  ctx.closePath();
  ctx.fillStyle = "rgba(245,158,11,0.05)";
  ctx.fill();
  ctx.strokeStyle = "rgba(245,158,11,0.22)";
  ctx.lineWidth = 1.5;
  ctx.stroke();

  // Draw 4 interconnected hub node clusters
  const hubs = [
    { x: w * 0.45, y: h * 0.25, r: 8, col: "#3b82f6" }, // Delhi area
    { x: w * 0.35, y: h * 0.58, r: 9, col: "#3b82f6" }, // Mumbai area
    { x: w * 0.52, y: h * 0.72, r: 10, col: "#8b5cf6" }, // Bangalore area
    { x: w * 0.58, y: h * 0.78, r: 8, col: "#8b5cf6" }  // Chennai area
  ];

  // Draw connection links
  ctx.strokeStyle = "rgba(255,255,255,0.08)";
  ctx.lineWidth = 1.5;
  for(let i = 0; i < hubs.length; i++) {
    for(let j = i + 1; j < hubs.length; j++) {
      ctx.beginPath();
      ctx.moveTo(hubs[i].x, hubs[i].y);
      ctx.lineTo(hubs[j].x, hubs[j].y);
      ctx.stroke();
    }
  }

  // Draw nodes
  hubs.forEach(node => {
    ctx.fillStyle = node.col;
    ctx.beginPath(); ctx.arc(node.x, node.y, node.r, 0, Math.PI * 2); ctx.fill();
    ctx.strokeStyle = "rgba(255,255,255,0.3)"; ctx.lineWidth = 1; ctx.stroke();
  });
}

// ─── Particle Background ───────────────────────────────────
function spawnParticles() {
  const container = document.getElementById("hero-particles");
  for (let i = 0; i < 30; i++) {
    const p = document.createElement("div");
    p.className = "particle";
    const size = 2 + Math.random() * 4;
    const col = ["#6366f1","#a855f7","#22d3ee","#34d399"][Math.floor(Math.random()*4)];
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
        speedBtn.style.color = "#38bdf8";
        speedBtn.style.borderColor = "rgba(56,189,248,0.4)";
      } else {
        APP.speed = 1200;
        speedBtn.textContent = "1x";
        speedBtn.style.color = "";
        speedBtn.style.borderColor = "";
      }
    };
    if (APP.speed === 600) {
      speedBtn.style.color = "#38bdf8";
      speedBtn.style.borderColor = "rgba(56,189,248,0.4)";
    }

    // Grouped / Stacked toggle switch matching system style
    const toggleWrap = el("div", "toggle-group");
    const optGrouped = el("button", "toggle-opt" + (barChartMode === "grouped" ? " on" : ""), "Grouped");
    const optStacked = el("button", "toggle-opt" + (barChartMode === "stacked" ? " on" : ""), "Stacked");
    
    optGrouped.onclick = () => {
      barChartMode = "grouped";
      optGrouped.classList.add("on");
      optStacked.classList.remove("on");
      renderViz(2);
    };
    
    optStacked.onclick = () => {
      barChartMode = "stacked";
      optStacked.classList.add("on");
      optGrouped.classList.remove("on");
      renderViz(2);
    };
    
    toggleWrap.append(optGrouped, optStacked);
    
    const divider = el("div", "ctrl-divider");

    c.append(wrap, playBtn, speedBtn, divider, toggleWrap);
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
        <div>
          <h2 class="viz1-title">Scientific Peer Clusters</h2>
          <p class="viz1-desc">Uncovering the hidden relationships between national wealth, R&D funding, and scientific impact.</p>
        </div>

        <div id="viz1-region-ui" style="display: none;">
          <button id="viz1-back-btn" style="background: linear-gradient(145deg, rgba(34,211,238,0.15), rgba(0,0,0,0.2)); border: 1px solid rgba(34,211,238,0.4); color: #22d3ee; padding: 10px 14px; border-radius: 6px; cursor: pointer; width: 100%; display: flex; align-items: center; justify-content: space-between; font-weight: 600; font-size: 13px; box-shadow: 0 2px 8px rgba(34,211,238,0.1); transition: all 0.2s ease;">
            ← Back to Global View <span id="viz1-region-tag" style="background: rgba(255,255,255,0.2); padding: 2px 6px; border-radius: 4px; font-size: 11px;"></span>
          </button>
        </div>

        <div class="viz1-control-group">
          <label>Compare Nations</label>
          <p style="font-size: 12px; color: #94a3b8; margin: 0; line-height: 1.4;">Click on bubbles in the chart to select countries for comparison.</p>
          <div id="viz1-compare-ui" style="display: flex; flex-wrap: wrap; gap: 8px; margin-top: 8px;"></div>
        </div>

        <div class="viz1-control-group">
          <label>
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#22d3ee" stroke-width="2"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
            Search Countries
          </label>
          <div class="viz1-search-container">
            <input type="text" id="viz1-search" class="viz1-search-input" placeholder="e.g. India, Japan, USA...">
            <svg class="viz1-search-large-icon" width="120" height="120" viewBox="0 0 24 24" fill="none" stroke="#22d3ee" stroke-width="3"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
          </div>
        </div>

        <div class="viz1-control-group">
          <label>Timeline <span id="viz1-year-label" style="margin-left: auto; background: rgba(255,255,255,0.1); padding: 2px 6px; border-radius: 4px;">${viz1Year}</span></label>
          <div style="display: flex; gap: 10px; align-items: center;">
            <button id="viz1-play-btn" class="viz1-play-btn">▶ Play</button>
            <input type="range" id="viz1-year-slider" min="${viz1YearsRange[0]}" max="${viz1YearsRange[1]}" value="${viz1Year}" style="flex: 1;">
          </div>
        </div>

        <div class="viz1-stats-card">
          <div class="viz1-stats-header">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline></svg>
            Snapshot
          </div>
          <div class="viz1-stats-row"><span>Nations:</span><span id="viz1-stat-nations">-</span></div>
          <div class="viz1-stats-row"><span>Regions:</span><span id="viz1-stat-regions">-</span></div>
          <div class="viz1-stats-row"><span>Publications:</span><span id="viz1-stat-pubs">-</span></div>
        </div>
      </div>

      <!-- MAIN PLOT AREA -->
      <div class="viz1-plot">
        <button id="viz1-specific-btn" class="viz1-specific-btn">Show Specific Countries</button>
        
        <div id="viz1-plotly-container" style="width: 100%; height: 100%;"></div>
        
        <div class="viz1-visual-guide">
          <h4>Visual Encodings</h4>
          <div style="display: grid; gap: 6px;">
            <div><strong style="color: #22d3ee;">X & Y Axes:</strong> 2D UMAP Projection (Mathematically combining Wealth, R&D Spend, Publication Volume, & Quality)</div>
            <div><strong style="color: #22d3ee;">Bubble Size:</strong> Total Publications (Volume)</div>
            <div><strong style="color: #22d3ee;">Color:</strong> Geographic Region</div>
          </div>
        </div>
      </div>
    </div>
  `;
  
  // Attach Event Listeners
  document.getElementById('viz1-back-btn').addEventListener('click', () => {
    viz1SelectedRegion = null;
    drawViz1Plotly();
    updateViz1RegionUI();
  });
  
  const slider = document.getElementById('viz1-year-slider');
  const label = document.getElementById('viz1-year-label');
  const playBtn = document.getElementById('viz1-play-btn');
  const search = document.getElementById('viz1-search');
  const specificBtn = document.getElementById('viz1-specific-btn');
  
  slider.addEventListener('input', (e) => {
    viz1Year = parseInt(e.target.value, 10);
    label.textContent = viz1Year;
    drawViz1Plotly();
  });
  
  playBtn.addEventListener('click', () => {
    viz1IsPlaying = !viz1IsPlaying;
    playBtn.innerHTML = viz1IsPlaying ? '⏸ Pause' : '▶ Play';
    
    if (viz1IsPlaying) {
      viz1PlayInterval = setInterval(() => {
        viz1Year++;
        if (viz1Year > viz1YearsRange[1]) viz1Year = viz1YearsRange[0];
        slider.value = viz1Year;
        label.textContent = viz1Year;
        drawViz1Plotly();
      }, viz1Speed);
    } else {
      clearInterval(viz1PlayInterval);
    }
  });
  
  search.addEventListener('input', (e) => {
    viz1SearchQuery = e.target.value;
    drawViz1Plotly();
  });
  
  specificBtn.addEventListener('click', () => {
    viz1ShowSpecific = !viz1ShowSpecific;
    specificBtn.textContent = viz1ShowSpecific ? 'Show All Countries' : 'Show Specific Countries';
    if (viz1ShowSpecific) {
        specificBtn.classList.add('active');
    } else {
        specificBtn.classList.remove('active');
    }
    drawViz1Plotly();
  });
  
  buildControls(1); // Clears the global top bar
  drawViz1Plotly();
  updateViz1RegionUI();
  hideLoading();
}

function updateViz1RegionUI() {
  const ui = document.getElementById('viz1-region-ui');
  const tag = document.getElementById('viz1-region-tag');
  if (ui && tag) {
    if (viz1SelectedRegion) {
      ui.style.display = 'block';
      tag.textContent = viz1SelectedRegion;
    } else {
      ui.style.display = 'none';
    }
  }
}

function updateViz1CompareUI() {
  const container = document.getElementById('viz1-compare-ui');
  if (!container) return;
  
  if (viz1ComparedCountries.length === 0) {
    container.innerHTML = '';
    return;
  }
  
  let html = '';
  viz1ComparedCountries.forEach(code => {
    const d = VIZ1_DATA.find(x => x.Country_Code === code);
    const name = d ? d.Country_Name : code;
    html += `<span style="background: rgba(34,211,238,0.2); color: #22d3ee; padding: 4px 8px; border-radius: 4px; font-size: 12px; display: flex; align-items: center; gap: 4px;">
      ${name} <span class="viz1-remove-compare" data-code="${code}" style="cursor: pointer;">✕</span>
    </span>`;
  });
  
  html += `<button id="viz1-clear-compare" style="background: transparent; border: none; color: #f43f5e; font-size: 12px; cursor: pointer; text-decoration: underline;">Clear All</button>`;
  
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
}

const VIZ1_SPECIFIC_COUNTRIES = [
  "USA", "CHN", "GBR", "DEU", "IND", "JPN", "FRA", "CAN", "ITA", "KOR", "AUS", "ESP", "BRA", "RUS", "NLD", 
  "IDN", "TUR", "IRN", "SAU", "POL", "CHE", "MYS", "PAK", "EGY", "MEX", "PRT", "SWE", "BEL", "ZAF", "NGA", "DNK", "UKR", "HKG", "AUT", "NOR",
  "IRQ", "ECU", "NPL", "VNM", "PER", "ETH", "GHA", "CYP", "COL", "UGA", "ARE", "BGD", "TJK", "PHL", "DZA"
];

function drawViz1Plotly() {
  const container = document.getElementById('viz1-plotly-container');
  if (!container || typeof VIZ1_DATA === 'undefined') return;
  
  const allRegions = getViz1Regions();
  const targetYear = parseInt(viz1Year, 10);
  let yearData = VIZ1_DATA.filter(d => d.Year === targetYear);
  if (viz1SelectedRegion) {
    yearData = yearData.filter(d => d.Region === viz1SelectedRegion);
  }
  
  // Update Snapshot
  const statNations = document.getElementById('viz1-stat-nations');
  const statRegions = document.getElementById('viz1-stat-regions');
  const statPubs = document.getElementById('viz1-stat-pubs');
  if (statNations) statNations.textContent = yearData.length;
  if (statRegions) {
      if (viz1SelectedRegion) statRegions.textContent = 1;
      else statRegions.textContent = allRegions.length;
  }
  if (statPubs) {
      const totalPubs = yearData.reduce((sum, d) => sum + (d.Total_Docs || 0), 0);
      statPubs.textContent = Math.round(totalPubs).toLocaleString();
  }
  
  const searchTerms = viz1SearchQuery.toLowerCase().split(',').map(s => s.trim()).filter(Boolean);
  const isSearchActive = searchTerms.length > 0;
  
  const matchesSearch = (countryName) => {
    if (!isSearchActive) return true;
    const name = (countryName || '').toLowerCase();
    return searchTerms.some(term => name.includes(term));
  };
  
  const isCompareActive = viz1ComparedCountries.length > 0;
  
  const traces = allRegions.map((region, globalIndex) => {
    const regionNodes = yearData.filter(d => d.Region === region);
    const regionColor = viz1ColorPalette[globalIndex % viz1ColorPalette.length];
    
    if (regionNodes.length === 0) {
      return { x: [], y: [], mode: 'markers', type: 'scatter', name: region, marker: { color: regionColor } };
    }
    
    const sizes = regionNodes.map(d => {
      if (viz1ShowSpecific && !VIZ1_SPECIFIC_COUNTRIES.includes(d.Country_Code)) return 0;
      return Math.max(6, Math.sqrt(d.Total_Docs || 0) * 0.08);
    });
    
    const opacities = regionNodes.map(d => {
      if (viz1ShowSpecific && !VIZ1_SPECIFIC_COUNTRIES.includes(d.Country_Code)) return 0;
      if (isCompareActive) return viz1ComparedCountries.includes(d.Country_Code) ? 1.0 : 0.05;
      if (!isSearchActive) return 0.85; 
      return matchesSearch(d.Country_Name) ? 1.0 : 0.15; 
    });
    
    const lineWidths = regionNodes.map(d => {
      if (viz1ShowSpecific && !VIZ1_SPECIFIC_COUNTRIES.includes(d.Country_Code)) return 0;
      if (isCompareActive) return viz1ComparedCountries.includes(d.Country_Code) ? 4 : 0.5;
      if (!isSearchActive) return 1; 
      return matchesSearch(d.Country_Name) ? 3 : 0.5; 
    });
    
    const lineColors = regionNodes.map(d => {
      if (viz1ShowSpecific && !VIZ1_SPECIFIC_COUNTRIES.includes(d.Country_Code)) return 'transparent';
      if (isCompareActive) return viz1ComparedCountries.includes(d.Country_Code) ? '#22d3ee' : 'rgba(255,255,255,0.05)';
      if (!isSearchActive) return 'rgba(255,255,255,0.7)'; 
      return matchesSearch(d.Country_Name) ? '#ffffff' : 'rgba(255,255,255,0.05)'; 
    });
    
    const hoverinfos = regionNodes.map(d => {
      if (viz1ShowSpecific && !VIZ1_SPECIFIC_COUNTRIES.includes(d.Country_Code)) return 'skip';
      return 'text';
    });
    
    const fmt = (v, decimals = 0) => { if (v == null || isNaN(v)) return 'N/A'; return Number(v).toLocaleString(undefined, { maximumFractionDigits: decimals }); };
    
    const text = regionNodes.map(d => (
      `<b><span style="font-size:16px">${d.Country_Name || 'Unknown'}</span></b><br>` +
      `<i>${d.Region || ''}</i><br><br>` +
      `📚 Publications: <b>${fmt(d.Total_Docs)}</b><br>🎯 H-Index: <b>${fmt(d.H_Index)}</b><br>` +
      `🔬 R&D Spend: <b>${fmt(d.GERD_Percent_GDP, 2)}%</b><br>💰 GDP/Capita: <b>$${fmt(d.GDP_Per_Capita_PPP)}</b>`
    ));
    
    return { 
      x: regionNodes.map(d => d.x), 
      y: regionNodes.map(d => d.y), 
      customdata: regionNodes.map(d => d.Country_Code), 
      mode: 'markers', 
      type: 'scatter', 
      name: region, 
      text: text, 
      hoverinfo: hoverinfos, 
      marker: { size: sizes, color: regionColor, opacity: opacities, line: { color: lineColors, width: lineWidths }, sizemode: 'diameter' } 
    };
  });
  
  const layout = {
    uirevision: 'true',
    title: false, 
    transition: { duration: viz1Speed * 0.85, easing: 'cubic-in-out' },
    paper_bgcolor: 'transparent', plot_bgcolor: 'transparent',
    font: { family: 'Plus Jakarta Sans, sans-serif', color: '#f8fafc' },
    xaxis: { title: 'Dimensionality Reduction (Wealth, R&D, Volume, Quality)', type: 'linear', showgrid: true, gridcolor: 'rgba(255,255,255,0.05)', zeroline: true, zerolinecolor: 'rgba(255,255,255,0.1)', showline: true, linecolor: 'rgba(255,255,255,0.2)', showticklabels: false },
    yaxis: { title: 'UMAP Projection Space', type: 'linear', showgrid: true, gridcolor: 'rgba(255,255,255,0.05)', zeroline: true, zerolinecolor: 'rgba(255,255,255,0.1)', showline: true, linecolor: 'rgba(255,255,255,0.2)', showticklabels: false },
    hovermode: 'closest',
    hoverlabel: { bgcolor: 'rgba(15, 23, 42, 0.95)', font: { family: 'Plus Jakarta Sans, sans-serif', size: 13, color: '#f8fafc' }, bordercolor: '#22d3ee' },
    legend: { font: { color: '#e2e8f0', size: 12 }, orientation: 'h', yanchor: 'bottom', y: 1.05, xanchor: 'center', x: 0.5, itemclick: false, itemdoubleclick: false },
    margin: { l: 20, r: 20, t: 40, b: 20 }
  };
  
  const config = { displayModeBar: false, responsive: true };
  
  if (typeof Plotly !== 'undefined') {
    Plotly.react(container, traces, layout, config).then(() => {
      container.on('plotly_click', function(data){
        const point = data.points && data.points[0];
        if (point && point.customdata) {
          const code = point.customdata;
          if (viz1ComparedCountries.includes(code)) {
            viz1ComparedCountries = viz1ComparedCountries.filter(c => c !== code);
          } else {
            viz1ComparedCountries.push(code);
          }
          drawViz1Plotly();
          updateViz1CompareUI();
        }
      });
      
      container.on('plotly_legendclick', function(data){
        const r = data.data[data.curveNumber] && data.data[data.curveNumber].name; 
        if (r) {
          viz1SelectedRegion = r;
          drawViz1Plotly();
          updateViz1RegionUI();
        }
        return false;
      });
    });
  }
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

  const getContinentColor = continent => {
    const map = {
      "Asia": "#f43f5e",       // Rose Red
      "Europe": "#38bdf8",     // Cyan
      "Americas": "#10b981",   // Emerald Green
      "Africa": "#f59e0b",     // Amber
      "Oceania": "#a855f7"     // Purple
    };
    return map[continent] || "#94a3b8";
  };

  const allBubbleData = DATA.getRidgelineData() || {};
  const year = Math.max(1999, Math.min(2024, APP.year || 2024));
  const yearData = allBubbleData[year] || [];

  const countryMaxTotal = {};
  Object.values(allBubbleData).flat().forEach(c => {
    if (c.country && c.total) {
      countryMaxTotal[c.country] = Math.max(countryMaxTotal[c.country] || 0, c.total);
    }
  });

  const countriesList = Array.from(new Set(
    Object.values(allBubbleData).flat().map(c => c.country)
  )).filter(name => (countryMaxTotal[name] || 0) >= 1000).sort();

  const getTier = ratio => {
    if (ratio >= 2.0) return "Elite";
    if (ratio >= 1.0) return "Balanced";
    return "Q4-Dominant";
  };

  const tierColors = {
    "Elite": "#38bdf8",       // Cyan/Blue
    "Balanced": "#94a3b8",    // Slate Gray
    "Q4-Dominant": "#f43f5e"  // Rose Red
  };

  const chartColors = {
    "q1": "#38bdf8",
    "q4": "#f43f5e"
  };

  const regionColors = {
    "Northern America": "#60a5fa",
    "Western Europe": "#c084fc",
    "Asiatic Region": "#2dd4bf",
    "Latin America": "#fb923c",
    "Eastern Europe": "#34d399",
    "Middle East": "#fbbf24",
    "Africa": "#f472b6",
    "Africa/Middle East": "#fbbf24",
    "Pacific Region": "#a855f7"
  };
  const getRegionColor = r => regionColors[r] || "#64748b";

  // Create grid container
  const container = document.createElement("div");
  container.className = "viz2-dashboard-container";
  container.style.width = "100%";
  container.style.height = "100%";

  // Map metric profiles to raw year entries
  const countryToRegionMap = {};
  yearData.forEach(c => {
    if (c.country && c.region) {
      countryToRegionMap[c.country] = c.region;
    }
  });

  // CSS Styles
  const styleBlock = document.createElement("style");
  styleBlock.textContent = `
    #panel-body {
      overflow-y: auto !important;
    }
    
    .viz2-dashboard-container {
      display: flex;
      flex-direction: column;
      gap: 1.5rem;
      width: 100%;
      height: 800px;
      box-sizing: border-box;
      padding: 0.5rem 2rem 1.5rem 1.5rem;
    }

    .viz2-top-row {
      display: grid;
      grid-template-columns: 1fr 290px;
      gap: 1.5rem;
      height: 580px;
      flex-shrink: 0;
    }
    
    .viz2-sidebar-card {
      background: rgba(15, 23, 42, 0.4);
      backdrop-filter: blur(12px);
      border: 1px solid rgba(255, 255, 255, 0.06);
      border-radius: 12px;
      padding: 1.25rem;
      display: flex;
      flex-direction: column;
      gap: 0.85rem;
      box-sizing: border-box;
      height: 100%;
      overflow-y: auto;
    }
    
    .viz2-sidebar-card::-webkit-scrollbar {
      width: 4px;
    }
    .viz2-sidebar-card::-webkit-scrollbar-track {
      background: transparent;
    }
    .viz2-sidebar-card::-webkit-scrollbar-thumb {
      background: rgba(255,255,255,0.1);
      border-radius: 2px;
    }
    
    .viz2-graph-card {
      background: rgba(15, 23, 42, 0.3);
      backdrop-filter: blur(12px);
      border: 1px solid rgba(255, 255, 255, 0.06);
      border-radius: 12px;
      padding: 1rem;
      box-sizing: border-box;
      height: 100%;
      display: flex;
      align-items: center;
      justify-content: center;
      position: relative;
    }
    
    .viz2-bottom-card {
      background: rgba(15, 23, 42, 0.4);
      backdrop-filter: blur(12px);
      border: 1px solid rgba(255, 255, 255, 0.06);
      border-radius: 12px;
      padding: 1.25rem 1.5rem;
      box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.4);
      box-sizing: border-box;
      width: 100%;
      min-height: 120px;
      flex-shrink: 0;
    }

    .viz2-stats-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
      gap: 1.25rem;
    }

    .viz2-metric-box {
      display: flex;
      flex-direction: column;
      gap: 0.25rem;
      border-right: 1px solid rgba(255, 255, 255, 0.08);
      padding-right: 1rem;
      box-sizing: border-box;
    }

    .viz2-metric-box:last-child {
      border-right: none;
    }

    .viz2-metric-title {
      font-size: 0.7rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 1px;
      color: var(--text-muted);
    }

    .viz2-metric-value {
      font-size: 1.6rem;
      font-weight: 800;
      color: var(--text);
      line-height: 1.15;
    }

    .viz2-metric-desc {
      font-size: 0.72rem;
      color: var(--text-muted);
    }
    
    .viz2-section-title {
      font-size: 0.72rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 1.5px;
      color: var(--text-muted);
      margin-bottom: 0.35rem;
      border-bottom: 1px solid rgba(255, 255, 255, 0.08);
      padding-bottom: 0.25rem;
    }

    .viz2-select-wrapper {
      display: flex;
      flex-direction: column;
      gap: 0.3rem;
    }

    .viz2-select-wrapper label {
      font-size: 0.72rem;
      text-transform: uppercase;
      letter-spacing: 1px;
      color: var(--text-muted);
      font-weight: 600;
    }

    .viz2-reset-btn {
      background: transparent;
      border: none;
      color: var(--accent3);
      font-size: 0.68rem;
      font-weight: 700;
      cursor: pointer;
      text-decoration: underline;
      padding: 0;
      float: right;
    }
    .viz2-reset-btn:hover {
      color: #fff;
    }
  `;
  container.appendChild(styleBlock);

  // Compute metric profiles for all countries
  const yearDataWithMetrics = yearData.map(c => {
    const metrics = getCountryMetrics(c.country, year, c.q1, c.q4, c.total);
    return {
      ...c,
      metrics: metrics
    };
  });

  // Continent filters list setup
  const continents = ["All", "Americas", "Europe", "Asia", "Africa", "Oceania"];

  // Sidebar card HTML skeleton
  const sidebar = document.createElement("div");
  sidebar.className = "viz2-sidebar-card";
  
  let sidebarHtml = `
    <div>
      <div class="project-badge" style="display: inline-block; margin-bottom: 0.35rem; font-size: 0.7rem;">Dashboard Module 02</div>
      <h3 style="font-size: 1.15rem; font-weight: 800; background: linear-gradient(135deg, #fff 0%, #94a3b8 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Global Quality Shift</h3>
    </div>

    <!-- Country Highlight Dropdown -->
    <div class="viz2-select-wrapper">
      <label>Highlight Country Profile</label>
      <select id="country-select-dropdown" class="ctrl-select" style="width: 100%;">
        <option value="">-- Highlight Spoke --</option>
        ${countriesList.map(c => {
          const region = countryToRegionMap[c];
          const label = region ? `${c} (${region})` : c;
          return `<option value="${c}" ${selectedCountryTrail === c ? "selected" : ""}>${label}</option>`;
        }).join("")}
      </select>
    </div>
  `;

  // Render Country metrics block (Publications, H-Index, R&D Spend, GDP/Capita) matching screenshot
  if (selectedCountryTrail) {
    const selectedMetrics = yearDataWithMetrics.find(c => c.country === selectedCountryTrail);
    if (selectedMetrics) {
      const q1 = selectedMetrics.q1 || 0;
      const q4 = selectedMetrics.q4 || 0;
      const qTotal = q1 + q4;
      const q1Pct = qTotal > 0 ? (q1 / qTotal) * 100 : 0;
      const q4Pct = qTotal > 0 ? (q4 / qTotal) * 100 : 0;
      
      sidebarHtml += `
        <!-- Country Profile Details Card (Screenshot Style + Bar Graph) -->
        <div class="viz2-country-card" style="background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 12px; padding: 1rem; display: flex; flex-direction: column; gap: 0.75rem; margin-top: 0.2rem; box-shadow: 0 4px 20px rgba(0,0,0,0.25);">
          <div style="display: flex; align-items: center; justify-content: space-between;">
            <span style="font-weight: 800; font-size: 1.05rem; color: #fff;">${selectedCountryTrail}</span>
            <span style="font-size: 0.68rem; font-weight: 700; background: rgba(56,189,248,0.15); color: #38bdf8; border: 1px solid rgba(56,189,248,0.3); border-radius: 9999px; padding: 0.15rem 0.5rem;">${selectedMetrics.metrics.continent}</span>
          </div>
          
          <div style="display: flex; flex-direction: column; gap: 0.65rem; margin-top: 0.25rem;">
            <!-- Publications -->
            <div style="display: flex; flex-direction: column; gap: 2px;">
              <div style="display: flex; align-items: center; gap: 0.5rem;">
                <span style="font-size: 1.1rem; width: 20px; text-align: center; filter: drop-shadow(0 0 2px rgba(56,189,248,0.4));">📚</span>
                <span style="font-size: 0.8rem; color: #94a3b8; flex: 1;">Publications:</span>
                <span style="font-size: 0.82rem; font-weight: 700; color: #fff;">${selectedMetrics.metrics.publications.toLocaleString()}</span>
              </div>
              <div style="width: 100%; height: 5px; background: rgba(255,255,255,0.06); border-radius: 3px; overflow: hidden; border: 1px solid rgba(255,255,255,0.02);">
                <div style="width: ${Math.min(100, (selectedMetrics.metrics.publications / 200000) * 100)}%; height: 100%; background: linear-gradient(90deg, #38bdf8, #60a5fa); border-radius: 3px; box-shadow: 0 0 4px #38bdf8;"></div>
              </div>
            </div>

            <!-- H-Index -->
            <div style="display: flex; flex-direction: column; gap: 2px;">
              <div style="display: flex; align-items: center; gap: 0.5rem;">
                <span style="font-size: 1.1rem; width: 20px; text-align: center; filter: drop-shadow(0 0 2px rgba(244,63,94,0.4));">🎯</span>
                <span style="font-size: 0.8rem; color: #94a3b8; flex: 1;">H-Index:</span>
                <span style="font-size: 0.82rem; font-weight: 700; color: #fff;">${selectedMetrics.metrics.h}</span>
              </div>
              <div style="width: 100%; height: 5px; background: rgba(255,255,255,0.06); border-radius: 3px; overflow: hidden; border: 1px solid rgba(255,255,255,0.02);">
                <div style="width: ${Math.min(100, (selectedMetrics.metrics.h / 1300) * 100)}%; height: 100%; background: linear-gradient(90deg, #f43f5e, #ec4899); border-radius: 3px; box-shadow: 0 0 4px #f43f5e;"></div>
              </div>
            </div>

            <!-- R&D Spend -->
            <div style="display: flex; flex-direction: column; gap: 2px;">
              <div style="display: flex; align-items: center; gap: 0.5rem;">
                <span style="font-size: 1.1rem; width: 20px; text-align: center; filter: drop-shadow(0 0 2px rgba(34,211,238,0.4));">🔬</span>
                <span style="font-size: 0.8rem; color: #94a3b8; flex: 1;">R&D Spend:</span>
                <span style="font-size: 0.82rem; font-weight: 700; color: #fff;">${selectedMetrics.metrics.rd.toFixed(2)}%</span>
              </div>
              <div style="width: 100%; height: 5px; background: rgba(255,255,255,0.06); border-radius: 3px; overflow: hidden; border: 1px solid rgba(255,255,255,0.02);">
                <div style="width: ${Math.min(100, (selectedMetrics.metrics.rd / 5.0) * 100)}%; height: 100%; background: linear-gradient(90deg, #2dd4bf, #34d399); border-radius: 3px; box-shadow: 0 0 4px #2dd4bf;"></div>
              </div>
            </div>

            <!-- GDP/Capita -->
            <div style="display: flex; flex-direction: column; gap: 2px;">
              <div style="display: flex; align-items: center; gap: 0.5rem;">
                <span style="font-size: 1.1rem; width: 20px; text-align: center; filter: drop-shadow(0 0 2px rgba(245,158,11,0.4));">💰</span>
                <span style="font-size: 0.8rem; color: #94a3b8; flex: 1;">GDP/Capita:</span>
                <span style="font-size: 0.82rem; font-weight: 700; color: #fff;">$${Math.round(selectedMetrics.metrics.gdp).toLocaleString()}</span>
              </div>
              <div style="width: 100%; height: 5px; background: rgba(255,255,255,0.06); border-radius: 3px; overflow: hidden; border: 1px solid rgba(255,255,255,0.02);">
                <div style="width: ${Math.min(100, (selectedMetrics.metrics.gdp / 80000) * 100)}%; height: 100%; background: linear-gradient(90deg, #fb923c, #fbbf24); border-radius: 3px; box-shadow: 0 0 4px #fb923c;"></div>
              </div>
            </div>
          </div>
          
          <!-- Stacked Bar Graph: Quality Share (Q1 vs Q4) -->
          <div style="margin-top: 0.45rem; border-top: 1px dashed rgba(255,255,255,0.08); padding-top: 0.55rem;">
            <div style="display: flex; justify-content: space-between; font-size: 0.72rem; color: #94a3b8; margin-bottom: 5px;">
              <span>Quality Split (Q1 vs Q4)</span>
              <span style="font-weight:700;"><span style="color:#38bdf8;">Q1: ${q1Pct.toFixed(0)}%</span> | <span style="color:#f43f5e;">Q4: ${q4Pct.toFixed(0)}%</span></span>
            </div>
            <div style="width: 100%; height: 12px; background: rgba(255,255,255,0.06); border-radius: 4px; display: flex; overflow: hidden; border: 1px solid rgba(255,255,255,0.04);">
              <div style="width: ${q1Pct}%; background: #38bdf8; height: 100%; box-shadow: inset 0 0 4px rgba(0,0,0,0.3);" title="Q1 Journals: ${q1.toLocaleString()}"></div>
              <div style="width: ${q4Pct}%; background: #f43f5e; height: 100%; box-shadow: inset 0 0 4px rgba(0,0,0,0.3);" title="Q4 Journals: ${q4.toLocaleString()}"></div>
            </div>
          </div>
        </div>
      `;
    }
  }

  // Render Continent Filter and Slider Panel
  sidebarHtml += `
    <!-- Continent Select Filter -->
    <div class="viz2-select-wrapper" style="margin-top: 0.2rem;">
      <label>Filter By Continent</label>
      <select id="continent-select" class="ctrl-select" style="width: 100%;">
        ${continents.map(c => `<option value="${c}" ${activeContinentFilter === c ? "selected" : ""}>${c === "All" ? "All Continents" : c}</option>`).join("")}
      </select>
      <div style="display: flex; flex-wrap: wrap; gap: 8px; margin-top: 8px; font-size: 0.68rem; line-height: 1.2;">
        <span style="display: flex; align-items: center; gap: 3px; color: #f43f5e; font-weight: 700;"><span style="display:inline-block; width:6px; height:6px; background:#f43f5e; border-radius:50%; box-shadow: 0 0 3px #f43f5e;"></span>Asia</span>
        <span style="display: flex; align-items: center; gap: 3px; color: #38bdf8; font-weight: 700;"><span style="display:inline-block; width:6px; height:6px; background:#38bdf8; border-radius:50%; box-shadow: 0 0 3px #38bdf8;"></span>Europe</span>
        <span style="display: flex; align-items: center; gap: 3px; color: #10b981; font-weight: 700;"><span style="display:inline-block; width:6px; height:6px; background:#10b981; border-radius:50%; box-shadow: 0 0 3px #10b981;"></span>Americas</span>
        <span style="display: flex; align-items: center; gap: 3px; color: #f59e0b; font-weight: 700;"><span style="display:inline-block; width:6px; height:6px; background:#f59e0b; border-radius:50%; box-shadow: 0 0 3px #f59e0b;"></span>Africa</span>
        <span style="display: flex; align-items: center; gap: 3px; color: #a855f7; font-weight: 700;"><span style="display:inline-block; width:6px; height:6px; background:#a855f7; border-radius:50%; box-shadow: 0 0 3px #a855f7;"></span>Oceania</span>
      </div>
    </div>

    <!-- Sort and Top Rank selector -->
    <div class="viz2-select-wrapper" style="margin-top: 0.4rem;">
      <label>Sort & Top Rank (Top 9)</label>
      <select id="sort-rank-select" class="ctrl-select" style="width: 100%;">
        <option value="Default" ${activeSortParameter === "Default" ? "selected" : ""}>Default (Whitelist / All)</option>
        <option value="publications" ${activeSortParameter === "publications" ? "selected" : ""}>Publications Volume</option>
        <option value="h" ${activeSortParameter === "h" ? "selected" : ""}>H-Index Score</option>
        <option value="rd" ${activeSortParameter === "rd" ? "selected" : ""}>R&D Spend (% GDP)</option>
        <option value="gdp" ${activeSortParameter === "gdp" ? "selected" : ""}>GDP per Capita</option>
        <option value="ratio" ${activeSortParameter === "ratio" ? "selected" : ""}>Q1 / Q4 Quality Ratio</option>
      </select>
    </div>

    <!-- Factor Filter Sliders -->
    <div style="display: flex; flex-direction: column; gap: 0.6rem; margin-top: 0.2rem;">
      <div>
        <button id="btn-reset-filters" class="viz2-reset-btn">Reset All</button>
        <div class="viz2-section-title">Filter By Factors</div>
      </div>
      
      <!-- Min Pubs -->
      <div style="display: flex; flex-direction: column; gap: 2px;">
        <div style="display: flex; justify-content: space-between; font-size: 0.68rem; color: #94a3b8;">
          <span>Min Publications</span>
          <span id="lbl-min-pub" style="font-weight: 700; color: #38bdf8;">${minPubFilter >= 1000 ? (minPubFilter / 1000).toFixed(0) + "k" : minPubFilter}</span>
        </div>
        <input type="range" id="slide-min-pub" class="ctrl-range" style="width: 100%;" min="0" max="200000" step="5000" value="${minPubFilter}">
      </div>

      <!-- Min H Index -->
      <div style="display: flex; flex-direction: column; gap: 2px;">
        <div style="display: flex; justify-content: space-between; font-size: 0.68rem; color: #94a3b8;">
          <span>Min H-Index</span>
          <span id="lbl-min-h" style="font-weight: 700; color: #38bdf8;">${minHIndexFilter}</span>
        </div>
        <input type="range" id="slide-min-h" class="ctrl-range" style="width: 100%;" min="0" max="1000" step="25" value="${minHIndexFilter}">
      </div>

      <!-- Min R&D Spend -->
      <div style="display: flex; flex-direction: column; gap: 2px;">
        <div style="display: flex; justify-content: space-between; font-size: 0.68rem; color: #94a3b8;">
          <span>Min R&D Spend (% GDP)</span>
          <span id="lbl-min-rd" style="font-weight: 700; color: #38bdf8;">${minRdFilter.toFixed(1)}%</span>
        </div>
        <input type="range" id="slide-min-rd" class="ctrl-range" style="width: 100%;" min="0" max="4.0" step="0.1" value="${minRdFilter}">
      </div>

      <!-- Min GDP/Capita -->
      <div style="display: flex; flex-direction: column; gap: 2px;">
        <div style="display: flex; justify-content: space-between; font-size: 0.68rem; color: #94a3b8;">
          <span>Min GDP/Capita</span>
          <span id="lbl-min-gdp" style="font-weight: 700; color: #38bdf8;">$${minGdpFilter.toLocaleString()}</span>
        </div>
        <input type="range" id="slide-min-gdp" class="ctrl-range" style="width: 100%;" min="0" max="80000" step="2000" value="${minGdpFilter}">
      </div>
    </div>
  `;

  sidebar.innerHTML = sidebarHtml;

  // Calculate Summary Statistics for current year
  const filteredYearData = yearData.filter(c => activeRegionFilter === "All" || c.region === activeRegionFilter);
  let globalQ1 = 0, globalQ4 = 0;
  filteredYearData.forEach(c => {
    globalQ1 += c.q1 || 0;
    globalQ4 += c.q4 || 0;
  });
  const globalRatio = globalQ4 > 0 ? (globalQ1 / globalQ4) : 0;

  // Graph card
  const graphCard = document.createElement("div");
  graphCard.className = "viz2-graph-card";
  graphCard.style.position = "relative";
  graphCard.innerHTML = `
    <!-- Top-right Explanation Box (Redesigned Compact Version) -->
    <div style="position: absolute; top: 0.6rem; right: 0.6rem; background: rgba(15, 23, 42, 0.85); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 8px; padding: 0.45rem 0.65rem; max-width: 320px; backdrop-filter: blur(8px); z-index: 10; pointer-events: none; display: flex; flex-direction: column; gap: 0.35rem; font-size: 0.65rem; line-height: 1.25; box-shadow: 0 4px 15px rgba(0,0,0,0.35);">
      <div style="font-weight: 800; color: #fff; font-size: 0.7rem; border-bottom: 1px solid rgba(255,255,255,0.08); padding-bottom: 3px; display: flex; align-items: center; gap: 4px;">
        <span>ℹ️</span> Quality Guide
      </div>
      <div style="display: flex; gap: 0.75rem; align-items: center;">
        <div style="display: flex; flex-direction: column; gap: 0.35rem; min-width: 140px;">
          <div style="display: flex; gap: 4px; align-items: center;">
            <span style="display: inline-block; width: 6px; height: 6px; background: #38bdf8; border-radius: 1px; flex-shrink: 0; box-shadow: 0 0 3px #38bdf8;"></span>
            <div><b style="color: #38bdf8;">Q1 (Elite):</b> Top 25% impact.</div>
          </div>
          <div style="display: flex; gap: 4px; align-items: center;">
            <span style="display: inline-block; width: 6px; height: 6px; background: #f43f5e; border-radius: 1px; flex-shrink: 0; box-shadow: 0 0 3px #f43f5e;"></span>
            <div><b style="color: #f43f5e;">Q4 (Low-tier):</b> Bottom 25% impact.</div>
          </div>
        </div>
        <div style="border-left: 1px dashed rgba(255,255,255,0.08); padding-left: 0.75rem; color: #94a3b8; font-size: 0.62rem; flex: 1;">
          <b style="color: #fff;">Q1/Q4 Ratio:</b> Research quality index. High ratio indicates strong elite share.
        </div>
      </div>
    </div>
  `;

  // Bottom card for horizontal metrics summary
  const bottomCard = document.createElement("div");
  bottomCard.className = "viz2-bottom-card";

  let metricsHtml = `
    <div class="viz2-stats-grid">
      <div class="viz2-metric-box">
        <span class="viz2-metric-title">${year} State</span>
        <span class="viz2-metric-value" style="color: #f59e0b;">${globalRatio.toFixed(2)}</span>
        <span class="viz2-metric-desc">Q1/Q4 Quality Ratio</span>
      </div>
      <div class="viz2-metric-box">
        <span class="viz2-metric-title">Elite Publications</span>
        <span class="viz2-metric-value">${(globalQ1 / 1000).toFixed(0)}k</span>
        <span class="viz2-metric-desc">Total Q1 Journals Published</span>
      </div>
      <div class="viz2-metric-box">
        <span class="viz2-metric-title">Low-tier Publications</span>
        <span class="viz2-metric-value">${(globalQ4 / 1000).toFixed(0)}k</span>
        <span class="viz2-metric-desc">Total Q4 Journals Published</span>
      </div>
  `;

  if (selectedCountryTrail) {
    const countryData = yearData.find(c => c.country === selectedCountryTrail);
    if (countryData) {
      metricsHtml += `
        <div class="viz2-metric-box" style="border-left: 1px dashed rgba(255, 255, 255, 0.15); padding-left: 1.5rem;">
          <span class="viz2-metric-title">${selectedCountryTrail} Profile</span>
          <span class="viz2-metric-value" style="color: #38bdf8;">${getTier(countryData.ratio).toUpperCase()}</span>
          <span class="viz2-metric-desc">Research Quality Category</span>
        </div>
        <div class="viz2-metric-box">
          <span class="viz2-metric-title">${selectedCountryTrail} Ratio</span>
          <span class="viz2-metric-value">${countryData.ratio.toFixed(2)}</span>
          <span class="viz2-metric-desc">Q1/Q4 Quality Ratio</span>
        </div>
        <div class="viz2-metric-box">
          <span class="viz2-metric-title">${selectedCountryTrail} Docs</span>
          <span class="viz2-metric-value">${(countryData.q1 + countryData.q4).toLocaleString()}</span>
          <span class="viz2-metric-desc">Q1: ${countryData.q1.toLocaleString()} | Q4: ${countryData.q4.toLocaleString()}</span>
        </div>
      `;
    }
  } else {
    let continentRatio = globalRatio;
    let ratioTitle = "Global";
    if (activeContinentFilter !== "All") {
      const contData = yearDataWithMetrics.filter(d => d.metrics.continent === activeContinentFilter);
      let contQ1 = 0, contQ4 = 0;
      contData.forEach(d => { contQ1 += d.q1; contQ4 += d.q4; });
      if (contQ4 > 0) continentRatio = contQ1 / contQ4;
      else if (contQ1 > 0) continentRatio = contQ1;
      ratioTitle = activeContinentFilter;
    }
    
    metricsHtml += `
      <div class="viz2-metric-box" style="border-left: 1px dashed rgba(255, 255, 255, 0.15); padding-left: 1.5rem;">
        <span class="viz2-metric-title">${ratioTitle} Q1/Q4 Avg</span>
        <span class="viz2-metric-value" style="font-size: 1.4rem; color: #f59e0b;">${continentRatio.toFixed(2)}</span>
        <span class="viz2-metric-desc">Average ratio for selected region</span>
      </div>
      <div class="viz2-metric-box">
        <span class="viz2-metric-title">Active Filter</span>
        <span class="viz2-metric-value" style="color: #10b981; font-size: 1.4rem;">${activeContinentFilter.toUpperCase()}</span>
        <span class="viz2-metric-desc">Continent being visualized</span>
      </div>
    `;
  }

  metricsHtml += `</div>`;
  bottomCard.innerHTML = metricsHtml;

  // Build structure: Top Row (Graph & Sidebar), Bottom Card (Summary)
  const topRow = document.createElement("div");
  topRow.className = "viz2-top-row";
  topRow.appendChild(graphCard);
  topRow.appendChild(sidebar);

  container.appendChild(topRow);
  container.appendChild(bottomCard);
  body.appendChild(container);

  // Apply filters on the database
  let displayData = [...yearDataWithMetrics];

  // Exclude low-data countries (total < 1000)
  if (activeContinentFilter === "All") {
    displayData = displayData.filter(d => d.total >= 1000);
  } else {
    displayData = displayData.filter(d => d.total >= 10);
  }

  // 1. Continent Filter
  if (activeContinentFilter !== "All") {
    displayData = displayData.filter(d => d.metrics.continent === activeContinentFilter);
  }

  // 2. Sliders Filters
  displayData = displayData.filter(d => {
    return d.metrics.publications >= minPubFilter &&
           d.metrics.h >= minHIndexFilter &&
           d.metrics.rd >= minRdFilter &&
           d.metrics.gdp >= minGdpFilter;
  });

  // 3. Sort & Rank Filter (Top 9)
  if (activeSortParameter !== "Default") {
    displayData.sort((a, b) => {
      let valA = 0, valB = 0;
      if (activeSortParameter === "publications") { valA = a.metrics.publications; valB = b.metrics.publications; }
      else if (activeSortParameter === "h") { valA = a.metrics.h; valB = b.metrics.h; }
      else if (activeSortParameter === "rd") { valA = a.metrics.rd; valB = b.metrics.rd; }
      else if (activeSortParameter === "gdp") { valA = a.metrics.gdp; valB = b.metrics.gdp; }
      else if (activeSortParameter === "ratio") { valA = a.ratio; valB = b.ratio; }
      return valB - valA;
    });
    displayData = displayData.slice(0, 9);
  } else {
    // Keep the default graph Same As It Was (whitelist of 10 countries) if no filters are active
    const hasActiveSliders = minPubFilter > 0 || minHIndexFilter > 0 || minRdFilter > 0 || minGdpFilter > 0;
    if (activeContinentFilter === "All" && !hasActiveSliders) {
      const whitelistDefault = [
        "China", "India", "Japan", "United States", "France", 
        "Germany", "Ireland", "Netherlands", "Switzerland", "United Kingdom"
      ];
      displayData = displayData.filter(d => whitelistDefault.includes(d.country));
    } else if (activeContinentFilter !== "All" && !hasActiveSliders) {
      // Smart selection for a specific continent: 7-9 interesting countries
      // 1. Sort by total volume and take top 4
      const byVolume = [...displayData].sort((a, b) => b.total - a.total).slice(0, 4);
      // 2. Sort by ratio and take top 2 and bottom 2
      const byRatio = [...displayData].sort((a, b) => b.ratio - a.ratio);
      const topRatio = byRatio.slice(0, 3); // Take 3 just in case of overlap
      const bottomRatio = byRatio.slice(Math.max(0, byRatio.length - 2)); // Bottom 2
      
      const selectedSet = new Set([...byVolume.map(d=>d.country), ...topRatio.map(d=>d.country), ...bottomRatio.map(d=>d.country)]);
      
      // Filter down to the selected set (should naturally result in 7-9 countries depending on overlap)
      displayData = displayData.filter(d => selectedSet.has(d.country));
    }
  }

  // Ensure selected country is in the displayData list if matching filters
  if (selectedCountryTrail) {
    const isIncluded = displayData.some(d => d.country === selectedCountryTrail);
    if (!isIncluded) {
      const selectedObj = yearDataWithMetrics.find(d => d.country === selectedCountryTrail);
      if (selectedObj) {
        // Only include if it satisfies the continent filter
        const matchContinent = activeContinentFilter === "All" || selectedObj.metrics.continent === activeContinentFilter;
        // Only include if it satisfies the factor filters
        const matchFactors = selectedObj.metrics.publications >= minPubFilter &&
                             selectedObj.metrics.h >= minHIndexFilter &&
                             selectedObj.metrics.rd >= minRdFilter &&
                             selectedObj.metrics.gdp >= minGdpFilter;
        if (matchContinent && matchFactors) {
          displayData.push(selectedObj);
          
          // Re-sort to maintain order if ranking is active
          if (activeSortParameter !== "Default") {
            displayData.sort((a, b) => {
              let valA = 0, valB = 0;
              if (activeSortParameter === "publications") { valA = a.metrics.publications; valB = b.metrics.publications; }
              else if (activeSortParameter === "h") { valA = a.metrics.h; valB = b.metrics.h; }
              else if (activeSortParameter === "rd") { valA = a.metrics.rd; valB = b.metrics.rd; }
              else if (activeSortParameter === "gdp") { valA = a.metrics.gdp; valB = b.metrics.gdp; }
              else if (activeSortParameter === "ratio") { valA = a.ratio; valB = b.ratio; }
              return valB - valA;
            });
          }
        }
      }
    }
  }

  // Sort display data for final rendering
  if (activeSortParameter === "Default") {
    displayData.sort((a, b) => {
      if (a.region !== b.region) {
        return a.region.localeCompare(b.region);
      }
      return a.country.localeCompare(b.country);
    });
  }

  // SVG Setup
  const W = graphCard.offsetWidth || 850;
  const H = graphCard.offsetHeight || 550;
  
  const svg = d3.select(graphCard).append("svg")
    .attr("width", W)
    .attr("height", H)
    .style("overflow", "visible");

  const margin = { top: 40, right: 30, bottom: 90, left: 65 };
  const innerWidth = W - margin.left - margin.right;
  const innerHeight = H - margin.top - margin.bottom;

  const chartG = svg.append("g")
    .attr("transform", `translate(${margin.left}, ${margin.top})`);

  // Max value calculator for Y-axis
  const yMaxVal = barChartMode === "grouped" 
    ? d3.max(displayData, d => Math.max(d.q1, d.q4)) || 10000 
    : d3.max(displayData, d => d.q1 + d.q4) || 10000;

  const yScale = d3.scaleLinear()
    .domain([0, yMaxVal * 1.05])
    .range([innerHeight, 0]);

  // Y Axis & Grid lines
  const yAxis = d3.axisLeft(yScale)
    .ticks(5)
    .tickSize(-innerWidth)
    .tickFormat(d => d >= 1000 ? `${(d / 1000).toFixed(0)}k` : d);

  const yAxisG = chartG.append("g")
    .attr("class", "y-axis")
    .call(yAxis);

  yAxisG.select(".domain").remove();
  yAxisG.selectAll(".tick line")
    .attr("stroke", "rgba(255, 255, 255, 0.06)")
    .attr("stroke-dasharray", "3,3");
  yAxisG.selectAll(".tick text")
    .attr("fill", "#94a3b8")
    .attr("font-size", "10px")
    .attr("dx", "-4px");

  // X Axis
  const xScale = d3.scaleBand()
    .domain(displayData.map(d => d.country))
    .range([0, innerWidth])
    .padding(0.25);

  const xAxis = d3.axisBottom(xScale);

  const xAxisG = chartG.append("g")
    .attr("class", "x-axis")
    .attr("transform", `translate(0, ${innerHeight})`)
    .call(xAxis);

  xAxisG.select(".domain").attr("stroke", "rgba(255, 255, 255, 0.1)");
  xAxisG.selectAll(".tick line").attr("stroke", "rgba(255, 255, 255, 0.1)");

  // Rotate country names to fit
  xAxisG.selectAll(".tick text")
    .style("fill", d => {
      const item = displayData.find(x => x.country === d);
      return item ? getContinentColor(item.metrics.continent) : "#94a3b8";
    })
    .attr("font-size", "9px")
    .attr("font-weight", "700")
    .style("text-anchor", "end")
    .attr("dx", "-8px")
    .attr("dy", "4px")
    .attr("transform", "rotate(-40)");

  // Draw bars group
  const countryGroups = chartG.selectAll(".country-bar-group")
    .data(displayData)
    .enter().append("g")
      .attr("class", "country-bar-group")
      .attr("transform", d => `translate(${xScale(d.country)}, 0)`)
      .style("cursor", "pointer")
      .style("transition", "opacity 0.2s ease");

  if (barChartMode === "grouped") {
    const xSubScale = d3.scaleBand()
      .domain(["q1", "q4"])
      .range([0, xScale.bandwidth()])
      .padding(0.08);

    // Q1 bars (elite - cyan)
    countryGroups.append("rect")
      .attr("class", "bar-q1")
      .attr("x", xSubScale("q1"))
      .attr("y", d => yScale(d.q1))
      .attr("width", xSubScale.bandwidth())
      .attr("height", d => innerHeight - yScale(d.q1))
      .attr("fill", chartColors.q1)
      .attr("fill-opacity", 0.8)
      .attr("rx", 2)
      .attr("stroke", chartColors.q1)
      .attr("stroke-width", 0.5)
      .attr("stroke-opacity", 0.3);

    // Q4 bars (low-tier - rose-red)
    countryGroups.append("rect")
      .attr("class", "bar-q4")
      .attr("x", xSubScale("q4"))
      .attr("y", d => yScale(d.q4))
      .attr("width", xSubScale.bandwidth())
      .attr("height", d => innerHeight - yScale(d.q4))
      .attr("fill", chartColors.q4)
      .attr("fill-opacity", 0.8)
      .attr("rx", 2)
      .attr("stroke", chartColors.q4)
      .attr("stroke-width", 0.5)
      .attr("stroke-opacity", 0.3);

    // Selection outline around the grouped bars
    countryGroups.filter(d => d.country === selectedCountryTrail)
      .append("rect")
        .attr("class", "bar-selection-outline")
        .attr("x", -3)
        .attr("y", d => Math.min(yScale(d.q1), yScale(d.q4)) - 3)
        .attr("width", xScale.bandwidth() + 6)
        .attr("height", d => innerHeight - Math.min(yScale(d.q1), yScale(d.q4)) + 6)
        .attr("fill", "none")
        .attr("stroke", "#ffffff")
        .attr("stroke-width", 2)
        .attr("rx", 5)
        .style("filter", "drop-shadow(0 0 4px #38bdf8)");

  } else {
    // Stacked mode
    // Bottom: Q4 (rose-red)
    countryGroups.append("rect")
      .attr("class", "bar-q4")
      .attr("x", 0)
      .attr("y", d => yScale(d.q4))
      .attr("width", xScale.bandwidth())
      .attr("height", d => innerHeight - yScale(d.q4))
      .attr("fill", chartColors.q4)
      .attr("fill-opacity", 0.8)
      .attr("stroke", chartColors.q4)
      .attr("stroke-width", 0.5)
      .attr("stroke-opacity", 0.3);

    // Top: Q1 (cyan)
    countryGroups.append("rect")
      .attr("class", "bar-q1")
      .attr("x", 0)
      .attr("y", d => yScale(d.q4 + d.q1))
      .attr("width", xScale.bandwidth())
      .attr("height", d => yScale(d.q4) - yScale(d.q4 + d.q1))
      .attr("fill", chartColors.q1)
      .attr("fill-opacity", 0.9)
      .attr("stroke", chartColors.q1)
      .attr("stroke-width", 0.5)
      .attr("stroke-opacity", 0.3);

    // Selection outline around the stacked bars
    countryGroups.filter(d => d.country === selectedCountryTrail)
      .append("rect")
        .attr("class", "bar-selection-outline")
        .attr("x", -3)
        .attr("y", d => yScale(d.q1 + d.q4) - 3)
        .attr("width", xScale.bandwidth() + 6)
        .attr("height", d => innerHeight - yScale(d.q1 + d.q4) + 6)
        .attr("fill", "none")
        .attr("stroke", "#ffffff")
        .attr("stroke-width", 2)
        .attr("rx", 5)
        .style("filter", "drop-shadow(0 0 4px #38bdf8)");
  }

  // Hover Interactions
  countryGroups
    .on("mouseenter", function(e, d) {
      // Dim other bars
      countryGroups.style("opacity", s => s.country === d.country ? 1.0 : 0.25);

      // Tooltip HTML content with macroeconomic factors
      showTip(e, `
        <div style="font-weight:700; font-size:13px; border-bottom:1px solid rgba(255,255,255,0.12); padding-bottom:4px; margin-bottom:4px; color:#fff;">${d.country}</div>
        <div style="font-size:11px; color:#94a3b8; margin-bottom: 3px;">Region: <span style="color:${getRegionColor(d.region)}; font-weight:600;">${d.region}</span></div>
        <div style="font-size:11px; margin-bottom: 3px;">Continent: <span style="color:#2dd4bf; font-weight:600;">${d.metrics.continent}</span></div>
        <div style="font-size:11px; margin-top:2px;">Q1 Journals (Elite): <span style="color:#38bdf8; font-weight:700;">${d.q1.toLocaleString()}</span></div>
        <div style="font-size:11px;">Q4 Journals (Low-tier): <span style="color:#f43f5e; font-weight:700;">${d.q4.toLocaleString()}</span></div>
        <div style="font-size:11px; margin-bottom: 2px;">Q1/Q4 Ratio: <span style="color:#f59e0b; font-weight:bold;">${d.ratio.toFixed(3)}</span></div>
        <div style="font-size:11px; margin-top:4px; border-top:1px dashed rgba(255,255,255,0.12); padding-top:4px; color: #cbd5e1;">
          <div>📚 Publications: <b>${d.metrics.publications.toLocaleString()}</b></div>
          <div>🎯 H-Index: <b>${d.metrics.h}</b></div>
          <div>🔬 R&D Spend: <b>${d.metrics.rd.toFixed(2)}%</b></div>
          <div>💰 GDP/Capita: <b>$${Math.round(d.metrics.gdp).toLocaleString()}</b></div>
        </div>
      `);
    })
    .on("mousemove", moveTip)
    .on("mouseleave", function() {
      // Restore bars opacities
      countryGroups.style("opacity", 1.0);
      hideTip();
    })
    .on("click", function(e, d) {
      selectedCountryTrail = d.country;
      renderViz(2);
    });

  // Bind Sidebar Event Listeners
  // 1. Country Selection Dropdown
  const sidebarCSelect = container.querySelector("#country-select-dropdown");
  if (sidebarCSelect) {
    sidebarCSelect.onchange = () => {
      selectedCountryTrail = sidebarCSelect.value || null;
      renderViz(2);
    };
  }

  // 2. Continent Select
  const contSel = container.querySelector("#continent-select");
  if (contSel) {
    contSel.onchange = () => {
      activeContinentFilter = contSel.value;
      renderViz(2);
    };
  }

  // 2b. Sort & Rank Select
  const sortRankSel = container.querySelector("#sort-rank-select");
  if (sortRankSel) {
    sortRankSel.onchange = () => {
      activeSortParameter = sortRankSel.value;
      renderViz(2);
    };
  }

  // 3. Reset All Button
  const resetBtn = container.querySelector("#btn-reset-filters");
  if (resetBtn) {
    resetBtn.onclick = () => {
      activeContinentFilter = "All";
      activeSortParameter = "Default";
      minPubFilter = 0;
      minHIndexFilter = 0;
      minRdFilter = 0;
      minGdpFilter = 0;
      renderViz(2);
    };
  }

  // 4. Sliders Event Hooks
  const setupSlider = (sliderId, labelId, filterSetter, formatter) => {
    const slider = container.querySelector(`#${sliderId}`);
    const label = container.querySelector(`#${labelId}`);
    if (slider && label) {
      slider.oninput = () => {
        const val = +slider.value;
        label.textContent = formatter(val);
        filterSetter(val);
      };
      slider.onchange = () => {
        renderViz(2);
      };
    }
  };

  setupSlider("slide-min-pub", "lbl-min-pub", val => minPubFilter = val, val => val >= 1000 ? `${(val / 1000).toFixed(0)}k` : val);
  setupSlider("slide-min-h", "lbl-min-h", val => minHIndexFilter = val, val => val);
  setupSlider("slide-min-rd", "lbl-min-rd", val => minRdFilter = val, val => `${val.toFixed(1)}%`);
  setupSlider("slide-min-gdp", "lbl-min-gdp", val => minGdpFilter = val, val => `$${val.toLocaleString()}`);
}
// ══════════════════════════════════════════════════════════
// VIZ 3: Top-10 Research Topics (Bar Chart Race)
// ══════════════════════════════════════════════════════════
// ══════════════════════════════════════════════════════════
// VIZ 3: Top-10 Research Topics (Bar Chart Race)
// ══════════════════════════════════════════════════════════
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
            --accent-glow: rgba(0, 242, 254, 0.15);
            --primary: #00f2fe;
            --primary-glow: rgba(0, 242, 254, 0.4);
            
            /* Topic Gradients */
            --g-ai: linear-gradient(90deg, #ff2a5f 0%, #ff7e40 100%);
            --g-crispr: linear-gradient(90deg, #00f2fe 0%, #4facfe 100%);
            --g-diseases: linear-gradient(90deg, #f857a6 0%, #ff5858 100%);
            --g-data: linear-gradient(90deg, #a18cd1 0%, #fbc2eb 100%);
            --g-energy: linear-gradient(90deg, #11998e 0%, #3afb65 100%);
            --g-robotics: linear-gradient(90deg, #f9d423 0%, #ff4e50 100%);
            --g-materials: linear-gradient(90deg, #00c6ff 0%, #0072ff 100%);
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
            background: rgba(0, 242, 254, 0.1);
            border: 1px solid rgba(0, 242, 254, 0.2);
            padding: 0.5rem 1rem;
            border-radius: 30px;
            font-weight: 600;
            color: var(--primary);
            text-shadow: 0 0 10px var(--primary-glow);
            box-shadow: 0 0 15px rgba(0, 242, 254, 0.05);
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
            color: #3afb65;
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
                    <button id="btnReset" class="btn-control" title="Restart to 1950">
                        <svg class="icon" style="width: 20px; height: 20px;" viewBox="0 0 24 24">
                            <path d="M12 5V1L7 6l5 5V7c3.31 0 6 2.69 6 6s-2.69 6-6 6-6-2.69-6-6H4c0 4.42 3.58 8 8 8s8-3.58 8-8-3.58-8-8-8z"/>
                        </svg>
                    </button>
                </div>

                <!-- Timeline Scrubber -->
                <div class="timeline-container">
                    <div class="timeline-labels">
                        <span id="labelStartYear">1950</span>
                        <span id="labelCurrentYear" style="font-weight: 700; color: var(--primary);">Year: 1950</span>
                        <span id="labelEndYear">2025</span>
                    </div>
                    <input type="range" id="timelineSlider" class="timeline-slider" min="1950" max="2025" value="1950">
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
                    <div id="yearIndicator" class="year-display">1950</div>
                </div>
                
                <div class="race-body" id="raceBody">
                    <!-- Watermark -->
                    <div id="watermarkYear" class="watermark-year">1950</div>
                    
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
                <h3>Cumulative Publication Trend (1950 - 2025)</h3>
            </div>
            <div class="chart-container">
                <canvas id="trendChart"></canvas>
            </div>
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
                    <h2 style="color: #ff5858; margin-bottom: 1rem;">Data File Missing</h2>
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
            "AI & Machine Learning": 1702,
            "CRISPR & Genomics": 1308,
            "Infectious Diseases": 2725,
            "Data Science & Big Data": 1703,
            "Renewable Energy": 2105,
            "Robotics & Automation": 2207,
            "Quantum Computing": 2500
        };

        const topicGradients = {
            "AI & Machine Learning": 'var(--g-ai)',
            "CRISPR & Genomics": 'var(--g-crispr)',
            "Infectious Diseases": 'var(--g-diseases)',
            "Data Science & Big Data": 'var(--g-data)',
            "Renewable Energy": 'var(--g-energy)',
            "Robotics & Automation": 'var(--g-robotics)',
            "Quantum Computing": 'var(--g-materials)'
        };

        const topicColors = {
            "AI & Machine Learning": '#ff2a5f',
            "CRISPR & Genomics": '#00f2fe',
            "Infectious Diseases": '#f857a6',
            "Data Science & Big Data": '#a18cd1',
            "Renewable Energy": '#11998e',
            "Robotics & Automation": '#f9d423',
            "Quantum Computing": '#00c6ff'
        };

        const years = [];
        for (let y = 1950; y <= 2025; y++) {
            years.push(y);
        }

        let globalData = {};  // globalData[year][topic] = sum
        let countryData = {}; // countryData[countryCode][year][topic] = count
        let countryMap = {};  // countryMap[countryCode] = countryName

        // Application State
        let currentYear = 1950;
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
                    data: years.map(y => globalData[y][topic]),
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
            
            if (recalcStats) {
                calculateAndRenderStats();
                updateLineChartData();
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
                }
            });
        }

        function updateLineChartData() {
            if (!lineChart) return;

            topics.forEach((topic, idx) => {
                const dataPoints = years.map(y => {
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
                let peakYear = 1950;
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

                // 2. Calculate Growth Rate (Earliest vs 2025)
                // Find first year with publications
                let firstActiveYear = 1950;
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
                    // Fall back to actual 1950 value if all are 0 or to make computation clean
                    const dataSrc = (selectedCountry === 'GLOBAL') ? globalData[1950] : countryData[selectedCountry][1950];
                    firstActiveVal = dataSrc[topic] || 0;
                }

                const data2025Src = (selectedCountry === 'GLOBAL') ? globalData[2025] : countryData[selectedCountry][2025];
                const val2025 = data2025Src[topic] || 0;

                let growthStr = 'N/A';
                if (firstActiveVal > 0) {
                    const growthPct = ((val2025 - firstActiveVal) / firstActiveVal) * 100;
                    growthStr = (growthPct >= 0 ? '+' : '') + growthPct.toLocaleString(undefined, {maximumFractionDigits: 0}) + '%';
                } else if (val2025 > 0) {
                    growthStr = 'New (+100%)';
                }

                // 3. Peak publications count
                const peakStr = peakPubs > 0 ? `${peakPubs.toLocaleString()} (${peakYear})` : 'N/A';

                // 4. Secondary Analytical Metric
                let footerLabel = '';
                let footerValue = '';
                
                if (selectedCountry === 'GLOBAL') {
                    // For global, show Top Contributing Country in 2025
                    const topC = getTopCountryInYear(topic, 2025);
                    footerLabel = 'Top Leader (2025)';
                    footerValue = topC.code ? `${topC.name} (${(topC.count / val2025 * 100).toFixed(0)}%)` : 'None';
                } else {
                    // For specific country, show their share of global publications in 2025
                    const global2025Val = globalData[2025][topic] || 0;
                    const country2025Val = val2025;
                    const share = global2025Val > 0 ? (country2025Val / global2025Val * 100) : 0;
                    
                    footerLabel = 'Global Share (2025)';
                    footerValue = share > 0 ? `${share.toFixed(1)}%` : '0%';
                }

                // Render Insight Card
                const card = document.createElement('div');
                card.className = 'insight-card';
                card.innerHTML = `
                    <div class="card-top">
                        <div class="card-title">${topic}</div>
                        <div class="subfield-pill">Subfield ${topicSubfields[topic]}</div>
                    </div>
                    <div class="card-metric">
                        <div class="metric-value">${totalPubs.toLocaleString()}</div>
                        <div class="metric-label">Total Pubs</div>
                    </div>
                    <div class="card-footer">
                        <div class="footer-item">
                            <span class="footer-label">Growth (vs 1950)</span>
                            <span class="footer-value highlight-green">${growthStr}</span>
                        </div>
                        <div class="footer-item">
                            <span class="footer-label">${footerLabel}</span>
                            <span class="footer-value" title="${footerValue}">${footerValue}</span>
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
            if (currentYear > 2025) {
                currentYear = 1950;
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
                currentYear = 1950;
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
        <div style="color:#f43f5e; font-size:0.8rem; text-transform:uppercase; letter-spacing:1px;">Avg Domestic (Citations)</div>
        <div style="color:#fff; font-size:1.5rem; font-weight:800;">${avgDom.toFixed(1)}</div>
      </div>
      <div style="text-align:center;">
        <div style="color:#10b981; font-size:0.8rem; text-transform:uppercase; letter-spacing:1px;">Avg Int'l (Citations)</div>
        <div style="color:#fff; font-size:1.5rem; font-weight:800;">${avgInt.toFixed(1)}</div>
      </div>
      <div style="text-align:center;">
        <div style="color:#38bdf8; font-size:0.8rem; text-transform:uppercase; letter-spacing:1px;">Avg Premium</div>
        <div style="color:#fff; font-size:1.5rem; font-weight:800;">+${avgGain.toFixed(1)}</div>
      </div>
    </div>
    <div style="display:flex; flex-direction:column; gap: 8px; background: rgba(15,23,42,0.5); padding: 10px 15px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.1);">
      <div style="display:flex; align-items:center;">
        <div style="width:12px; height:12px; border-radius:50%; background:#f43f5e; border:1.5px solid #fff; margin-right:10px;"></div>
        <span style="color:#e2e8f0; font-size:0.85rem; font-weight:600;">Domestic (Citations/Paper)</span>
      </div>
      <div style="display:flex; align-items:center;">
        <div style="width:12px; height:12px; border-radius:50%; background:#10b981; border:1.5px solid #fff; margin-right:10px;"></div>
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
    
    <div>
        <div style="color:#f43f5e; font-size:0.85rem; font-weight:700; text-transform:uppercase; margin-bottom:5px;">Domestic Impact</div>
        <div style="color:#94a3b8; font-size:0.85rem; line-height:1.4;">The average number of citations received by research papers authored exclusively by researchers from within this specific country or region. It serves as a baseline for measuring local research influence.</div>
    </div>
    
    <div>
        <div style="color:#10b981; font-size:0.85rem; font-weight:700; text-transform:uppercase; margin-bottom:5px;">Int'l Collab Impact</div>
        <div style="color:#94a3b8; font-size:0.85rem; line-height:1.4;">The average number of citations received by research papers co-authored with at least one researcher from a different country. This usually represents research with a broader global reach.</div>
    </div>
    
    <div>
        <div style="color:#38bdf8; font-size:0.85rem; font-weight:700; text-transform:uppercase; margin-bottom:5px;">Collaboration Premium</div>
        <div style="color:#94a3b8; font-size:0.85rem; line-height:1.4;">The absolute difference (gain) in citations between internationally co-authored papers and purely domestic papers. A higher premium indicates that cross-border teamwork yields significantly more scientific attention.</div>
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
    .text(`The Collaboration Premium: Citation Gap (Citations per Paper)`);

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
        <span style="color:#f43f5e; font-weight:600; font-size:12px;">Domestic:</span>
        <span style="color:#fff; font-weight:700; font-size:13px;">${d.domestic.toFixed(1)} citations</span>
      </div>
      <div style="display:flex; justify-content:space-between; margin-bottom:8px;">
        <span style="color:#10b981; font-weight:600; font-size:12px;">Int'l Collab:</span>
        <span style="color:#fff; font-weight:700; font-size:13px;">${d.international.toFixed(1)} citations</span>
      </div>
      <div style="display:flex; justify-content:space-between; border-top:1px dashed rgba(255,255,255,0.2); padding-top:8px; margin-bottom: ${d.isRegionAgg ? '8px' : '0'};">
        <span style="color:#38bdf8; font-weight:800; font-size:13px;">Premium:</span>
        <span style="color:#38bdf8; font-weight:800; font-size:14px;">+${d.gain.toFixed(1)}</span>
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
      .attr("fill","#f43f5e").attr("stroke","#fff").attr("stroke-width",1.5)
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
      .attr("fill","#10b981").attr("stroke","#fff").attr("stroke-width",1.5)
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
    .attr("stroke", "rgba(168,85,247,0.3)")
    .attr("stroke-width", d => Math.sqrt(d.weight)/2);
  const rSc = d3.scaleSqrt().domain([0, 10000]).range([3, 25]);
  const tierColors = { "Premier":"#f43f5e", "Central / State":"#22d3ee", "Affiliated / Private":"#f59e0b" };
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
          <span>${partner.name}</span> <span style="color:#22d3ee; font-weight:bold;">${l.weight}</span>
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
