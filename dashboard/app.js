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
  const bubbles = [
    {x:0.3,y:0.3,r:15,col:"rgba(168,85,247,0.7)"},{x:0.4,y:0.25,r:25,col:"rgba(168,85,247,0.7)"},
    {x:0.7,y:0.6,r:20,col:"rgba(34,211,238,0.6)"},{x:0.6,y:0.7,r:18,col:"rgba(34,211,238,0.6)"},
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

  // Draw 3 columns of node blocks
  const colX = [w * 0.25, w * 0.5, w * 0.75];
  const nodeW = 10;
  
  // Year columns flow path curves
  ctx.lineWidth = 1.5;
  
  // Draw some smooth ribbons connecting columns
  const flows = [
    { y1: h*0.3, y2: h*0.3, col: "rgba(56,189,248,0.3)" }, // Elite flow (blue)
    { y1: h*0.3, y2: h*0.7, col: "rgba(244,63,94,0.15)" }, // Elite -> Q4 drift
    { y1: h*0.5, y2: h*0.5, col: "rgba(148,163,184,0.25)" }, // Balanced
    { y1: h*0.7, y2: h*0.7, col: "rgba(244,63,94,0.3)" }  // Q4 dominant
  ];

  flows.forEach(f => {
    ctx.strokeStyle = f.col;
    ctx.beginPath();
    ctx.moveTo(colX[0] + nodeW, f.y1);
    ctx.bezierCurveTo((colX[0]+colX[1])/2, f.y1, (colX[0]+colX[1])/2, f.y2, colX[1], f.y2);
    ctx.stroke();
    
    ctx.beginPath();
    ctx.moveTo(colX[1] + nodeW, f.y2);
    ctx.bezierCurveTo((colX[1]+colX[2])/2, f.y2, (colX[1]+colX[2])/2, f.y2, colX[2], f.y2);
    ctx.stroke();
  });

  // Draw node blocks
  colX.forEach(x => {
    // Elite block
    ctx.fillStyle = "#38bdf8";
    ctx.fillRect(x, h * 0.22, nodeW, h * 0.16);
    // Balanced block
    ctx.fillStyle = "#94a3b8";
    ctx.fillRect(x, h * 0.44, nodeW, h * 0.12);
    // Q4 block
    ctx.fillStyle = "#f43f5e";
    ctx.fillRect(x, h * 0.62, nodeW, h * 0.22);
  });
}

function drawPreview3() {
  const c = document.getElementById("preview-3");
  const ctx = c.getContext("2d");
  c.width = c.offsetWidth; c.height = c.offsetHeight;
  const w = c.width, h = c.height;
  const bars = [0.8,0.6,0.5,0.4];
  const colors = ["#6366f1","#22d3ee","#f59e0b","#f43f5e"];
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
    const y = 30 + i*25;
    const x1 = w*0.2 + Math.random()*w*0.2;
    const x2 = w*0.6 + Math.random()*w*0.2;
    ctx.strokeStyle = "rgba(255,255,255,0.2)"; ctx.lineWidth = 2;
    ctx.beginPath(); ctx.moveTo(x1, y); ctx.lineTo(x2, y); ctx.stroke();
    ctx.fillStyle = "#f43f5e"; ctx.beginPath(); ctx.arc(x1, y, 4, 0, Math.PI*2); ctx.fill();
    ctx.fillStyle = "#10b981"; ctx.beginPath(); ctx.arc(x2, y, 4, 0, Math.PI*2); ctx.fill();
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
  hideLoading();
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
    // Get unique sorted list of all countries across all years
    const rawData = DATA.getRidgelineData() || {};
    const countriesList = Array.from(new Set(
      Object.values(rawData).flat().map(c => c.country)
    )).sort();

    const cSel = document.createElement("select");
    cSel.className = "ctrl-select";
    cSel.innerHTML = `<option value="">-- Highlight Trajectory --</option>` +
      countriesList.map(c => `<option value="${c}">${c}</option>`).join("");
    cSel.value = selectedCountryTrail || "";
    cSel.onchange = () => {
      selectedCountryTrail = cSel.value || null;
      renderViz(2);
    };
    c.append(el("span", "ctrl-label", "Highlight Country:"), cSel);
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
    c.append(el("span","ctrl-label","Order By:"), sortSel);
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
  const W = body.offsetWidth || 900, H = body.offsetHeight || 500;
  
  const iframe = document.createElement("iframe");
  iframe.src = "graph1.html";
  iframe.style.width = "100%";
  iframe.style.height = H + "px";
  iframe.style.border = "none";
  iframe.style.borderRadius = "8px"; // aesthetic touch
  
  body.appendChild(iframe);
}

