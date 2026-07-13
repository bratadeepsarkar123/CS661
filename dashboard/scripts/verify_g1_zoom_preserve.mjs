/**
 * Verify G1 user zoom survives year scrub / drawViz1Plotly.
 * Usage: node scripts/verify_g1_zoom_preserve.mjs [baseUrl]
 * Default: serves dashboard/ on an ephemeral port.
 */
import { createRequire } from 'module';
import { createServer } from 'http';
import { readFileSync, existsSync, statSync } from 'fs';
import { join, extname, dirname } from 'path';
import { fileURLToPath } from 'url';

const require = createRequire(import.meta.url);
const puppeteer = require('puppeteer');

const __dirname = dirname(fileURLToPath(import.meta.url));
const DASHBOARD_ROOT = join(__dirname, '..');
const EPS = 1e-4;

const MIME = {
  '.html': 'text/html',
  '.js': 'application/javascript',
  '.css': 'text/css',
  '.json': 'application/json',
  '.svg': 'image/svg+xml',
  '.png': 'image/png',
  '.ico': 'image/x-icon',
  '.woff2': 'font/woff2',
};

function startStaticServer(root) {
  return new Promise((resolve) => {
    const server = createServer((req, res) => {
      let urlPath = decodeURIComponent((req.url || '/').split('?')[0]);
      if (urlPath === '/') urlPath = '/index.html';
      const filePath = join(root, urlPath.replace(/^\//, ''));
      if (!filePath.startsWith(root) || !existsSync(filePath) || !statSync(filePath).isFile()) {
        res.writeHead(404);
        res.end('not found');
        return;
      }
      res.writeHead(200, { 'Content-Type': MIME[extname(filePath)] || 'application/octet-stream' });
      res.end(readFileSync(filePath));
    });
    server.listen(0, '127.0.0.1', () => {
      const { port } = server.address();
      resolve({ server, baseUrl: `http://127.0.0.1:${port}` });
    });
  });
}

function nearlyEq(a, b, eps = EPS) {
  return Math.abs(a - b) <= eps;
}

function rangesMatch(a, b, eps = EPS) {
  return a && b && nearlyEq(a[0], b[0], eps) && nearlyEq(a[1], b[1], eps);
}

async function main() {
  const argUrl = process.argv[2];
  let server = null;
  let baseUrl = argUrl;
  if (!baseUrl) {
    ({ server, baseUrl } = await startStaticServer(DASHBOARD_ROOT));
  }
  console.log('Base URL:', baseUrl);

  const browser = await puppeteer.launch({
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox'],
  });
  const page = await browser.newPage();
  page.setDefaultTimeout(60000);

  const failures = [];
  try {
    await page.goto(`${baseUrl}/index.html`, { waitUntil: 'networkidle0' });

    await page.evaluate(() => {
      if (typeof openViz === 'function') return openViz(1);
      const card = document.getElementById('card-1');
      if (card) card.click();
    });

    // Plotly puts .js-plotly-plot on the container itself (not a child).
    await page.waitForSelector('#viz1-plotly-container.js-plotly-plot', { timeout: 45000 });
    await page.waitForFunction(() => {
      const el = document.getElementById('viz1-plotly-container');
      return el && el.layout && el.layout.xaxis && el.layout.xaxis.range && el.layout.xaxis.range.length === 2;
    }, { timeout: 45000 });

    // Snapshot full-view axes, then apply a known user zoom via Plotly.relayout
    const fullAxes = await page.evaluate(() => ({
      x: document.getElementById('viz1-plotly-container').layout.xaxis.range.slice(),
      y: document.getElementById('viz1-plotly-container').layout.yaxis.range.slice(),
    }));

    const zoomX = [
      fullAxes.x[0] + (fullAxes.x[1] - fullAxes.x[0]) * 0.25,
      fullAxes.x[0] + (fullAxes.x[1] - fullAxes.x[0]) * 0.55,
    ];
    const zoomY = [
      fullAxes.y[0] + (fullAxes.y[1] - fullAxes.y[0]) * 0.30,
      fullAxes.y[0] + (fullAxes.y[1] - fullAxes.y[0]) * 0.60,
    ];

    await page.evaluate(async (zx, zy) => {
      const el = document.getElementById('viz1-plotly-container');
      await Plotly.relayout(el, {
        'xaxis.range': zx,
        'yaxis.range': zy,
        'xaxis.autorange': false,
        'yaxis.autorange': false,
      });
    }, zoomX, zoomY);

    // Allow plotly_relayout handler to store viz1UserZoom
    await page.waitForFunction(
      (zx, zy) => {
        if (typeof viz1UserZoom === 'undefined' || !viz1UserZoom) return false;
        const x = viz1UserZoom.x;
        const y = viz1UserZoom.y;
        return (
          Math.abs(x[0] - zx[0]) < 1e-4 &&
          Math.abs(x[1] - zx[1]) < 1e-4 &&
          Math.abs(y[0] - zy[0]) < 1e-4 &&
          Math.abs(y[1] - zy[1]) < 1e-4
        );
      },
      { timeout: 8000 },
      zoomX,
      zoomY
    );

    const year0 = await page.evaluate(() => parseInt(viz1Year, 10));

    // Advance year a few steps (scrub path) and assert ranges stay locked
    for (let step = 1; step <= 3; step++) {
      const nextYear = year0 + step;
      await page.evaluate(async (y) => {
        viz1Year = y;
        const slider = document.getElementById('viz1-year-slider');
        const label = document.getElementById('viz1-year-label');
        if (slider) slider.value = String(y);
        if (label) label.textContent = String(y);
        await drawViz1Plotly({ animate: false });
      }, nextYear);

      await page.waitForFunction(
        (y) => typeof viz1LastDrawnYear !== 'undefined' && viz1LastDrawnYear === y,
        { timeout: 15000 },
        nextYear
      );
      await new Promise((r) => setTimeout(r, 120));

      const after = await page.evaluate(() => {
        const el = document.getElementById('viz1-plotly-container');
        const full = el._fullLayout;
        const lay = el.layout;
        const xr = (full && full.xaxis && full.xaxis.range) || (lay && lay.xaxis && lay.xaxis.range);
        const yr = (full && full.yaxis && full.yaxis.range) || (lay && lay.yaxis && lay.yaxis.range);
        return {
          x: xr ? xr.slice() : null,
          y: yr ? yr.slice() : null,
          userZoom: viz1UserZoom ? { x: viz1UserZoom.x.slice(), y: viz1UserZoom.y.slice() } : null,
          year: viz1Year,
        };
      });

      if (!after.x || !after.y || !rangesMatch(after.x, zoomX) || !rangesMatch(after.y, zoomY)) {
        failures.push(
          `Year ${after.year}: axis ranges drifted. got x=${JSON.stringify(after.x)} y=${JSON.stringify(after.y)}; expected x=${JSON.stringify(zoomX)} y=${JSON.stringify(zoomY)}`
        );
      }
      if (!after.userZoom || !rangesMatch(after.userZoom.x, zoomX) || !rangesMatch(after.userZoom.y, zoomY)) {
        failures.push(`Year ${after.year}: viz1UserZoom not preserved: ${JSON.stringify(after.userZoom)}`);
      }
      console.log(`OK year ${after.year}: zoom locked`);
    }

    // Reset Zoom must restore full view and clear stored zoom
    await page.evaluate(() => {
      resetViz1Zoom();
    });
    await new Promise((r) => setTimeout(r, 150));
    const resetState = await page.evaluate(() => {
      const el = document.getElementById('viz1-plotly-container');
      const full = el._fullLayout;
      const lay = el.layout;
      const xr = (full && full.xaxis && full.xaxis.range) || (lay && lay.xaxis && lay.xaxis.range);
      const yr = (full && full.yaxis && full.yaxis.range) || (lay && lay.yaxis && lay.yaxis.range);
      return {
        x: xr ? xr.slice() : null,
        y: yr ? yr.slice() : null,
        userZoom: viz1UserZoom,
        isZoomed: viz1IsZoomed,
      };
    });
    if (!resetState.x || !resetState.y || !rangesMatch(resetState.x, fullAxes.x) || !rangesMatch(resetState.y, fullAxes.y)) {
      failures.push(
        `Reset Zoom did not restore full axes. got x=${JSON.stringify(resetState.x)} y=${JSON.stringify(resetState.y)}; expected x=${JSON.stringify(fullAxes.x)} y=${JSON.stringify(fullAxes.y)}`
      );
    }
    if (resetState.userZoom != null || resetState.isZoomed) {
      failures.push(`Reset Zoom left zoom state: userZoom=${JSON.stringify(resetState.userZoom)} isZoomed=${resetState.isZoomed}`);
    }
    console.log('OK reset zoom restores full view');

    // Re-lock zoom and exercise Play-style year bumps with animate:true
    await page.evaluate(async (zx, zy) => {
      const el = document.getElementById('viz1-plotly-container');
      await Plotly.relayout(el, {
        'xaxis.range': zx,
        'yaxis.range': zy,
        'xaxis.autorange': false,
        'yaxis.autorange': false,
      });
    }, zoomX, zoomY);
    await page.waitForFunction(() => !!viz1UserZoom, { timeout: 8000 });

    const playStart = await page.evaluate(() => parseInt(viz1Year, 10));
    const stabilityLog = [];
    for (let step = 1; step <= 5; step++) {
      const nextYear = playStart + step;
      // Kick animate, then sample ranges mid-lerp to catch camera thrash
      await page.evaluate((y) => {
        viz1Year = y;
        const slider = document.getElementById('viz1-year-slider');
        const label = document.getElementById('viz1-year-label');
        if (slider) slider.value = String(y);
        if (label) label.textContent = String(y);
        // fire-and-forget animate; we poll mid-flight
        drawViz1Plotly({ animate: true });
      }, nextYear);

      // Mid-lerp samples (~3 over ~300ms)
      for (let s = 0; s < 3; s++) {
        await new Promise((r) => setTimeout(r, 90));
        const mid = await page.evaluate(() => {
          const el = document.getElementById('viz1-plotly-container');
          const full = el._fullLayout;
          const lay = el.layout;
          const xr = (full && full.xaxis && full.xaxis.range) || (lay && lay.xaxis && lay.xaxis.range);
          const yr = (full && full.yaxis && full.yaxis.range) || (lay && lay.yaxis && lay.yaxis.range);
          return {
            x: xr ? xr.slice() : null,
            y: yr ? yr.slice() : null,
            year: viz1Year,
            motion: !!viz1MotionRaf,
          };
        });
        stabilityLog.push(mid);
        if (!mid.x || !mid.y || !rangesMatch(mid.x, zoomX) || !rangesMatch(mid.y, zoomY)) {
          failures.push(
            `Mid-lerp thrash year ${mid.year} sample: x=${JSON.stringify(mid.x)} y=${JSON.stringify(mid.y)} (expected locked zoom)`
          );
        }
      }

      await page.waitForFunction(
        (y) => typeof viz1LastDrawnYear !== 'undefined' && viz1LastDrawnYear === y && !viz1MotionRaf,
        { timeout: 20000 },
        nextYear
      );
      await new Promise((r) => setTimeout(r, 80));
      const after = await page.evaluate(() => {
        const el = document.getElementById('viz1-plotly-container');
        const full = el._fullLayout;
        const lay = el.layout;
        const xr = (full && full.xaxis && full.xaxis.range) || (lay && lay.xaxis && lay.xaxis.range);
        const yr = (full && full.yaxis && full.yaxis.range) || (lay && lay.yaxis && lay.yaxis.range);
        return {
          x: xr ? xr.slice() : null,
          y: yr ? yr.slice() : null,
          year: viz1Year,
        };
      });
      if (!after.x || !after.y || !rangesMatch(after.x, zoomX) || !rangesMatch(after.y, zoomY)) {
        failures.push(
          `Play-style year ${after.year}: axis ranges drifted. got x=${JSON.stringify(after.x)} y=${JSON.stringify(after.y)}`
        );
      }
      console.log(`OK animate year ${after.year}: zoom locked (identical across mid-lerp samples)`);
    }
    // All 5 year end-states + mid samples must match the same zoom box
    const first = stabilityLog[0];
    for (let i = 1; i < stabilityLog.length; i++) {
      const s = stabilityLog[i];
      if (!rangesMatch(s.x, first.x) || !rangesMatch(s.y, first.y)) {
        failures.push(
          `Range thrash across samples: sample0=${JSON.stringify(first)} sample${i}=${JSON.stringify(s)}`
        );
      }
    }
    console.log(`OK visual stability: ${stabilityLog.length} range samples identical while zoomed`);
  } finally {
    await browser.close();
    if (server) server.close();
  }

  if (failures.length) {
    console.error('\nFAIL:');
    failures.forEach((f) => console.error(' -', f));
    process.exit(1);
  }
  console.log('\nPASS: G1 user zoom preserved across year updates; Reset Zoom clears it.');
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
