import type { Stats, Stop } from "./types";

async function getJson<T>(url: string): Promise<T> {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`Błąd ${res.status}`);
  return (await res.json()) as T;
}

export function fetchStops(q: string): Promise<Stop[]> {
  return getJson<Stop[]>(`/api/stops?q=${encodeURIComponent(q)}`);
}

export function fetchStats(stopId: number): Promise<Stats> {
  return getJson<Stats>(`/api/stops/${stopId}/stats`);
}