// ══════════════════════════════════════════════════════════
// VIZ 2: Global Quality Shift (Beeswarm Bubble Chart)
// ══════════════════════════════════════════════════════════
let activeRegionFilter = "All";
let selectedCountryTrail = null;

function renderViz2(body) {
  const allBubbleData = DATA.getRidgelineData() || {};
  const steps = [1999, 2007, 2016, 2024];
  const categories = ["Elite", "Balanced", "Q4-Dominant"];

  const W = body.offsetWidth || 900, H = body.offsetHeight || 600;
  const m = { top: 70, right: 260, bottom: 50, left: 100 }; // Extra right margin for interactive legend
  const innerWidth = W - m.left - m.right;
  const innerHeight = H - m.top - m.bottom;

  // Clear body and append SVG
  const svg = d3.select(body).append("svg")
    .attr("width", W)
    .attr("height", H)
    .style("overflow", "visible");

  // Helper to categorize ratio
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

  const regionColors = {
    "Northern America": "#60a5fa",
    "Western Europe": "#c084fc",
    "Asiatic Region": "#f43f5e",
    "Latin America": "#fb923c",
    "Eastern Europe": "#34d399",
    "Middle East": "#fbbf24",
    "Africa": "#f472b6",
    "Pacific Region": "#2dd4bf"
  };
  const getRegionColor = r => regionColors[r] || "#64748b";

  // ── Layout Node Blocks ─────────────────────────────────────────────
  const xSc = d3.scalePoint().domain(steps).range([m.left, m.left + innerWidth]);
  const nodeWidth = 24;
  const nodeGap = 45;
  const H_col = innerHeight - 40;
  const H_nodes = H_col - 2 * nodeGap;

  const nodes = {}; // nodes[year][category] = { x, y, h, total, count, countries }

  steps.forEach(year => {
    const list = allBubbleData[year] || [];
    // Apply region filter if any
    const filteredList = list.filter(c => activeRegionFilter === "All" || c.region === activeRegionFilter);
    const totalCount = filteredList.length;

    const countriesByTier = { "Elite": [], "Balanced": [], "Q4-Dominant": [] };
    filteredList.forEach(c => {
      const tier = getTier(c.ratio);
      countriesByTier[tier].push(c);
    });

    const scale = d3.scaleLinear().domain([0, totalCount || 1]).range([0, H_nodes]);

    let currentY = m.top + 20;
    nodes[year] = {};

    categories.forEach(cat => {
      const matched = countriesByTier[cat];
      const h = scale(matched.length);
      nodes[year][cat] = {
        x: xSc(year),
        y: currentY,
        h: h,
        count: matched.length,
        countries: matched,
        total: totalCount
      };
      currentY += h + nodeGap;
    });
  });

  // ── Compute Links (Ribbons) ────────────────────────────────────────
  const links = []; // Array of { sYear, tYear, sCat, tCat, countries, value, sourceY, targetY, sourceH, targetH }

  for (let i = 0; i < steps.length - 1; i++) {
    const y1 = steps[i];
    const y2 = steps[i + 1];

    const list1 = allBubbleData[y1] || [];
    const list2 = allBubbleData[y2] || [];

    const map1 = new Map(list1.map(c => [c.country, c]));
    const map2 = new Map(list2.map(c => [c.country, c]));

    // Common countries matching filters
    const commonCountries = Array.from(map1.keys())
      .filter(name => map2.has(name))
      .filter(name => {
        const c1 = map1.get(name);
        return activeRegionFilter === "All" || c1.region === activeRegionFilter;
      });

    // Group transitions
    const transitions = {};
    commonCountries.forEach(name => {
      const c1 = map1.get(name);
      const c2 = map2.get(name);
      const t1 = getTier(c1.ratio);
      const t2 = getTier(c2.ratio);
      const key = `${t1}->${t2}`;
      if (!transitions[key]) {
        transitions[key] = [];
      }
      transitions[key].push({
        country: name,
        region: c1.region,
        total1: c1.total,
        total2: c2.total,
        ratio1: c1.ratio,
        ratio2: c2.ratio
      });
    });

    // Create link structures
    Object.entries(transitions).forEach(([key, list]) => {
      const [sCat, tCat] = key.split("->");
      links.push({
        sYear: y1,
        tYear: y2,
        sCat: sCat,
        tCat: tCat,
        countries: list,
        value: list.length
      });
    });
  }

  // ── Calculate Link Offsets (Sankey ordering to prevent crosses) ────
  const sourceOffsets = {};
  const targetOffsets = {};
  steps.forEach(year => {
    sourceOffsets[year] = { "Elite": 0, "Balanced": 0, "Q4-Dominant": 0 };
    targetOffsets[year] = { "Elite": 0, "Balanced": 0, "Q4-Dominant": 0 };
  });

  // Sort links to exit and enter nodes cleanly:
  // Outgoing links sorted by target category index (0, 1, 2)
  // Incoming links sorted by source category index (0, 1, 2)
  const categoryOrder = { "Elite": 0, "Balanced": 1, "Q4-Dominant": 2 };

  links.forEach(link => {
    const sNode = nodes[link.sYear][link.sCat];
    const tNode = nodes[link.tYear][link.tCat];

    const sScale = d3.scaleLinear().domain([0, sNode.total || 1]).range([0, H_nodes]);
    const tScale = d3.scaleLinear().domain([0, tNode.total || 1]).range([0, H_nodes]);

    link.sourceH = sScale(link.value);
    link.targetH = tScale(link.value);
  });

  // Group links by transition step to order them
  for (let i = 0; i < steps.length - 1; i++) {
    const y1 = steps[i];
    const y2 = steps[i + 1];

    const stepLinks = links.filter(l => l.sYear === y1 && l.tYear === y2);

    // Outgoing links: sorted by target category index
    categories.forEach(sCat => {
      const outgoing = stepLinks.filter(l => l.sCat === sCat)
        .sort((a, b) => categoryOrder[a.tCat] - categoryOrder[b.tCat]);

      outgoing.forEach(link => {
        link.sourceY = nodes[y1][sCat].y + sourceOffsets[y1][sCat];
        sourceOffsets[y1][sCat] += link.sourceH;
      });
    });

    // Incoming links: sorted by source category index
    categories.forEach(tCat => {
      const incoming = stepLinks.filter(l => l.tCat === tCat)
        .sort((a, b) => categoryOrder[a.sCat] - categoryOrder[b.sCat]);

      incoming.forEach(link => {
        link.targetY = nodes[y2][tCat].y + targetOffsets[y2][tCat];
        targetOffsets[y2][tCat] += link.targetH;
      });
    });
  }

  // ── Render Ribbons (Flow Links) ────────────────────────────────────
  // Path generator for horizontal Alluvial flow ribbons
  const ribbonPath = link => {
    const x1 = link.sourceX + nodeWidth;
    const x2 = link.targetX;
    const y1 = link.sourceY;
    const y2 = link.targetY;
    const h1 = link.sourceH;
    const h2 = link.targetH;

    const path = d3.path();
    const ctrlX = (x1 + x2) / 2;
    path.moveTo(x1, y1);
    path.bezierCurveTo(ctrlX, y1, ctrlX, y2, x2, y2);
    path.lineTo(x2, y2 + h2);
    path.bezierCurveTo(ctrlX, y2 + h2, ctrlX, y1 + h1, x1, y1 + h1);
    path.closePath();
    return path.toString();
  };

  // Map node coordinates back to link objects for path drawing
  links.forEach(link => {
    link.sourceX = nodes[link.sYear][link.sCat].x;
    link.targetX = nodes[link.tYear][link.tCat].x;
  });

  // Render the paths
  const ribbons = svg.selectAll(".flow-ribbon")
    .data(links)
    .enter().append("path")
      .attr("class", "flow-ribbon")
      .attr("d", ribbonPath)
      .attr("fill", d => tierColors[d.sCat])
      .attr("fill-opacity", d => {
        // If a country is selected, dim all ribbons that don't contain it
        if (selectedCountryTrail) {
          const hasCountry = d.countries.some(c => c.country === selectedCountryTrail);
          return hasCountry ? 0.75 : 0.05;
        }
        return 0.28;
      })
      .attr("stroke", d => tierColors[d.sCat])
      .attr("stroke-width", 0.5)
      .attr("stroke-opacity", d => selectedCountryTrail ? 0.8 : 0.15)
      .style("transition", "fill-opacity 0.3s ease, stroke-opacity 0.3s ease");

  // Interaction handlers for ribbons
  ribbons
    .on("mouseenter", function(e, d) {
      if (selectedCountryTrail) return; // ignore general highlights if tracking a country

      d3.select(this)
        .attr("fill-opacity", 0.65)
        .attr("stroke-opacity", 0.6);

      const countriesList = d.countries.sort((a,b) => b.total1 - a.total1);
      const topList = countriesList.slice(0, 10).map(c => 
        `<div style="display:flex; justify-content:space-between; margin:2px 0;">
          <span style="color:${getRegionColor(c.region)}; font-weight:600;">${c.country}</span>
          <span style="color:#94a3b8;">${c.ratio1.toFixed(2)} → ${c.ratio2.toFixed(2)}</span>
        </div>`
      ).join("");

      const overflow = countriesList.length > 10 ? 
        `<div style="text-align:center; font-size:10px; color:#64748b; margin-top:4px;">+ ${countriesList.length - 10} more countries</div>` : "";

      showTip(e, `
        <div style="font-size:13px; font-weight:700; border-bottom:1px solid #1e293b; padding-bottom:6px; margin-bottom:6px;">
          ${d.sYear} → ${d.tYear} Migration (${d.sCat} → ${d.tCat})
        </div>
        <div style="font-size:12px; margin-bottom:6px; color:#cbd5e1;">
          Transitioning Countries: <span style="color:#f59e0b; font-weight:700;">${d.value}</span>
        </div>
        <div style="border-top:1px dashed #1e293b; padding-top:6px; max-height:220px; overflow-y:auto; width:250px;">
          ${topList}
          ${overflow}
        </div>
      `);
    })
    .on("mousemove", moveTip)
    .on("mouseleave", function(e, d) {
      if (selectedCountryTrail) return;

      d3.select(this)
        .attr("fill-opacity", 0.28)
        .attr("stroke-opacity", 0.15);
      hideTip();
    });

  // ── Render Node Blocks ─────────────────────────────────────────────
  steps.forEach(year => {
    categories.forEach(cat => {
      const node = nodes[year][cat];
      if (node.count === 0) return;

      // Draw node block rect
      svg.append("rect")
        .attr("x", node.x)
        .attr("y", node.y)
        .attr("width", nodeWidth)
        .attr("height", node.h)
        .attr("fill", tierColors[cat])
        .attr("opacity", 0.9)
        .attr("rx", 3)
        .attr("stroke", "#0f172a")
        .attr("stroke-width", 1)
        .on("mouseover", (e) => {
          if (selectedCountryTrail) return;
          // Dim all ribbons that are not connected to this node
          svg.selectAll(".flow-ribbon")
            .attr("fill-opacity", d => {
              const connected = (d.sYear === year && d.sCat === cat) || (d.tYear === year && d.tCat === cat);
              return connected ? 0.65 : 0.05;
            });
          showTip(e, `
            <div style="font-size:13px; font-weight:700; color:#fff;">${cat} tier in ${year}</div>
            <div style="font-size:11px; color:#cbd5e1; margin-top:2px;">
              Countries: <span style="font-weight:700; color:#f59e0b;">${node.count}</span> (${((node.count/node.total)*100).toFixed(0)}% of total)
            </div>
          `);
        })
        .on("mousemove", moveTip)
        .on("mouseleave", () => {
          if (selectedCountryTrail) return;
          svg.selectAll(".flow-ribbon")
            .attr("fill-opacity", 0.28);
          hideTip();
        });

      // Draw country count text inside/on the block if height is enough
      if (node.h > 15) {
        svg.append("text")
          .attr("x", node.x + nodeWidth / 2)
          .attr("y", node.y + node.h / 2 + 4)
          .attr("text-anchor", "middle")
          .attr("fill", "#0f172a")
          .attr("font-size", "10")
          .attr("font-weight", "900")
          .attr("pointer-events", "none")
          .text(node.count);
      }
    });

    // Draw Column Year Header
    svg.append("text")
      .attr("x", xSc(year) + nodeWidth / 2)
      .attr("y", m.top - 12)
      .attr("text-anchor", "middle")
      .attr("fill", "#f8fafc")
      .attr("font-size", "14")
      .attr("font-weight", "800")
      .text(year);
  });

  // ── Trajectory Line for selected country ───────────────────────────
  if (selectedCountryTrail) {
    const history = [];
    steps.forEach(yr => {
      const list = allBubbleData[yr] || [];
      const match = list.find(c => c.country === selectedCountryTrail);
      if (match) {
        const cat = getTier(match.ratio);
        const node = nodes[yr][cat];
        // Calculate center y offset in this node
        history.push({
          x: node.x + nodeWidth / 2,
          y: node.y + node.h / 2
        });
      }
    });

    if (history.length > 1) {
      const lineGen = d3.line().x(d => d.x).y(d => d.y);
      svg.append("path")
        .datum(history)
        .attr("fill", "none")
        .attr("stroke", "#fff")
        .attr("stroke-width", 3)
        .style("filter", "drop-shadow(0px 0px 8px #6366f1)")
        .attr("d", lineGen);

      svg.selectAll(".selected-dot")
        .data(history)
        .enter().append("circle")
        .attr("cx", d => d.x)
        .attr("cy", d => d.y)
        .attr("r", 5.5)
        .attr("fill", "#fff")
        .attr("stroke", "#6366f1")
        .attr("stroke-width", 2);
    }
  }

  // ── Draw Interactive Legend (Right Hand Side) ──────────────────────
  const legX = m.left + innerWidth + 50;
  const legY = m.top + 30;
  const legend = svg.append("g").attr("class", "legend");

  legend.append("text")
    .attr("x", legX).attr("y", legY - 14)
    .attr("fill", "#e2e8f0").attr("font-size", "11").attr("font-weight", "700").attr("letter-spacing", "0.5px")
    .text("FILTER BY REGION");

  let offset = 0;
  Object.entries(regionColors).forEach(([region, color]) => {
    const row = legend.append("g")
      .attr("transform", `translate(${legX}, ${legY + offset})`)
      .style("cursor", "pointer")
      .on("click", (e) => {
        e.stopPropagation();
        activeRegionFilter = (activeRegionFilter === region) ? "All" : region;
        renderViz(2); // redraw to apply filter
      });

    const isFiltered = activeRegionFilter === region;
    const isAll = activeRegionFilter === "All";

    row.append("circle")
      .attr("cx", 6).attr("cy", 6)
      .attr("r", 6)
      .attr("fill", color)
      .attr("opacity", isFiltered || isAll ? 0.9 : 0.2);

    row.append("text")
      .attr("x", 20).attr("y", 10)
      .attr("fill", isFiltered ? "#fff" : "#94a3b8")
      .attr("font-size", "10.5")
      .attr("font-weight", isFiltered ? "700" : "400")
      .text(region);

    offset += 20;
  });

  if (activeRegionFilter !== "All") {
    legend.append("g")
      .attr("transform", `translate(${legX}, ${legY + offset + 10})`)
      .style("cursor", "pointer")
      .on("click", (e) => {
        e.stopPropagation();
        activeRegionFilter = "All";
        renderViz(2);
      })
      .append("text")
        .attr("x", 0).attr("y", 10)
        .attr("fill", "#f43f5e")
        .attr("font-size", "10")
        .attr("font-weight", "700")
        .text("❌ Clear Region Filter");
  }

  // ── Global Stats Panel at the Bottom Right ────────────────────────
  const statsY = H - m.bottom - 70;
  const statsBox = svg.append("g").attr("transform", `translate(${legX}, ${statsY})`);

  statsBox.append("rect")
    .attr("width", 170).attr("height", 80)
    .attr("rx", 6).attr("fill", "#0f172a").attr("stroke", "#1e293b").attr("stroke-width", 1);

  // Compute global summary statistics for selected year
  const yearRecords = allBubbleData[2024] || []; // default to final year summary
  const filteredRecords = yearRecords.filter(c => activeRegionFilter === "All" || c.region === activeRegionFilter);
  const globalQ1 = d3.sum(filteredRecords, d => d.q1);
  const globalQ4 = d3.sum(filteredRecords, d => d.q4);
  const globalRatio = globalQ1 / (globalQ4 || 1);

  statsBox.append("text").attr("x", 10).attr("y", 18).attr("fill", "#64748b").attr("font-size", "9").attr("font-weight", "600").text("2024 END STATE");
  statsBox.append("text").attr("x", 10).attr("y", 35).attr("fill", "#e2e8f0").attr("font-size", "11").text(`Q1 ratio: `).append("tspan").attr("fill", "#f59e0b").attr("font-weight", "700").text(globalRatio.toFixed(2));
  statsBox.append("text").attr("x", 10).attr("y", 51).attr("fill", "#94a3b8").attr("font-size", "10").text(`Q1 Docs: ${(globalQ1/1000).toFixed(0)}k`);
  statsBox.append("text").attr("x", 10).attr("y", 66).attr("fill", "#94a3b8").attr("font-size", "10").text(`Q4 Docs: ${(globalQ4/1000).toFixed(0)}k`);
}
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
            gap: 1.5rem;
        }

        .filter-group {
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
        }

        .filter-group label {
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: var(--text-muted);
            font-weight: 600;
        }

        .styled-select {
            background: rgba(25, 30, 50, 0.8);
            border: 1px solid var(--card-border);
            color: var(--text-main);
            padding: 0.8rem 1.2rem;
            border-radius: 10px;
            outline: none;
            font-size: 0.95rem;
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
            gap: 1rem;
            margin-top: 0.5rem;
        }

        .btn-control {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid var(--card-border);
            color: var(--text-main);
            width: 48px;
            height: 48px;
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

    <!-- Main Grid Content -->
    <div class="dashboard-grid">
        
        <!-- Left Panel: Controls & Bar Chart Race -->
        <div class="control-panel">
            
            <!-- Controls Card -->
            <div class="glass-card">
                <div style="display: flex; flex-direction: column; gap: 1.25rem;">
                    
                    <!-- Country Selector -->
                    <div class="filter-group">
                        <label for="countrySelect">Region / Country Filter</label>
                        <select id="countrySelect" class="styled-select">
                            <option value="GLOBAL">Global (All Countries)</option>
                        </select>
                    </div>

                    <!-- Playback Controls & Slider Row -->
                    <div style="display: flex; align-items: flex-end; gap: 1.5rem; flex-wrap: wrap;">
                        
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

// ══════════════════════════════════════════════════════════
// VIZ 4: The Collaboration Premium (Dumbbell Plot)
// ══════════════════════════════════════════════════════════
function renderViz4(body) {
  let data = DATA.getCollabData(); // Using static 2024 view to see exact premiums as requested
  if (APP.sort === "gain")          data.sort((a,b)=>b.gain-a.gain);
  else if (APP.sort === "international") data.sort((a,b)=>b.international-a.international);
  else if (APP.sort === "domestic") data.sort((a,b)=>b.domestic-a.domestic);
  else                              data.sort((a,b)=>a.name.localeCompare(b.name));

  const W = body.offsetWidth || 900, H = body.offsetHeight || 500;
  const m = { top: 60, right: 60, bottom: 40, left: 180 };
  const svg = d3.select(body).append("svg").attr("width",W).attr("height",H);

  svg.append("text").attr("x",W/2).attr("y",30).attr("text-anchor","middle")
    .attr("fill","#e2e8f0").attr("font-size","15").attr("font-weight","700")
    .text(`The Collaboration Premium: Citation Gap (Domestic vs International Co-authorship)`);

  const xSc = d3.scaleLinear().domain([0, d3.max(data,d=>d.international)*1.05]).range([m.left, W-m.right]);
  const ySc = d3.scaleBand().domain(data.map(d=>d.name)).range([m.top, H-m.bottom]).padding(0.4);

  svg.append("g").attr("transform",`translate(0,${H-m.bottom})`)
     .call(d3.axisBottom(xSc).ticks(8))
     .call(g => g.select(".domain").attr("stroke","#334155"))
     .call(g => g.selectAll("line").attr("stroke","rgba(255,255,255,0.05)").attr("y2",-(H-m.top-m.bottom)));
     
  svg.append("g").attr("transform",`translate(${m.left},0)`)
     .call(d3.axisLeft(ySc).tickSize(0))
     .call(g => g.select(".domain").remove())
     .selectAll("text").attr("font-size","12").attr("fill","#cbd5e1");

  const cy = d => ySc(d.name)+ySc.bandwidth()/2;

  // Connectors
  svg.selectAll(".con").data(data).join("line").attr("class","con")
    .attr("x1",d=>xSc(d.domestic)).attr("x2",d=>xSc(d.international))
    .attr("y1",cy).attr("y2",cy)
    .attr("stroke","rgba(255,255,255,0.15)").attr("stroke-width",3);

  // Domestic
  svg.selectAll(".dd").data(data).join("circle").attr("class","dd")
    .attr("cx",d=>xSc(d.domestic)).attr("cy",cy).attr("r",7)
    .attr("fill","#f43f5e").attr("stroke","rgba(255,255,255,0.4)").attr("stroke-width",1.5)
    .on("mouseover",(e,d)=>showTip(e,`<strong>${d.name}</strong>Domestic Citations/Paper: ${d.domestic}`))
    .on("mousemove",moveTip).on("mouseleave",hideTip);

  // International
  svg.selectAll(".di").data(data).join("circle").attr("class","di")
    .attr("cx",d=>xSc(d.international)).attr("cy",cy).attr("r",7)
    .attr("fill","#10b981").attr("stroke","rgba(255,255,255,0.4)").attr("stroke-width",1.5)
    .on("mouseover",(e,d)=>showTip(e,`<strong>${d.name}</strong>Int'l Citations/Paper: ${d.international}<br>Gain: +${d.gain}`))
    .on("mousemove",moveTip).on("mouseleave",hideTip);

  // Legend
  const leg = svg.append("g").attr("transform",`translate(${W-200},20)`);
  [["#f43f5e","Domestic Citation Impact"],["#10b981","International Co-authored Impact"]].forEach(([col,lbl],i)=>{
    leg.append("circle").attr("cx",6).attr("cy",i*20+5).attr("r",6).attr("fill",col);
    leg.append("text").attr("x",20).attr("y",i*20+10).attr("fill","#94a3b8").attr("font-size","11").text(lbl);
  });
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
