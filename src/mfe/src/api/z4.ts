import { agentFetch } from "../pantheon";
import { ApiError, formatHttpError } from "./errors";
import type { Goal, HomeProjection, MarketProjection } from "./types";

async function readJson<T>(res: Response): Promise<T> {
  if (!res.ok) {
    let body: unknown;
    const text = await res.text();
    try {
      body = text ? JSON.parse(text) : undefined;
    } catch {
      body = text || undefined;
    }
    const message = formatHttpError(res.status, res.url, body);
    console.error("Z4 API error", message);
    throw new ApiError(res.status, message, body);
  }
  return res.json() as Promise<T>;
}

export async function fetchHome(): Promise<HomeProjection> {
  return readJson(await agentFetch("/api/v1/home"));
}

export async function putGoal(text: string): Promise<Goal> {
  return readJson(
    await agentFetch("/api/v1/goal", {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text }),
    }),
  );
}

export async function lockComponent(componentId: number, listingId?: number): Promise<HomeProjection> {
  const qs = listingId != null ? `?listing=${listingId}` : "";
  return readJson(
    await agentFetch(`/api/v1/builds/lock/component/${componentId}${qs}`, { method: "POST" }),
  );
}

export async function lockDraft(draftId: string): Promise<HomeProjection> {
  return readJson(
    await agentFetch("/api/v1/builds/lock/draft", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ draftId }),
    }),
  );
}

export async function unlockCategory(category: string): Promise<HomeProjection> {
  return readJson(
    await agentFetch("/api/v1/builds/unlock", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ category }),
    }),
  );
}

export async function fetchMarket(q: string): Promise<MarketProjection> {
  const qs = q.trim() ? `?q=${encodeURIComponent(q.trim())}` : "";
  return readJson(await agentFetch(`/api/v1/market${qs}`));
}

export function formatPrice(cents: number, currency = "USD"): string {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: currency || "USD",
  }).format(cents / 100);
}
