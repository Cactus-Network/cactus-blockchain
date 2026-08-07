// Formatting helpers.  Amounts arrive from the API as strings ({mojo, cactus})
// because mojo values exceed 2^53 — never Number() a mojo string.

export function fmtInt(n) {
  return Number(n).toLocaleString("en-US");
}

// Thousands-separate the integer part of a decimal string with string ops.
function fmtDecimal(s, suffix) {
  const [whole, frac] = s.split(".");
  const sep = whole.replace(/\B(?=(\d{3})+(?!\d))/g, ",");
  return (frac ? `${sep}.${frac}` : sep) + suffix;
}

export function fmtCac(amountObj, suffix = " CAC") {
  return amountObj ? fmtDecimal(amountObj.cactus, suffix) : "—";
}

// CAT amounts ({mojo, tokens}, 3 decimals) — e.g. an address page's FavCoins.
export function fmtTokens(amountObj, suffix = "") {
  return amountObj ? fmtDecimal(amountObj.tokens, suffix) : "—";
}

const BYTE_UNITS = ["B", "KiB", "MiB", "GiB", "TiB", "PiB", "EiB"];

// Precision loss converting a >2^53 string to Number is acceptable here:
// display/plotting only, never arithmetic that goes back to the chain.
export function fmtBytes(bytesStr) {
  let v = Number(bytesStr);
  if (v === 0) return "0";
  if (!isFinite(v) || v < 0) return "—";
  let u = 0;
  while (v >= 1024 && u < BYTE_UNITS.length - 1) {
    v /= 1024;
    u += 1;
  }
  return `${v.toFixed(2)} ${BYTE_UNITS[u]}`;
}

export function relTime(ts) {
  if (ts == null) return "—";
  const secs = Math.floor(Date.now() / 1000 - ts);
  if (secs < 5) return "just now";
  if (secs < 60) return `${secs} s ago`;
  if (secs < 3600) return `${Math.floor(secs / 60)} min ago`;
  if (secs < 172800) return `${Math.floor(secs / 3600)} h ago`;
  return `${Math.floor(secs / 86400)} d ago`;
}

export function absTime(ts) {
  if (ts == null) return "—";
  return new Date(ts * 1000).toLocaleString();
}

export function truncHash(h, keep = 6) {
  if (!h) return "—";
  const s = h.startsWith("0x") ? h.slice(2) : h;
  return `0x${s.slice(0, keep)}…${s.slice(-keep)}`;
}

export function truncAddr(a, keep = 8) {
  if (!a) return "—";
  return `${a.slice(0, keep + 4)}…${a.slice(-keep)}`;
}

// ------------------------------------------------------------- DOM helpers
// All dynamic values are inserted via textContent — API data is untrusted.

export function el(tag, attrs = {}, ...children) {
  const node = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) {
    if (k === "class") node.className = v;
    else if (k.startsWith("on")) node.addEventListener(k.slice(2), v);
    else node.setAttribute(k, v);
  }
  for (const child of children) {
    if (child == null) continue;
    node.append(child.nodeType ? child : document.createTextNode(String(child)));
  }
  return node;
}

// Truncated hash/address with full value in title + a copy button.
export function copyable(full, shown) {
  const btn = el(
    "button",
    {
      class: "copy",
      title: "Copy to clipboard",
      onclick: (ev) => {
        ev.preventDefault();
        navigator.clipboard && navigator.clipboard.writeText(full);
        btn.textContent = "✓";
        setTimeout(() => (btn.textContent = "⧉"), 900);
      },
    },
    "⧉"
  );
  return el("span", { class: "hash", title: full }, shown, btn);
}
