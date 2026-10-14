import { queryOptions, useQuery } from "@tanstack/react-query";
import { useSyncExternalStore } from "react";

export type Category = { slug: string; name: string };
export type Product = {
  id: string; name: string; brand: string; category: string;
  price: number; oldPrice?: number; rating: number; reviews: number;
  isNew?: boolean; hasVideo?: boolean; image: string; youtubeId?: string;
  marketUrl: string; short: string[]; specs: Record<string, string>;
  pros: string[]; cons: string[];
};
export type Catalog = { updated: string; categories: Category[]; products: Product[] };

// Data is loaded at runtime from /products.json so it can be updated without rebuilding.
export const catalogQuery = queryOptions({
  queryKey: ["catalog"],
  queryFn: async (): Promise<Catalog> => {
    const base = import.meta.env.BASE_URL || "/";
    const res = await fetch(`${base}products.json`, { cache: "no-cache" });
    if (!res.ok) throw new Error("catalog");
    return res.json();
  },
  staleTime: 5 * 60_000,
});

export function useCatalog() {
  return useQuery(catalogQuery);
}

export const formatPrice = (n: number) => new Intl.NumberFormat("ru-RU").format(n) + " ₽";

// Favorites store (localStorage)
const KEY = "ts-favorites";
let favs: string[] = [];
let loaded = false;
const subs = new Set<() => void>();
function load() {
  if (loaded || typeof window === "undefined") return;
  loaded = true;
  try { favs = JSON.parse(localStorage.getItem(KEY) || "[]"); } catch { favs = []; }
}
const EMPTY: string[] = [];
export function useFavorites() {
  const list = useSyncExternalStore(
    (cb) => { load(); subs.add(cb); cb(); return () => subs.delete(cb); },
    () => { load(); return favs; },
    () => EMPTY,
  );
  const toggle = (id: string) => {
    favs = favs.includes(id) ? favs.filter((x) => x !== id) : [...favs, id];
    localStorage.setItem(KEY, JSON.stringify(favs));
    subs.forEach((s) => s());
  };
  return { list, toggle, has: (id: string) => list.includes(id) };
}
