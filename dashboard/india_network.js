// ============================================================
// Module 5 — India Domestic HE Network (Leaflet)
// Right detail panel · center-left focus · India-only basemap
// ============================================================

const INDIA = (() => {
  const BASE = "data/india_network/";
  const TIER_LABELS = {
    premier: "Premier",
    state_affiliated: "State & Affiliated",
  };
  const TIER_COLORS = {
    premier: "#3b82f6",
    state_affiliated: "#a855f7",
  };
  const INDIA_BOUNDS = L.latLngBounds([6.4, 68.0], [37.8, 97.8]);
  const FOCUS_X_RATIO = 0.36; // center-left of map pane (panel is on the right)
  const FOCUS_Y_RATIO = 0.48;
  const HIT_RADIUS_MULT = 2.5;
  const MIN_HIT_PX = 14;

  const cache = {
    overview: null,
    full: null,
    outline: null,
    manifest: null,
    byYear: {},
    loadPromise: null,
  };

  function fetchJson(url) {
    return fetch(url).then((res) => {
      if (!res.ok) throw new Error(`Failed to load ${url}`);
      return res.text().then((text) => JSON.parse(text.replace(/:\s*NaN/g, ": null")));
    });
  }

  function loadYearPayload(year) {
    const key = String(year);
    if (cache.byYear[key]) return Promise.resolve(cache.byYear[key]);
    const url = `${BASE}${key}_full.json`;
    return fetchJson(url)
      .then((data) => {
        cache.byYear[key] = data;
        return data;
      })
      .catch(() => {
        if (cache.full) return cache.full;
        throw new Error(`No payload for year ${year}`);
      });
  }

  function availableYears() {
    if (cache.manifest?.available_years?.length) {
      return cache.manifest.available_years.map(Number);
    }
    return [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024];
  }

  function isValidCoord(node) {
    return (
      node &&
      Number.isFinite(node.lat) &&
      Number.isFinite(node.lon) &&
      node.lat >= 6 &&
      node.lat <= 38 &&
      node.lon >= 68 &&
      node.lon <= 98
    );
  }

  function tierLabel(tier) {
    return TIER_LABELS[tier] || tier;
  }

  function ensureLoaded() {
    if (cache.overview && cache.full) return Promise.resolve(cache);
    if (!cache.loadPromise) {
      cache.loadPromise = Promise.all([
        fetchJson(`${BASE}2024_overview.json`),
        fetchJson(`${BASE}2024_full.json`),
        fetch(`${BASE}manifest.json`)
          .then((r) => (r.ok ? r.json() : null))
          .catch(() => null),
        fetch(`${BASE}india_outline.geojson`)
          .then((r) => (r.ok ? r.json() : null))
          .catch(() => null),
      ]).then(([overview, full, manifest, outline]) => {
        cache.overview = overview;
        cache.full = full;
        cache.manifest = manifest;
        cache.outline = outline;
        if (full?.year && full.year !== "all") {
          cache.byYear[String(full.year)] = full;
        }
        return cache;
      });
    }
    return cache.loadPromise;
  }

  function projectLinear(lat, lon, width, height, pad = 20) {
    const minLat = 6.5;
    const maxLat = 37.5;
    const minLon = 68.0;
    const maxLon = 97.5;
    return {
      x: pad + ((lon - minLon) / (maxLon - minLon)) * (width - 2 * pad),
      y: pad + ((maxLat - lat) / (maxLat - minLat)) * (height - 2 * pad),
    };
  }

  function filterNetwork(payload, tierFilter) {
    const nodes = payload.nodes.filter(isValidCoord);
    const filteredNodes =
      tierFilter === "All" ? nodes : nodes.filter((n) => n.tier === tierFilter);
    const ids = new Set(filteredNodes.map((n) => n.id));
    const edges = (payload.edges || []).filter(
      (e) => ids.has(e.source) && ids.has(e.target)
    );
    const nodeById = new Map(filteredNodes.map((n) => [n.id, n]));
    const hubIds = new Set(filteredNodes.filter((n) => n.is_hub).map((n) => n.id));
    return { nodes: filteredNodes, edges, nodeById, hubIds, meta: payload };
  }

  function egoSet(nodeId, edges) {
    const set = new Set([nodeId]);
    edges.forEach((e) => {
      if (e.source === nodeId) set.add(e.target);
      if (e.target === nodeId) set.add(e.source);
    });
    return set;
  }

  function markerRadius(node) {
    const works = node.total_works || 0;
    if (node.is_hub) return Math.min(14, Math.max(7, 5 + Math.sqrt(works) * 0.015));
    return Math.min(9, Math.max(4, 3 + Math.sqrt(works) * 0.008));
  }

  function hitRadius(node) {
    return Math.max(MIN_HIT_PX, markerRadius(node) * HIT_RADIUS_MULT);
  }

  function collabStats(node, net) {
    const links = net.edges.filter((e) => e.source === node.id || e.target === node.id);
    const collabTotal = links.reduce((s, l) => s + (l.weight || 0), 0);
    return { links, collabTotal };
  }

  function focusInstitutionOnMap(map, lat, lon, mapStageEl) {
    const zoom = Math.max(map.getZoom(), 6);
    map.flyTo([lat, lon], zoom, { duration: 0.65 });
    map.once("moveend", function alignFocus() {
      map.off("moveend", alignFocus);
      const pt = map.latLngToContainerPoint([lat, lon]);
      const mapW = mapStageEl.clientWidth || map.getSize().x;
      const targetX = mapW * FOCUS_X_RATIO;
      const targetY = map.getSize().y * FOCUS_Y_RATIO;
      map.panBy([pt.x - targetX, pt.y - targetY], { animate: true, duration: 0.4 });
    });
  }

  function buildDefaultPanelHtml(net) {
    const summaries = net.meta.tier_summary || [];
    const tierLines = summaries
      .map(
        (t) =>
          `<div class="india-tier-chip"><span class="dot" style="background:${TIER_COLORS[t.tier] || "#94a3b8"}"></span>` +
          `<strong>${tierLabel(t.tier)}</strong> · ${t.institution_count} inst · avg works ${Math.round(t.mean_total_works || 0).toLocaleString()}` +
          (t.mean_research_funding_cr != null ? ` · avg fund ₹${t.mean_research_funding_cr} Cr` : "") +
          `</div>`
      )
      .join("");

    const footnote =
      net.meta.quality_note ||
      "~120 research-active institutions mapped; tier averages include wider affiliated systems.";

    return `
      <h4>India Domestic HE Network</h4>
      <p class="india-panel-intro">Overview mode: hub-to-hub domestic co-publication links. Click or hover a node (generous hit area) for details. Pan and scroll to explore.</p>
      <div class="india-tier-strip india-tier-strip-panel">${tierLines}</div>
      <div class="india-lecture-callouts">
        <p><strong>Encoding</strong> — position = geography; color = tier (2 levels); node size ∝ √(publications).</p>
        <p><strong>Focus + context</strong> — click an institution to highlight its ego-network; rest dims.</p>
        <p><strong>Data note</strong> — ${net.meta.year && net.meta.year !== "all" ? `Showing co-publications for ${net.meta.year}.` : "All-years rollup."} OpenAlex cache complete for 120 institutions; NIRF funding/patents from official PDFs where available.</p>
      </div>
      <p class="india-footnote india-footnote-panel">${footnote}</p>
      <div class="india-hover-preview" id="india-hover-preview" hidden></div>
    `;
  }

  function buildDetailPanelHtml(node, net, tab, locked) {
    const { links, collabTotal } = collabStats(node, net);
    const col = TIER_COLORS[node.tier] || "#3b82f6";
    const lockLabel = locked ? "" : `<p class="india-preview-badge">Preview — click map node to lock</p>`;

    const tabs = `
      <div class="india-sidebar-tabs">
        <button type="button" class="india-tab ${tab === "publications" ? "active" : ""}" data-tab="publications">Publications</button>
        <button type="button" class="india-tab ${tab === "funding" ? "active" : ""}" data-tab="funding">Funding</button>
      </div>`;

    const zeroNote =
      collabTotal === 0
        ? `<p class="india-data-note">No domestic co-pub edge in pilot export yet — OpenAlex works fetch still in progress for most institutions.</p>`
        : "";

    if (tab === "funding") {
      const fundCr = node.research_funding_cr;
      const expCr = node.total_expenditure_cr;
      const projects = node.sponsored_projects;
      const fundYear = node.funding_academic_year || "—";
      const tierFund = (net.meta.tier_summary || []).find((t) => t.tier === node.tier);
      const tierAvg = tierFund?.mean_research_funding_cr;
      const fundStatus = node.funding_status || (fundCr != null ? "reported" : "unavailable");
      const patentStatus = node.patent_status || (node.patents_published != null ? "reported" : "unavailable");

      let fundingBlock = "";
      if (fundStatus === "unranked") {
        fundingBlock = `<p class="india-data-note">Not ranked in NIRF 2024 — no official funding submission available.</p>`;
      } else if (fundStatus === "unavailable" && fundCr == null) {
        fundingBlock = `<p class="india-data-note">Ranked in NIRF 2024 but sponsored-research amount not found in scraped PDFs.</p>`;
      } else {
        fundingBlock = `
        <div class="inst-stat-row"><span>Sponsored research received</span><strong>${fundCr != null ? "₹" + fundCr.toFixed(1) + " Cr" : "—"}</strong></div>
        <div class="inst-stat-row"><span>NIRF academic year</span><strong>${fundYear}</strong></div>
        <div class="inst-stat-row"><span>Sponsored projects (count)</span><strong>${projects != null ? projects : "—"}</strong></div>
        <div class="inst-stat-row"><span>Total expenditure</span><strong>${expCr != null ? "₹" + expCr.toFixed(1) + " Cr" : "—"}</strong></div>`;
      }

      let patentBlock = "";
      if (patentStatus === "unranked") {
        patentBlock = `<p class="india-data-note">Patents: not ranked in NIRF 2024.</p>`;
      } else if (patentStatus === "duplicate_resolved") {
        patentBlock = `<p class="india-data-note">Patent counts withheld — duplicate source row resolved (see pipeline audit).</p>`;
      } else if (patentStatus === "unavailable" || node.patents_published == null) {
        patentBlock = `<p class="india-data-note">Patents: no Innovation-category NIRF PDF on nirfindia.org for this institute.</p>`;
      } else {
        patentBlock = `
        <div class="inst-stat-row"><span>Patents published (${node.patent_calendar_year || "—"})</span><strong>${node.patents_published}</strong></div>
        <div class="inst-stat-row"><span>Patents granted</span><strong>${node.patents_granted != null ? node.patents_granted : "—"}</strong></div>`;
      }

      return `
        ${lockLabel}
        <button type="button" class="india-panel-close" aria-label="Clear selection">×</button>
        <h3 class="inst-name">${node.name}</h3>
        <span class="inst-tier" style="background:${col}33;color:${col}">${tierLabel(node.tier)}</span>
        ${tabs}
        ${fundingBlock}
        <div class="inst-stat-row"><span>NIRF rank (Overall)</span><strong>${node.nirf_rank != null ? "#" + node.nirf_rank : "—"}</strong></div>
        ${patentBlock}
        ${tierAvg != null ? `<p class="india-funding-note">${tierLabel(node.tier)} tier avg sponsored research: <strong>₹${tierAvg.toFixed(1)} Cr</strong> (institutions with NIRF submissions only).</p>` : ""}
        <p class="india-funding-note">Source: official NIRF PDFs on nirfindia.org (free). Not all HEIs file detailed returns.</p>
      `;
    }

    return `
      ${lockLabel}
      <button type="button" class="india-panel-close" aria-label="Clear selection">×</button>
      <h3 class="inst-name">${node.name}</h3>
      <span class="inst-tier" style="background:${col}33;color:${col}">${tierLabel(node.tier)}</span>
      ${tabs}
      <div class="inst-stat-row"><span>OpenAlex works (2015–24)</span><strong>${(node.total_works || 0).toLocaleString()}</strong></div>
      <div class="inst-stat-row"><span>SCImago impact (${node.scimago_year || "—"})</span><strong>${node.scimago_pct != null ? node.scimago_pct + "%" : "—"}</strong></div>
      <div class="inst-stat-row"><span>Domestic co-pubs (pilot)</span><strong>${collabTotal || "—"}</strong></div>
      ${zeroNote}
      <ul class="india-partner-list">
        ${links
          .sort((a, b) => (b.weight || 0) - (a.weight || 0))
          .slice(0, 10)
          .map((l) => {
            const pid = l.source === node.id ? l.target : l.source;
            const partner = net.nodeById.get(pid);
            if (!partner) return "";
            return `<li><span>${partner.name}</span><strong>${l.weight || 0}</strong></li>`;
          })
          .join("") || "<li class='india-search-empty'>No partners in pilot edge set</li>"}
      </ul>
    `;
  }

  function drawCardPreview(canvasId) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;
    ensureLoaded()
      .then(() => {
        const ctx = canvas.getContext("2d");
        canvas.width = canvas.offsetWidth || 400;
        canvas.height = canvas.offsetHeight || 220;
        const w = canvas.width;
        const h = canvas.height;
        ctx.fillStyle = "#0f172a";
        ctx.fillRect(0, 0, w, h);
        const hubs = cache.overview.nodes.filter((n) => n.is_hub && isValidCoord(n));
        const hubIds = new Set(hubs.map((n) => n.id));
        const hubEdges = (cache.overview.edges || []).filter(
          (e) => hubIds.has(e.source) && hubIds.has(e.target)
        );
        const byId = new Map(hubs.map((n) => [n.id, n]));
        hubs.forEach((n) => {
          const p = projectLinear(n.lat, n.lon, w, h);
          n._px = p.x;
          n._py = p.y;
        });
        hubEdges.forEach((e) => {
          const s = byId.get(e.source);
          const t = byId.get(e.target);
          if (!s || !t) return;
          ctx.beginPath();
          ctx.moveTo(s._px, s._py);
          ctx.lineTo(t._px, t._py);
          ctx.strokeStyle = "rgba(168,85,247,0.45)";
          ctx.lineWidth = Math.max(1, Math.sqrt(e.weight || 1) * 0.4);
          ctx.stroke();
        });
        hubs.forEach((n) => {
          ctx.beginPath();
          ctx.arc(n._px, n._py, 5, 0, Math.PI * 2);
          ctx.fillStyle = TIER_COLORS[n.tier] || "#3b82f6";
          ctx.fill();
        });
      })
      .catch(() => {});
  }

  function render(body, options) {
    const {
      tierFilter = "All",
      selectedNodeId = null,
      displayYear = null,
      onSelect,
      onYearChange,
    } = options;
    let activeYear = displayYear;
    let net = filterNetwork(cache.full, tierFilter);

    body.innerHTML = "";
    body.classList.add("india-fullbleed");

    const layout = document.createElement("div");
    layout.className = "india-map-layout";

    const mapStage = document.createElement("div");
    mapStage.className = "india-map-stage";

    const mapEl = document.createElement("div");
    mapEl.className = "india-leaflet-map";

    const searchWrap = document.createElement("div");
    searchWrap.className = "india-map-search";
    searchWrap.innerHTML = `
      <input type="search" class="india-search-input" placeholder="Search university…" autocomplete="off" />
      <div class="india-search-results" hidden></div>
    `;

    const toolbar = document.createElement("div");
    toolbar.className = "india-map-toolbar";
    toolbar.innerHTML = `
      <button type="button" class="india-tool-btn" data-action="reset" title="Reset view">⌂ India</button>
    `;

    const sidePanel = document.createElement("aside");
    sidePanel.className = "india-detail-panel";
    sidePanel.innerHTML = buildDefaultPanelHtml(net);

    mapStage.append(mapEl, searchWrap, toolbar);
    layout.append(mapStage, sidePanel);
    body.appendChild(layout);

    const map = L.map(mapEl, {
      zoomControl: false,
      minZoom: 4,
      maxZoom: 14,
      maxBounds: INDIA_BOUNDS.pad(0.05),
      maxBoundsViscosity: 0.85,
    });

    L.tileLayer("https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png", {
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OSM</a> &copy; CARTO',
      subdomains: "abcd",
      maxZoom: 19,
    }).addTo(map);

    L.control.zoom({ position: "bottomright" }).addTo(map);

    if (cache.outline) {
      L.geoJSON(cache.outline, {
        interactive: false,
        style: {
          color: "#64748b",
          weight: 1.2,
          fillColor: "#334155",
          fillOpacity: 0.08,
        },
      }).addTo(map);
    }

    const edgeLayer = L.layerGroup().addTo(map);
    const markerLayer = L.layerGroup().addTo(map);
    const hitLayer = L.layerGroup().addTo(map);
    const labelLayer = L.layerGroup().addTo(map);

    let selectedId = selectedNodeId;
    let hoverId = null;
    let panelTab = "publications";
    let locked = false;

    function visibleGraph() {
      if (selectedId) {
        const ego = egoSet(selectedId, net.edges);
        return {
          nodes: net.nodes.filter((n) => ego.has(n.id)),
          edges: net.edges.filter((e) => ego.has(e.source) && ego.has(e.target)),
        };
      }
      return {
        nodes: net.nodes,
        edges: net.edges.filter(
          (e) => net.hubIds.has(e.source) && net.hubIds.has(e.target)
        ),
      };
    }

    function wirePanel(node, isLocked) {
      sidePanel.querySelector(".india-panel-close")?.addEventListener("click", clearSelection);
      sidePanel.querySelectorAll(".india-tab").forEach((btn) => {
        btn.addEventListener("click", () => {
          panelTab = btn.dataset.tab;
          sidePanel.innerHTML = buildDetailPanelHtml(node, net, panelTab, isLocked);
          wirePanel(node, isLocked);
        });
      });
    }

    function showDefaultPanel() {
      sidePanel.innerHTML = buildDefaultPanelHtml(net);
    }

    function showHoverPanel(node) {
      if (locked) return;
      sidePanel.innerHTML = buildDetailPanelHtml(node, net, panelTab, false);
      wirePanel(node, false);
    }

    function showLockedPanel(node) {
      sidePanel.innerHTML = buildDetailPanelHtml(node, net, panelTab, true);
      wirePanel(node, true);
    }

    const markerMeta = new Map();

    function drawNetwork(fullRedraw = true) {
      if (fullRedraw) {
        edgeLayer.clearLayers();
        markerLayer.clearLayers();
        hitLayer.clearLayers();
        labelLayer.clearLayers();
        markerMeta.clear();
      }

      const { nodes: visNodes, edges: visEdges } = visibleGraph();

      if (fullRedraw) {
        visEdges.forEach((e) => {
          const a = net.nodeById.get(e.source);
          const b = net.nodeById.get(e.target);
          if (!a || !b) return;
          L.polyline(
            [
              [a.lat, a.lon],
              [b.lat, b.lon],
            ],
            {
              color: "#c084fc",
              weight: Math.max(1.5, Math.sqrt(e.weight || 1) * 0.55),
              opacity: 0.85,
            }
          ).addTo(edgeLayer);
        });

        visNodes.forEach((node) => {
          const r = markerRadius(node);
          const col = TIER_COLORS[node.tier] || node.color || "#3b82f6";
          const isSelected = node.id === selectedId;

          const vis = L.circleMarker([node.lat, node.lon], {
            radius: r,
            fillColor: col,
            color: isSelected ? "#ffffff" : "rgba(255,255,255,0.65)",
            weight: isSelected ? 3 : 1.5,
            fillOpacity: 0.9,
            opacity: 1,
            interactive: false,
          }).addTo(markerLayer);
          markerMeta.set(node.id, { layer: vis, node });

          if (node.is_hub || isSelected) {
            L.marker([node.lat, node.lon], {
              interactive: false,
              icon: L.divIcon({
                className: "india-hub-label",
                html: `<span>${node.city || node.name.split(" ").slice(-1)[0]}</span>`,
                iconSize: [0, 0],
                iconAnchor: [-8, r + 6],
              }),
            }).addTo(labelLayer);
          }

          const hit = L.circleMarker([node.lat, node.lon], {
            radius: hitRadius(node),
            fillOpacity: 0,
            opacity: 0,
            stroke: false,
            interactive: true,
            bubblingMouseEvents: false,
          });

          hit.on("mouseover", () => {
            hoverId = node.id;
            if (!locked) showHoverPanel(node);
            applyHighlight();
          });

          hit.on("mouseout", () => {
            if (hoverId === node.id) hoverId = null;
            if (!locked) showDefaultPanel();
            applyHighlight();
          });

          hit.on("click", (evt) => {
            L.DomEvent.stopPropagation(evt);
            selectNode(node);
          });

          hit.addTo(hitLayer);
        });
      }

      applyHighlight();
    }

    function applyHighlight() {
      markerMeta.forEach(({ layer, node }, nodeId) => {
        const r = markerRadius(node);
        const isSelected = nodeId === selectedId;
        const isHover = nodeId === hoverId && !locked;
        layer.setRadius(isSelected ? r + 2 : r);
        layer.setStyle({
          color: isSelected || isHover ? "#ffffff" : "rgba(255,255,255,0.65)",
          weight: isSelected ? 3 : isHover ? 2 : 1.5,
          fillOpacity: 0.9,
          opacity: 1,
        });
      });
    }

    function selectNode(node) {
      const already = selectedId === node.id;
      locked = true;
      selectedId = node.id;
      panelTab = "publications";
      drawNetwork(true);
      showLockedPanel(node);
      if (!already) {
        focusInstitutionOnMap(map, node.lat, node.lon, mapStage);
      }
      if (onSelect) onSelect(node, net);
    }

    function clearSelection() {
      locked = false;
      selectedId = null;
      hoverId = null;
      panelTab = "publications";
      showDefaultPanel();
      drawNetwork(true);
      if (onSelect) onSelect(null, net);
    }

    map.on("click", () => {
      if (locked) clearSelection();
    });

    drawNetwork(true);

    if (selectedId) {
      const node = net.nodeById.get(selectedId);
      if (node) {
        locked = true;
        showLockedPanel(node);
        requestAnimationFrame(() => focusInstitutionOnMap(map, node.lat, node.lon, mapStage));
      }
    }

    const searchInput = searchWrap.querySelector(".india-search-input");
    const searchResults = searchWrap.querySelector(".india-search-results");

    function runSearch(q) {
      const query = q.trim().toLowerCase();
      if (!query) {
        searchResults.hidden = true;
        return;
      }
      const hits = net.nodes
        .filter(
          (n) =>
            n.name.toLowerCase().includes(query) ||
            (n.city && n.city.toLowerCase().includes(query))
        )
        .slice(0, 8);
      if (!hits.length) {
        searchResults.innerHTML = `<div class="india-search-empty">No match</div>`;
        searchResults.hidden = false;
        return;
      }
      searchResults.innerHTML = hits
        .map(
          (n) =>
            `<button type="button" class="india-search-hit" data-id="${n.id}">${n.name}<span>${n.city || ""}</span></button>`
        )
        .join("");
      searchResults.hidden = false;
      searchResults.querySelectorAll(".india-search-hit").forEach((btn) => {
        btn.addEventListener("click", () => {
          const node = net.nodeById.get(btn.dataset.id);
          if (node) {
            selectNode(node);
            searchInput.value = node.name;
            searchResults.hidden = true;
          }
        });
      });
    }

    searchInput.addEventListener("input", () => runSearch(searchInput.value));
    toolbar.querySelector('[data-action="reset"]').addEventListener("click", () => {
      clearSelection();
      map.fitBounds(INDIA_BOUNDS, { padding: [28, 28], animate: true });
    });

    function fitIndia(keepView = false) {
      map.invalidateSize();
      if (!keepView && !selectedId) {
        map.fitBounds(INDIA_BOUNDS, { padding: [28, 28] });
      }
    }

    requestAnimationFrame(() => requestAnimationFrame(() => fitIndia(false)));

    const ro = typeof ResizeObserver !== "undefined" ? new ResizeObserver(() => fitIndia(true)) : null;
    ro?.observe(mapStage);

    function destroy() {
      ro?.disconnect();
      body.classList.remove("india-fullbleed");
      map.remove();
    }

    function getPayloadForView() {
      if (activeYear && cache.byYear[String(activeYear)]) {
        return cache.byYear[String(activeYear)];
      }
      return cache.full;
    }

    return {
      destroy,
      setTier(newTier) {
        const prev = selectedId;
        net = filterNetwork(getPayloadForView(), newTier);
        if (prev && !net.nodeById.has(prev)) {
          locked = false;
          selectedId = null;
          showDefaultPanel();
        } else if (prev) {
          showLockedPanel(net.nodeById.get(prev));
        }
        drawNetwork(true);
      },
      setYear(year) {
        const y = Number(year);
        if (!Number.isFinite(y)) return Promise.resolve();
        if (activeYear === y && cache.byYear[String(y)]) {
          return Promise.resolve();
        }
        return loadYearPayload(y).then((payload) => {
          activeYear = y;
          cache.full = payload;
          const prev = selectedId;
          net = filterNetwork(payload, tierFilter);
          if (prev && !net.nodeById.has(prev)) {
            locked = false;
            selectedId = null;
            showDefaultPanel();
          } else if (prev) {
            showLockedPanel(net.nodeById.get(prev));
          } else {
            showDefaultPanel();
          }
          drawNetwork(true);
          if (onYearChange) onYearChange(y);
        });
      },
      getYear() {
        return activeYear;
      },
      resize() {
        fitIndia(true);
      },
    };
  }

  return {
    ensureLoaded,
    isReady: () => Boolean(cache.overview),
    availableYears,
    drawCardPreview,
    render,
    TIER_LABELS,
    TIER_COLORS,
  };
})();
