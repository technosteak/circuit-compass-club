import { createFileRoute, Link } from "@tanstack/react-router";
import { useMemo, useState } from "react";
import { SlidersHorizontal } from "lucide-react";
import { CATS, Grid, GridSkeleton, useProducts } from "@/components/site";

export const Route = createFileRoute("/category/$slug")({
  head: ({ params }) => {
    const name = CATS.find((c) => c.slug === params.slug)?.name ?? "Каталог";
    return {
      meta: [
        { title: `${name} — обзоры и цены | ТехноСтейк` },
        { name: "description", content: `${name}: рейтинги, характеристики и видеообзоры. Выбирайте лучшее на ТехноСтейк.` },
        { property: "og:title", content: `${name} | ТехноСтейк` },
        { property: "og:description", content: `Подборка: ${name.toLowerCase()} с обзорами и ценами.` },
      ],
    };
  },
  component: CategoryPage,
});

function CategoryPage() {
  const { slug } = Route.useParams();
  const cat = CATS.find((c) => c.slug === slug);
  const { products, isLoading } = useProducts();
  const inCat = products.filter((p) => p.category === slug);
  const brands = [...new Set(inCat.map((p) => p.brand))];
  const maxP = Math.max(0, ...inCat.map((p) => p.price));

  const [sel, setSel] = useState<string[]>([]);
  const [max, setMax] = useState<number | null>(null);
  const [minRating, setMinRating] = useState(0);
  const [video, setVideo] = useState(false);
  const [sort, setSort] = useState("popular");
  const [showF, setShowF] = useState(false);

  const list = useMemo(() => {
    const r = inCat.filter((p) =>
      (!sel.length || sel.includes(p.brand)) && p.price <= (max ?? Infinity) && p.rating >= minRating && (!video || p.hasVideo));
    const s = { popular: (a: any, b: any) => b.reviews - a.reviews, cheap: (a: any, b: any) => a.price - b.price, exp: (a: any, b: any) => b.price - a.price, rating: (a: any, b: any) => b.rating - a.rating }[sort]!;
    return [...r].sort(s);
  }, [inCat, sel, max, minRating, video, sort]);

  return (
    <div className="container-site py-8">
      <nav className="mb-4 text-sm text-muted-foreground"><Link to="/" className="hover:text-primary">Главная</Link> / <span className="text-foreground">{cat?.name ?? slug}</span></nav>
      <div className="mb-6 flex flex-wrap items-end justify-between gap-3">
        <h1 className="font-display text-3xl font-extrabold">{cat?.name ?? "Категория"} <span className="text-lg font-medium text-muted-foreground">{list.length}</span></h1>
        <div className="flex gap-2">
          <button onClick={() => setShowF(!showF)} className="inline-flex h-10 items-center gap-2 rounded-xl border border-border px-4 text-sm font-medium lg:hidden"><SlidersHorizontal className="h-4 w-4" />Фильтры</button>
          <select value={sort} onChange={(e) => setSort(e.target.value)} className="h-10 rounded-xl border border-border bg-background px-3 text-sm">
            <option value="popular">По популярности</option>
            <option value="rating">По рейтингу</option>
            <option value="cheap">Сначала дешевле</option>
            <option value="exp">Сначала дороже</option>
          </select>
        </div>
      </div>
      <div className="grid gap-6 lg:grid-cols-[260px_1fr]">
        <aside className={`${showF ? "block" : "hidden"} h-fit space-y-6 rounded-2xl border border-border bg-muted p-5 lg:sticky lg:top-32 lg:block`}>
          <div>
            <p className="mb-2 font-semibold">Цена до</p>
            <input type="range" min={0} max={maxP || 1} step={500} value={max ?? maxP} onChange={(e) => setMax(+e.target.value)} className="w-full accent-[var(--primary)]" />
            <p className="text-sm text-muted-foreground">{new Intl.NumberFormat("ru-RU").format(max ?? maxP)} ₽</p>
          </div>
          {brands.length > 0 && (
            <div>
              <p className="mb-2 font-semibold">Бренд</p>
              {brands.map((b) => (
                <label key={b} className="flex items-center gap-2 py-1 text-sm">
                  <input type="checkbox" checked={sel.includes(b)} onChange={() => setSel(sel.includes(b) ? sel.filter((x) => x !== b) : [...sel, b])} className="accent-[var(--primary)]" />{b}
                </label>
              ))}
            </div>
          )}
          <div>
            <p className="mb-2 font-semibold">Рейтинг</p>
            {[0, 4, 4.5].map((r) => (
              <label key={r} className="flex items-center gap-2 py-1 text-sm">
                <input type="radio" name="r" checked={minRating === r} onChange={() => setMinRating(r)} className="accent-[var(--primary)]" />{r ? `от ${r} ★` : "Любой"}
              </label>
            ))}
          </div>
          <label className="flex items-center gap-2 text-sm font-medium">
            <input type="checkbox" checked={video} onChange={(e) => setVideo(e.target.checked)} className="accent-[var(--primary)]" />Есть видеообзор
          </label>
          <button onClick={() => { setSel([]); setMax(null); setMinRating(0); setVideo(false); }} className="text-sm font-medium text-primary">Сбросить фильтры</button>
        </aside>
        <div>
          {isLoading ? <GridSkeleton n={6} /> : list.length ? <Grid items={list} /> : <p className="rounded-2xl bg-muted p-10 text-center text-muted-foreground">Ничего не найдено. Попробуйте изменить фильтры.</p>}
        </div>
      </div>
    </div>
  );
}
