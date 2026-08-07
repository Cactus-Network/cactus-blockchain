import { apiGet, ApiError, stash } from "./api.js";
import { fmtInt } from "./format.js";
import * as dashboard from "./pages/dashboard.js";
import * as blocksPage from "./pages/blocks.js";
import * as blockPage from "./pages/block.js";
import * as addressPage from "./pages/address.js";
import * as coinPage from "./pages/coin.js";
import * as chartsPage from "./pages/charts.js";
import * as peersPage from "./pages/peers.js";

const main = document.getElementById("main");

const routes = {
  dashboard: dashboard.render,
  blocks: blocksPage.render,
  block: blockPage.render,
  address: addressPage.render,
  coin: coinPage.render,
  charts: chartsPage.render,
  peers: peersPage.render,
};

function parseHash() {
  const h = location.hash.replace(/^#\/?/, "");
  if (!h) return { page: "dashboard", arg: null };
  const [head, ...rest] = h.split("/");
  const arg = rest.length ? decodeURIComponent(rest.join("/")) : null;
  if (head in routes) return { page: head, arg };
  return { page: "dashboard", arg: null };
}

let cleanup = null;

async function render() {
  const { page, arg } = parseHash();
  if (cleanup) {
    cleanup();
    cleanup = null;
  }
  document.querySelectorAll(".site-nav a").forEach((a) => {
    a.classList.toggle("active", a.dataset.nav === page);
  });
  main.replaceChildren();
  window.scrollTo(0, 0);
  try {
    cleanup = (await routes[page](main, arg)) || null;
  } catch (err) {
    const box = document.createElement("div");
    box.className = "error-box";
    box.textContent =
      err instanceof ApiError && err.status === 404
        ? `Not found: ${err.message}`
        : `Error: ${err.message}`;
    main.replaceChildren(box);
  }
}

window.addEventListener("hashchange", render);

// ------------------------------------------------------------- theme toggle

const toggle = document.getElementById("theme-toggle");
toggle.addEventListener("click", () => {
  const root = document.documentElement;
  const dark = root.dataset.theme
    ? root.dataset.theme === "dark"
    : matchMedia("(prefers-color-scheme: dark)").matches;
  root.dataset.theme = dark ? "light" : "dark";
  localStorage.setItem("theme", root.dataset.theme);
  window.dispatchEvent(new Event("themechange"));
});

// ------------------------------------------------------------- search

const form = document.getElementById("search-form");
const input = document.getElementById("search-input");
const errBox = document.getElementById("search-error");

form.addEventListener("submit", async (ev) => {
  ev.preventDefault();
  const q = input.value.trim();
  if (!q) return;
  errBox.hidden = true;
  try {
    const res = await apiGet(`/search?q=${encodeURIComponent(q)}`);
    const ident =
      res.kind === "block"
        ? String(res.result.height)
        : res.kind === "address"
          ? res.result.address
          : res.result.coin_name;
    stash(res.kind, ident, res.result);
    input.value = "";
    location.hash = `#/${res.kind}/${ident}`;
  } catch (err) {
    errBox.textContent = `No match for “${q}”${err.message ? ` — ${err.message}` : ""}`;
    errBox.hidden = false;
  }
});

// ------------------------------------------------------------- sync banner

const banner = document.getElementById("sync-banner");

async function refreshBanner() {
  try {
    const s = await apiGet("/stats");
    const nodePeak = s.node && s.node.peak_height;
    const tail = s.index.tail_height ?? s.index.tip_height;
    const showLag = nodePeak != null && tail != null && tail < nodePeak - 5;
    const nodeSyncing = s.node && s.node.synced === false;
    if (showLag || nodeSyncing) {
      const parts = [];
      if (nodeSyncing && s.node.sync_tip_height) {
        parts.push(
          `node syncing ${fmtInt(s.node.sync_progress_height)} / ${fmtInt(s.node.sync_tip_height)}`
        );
      }
      if (tail != null && nodePeak != null) {
        parts.push(`index at ${fmtInt(tail)} of ${fmtInt(nodePeak)}`);
      }
      banner.textContent = `⏳ Catching up — ${parts.join(", ")}. Recent data may be incomplete.`;
      banner.hidden = false;
    } else {
      banner.hidden = true;
    }
  } catch {
    /* banner is best-effort */
  }
}

refreshBanner();
setInterval(() => {
  if (!document.hidden) refreshBanner();
}, 30000);

render();
