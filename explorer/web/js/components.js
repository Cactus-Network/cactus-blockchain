// Shared table renderers (dashboard, blocks page, address page).

import { el, copyable, fmtCac, fmtInt, relTime, truncHash, truncAddr } from "./format.js";

export function blockTable(blocks, { showFarmer = true } = {}) {
  const rows = blocks.map((b) =>
    el(
      "tr",
      {},
      el("td", { class: "num" }, el("a", { href: `#/block/${b.height}` }, fmtInt(b.height))),
      el("td", {}, b.timestamp != null ? relTime(b.timestamp) : el("span", { class: "muted", title: "non-transaction block" }, "—")),
      el(
        "td",
        { class: "hide-narrow" },
        el("a", { href: `#/block/${b.header_hash}`, class: "hash", title: b.header_hash }, truncHash(b.header_hash))
      ),
      showFarmer
        ? el(
            "td",
            { class: "hide-narrow" },
            el(
              "a",
              { href: `#/address/${b.farmer_address}`, class: "hash", title: b.farmer_address },
              truncAddr(b.farmer_address)
            )
          )
        : null,
      el("td", { class: "num" }, b.fees ? fmtCac(b.fees, "") : el("span", { class: "muted" }, "—"))
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
          el("th", { class: "num" }, "Height"),
          el("th", {}, "Time"),
          el("th", { class: "hide-narrow" }, "Block hash"),
          showFarmer ? el("th", { class: "hide-narrow" }, "Farmer") : null,
          el("th", { class: "num" }, "Fees (CAC)")
        )
      ),
      el("tbody", {}, ...rows)
    )
  );
}

export function coinTable(coins, { amountHeader = "Amount (CAC)", fmtAmount = fmtCac } = {}) {
  const rows = coins.map((c) =>
    el(
      "tr",
      {},
      el(
        "td",
        {},
        el("a", { href: `#/coin/${c.coin_name}`, class: "hash", title: c.coin_name }, truncHash(c.coin_name))
      ),
      el("td", { class: "num" }, fmtAmount(c.amount, "")),
      el("td", { class: "num" }, el("a", { href: `#/block/${c.confirmed_height}` }, fmtInt(c.confirmed_height))),
      el(
        "td",
        {},
        c.spent
          ? el("a", { href: `#/block/${c.spent_height}` }, `spent @ ${fmtInt(c.spent_height)}`)
          : el("span", { class: "badge" }, "unspent")
      ),
      el("td", { class: "hide-narrow" }, c.coinbase ? el("span", { class: "badge reward" }, "⛏ reward") : "")
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
          el("th", {}, "Coin"),
          el("th", { class: "num" }, amountHeader),
          el("th", { class: "num" }, "Confirmed"),
          el("th", {}, "Status"),
          el("th", { class: "hide-narrow" }, "")
        )
      ),
      el("tbody", {}, ...rows)
    )
  );
}

export function kvList(pairs) {
  const dl = el("dl", { class: "kv" });
  for (const [label, value] of pairs) {
    if (value == null) continue;
    dl.append(el("dt", {}, label), el("dd", {}, value.nodeType ? value : String(value)));
  }
  return dl;
}

export { copyable };
