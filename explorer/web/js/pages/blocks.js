import { apiGet } from "../api.js";
import { el } from "../format.js";
import { blockTable } from "../components.js";

const PAGE = 50;

export async function render(main) {
  main.append(el("div", { class: "loading" }, "Loading…"));

  // Keyset paging on height: stack of "before" cursors for the newer-page path.
  const cursors = [];
  let current = null; // undefined cursor = newest

  const card = el("div", { class: "card" });
  const newer = el("button", { onclick: () => page(cursors.pop()) }, "← Newer");
  const older = el("button", {}, "Older →");
  const pager = el("div", { class: "pager" }, newer, older);

  async function page(before) {
    const qs = before != null ? `?before_height=${before}&limit=${PAGE}` : `?limit=${PAGE}`;
    const data = await apiGet(`/blocks${qs}`);
    const blocks = data.blocks;
    current = before ?? null;

    card.replaceChildren(blockTable(blocks));
    newer.disabled = current == null;
    older.disabled = blocks.length < PAGE;
    older.onclick = () => {
      cursors.push(current);
      page(blocks[blocks.length - 1].height);
    };
  }

  await page(null);
  main.replaceChildren(el("h1", {}, "Blocks"), card, pager);
}
