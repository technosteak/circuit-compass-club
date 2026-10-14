import { Link, useNavigate } from "@tanstack/react-router";
import { Cpu, Heart, Menu, Search, Star, X, ShoppingBag, PlayCircle } from "lucide-react";
import { useState, type FormEvent } from "react";
import { formatPrice, useCatalog, useFavorites, type Product } from "@/lib/catalog";

export const CATS = [
  { slug: "smartphones", name: "Смартфоны" },
  { slug: "laptops", name: "Ноутбуки" },
  { slug: "games", name: "Игры" },
  { slug: "smart-home", name: "Умный дом" },
  { slug: "audio", name: "Аудио" },
];

export function Logo() {
  return (
    <Link to="/" className="flex shrink-0 items-center gap-2">
      <span className="grid h-9 w-9 place-items-center rounded-xl bg-primary text-primary-foreground shadow-soft">
        <Cpu className="h-5 w-5" />
      </span>
      <span className="font-display text-xl font-extrabold tracking-tight">
        Техно<span className="text-primary">Стейк</span>
      </span>
    </Link>
  );
}

function SearchBox({ onDone }: { onDone?: () => void }) {
  const [q, setQ] = useState("");
  const nav = useNavigate();
  const submit = (e: FormEvent) => {
    e.preventDefault();
    nav({ to: "/search", search: { q: q.trim() } });
    onDone?.();
  };
  return (
    <form onSubmit={submit} className="relative w-full" role="search">
      <Search className="pointer-events-none absolute left-3.5 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
      <input
        value={q} onChange={(e) => setQ(e.target.value)}
        placeholder="Искать смартфоны, ноутбуки, наушники…"
        aria-label="Поиск по каталогу"
        className="h-11 w-full rounded-xl border border-border bg-muted pl-10 pr-24 text-sm outline-none transition focus:border-primary focus:bg-background focus:ring-4 focus:ring-primary/10"
      />
      <button className="absolute right-1.5 top-1.5 h-8 rounded-lg bg-primary px-4 text-sm font-semibold text-primary-foreground hover:bg-primary/90">
        Найти
      </button>
    </form>
  );
}

export function Header() {
  const [open, setOpen] = useState(false);
  const { list } = useFavorites();
  return (
    <header className="sticky top-0 z-40 border-b border-border bg-background/90 backdrop-blur">
      <div className="container-site flex h-16 items-center gap-4">
        <button className="lg:hidden" aria-label="Меню" onClick={() => setOpen(true)}>
          <Menu className="h-6 w-6" />
        </button>
        <Logo />
        <div className="hidden flex-1 md:block"><SearchBox /></div>
        <Link to="/favorites" className="relative ml-auto grid h-10 w-10 place-items-center rounded-xl hover:bg-muted md:ml-0" aria-label="Избранное">
          <Heart className="h-5 w-5" />
          {list.length > 0 && (
            <span className="absolute -right-0.5 -top-0.5 grid h-5 min-w-5 place-items-center rounded-full bg-primary px-1 text-[11px] font-bold text-primary-foreground">{list.length}</span>
          )}
        </Link>
      </div>
      <div className="container-site pb-3 md:hidden"><SearchBox /></div>
      <nav className="container-site hidden h-11 items-center gap-1 lg:flex">
        {CATS.map((c) => (
          <Link key={c.slug} to="/category/$slug" params={{ slug: c.slug }}
            className="rounded-lg px-3 py-1.5 text-sm font-medium text-muted-foreground transition hover:bg-muted hover:text-foreground"
            activeProps={{ className: "bg-accent text-primary" }}>
            {c.name}
          </Link>
        ))}
        <span className="ml-auto flex gap-1">
          <Link to="/about" className="px-3 py-1.5 text-sm text-muted-foreground hover:text-foreground">О проекте</Link>
          <Link to="/contacts" className="px-3 py-1.5 text-sm text-muted-foreground hover:text-foreground">Контакты</Link>
        </span>
      </nav>

      {open && (
        <div className="fixed inset-0 z-50 lg:hidden">
          <div className="absolute inset-0 bg-foreground/30 animate-in fade-in" onClick={() => setOpen(false)} />
          <aside className="absolute inset-y-0 left-0 flex w-80 max-w-[85%] flex-col gap-6 bg-background p-5 shadow-xl animate-in slide-in-from-left">
            <div className="flex items-center justify-between">
              <Logo />
              <button aria-label="Закрыть" onClick={() => setOpen(false)}><X className="h-6 w-6" /></button>
            </div>
            <SearchBox onDone={() => setOpen(false)} />
            <div>
              <p className="mb-2 text-xs font-semibold uppercase tracking-wider text-muted-foreground">Категории</p>
              {CATS.map((c) => (
                <Link key={c.slug} to="/category/$slug" params={{ slug: c.slug }} onClick={() => setOpen(false)}
                  className="block rounded-lg px-3 py-2.5 font-medium hover:bg-muted">{c.name}</Link>
              ))}
            </div>
            <div className="border-t border-border pt-4">
              {([["/favorites", "Избранное"], ["/about", "О проекте"], ["/contacts", "Контакты"], ["/privacy", "Политика конфиденциальности"]] as const).map(([to, l]) => (
                <Link key={to} to={to} onClick={() => setOpen(false)} className="block rounded-lg px-3 py-2 text-sm text-muted-foreground hover:bg-muted">{l}</Link>
              ))}
            </div>
          </aside>
        </div>
      )}
    </header>
  );
}

