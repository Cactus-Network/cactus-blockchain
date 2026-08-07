import { apiGet, takeStash } from "../api.js";
import { el, fmtCac, fmtInt, absTime, relTime, truncHash } from "../format.js";
import { kvList, copyable } from "../components.js";

export async function render(main, ident) {
  if (!ident) {
    location.hash = "#/blocks";
    return;
  }
  main.append(el("div", { class: "loading" }, "Loading…"));

  const b = takeStash("block", ident) || (await apiGet(`/block/${encodeURIComponent(ident)}`));

  const ts =
    b.timestamp != null
      ? `${absTime(b.timestamp)} (${relTime(b.timestamp)})`
      : el("span", { class: "muted" }, "— (non-transaction block: no timestamp)");

  main.replaceChildren(
    el("h1", {}, `Block ${fmtInt(b.height)}`),
    el(
      "div",
      { class: "pager" },
      el("button", { onclick: () => (location.hash = `#/block/${b.height - 1}`) }, "← Prev"),
      el("button", { onclick: () => (location.hash = `#/block/${b.height + 1}`) }, "Next →")
    ),
    el(
      "div",
      { class: "card" },
      kvList([
        ["Height", fmtInt(b.height)],
        ["Header hash", copyable(b.header_hash, b.header_hash)],
        [
          "Previous block",
          el("a", { href: `#/block/${b.prev_hash}`, class: "hash" }, truncHash(b.prev_hash, 10)),
        ],
        ["Timestamp", ts],
        ["Transaction block", b.is_transaction_block ? "yes" : "no"],
        [
          "Farmer",
          el("a", { href: `#/address/${b.farmer_address}`, class: "hash" }, b.farmer_address),
        ],
        ["Pool", el("a", { href: `#/address/${b.pool_address}`, class: "hash" }, b.pool_address)],
        ["Farmer reward", fmtCac(b.farmer_reward)],
        ["Pool reward", fmtCac(b.pool_reward)],
        ["Fees", b.fees ? fmtCac(b.fees) : el("span", { class: "muted" }, "—")],
        [
          "Coins",
          b.coins
            ? `${fmtInt(b.coins.additions)} added (${fmtCac(b.coins.added_value)}), ${fmtInt(b.coins.removals)} removed`
            : null,
        ],
        ["Weight", fmtInt(b.weight)],
        ["Total iterations", fmtInt(b.total_iters)],
        ["Signage point index", b.signage_point_index],
        ["Sub-slot iterations", fmtInt(b.sub_slot_iters)],
      ])
    )
  );
}
