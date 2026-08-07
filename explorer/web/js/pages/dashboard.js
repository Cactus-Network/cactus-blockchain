import { apiGet } from "../api.js";
import { el, fmtBytes, fmtCac, fmtInt } from "../format.js";
import { blockTable } from "../components.js";
import { makeSparkline } from "../charts.js";

const REFRESH_MS = 15000; // ~block time is 19s

function tile(label, value, sub) {
  return el(
    "div",
    { class: "tile" },
    el("div", { class: "label" }, label),
    el("div", { class: "value" }, value),
    sub ? el("div", { class: "sub" }, sub) : null
  );
}

export async function render(main) {
  main.append(el("div", { class: "loading" }, "Loading…"));

  const tiles = el("div", { class: "tiles" });
  const blocksCard = el("div", { class: "card" });
  const sparkDestroys = [];
  let stopped = false;

  async function refresh() {
    const [stats, latest] = await Promise.all([apiGet("/stats"), apiGet("/blocks?limit=15")]);
    if (stopped) return;

    const node = stats.node || {};
    while (sparkDestroys.length) sparkDestroys.pop()();
    tiles.replaceChildren();

    tiles.append(
      tile(
        "Peak height",
        node.peak_height != null ? fmtInt(node.peak_height) : stats.index.tip_height != null ? fmtInt(stats.index.tip_height) : "—",
        node.synced === false ? "node syncing" : "synced"
      )
    );

    // Netspace tile carries the 30d trend sparkline.
    const netTile = tile("Netspace", node.space_bytes ? fmtBytes(node.space_bytes) : "—", "estimated total space");
    const spark = el("div", { class: "spark" });
    netTile.append(spark);
    tiles.append(netTile);

    tiles.append(
      tile("Difficulty", node.difficulty != null ? fmtInt(node.difficulty) : "—"),
      tile("Emitted supply", fmtCac(stats.emitted_supply), "unclaimed rewards included"),
      tile("Mempool", node.mempool_size != null ? fmtInt(node.mempool_size) : "—", "pending spend bundles"),
      tile(
        "Avg block time",
        node.average_block_time != null ? `${Math.round(node.average_block_time)} s` : "—"
      )
    );

    blocksCard.replaceChildren(
      el("h2", { style: "margin-top:0" }, "Latest blocks"),
      blockTable(latest.blocks),
      el("p", {}, el("a", { href: "#/blocks" }, "All blocks →"))
    );

    // Sparkline data is cheap (cached server-side) and refreshes with the tile.
    try {
      const c = await apiGet("/charts?days=30");
      if (!stopped && c.days.length > 1) {
        sparkDestroys.push(makeSparkline(spark, c.days, c.netspace_bytes.map(Number)));
      }
    } catch {
      /* sparkline is optional */
    }
  }

  await refresh();
  main.replaceChildren(
    el("h1", {}, el("a", { class: "home-link", href: "https://www.cactus-network.net/", target: "_top" }, "🌵 Cactus blockchain")),
    tiles,
    blocksCard
  );

  const timer = setInterval(() => {
    if (!document.hidden) refresh().catch(() => {});
  }, REFRESH_MS);
  const onVis = () => {
    if (!document.hidden) refresh().catch(() => {});
  };
  document.addEventListener("visibilitychange", onVis);

  return () => {
    stopped = true;
    clearInterval(timer);
    document.removeEventListener("visibilitychange", onVis);
    while (sparkDestroys.length) sparkDestroys.pop()();
  };
}
