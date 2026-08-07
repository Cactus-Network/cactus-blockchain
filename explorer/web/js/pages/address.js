import { apiGet, takeStash } from "../api.js";
import { el, fmtCac, fmtInt, fmtTokens } from "../format.js";
import { coinTable, kvList, copyable } from "../components.js";

const PAGE = 50;

export async function render(main, address) {
  if (!address) {
    location.hash = "#/";
    return;
  }
  main.append(el("div", { class: "loading" }, "Loading…"));

  let offset = 0;
  let data = takeStash("address", address);
  if (!data) data = await apiGet(`/address/${encodeURIComponent(address)}?limit=${PAGE}&offset=0`);

  const coinsCard = el("div", { class: "card" });
  const newer = el("button", {}, "← Newer");
  const older = el("button", {}, "Older →");
  const pager = el("div", { class: "pager" }, newer, older);

  function paint(d) {
    coinsCard.replaceChildren(coinTable(d.coins));
    newer.disabled = offset === 0;
    older.disabled = d.coins.length < PAGE;
  }

  async function page(newOffset) {
    offset = Math.max(0, newOffset);
    const d = await apiGet(`/address/${encodeURIComponent(address)}?limit=${PAGE}&offset=${offset}`);
    paint(d);
  }

  newer.addEventListener("click", () => page(offset - PAGE));
  older.addEventListener("click", () => page(offset + PAGE));

  // Known CATs (e.g. FavCoin) held by this address; empty unless it holds any.
  // Token coin lists are the 50 most recent coins, unpaged.
  const tokenSections = (data.tokens || []).flatMap((t) => [
    el("h2", {}, `${t.name} (${t.symbol})`),
    el(
      "div",
      { class: "card", style: "margin-bottom:16px" },
      kvList([
        ["Balance", fmtTokens(t.balance, ` ${t.symbol}`)],
        ["Total received", fmtTokens(t.total_received, ` ${t.symbol}`)],
        ["Coins (unspent / total)", `${fmtInt(t.unspent_count)} / ${fmtInt(t.coin_count)}`],
        ["Asset id", copyable(t.asset_id, t.asset_id)],
      ]),
      coinTable(t.coins, { amountHeader: `Amount (${t.symbol})`, fmtAmount: fmtTokens })
    ),
  ]);

  main.replaceChildren(
    el("h1", {}, "Address"),
    el(
      "div",
      { class: "card", style: "margin-bottom:16px" },
      kvList([
        ["Address", copyable(data.address, data.address)],
        ["Puzzle hash", copyable(data.puzzle_hash, data.puzzle_hash)],
        ["Balance", fmtCac(data.balance)],
        ["Total received", fmtCac(data.total_received)],
        ["Coins (unspent / total)", `${fmtInt(data.unspent_count)} / ${fmtInt(data.coin_count)}`],
        ["Reward coins", fmtInt(data.reward_coin_count)],
        ["Blocks won (farmer)", fmtInt(data.blocks_won_as_farmer)],
        ["Blocks won (pool)", fmtInt(data.blocks_won_as_pool)],
      ])
    ),
    ...tokenSections,
    el("h2", {}, "Coins"),
    coinsCard,
    pager
  );
  paint(data);
}
