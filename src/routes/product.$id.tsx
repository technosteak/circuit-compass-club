import { createFileRoute, Link } from "@tanstack/react-router";
import { Check, Heart, Minus, ShieldCheck } from "lucide-react";
import { CATS, Grid, MarketButton, Stars, useProducts } from "@/components/site";
import { formatPrice, useFavorites } from "@/lib/catalog";

export const Route = createFileRoute("/product/$id")({
  head: () => ({
    meta: [
      { title: "Обзор товара | ТехноСтейк" },
      { name: "description", content: "Характеристики, видеообзор, плюсы и минусы. Лучшая цена на Яндекс Маркете." },
      { property: "og:title", content: "Обзор товара | ТехноСтейк" },
      { property: "og:description", content: "Подробный обзор с характеристиками и видео." },
    ],
  }),
  component: ProductPage,
});

function ProductPage() {
  const { id } = Route.useParams();
  const { products, isLoading } = useProducts();
  const fav = useFavorites();
  const p = products.find((x) => x.id === id);

  if (isLoading) return <div className="container-site py-10"><div className="h-[500px] animate-pulse rounded-3xl bg-muted" /></div>;
  if (!p) return <div className="container-site py-20 text-center"><h1 className="text-2xl font-bold">Товар не найден</h1><Link to="/" className="mt-4 inline-block text-primary">На главную</Link></div>;

  const cat = CATS.find((c) => c.slug === p.category);
  const similar = products.filter((x) => x.category === p.category && x.id !== p.id).concat(products.filter((x) => x.category !== p.category)).slice(0, 4);

  return (
    <div className="container-site py-8">
      <title>{`${p.name} — обзор и цена | ТехноСтейк`}</title>
      <nav className="mb-5 flex flex-wrap gap-1 text-sm text-muted-foreground">
        <Link to="/" className="hover:text-primary">Главная</Link> /
        <Link to="/category/$slug" params={{ slug: p.category }} className="hover:text-primary">{cat?.name}</Link> /
        <span className="truncate text-foreground">{p.name}</span>
      </nav>

      <div className="grid gap-8 lg:grid-cols-2">
        <div className="overflow-hidden rounded-3xl border border-border bg-muted">
          <img src={p.image} alt={p.name} className="aspect-square w-full object-cover" />
        </div>
        <div className="flex flex-col gap-5">
          <p className="text-sm font-semibold text-primary">{p.brand}</p>
          <h1 className="font-display text-3xl font-extrabold leading-tight sm:text-4xl">{p.name}</h1>
          <div className="flex items-center gap-2"><Stars value={p.rating} /><b>{p.rating}</b><span className="text-muted-foreground">· {p.reviews} отзывов</span></div>
          <ul className="flex flex-wrap gap-2">{p.short.map((s) => <li key={s} className="rounded-lg bg-muted px-3 py-1 text-sm">{s}</li>)}</ul>
          <div className="rounded-2xl border border-border bg-muted p-5">
            <div className="flex items-baseline gap-3">
              <span className="text-4xl font-extrabold">{formatPrice(p.price)}</span>
              {p.oldPrice && <span className="text-lg text-muted-foreground line-through">{formatPrice(p.oldPrice)}</span>}
            </div>
            <div className="mt-4 flex flex-col gap-3 sm:flex-row">
              <MarketButton url={p.marketUrl} large />
              <button onClick={() => fav.toggle(p.id)} className="inline-flex h-14 items-center justify-center gap-2 rounded-xl border border-border bg-background px-5 font-semibold hover:bg-muted">
                <Heart className={`h-5 w-5 ${fav.has(p.id) ? "fill-destructive text-destructive" : ""}`} />{fav.has(p.id) ? "В избранном" : "В избранное"}
              </button>
            </div>
            <p className="mt-3 flex items-center gap-1.5 text-xs text-muted-foreground"><ShieldCheck className="h-4 w-4" />Покупка и доставка — на Яндекс Маркете</p>
          </div>
        </div>
      </div>

      <div className="mt-12 grid gap-8 lg:grid-cols-[1.4fr_1fr]">
        <div className="space-y-8">
          {p.youtubeId && (
            <section>
              <h2 className="mb-4 font-display text-2xl font-extrabold">Видеообзор</h2>
              <div className="aspect-video overflow-hidden rounded-2xl border border-border bg-muted">
                <iframe className="h-full w-full" src={`https://www.youtube-nocookie.com/embed/${p.youtubeId}`} title={`Обзор ${p.name}`} loading="lazy" allow="accelerometer; encrypted-media; gyroscope; picture-in-picture" allowFullScreen />
              </div>
            </section>
          )}
          <section className="grid gap-4 sm:grid-cols-2">
            <div className="rounded-2xl border border-border bg-card p-5">
              <h3 className="mb-3 font-bold text-success">Плюсы</h3>
              {p.pros.map((x) => <p key={x} className="flex gap-2 py-1 text-sm"><Check className="h-4 w-4 shrink-0 text-success" />{x}</p>)}
            </div>
            <div className="rounded-2xl border border-border bg-card p-5">
              <h3 className="mb-3 font-bold text-destructive">Минусы</h3>
              {p.cons.map((x) => <p key={x} className="flex gap-2 py-1 text-sm"><Minus className="h-4 w-4 shrink-0 text-destructive" />{x}</p>)}
            </div>
          </section>
        </div>
        <section>
          <h2 className="mb-4 font-display text-2xl font-extrabold">Характеристики</h2>
          <table className="w-full overflow-hidden rounded-2xl border border-border text-sm">
            <tbody>
              {Object.entries(p.specs).map(([k, v], i) => (
                <tr key={k} className={i % 2 ? "bg-background" : "bg-muted"}>
                  <td className="w-1/2 px-4 py-3 text-muted-foreground">{k}</td>
                  <td className="px-4 py-3 font-medium">{v}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>
      </div>

      <section className="mt-16">
        <h2 className="mb-6 font-display text-2xl font-extrabold">Похожие товары</h2>
        <Grid items={similar} />
      </section>
    </div>
  );
}
