export function getPantheon(): PantheonBootstrap {
  if (typeof window !== "undefined" && window.__PANTHEON__) {
    return window.__PANTHEON__;
  }
  // Local Vite preview fallback (not used inside Hub).
  return {
    instanceId: "local-dev",
    hubBaseUrl: "http://127.0.0.1:8787",
    hubPort: 8787,
    proxyBasePath: "",
    mfeSession: "",
  };
}

export async function agentFetch(path: string, init: RequestInit = {}): Promise<Response> {
  const cfg = getPantheon();
  const headers = new Headers(init.headers);
  if (cfg.mfeSession) {
    headers.set("X-Pantheon-Mfe-Session", cfg.mfeSession);
  }
  // Outside Hub (local vite + direct API), attach proxy secret for non-health routes.
  if (!cfg.proxyBasePath) {
    headers.set("x-pantheon-proxy-secret", "dev-proxy-secret");
  }
  const base = cfg.proxyBasePath || cfg.hubBaseUrl;
  const url = `${base.replace(/\/$/, "")}${path.startsWith("/") ? path : `/${path}`}`;
  return fetch(url, { ...init, headers });
}
