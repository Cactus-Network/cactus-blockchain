// uPlot factory with theme-aware chrome and a crosshair tooltip.
// All explorer charts are single series — no legend (the card title names the
// series); the accent hue carries the mark, grid/axes stay recessive.

function themeVars() {
  const cs = getComputedStyle(document.documentElement);
  return {
    accent: cs.getPropertyValue("--accent").trim(),
    accentFill: cs.getPropertyValue("--accent-fill").trim(),
    grid: cs.getPropertyValue("--grid").trim(),
    baseline: cs.getPropertyValue("--baseline").trim(),
    muted: cs.getPropertyValue("--muted").trim(),
  };
}

function fmtDay(ts) {
  return new Date(ts * 1000).toLocaleDateString(undefined, {
    year: "numeric",
    month: "short",
    day: "numeric",
  });
}

// Crosshair tooltip: value leads (strong), date follows (secondary).
function tooltipPlugin(fmtValue) {
  let tt;
  return {
    hooks: {
      init(u) {
        tt = document.createElement("div");
        tt.className = "chart-tooltip";
        tt.style.display = "none";
        u.over.appendChild(tt);
        u.over.addEventListener("mouseleave", () => (tt.style.display = "none"));
      },
      setCursor(u) {
        const { idx, left, top } = u.cursor;
        if (idx == null || left < 0) {
          tt.style.display = "none";
          return;
        }
        const x = u.data[0][idx];
        const y = u.data[1][idx];
        if (y == null) {
          tt.style.display = "none";
          return;
        }
        tt.replaceChildren();
        const v = document.createElement("div");
        v.className = "tt-value";
        v.textContent = fmtValue(y);
        const l = document.createElement("div");
        l.className = "tt-label";
        l.textContent = fmtDay(x);
        tt.append(v, l);
        tt.style.display = "block";
        const rect = u.over.getBoundingClientRect();
        const w = tt.offsetWidth;
        tt.style.left = `${Math.min(left + 12, rect.width - w - 4)}px`;
        tt.style.top = `${Math.max(top - 40, 0)}px`;
      },
    },
  };
}

/**
 * Render a single-series chart into `slot`.
 * kind: "line" (2px stroke, optional low-alpha area) or "bars" (columns).
 * Returns a destroy() function; charts re-instantiate on theme change
 * (uPlot takes colors at init).
 */
export function makeChart(slot, { data, kind = "line", height = 260, area = false, fmtValue, fmtTick, axisWidth = 64 }) {
  let plot = null;

  function build() {
    const t = themeVars();
    const series1 = {
      stroke: t.accent,
      width: 2,
      points: { show: false },
    };
    if (kind === "bars") {
      series1.paths = uPlot.paths.bars({ size: [0.7, 100], align: 0 });
      series1.fill = t.accent;
      series1.width = 0;
    } else if (area) {
      series1.fill = t.accentFill;
    }

    const axisChrome = {
      stroke: t.muted,
      grid: { stroke: t.grid, width: 1 },
      ticks: { stroke: t.baseline, width: 1, size: 4 },
      font: "12px system-ui, sans-serif",
    };

    plot = new uPlot(
      {
        width: slot.clientWidth,
        height,
        cursor: { y: false, points: { show: false } },
        select: { show: false },
        scales: { x: { time: true } },
        axes: [
          { ...axisChrome },
          { ...axisChrome, size: axisWidth, values: (u, vals) => vals.map(fmtTick || ((v) => v)) },
        ],
        series: [{}, series1],
        plugins: [tooltipPlugin(fmtValue || ((v) => String(v)))],
      },
      data,
      slot
    );
  }

  build();

  const ro = new ResizeObserver(() => {
    if (plot && slot.clientWidth > 0) plot.setSize({ width: slot.clientWidth, height });
  });
  ro.observe(slot);

  const onTheme = () => {
    if (!plot) return;
    const d = plot.data;
    plot.destroy();
    plot = null;
    build();
    plot.setData(d);
  };
  window.addEventListener("themechange", onTheme);

  return () => {
    ro.disconnect();
    window.removeEventListener("themechange", onTheme);
    if (plot) plot.destroy();
    plot = null;
  };
}

// 12-point-ish stat-tile sparkline: no axes, no cursor — trend only.
export function makeSparkline(slot, xs, ys, height = 36) {
  const t = themeVars();
  const plot = new uPlot(
    {
      width: slot.clientWidth || 180,
      height,
      cursor: { show: false },
      select: { show: false },
      legend: { show: false },
      scales: { x: { time: false } },
      axes: [{ show: false }, { show: false }],
      series: [{}, { stroke: t.accent, width: 1.5, points: { show: false }, fill: t.accentFill }],
    },
    [xs, ys],
    slot
  );
  return () => plot.destroy();
}
