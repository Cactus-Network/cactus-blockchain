import { apiGet, ApiError } from "../api.js";
import { el, fmtBytes, relTime } from "../format.js";
import { copyable } from "../components.js";

const REFRESH_MS = 30000;

// IPv6 literals need brackets in host:port notation.
function hostPort(p) {
  return p.host.includes(":") ? `[${p.host}]:${p.port}` : `${p.host}:${p.port}`;
}

function commandFor(p) {
  return `cactus peer -a ${hostPort(p)} full_node`;
}

function peerTable(peers) {
  const rows = peers.map((p) =>
    el(
      "tr",
      {},
      el("td", {}, el("span", { class: "hash" }, hostPort(p))),
      el("td", {}, p.connected_since != null ? relTime(p.connected_since) : "—"),
      el("td", { class: "hide-narrow" }, p.last_message_time != null ? relTime(p.last_message_time) : "—"),
      el(
        "td",
        { class: "hide-narrow num" },
        `${fmtBytes(p.bytes_read || 0)} / ${fmtBytes(p.bytes_written || 0)}`
      ),
      el("td", {}, copyable(commandFor(p), el("code", {}, commandFor(p))))
    )
  );

  return el(
    "div",
    { class: "tbl-wrap" },
    el(
      "table",
      {},
      el(
        "thead",
        {},
        el(
          "tr",
          {},
          el("th", {}, "Node"),
          el("th", {}, "Connected"),
          el("th", { class: "hide-narrow" }, "Last message"),
          el("th", { class: "hide-narrow num" }, "Received / sent"),
          el("th", {}, "Add this peer")
        )
      ),
      el("tbody", {}, ...rows)
    )
  );
}

export async function render(main) {
  main.append(el("div", { class: "loading" }, "Loading…"));

  const intro = el(
    "div",
    { class: "card" },
    el(
      "p",
      { style: "margin-top:0" },
      "These are full nodes the explorer's own node is connected to right now — live, reachable peers. ",
      "New farmers whose node is stuck looking for connections can add one manually:"
    ),
    el("p", {}, copyable("cactus peer -a <host>:<port> full_node", el("code", {}, "cactus peer -a <host>:<port> full_node"))),
    el(
      "p",
      { class: "muted", style: "margin-bottom:0" },
      "Pick any node below (longest-connected first), copy its command with ⧉, and run it on your machine. ",
      "The default mainnet port is 11444."
    )
  );

  const card = el("div", { class: "card" });
  let stopped = false;

  async function refresh() {
    const data = await apiGet("/peers");
    if (stopped) return;
    if (!data.peers.length) {
      card.replaceChildren(el("p", { class: "muted" }, "No public peers connected at the moment — try again shortly."));
      return;
    }
    card.replaceChildren(peerTable(data.peers));
  }

  try {
    await refresh();
  } catch (err) {
    if (err instanceof ApiError && err.status === 503) {
      card.replaceChildren(el("p", { class: "muted" }, "The full node is unreachable right now — peer list unavailable."));
    } else {
      throw err;
    }
  }

  main.replaceChildren(el("h1", {}, "Nodes / Peers"), intro, card);

  const timer = setInterval(() => {
    if (!document.hidden) refresh().catch(() => {});
  }, REFRESH_MS);

  return () => {
    stopped = true;
    clearInterval(timer);
  };
}
