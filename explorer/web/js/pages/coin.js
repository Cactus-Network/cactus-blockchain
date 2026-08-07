import { apiGet, takeStash } from "../api.js";
import { el, fmtCac, fmtInt, absTime, truncHash } from "../format.js";
import { coinTable, kvList, copyable } from "../components.js";

export async function render(main, coinId) {
  if (!coinId) {
    location.hash = "#/";
    return;
  }
  main.append(el("div", { class: "loading" }, "Loading…"));

  const c = takeStash("coin", coinId) || (await apiGet(`/coin/${encodeURIComponent(coinId)}`));

  const pieces = [
    el("h1", {}, "Coin"),
    el(
      "div",
      { class: "card" },
      kvList([
        ["Coin id", copyable(c.coin_name, c.coin_name)],
        ["Address", el("a", { href: `#/address/${c.address}`, class: "hash" }, c.address)],
        ["Amount", fmtCac(c.amount)],
        ["Type", c.coinbase ? "farming reward (coinbase)" : "transaction output"],
        [
          "Confirmed",
          el("a", { href: `#/block/${c.confirmed_height}` }, `block ${fmtInt(c.confirmed_height)}`),
        ],
        [
          "Status",
          c.spent
            ? el("a", { href: `#/block/${c.spent_height}` }, `spent at block ${fmtInt(c.spent_height)}`)
            : "unspent",
        ],
        ["Timestamp", c.timestamp != null ? absTime(c.timestamp) : "—"],
        [
          "Parent coin",
          el("a", { href: `#/coin/${c.parent_coin_name}`, class: "hash" }, truncHash(c.parent_coin_name, 10)),
        ],
      ])
    ),
  ];

  if (c.children && c.children.length) {
    pieces.push(el("h2", {}, `Children (${c.children.length})`), el("div", { class: "card" }, coinTable(c.children)));
  }

  if (c.spend) {
    pieces.push(
      el("h2", {}, "Spend"),
      el(
        "div",
        { class: "card" },
        kvList([
          ["Spent at height", fmtInt(c.spend.height)],
          ["Puzzle reveal", el("span", { class: "hash", style: "font-size:12px" }, c.spend.puzzle_reveal || "—")],
          ["Solution", el("span", { class: "hash", style: "font-size:12px" }, c.spend.solution || "—")],
        ])
      )
    );
  }

  main.replaceChildren(...pieces);
}
