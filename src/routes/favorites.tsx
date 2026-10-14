import { createFileRoute, Link } from "@tanstack/react-router";
import { Grid, useProducts } from "@/components/site";
import { useFavorites } from "@/lib/catalog";

export const Route = createFileRoute("/favorites")({
  head: () => ({
    meta: [
      { title: "Избранное | ТехноСтейк" },
      { name: "description", content: "Сохранённые товары в ТехноСтейк." },
      { property: "og:title", content: "Избранное | ТехноСтейк" },
      { property: "og:description", content: "Ваши отложенные гаджеты." },
    ],
  }),
  component: Fav,
});

function Fav() {
  const { products } = useProducts();
  const { list } = useFavorites();
  const items = products.filter((p) => list.includes(p.id));
  return (
    <div className="container-site py-10">
      <h1 className="mb-6 font-display text-3xl font-extrabold">Избранное</h1>
      {items.length ? <Grid items={items} /> : (
        <div className="rounded-2xl bg-muted p-10 text-center text-muted-foreground">
          Пока пусто. Нажмите ♡ на карточке товара. <Link to="/" className="font-semibold text-primary">В каталог</Link>
        </div>
      )}
    </div>
  );
}
