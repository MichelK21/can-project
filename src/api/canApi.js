const API_BASE = import.meta.env.VITE_API_BASE_URL;

async function apiFetch(path, options = {}) {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
    ...options,
  });

  if (!res.ok) {
    const contentType = res.headers.get("content-type") || "";
    let msg = `HTTP ${res.status}`;

    if (contentType.includes("application/json")) {
      const data = await res.json().catch(() => null);
      msg = data?.detail || JSON.stringify(data) || msg;
    } else {
      const text = await res.text().catch(() => "");
      msg = text || msg;
    }

    throw new Error(msg);
  }
  if (res.status === 204) return null;

  return res.json();
}

// ===== API =====

export function seed() {
  return apiFetch("/admin/seed", { method: "POST" });
}

export function getTeams() {
  return apiFetch("/teams");
}

export function getMatches() {
  return apiFetch("/matches");
}

export function getStandings() {
  return apiFetch("/standings");
}

export function health() {
  return apiFetch("/health");
}