export function Footer() {
  return (
    <footer className="mt-20 border-t border-border bg-muted">
      <div className="container-site grid gap-10 py-12 sm:grid-cols-2 lg:grid-cols-4">
        <div className="space-y-3">
          <Logo />
          <p className="text-sm text-muted-foreground">Честные обзоры и подборки техники. Помогаем выбрать лучшее.</p>
        </div>
        <div>
          <p className="mb-3 font-semibold">Категории</p>
          {CATS.map((c) => (
            <Link key={c.slug} to="/category/$slug" params={{ slug: c.slug }} className="block py-1 text-sm text-muted-foreground hover:text-primary">{c.name}</Link>
          ))}
        </div>
        <div>
          <p className="mb-3 font-semibold">Проект</p>
          <Link to="/about" className="block py-1 text-sm text-muted-foreground hover:text-primary">О проекте</Link>
          <Link to="/contacts" className="block py-1 text-sm text-muted-foreground hover:text-primary">Контакты</Link>
          <Link to="/privacy" className="block py-1 text-sm text-muted-foreground hover:text-primary">Политика конфиденциальности</Link>
        </div>
        <div className="text-sm text-muted-foreground">
          <p className="mb-3 font-semibold text-foreground">Важно</p>
          Цены носят информационный характер. Покупка совершается на сайте партнёра — Яндекс Маркета.
        </div>
      </div>
      <div className="border-t border-border py-5 text-center text-xs text-muted-foreground">
        © {new Date().getFullYear()} ТехноСтейк · technosteak.ru
      </div>
    </footer>
  );
}

export function Stars({ value, size = "h-4 w-4" }: { value: number; size?: string }) {
  return (
    <span className="inline-flex items-center gap-0.5" aria-label={`Рейтинг ${value} из 5`}>
      {[1, 2, 3, 4, 5].map((i) => (
        <Star key={i} className={`${size} ${i <= Math.round(value) ? "fill-star text-star" : "text-border"}`} />
      ))}
    </span>
  );
}

export function MarketButton({ url, large }: { url: string; large?: boolean }) {
  return (
    <a href={url} target="_blank" rel="sponsored nofollow noopener noreferrer"
      className={`inline-flex items-center justify-center gap-2 rounded-xl bg-primary font-semibold text-primary-foreground shadow-soft transition hover:bg-primary/90 hover:shadow-lift ${large ? "h-14 w-full px-8 text-base sm:w-auto" : "h-10 w-full text-sm"}`}>
      <ShoppingBag className={large ? "h-5 w-5" : "h-4 w-4"} />
      {large ? "Купить на Яндекс Маркете" : "Смотреть на Маркете"}
    </a>
  );
}

export function ProductCard({ p }: { p: Product }) {
  const fav = useFavorites();
  return (
    <article className="card-lift group flex flex-col overflow-hidden rounded-2xl border border-border bg-card">
      <div className="relative aspect-[4/3] overflow-hidden bg-muted">
        <Link to="/product/$id" params={{ id: p.id }}>
          <img src={p.image} alt={p.name} loading="lazy" className="h-full w-full object-cover transition duration-500 group-hover:scale-105" />
        </Link>
        <div className="absolute left-3 top-3 flex gap-1.5">
          {p.isNew && <span className="rounded-md bg-primary px-2 py-0.5 text-xs font-semibold text-primary-foreground">Новинка</span>}
          {p.hasVideo && <span className="inline-flex items-center gap-1 rounded-md bg-background/90 px-2 py-0.5 text-xs font-semibold"><PlayCircle className="h-3 w-3 text-primary" />Обзор</span>}
        </div>
        <button onClick={() => fav.toggle(p.id)} aria-label="В избранное"
          className="absolute right-3 top-3 grid h-9 w-9 place-items-center rounded-full bg-background/90 shadow-soft hover:scale-110 transition">
          <Heart className={`h-4 w-4 ${fav.has(p.id) ? "fill-destructive text-destructive" : ""}`} />
        </button>
      </div>
      <div className="flex flex-1 flex-col gap-2 p-4">
        <div className="flex items-center gap-2 text-sm">
          <Stars value={p.rating} size="h-3.5 w-3.5" />
          <span className="font-semibold">{p.rating}</span>
          <span className="text-muted-foreground">({p.reviews})</span>
        </div>
        <Link to="/product/$id" params={{ id: p.id }} className="line-clamp-2 font-semibold leading-snug hover:text-primary">{p.name}</Link>
        <ul className="flex flex-wrap gap-1">
          {p.short.map((s) => <li key={s} className="rounded-md bg-muted px-2 py-0.5 text-xs text-muted-foreground">{s}</li>)}
        </ul>
        <div className="mt-auto flex items-baseline gap-2 pt-2">
          <span className="text-xl font-extrabold">{formatPrice(p.price)}</span>
          {p.oldPrice && <span className="text-sm text-muted-foreground line-through">{formatPrice(p.oldPrice)}</span>}
        </div>
        <MarketButton url={p.marketUrl} />
      </div>
    </article>
  );
}

export function Grid({ items }: { items: Product[] }) {
  return <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">{items.map((p) => <ProductCard key={p.id} p={p} />)}</div>;
}

export function GridSkeleton({ n = 4 }: { n?: number }) {
  return (
    <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
      {Array.from({ length: n }).map((_, i) => <div key={i} className="h-96 animate-pulse rounded-2xl bg-muted" />)}
    </div>
  );
}

export function useProducts() {
  const q = useCatalog();
  return { ...q, products: q.data?.products ?? [] };
}

export function Page({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div className="container-site py-12">
      <article className="prose-site mx-auto max-w-3xl rounded-3xl border border-border bg-card p-6 sm:p-10">
        <h1 className="mb-6 font-display text-3xl font-extrabold">{title}</h1>
        {children}
      </article>
    </div>
  );
}
