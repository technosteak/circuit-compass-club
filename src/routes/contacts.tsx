import { createFileRoute } from "@tanstack/react-router";
import { Page } from "@/components/site";

export const Route = createFileRoute("/contacts")({
  head: () => ({
    meta: [
      { title: "Контакты | ТехноСтейк" },
      { name: "description", content: "Связаться с редакцией ТехноСтейк." },
      { property: "og:title", content: "Контакты ТехноСтейк" },
      { property: "og:description", content: "Вопросы, предложения и сотрудничество." },
    ],
  }),
  component: () => (
    <Page title="Контакты">
      <p>Мы открыты к вопросам, замечаниям и предложениям о сотрудничестве.</p>
      <p><b>Электронная почта:</b> <a href="mailto:info@technosteak.ru">info@technosteak.ru</a></p>
      <p><b>Сотрудничество и реклама:</b> <a href="mailto:partners@technosteak.ru">partners@technosteak.ru</a></p>
      <p>Обычно мы отвечаем в течение 1–2 рабочих дней.</p>
    </Page>
  ),
});
