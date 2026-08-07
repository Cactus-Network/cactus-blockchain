// Thin fetch wrapper over the explorer JSON API (same-origin under /api).

export class ApiError extends Error {
  constructor(status, detail) {
    super(detail || `HTTP ${status}`);
    this.status = status;
  }
}

export async function apiGet(path) {
  const resp = await fetch(`/api${path}`, { headers: { Accept: "application/json" } });
  let body = null;
  try {
    body = await resp.json();
  } catch {
    /* non-JSON error body */
  }
  if (!resp.ok) throw new ApiError(resp.status, body && body.detail);
  return body;
}

// One-slot handoff cache: /api/search already returns the full result, so the
// page navigated to can render without refetching.
let handoff = null;

export function stash(kind, ident, data) {
  handoff = { kind, ident, data };
}

export function takeStash(kind, ident) {
  if (handoff && handoff.kind === kind && handoff.ident === ident) {
    const d = handoff.data;
    handoff = null;
    return d;
  }
  return null;
}
