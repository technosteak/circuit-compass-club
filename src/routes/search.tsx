import { createFileRoute } from "@tanstack/react-router";
import { Grid, GridSkeleton, useProducts } from "@/components/site";

export const Route = createFileRoute("/search")({
  validateSearch: (s: Record<string, unknown>) => ({ q: typeof s.q === "string" ? s.q : "" }),
  head: () => ({
    meta: [
      { title: "Поиск по каталогу | ТехноСтейк" },
      { name: "description", content: "Поиск техники по каталогу ТехноСтейк." },
      { property: "og:title", content: "Поиск | ТехноСтейк" },
      { property: "og:description", content: "Найдите нужный гаджет в каталоге." },
    ],
  }),
  component: SearchPage,
});

function SearchPage() {
  const { q } = Route.useSearch();
  const { products, isLoading } = useProducts();
  const terms = q.toLowerCase().split(/\s+/).filter(Boolean);
  const res = products.filter((p) => {
    const hay = [p.name, p.brand, ...p.short, ...Object.values(p.specs)].join(" ").toLowerCase();
    return terms.every((t) => hay.includes(t));
  });
  return (
    <div className="container-site py-10">
      <h1 className="mb-6 font-display text-3xl font-extrabold">{q ? <>Результаты по запросу «{q}» <span className="text-lg text-muted-foreground">{res.length}</span></> : "Все товары"}</h1>
      {isLoading ? <GridSkeleton /> : res.length ? <Grid items={res} /> : <p className="rounded-2xl bg-muted p-10 text-center text-muted-foreground">Ничего не найдено. Попробуйте другой запрос.</p>}
    </div>
  );
}
