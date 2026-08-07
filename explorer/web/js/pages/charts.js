import { apiGet } from "../api.js";
import { el, fmtBytes, fmtCac, fmtInt } from "../format.js";
import { makeChart } from "../charts.js";

const RANGES = [
  { label: "30 d", days: 30 },
  { label: "90 d", days: 90 },
  { label: "1 y", days: 365 },
  { label: "All", days: 0 },
];

function chartCard(title, sub) {
  const slot = el("div", { class: "chart-slot" });
  const card = el(
    "div",
    { class: "chart-card" },
    el("h3", {}, title),
    el("div", { class: "chart-sub" }, sub),
    slot
  );
  return { card, slot };
}

export async function render(main) {
  main.append(el("div", { class: "loading" }, "Loading…"));

  const destroys = [];
  let currentDays = 365;

  const picker = el("div", { class: "range-picker" });
  const net = chartCard("Netspace", "estimated network space, daily");
  const blk = chartCard("Blocks per day", "all blocks, from height deltas at day boundaries");
  const fee = chartCard("Fees per day", "total transaction fees");

  async function draw(days) {
    currentDays = days;
    picker.querySelectorAll("button").forEach((b) => b.classList.toggle("active", Number(b.dataset.days) === days));
    while (destroys.length) destroys.pop()();

    const c = await apiGet(`/charts?days=${days}`);
    if (c.days.length < 2) {
      net.slot.replaceChildren(el("div", { class: "muted", style: "padding:24px 0" }, "Not enough indexed history yet — check back once the backfill has progressed."));
      blk.slot.replaceChildren();
      fee.slot.replaceChildren();
      return;
    }

    // fees arrive in mojo strings; CAC floats are fine for plotting.
    const feesCac = c.fees_mojo.map((m) => Number(m) / 1e12);

    destroys.push(
      makeChart(net.slot, {
        data: [c.days, c.netspace_bytes.map(Number)],
        kind: "line",
        area: true,
        axisWidth: 92,
        fmtValue: (v) => fmtBytes(v),
        fmtTick: (v) => fmtBytes(v),
      }),
      makeChart(blk.slot, {
        data: [c.days, c.blocks],
        kind: "bars",
        fmtValue: (v) => `${fmtInt(v)} blocks`,
        fmtTick: (v) => fmtInt(v),
      }),
      makeChart(fee.slot, {
        data: [c.days, feesCac],
        kind: "bars",
        fmtValue: (v) => fmtCac({ cactus: v.toFixed(3) }),
        fmtTick: (v) => String(v),
      })
    );
  }

  for (const r of RANGES) {
    picker.append(
      el("button", { "data-days": String(r.days), onclick: () => draw(r.days).catch(() => {}) }, r.label)
    );
  }

  main.replaceChildren(el("h1", {}, "Charts"), picker, net.card, blk.card, fee.card);
  await draw(currentDays);

  return () => {
    while (destroys.length) destroys.pop()();
  };
}
