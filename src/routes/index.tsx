import { createFileRoute, Link } from "@tanstack/react-router";
import { ArrowRight, PlayCircle, Sparkles, Smartphone, Laptop, Gamepad2, Home, Headphones } from "lucide-react";
import { CATS, Grid, GridSkeleton, Stars, formatPriceSafe, useProducts } from "@/components/home-helpers";

export const Route = createFileRoute("/")({
  head: () => ({
    meta: [
      { title: "ТехноСтейк — обзоры и выбор техники" },
      { name: "description", content: "Обзоры смартфонов, ноутбуков, игр, умного дома и аудио. Сравнивайте характеристики и выбирайте лучшее." },
      { property: "og:title", content: "ТехноСтейк — обзоры и выбор техники" },
      { property: "og:description", content: "Видеообзоры, рейтинги и подборки лучшей техники месяца." },
    ],
  }),
  component: Index,
});

const ICONS = [Smartphone, Laptop, Gamepad2, Home, Headphones];

function Index() {
  const { products, isLoading } = useProducts();
  const top = [...products].sort((a, b) => b.rating - a.rating).slice(0, 3);
  const fresh = products.filter((p) => p.isNew).slice(0, 8);
  const video = products.filter((p) => p.hasVideo && p.youtubeId).slice(0, 3);

  return (
    <>
      <section className="hero-bg border-b border-border">
        <div className="container-site grid items-center gap-10 py-14 lg:grid-cols-2 lg:py-20">
          <div>
            <span className="inline-flex items-center gap-1.5 rounded-full border border-border bg-background px-3 py-1 text-xs font-semibold text-primary">
              <Sparkles className="h-3.5 w-3.5" /> Топ-гаджеты месяца
            </span>
            <h1 className="mt-5 font-display text-4xl font-extrabold leading-[1.05] tracking-tight sm:text-5xl lg:text-6xl">
              Выбирайте технику <span className="text-primary">с умом</span>, а не наугад
            </h1>
            <p className="mt-5 max-w-lg text-lg text-muted-foreground">
              Честные обзоры, видео и сравнение характеристик — в одном месте. Лучшие цены на Яндекс Маркете.
            </p>
            <div className="mt-8 flex flex-wrap gap-3">
              <Link to="/category/$slug" params={{ slug: "smartphones" }} className="inline-flex h-12 items-center gap-2 rounded-xl bg-primary px-6 font-semibold text-primary-foreground shadow-soft hover:bg-primary/90">
                Перейти в каталог <ArrowRight className="h-4 w-4" />
              </Link>
              <a href="#video" className="inline-flex h-12 items-center gap-2 rounded-xl border border-border bg-background px-6 font-semibold hover:bg-muted">
                <PlayCircle className="h-4 w-4" /> Видеообзоры
              </a>
            </div>
          </div>
          <div className="grid gap-3">
            {top.length === 0 && <div className="h-80 animate-pulse rounded-3xl bg-muted" />}
            {top.map((p, i) => (
              <Link key={p.id} to="/product/$id" params={{ id: p.id }}
                className="card-lift flex items-center gap-4 rounded-2xl border border-border bg-card p-3">
                <img src={p.image} alt={p.name} className="h-20 w-20 shrink-0 rounded-xl object-cover" />
                <div className="min-w-0 flex-1">
                  <p className="text-xs font-semibold text-primary">#{i + 1} месяца</p>
                  <p className="truncate font-semibold">{p.name}</p>
                  <Stars value={p.rating} size="h-3.5 w-3.5" />
                </div>
                <span className="shrink-0 font-extrabold">{formatPriceSafe(p.price)}</span>
              </Link>
            ))}
          </div>
        </div>
      </section>

      <section className="container-site mt-10 grid grid-cols-2 gap-3 sm:grid-cols-5">
        {CATS.map((c, i) => {
          const I = ICONS[i] ?? Smartphone;
          return (
            <Link key={c.slug} to="/category/$slug" params={{ slug: c.slug }}
              className="card-lift flex flex-col items-center gap-2 rounded-2xl border border-border bg-card p-5 text-center font-semibold">
              <span className="grid h-12 w-12 place-items-center rounded-xl bg-accent text-primary"><I className="h-6 w-6" /></span>
              {c.name}
            </Link>
          );
        })}
      </section>

      <Section title="Популярные новинки">
        {isLoading ? <GridSkeleton /> : <Grid items={fresh} />}
      </Section>

      <Section title="Лучшие видеообзоры" id="video">
        <div className="grid gap-5 md:grid-cols-3">
          {video.map((p) => (
            <Link key={p.id} to="/product/$id" params={{ id: p.id }} className="card-lift group overflow-hidden rounded-2xl border border-border bg-card">
              <div className="relative aspect-video">
                <img src={`https://i.ytimg.com/vi/${p.youtubeId}/hqdefault.jpg`} alt={p.name} loading="lazy" className="h-full w-full object-cover" />
                <span className="absolute inset-0 grid place-items-center bg-foreground/20 transition group-hover:bg-foreground/30">
                  <PlayCircle className="h-14 w-14 text-primary-foreground drop-shadow" />
                </span>
              </div>
              <div className="p-4">
                <p className="font-semibold">Обзор: {p.name}</p>
                <p className="text-sm text-muted-foreground">{formatPriceSafe(p.price)}</p>
              </div>
            </Link>
          ))}
        </div>
      </Section>

      <Section title="Все товары">
        {isLoading ? <GridSkeleton n={8} /> : <Grid items={products} />}
      </Section>
    </>
  );
}

function Section({ title, id, children }: { title: string; id?: string; children: React.ReactNode }) {
  return (
    <section id={id} className="container-site mt-16 scroll-mt-28">
      <h2 className="mb-6 font-display text-2xl font-extrabold tracking-tight sm:text-3xl">{title}</h2>
      {children}
    </section>
  );
}
