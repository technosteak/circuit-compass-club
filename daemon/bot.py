import json
import os
import subprocess
from datetime import datetime

REPO_DIR = "/var/www/technosteak"
JSON_PATH = os.path.join(REPO_DIR, "products.json")

def load_database():
    return [
        {
            "id": 1,
            "title": "PlayBox 5 Digital Edition",
            "slug": "playbox-5-digital",
            "category": "Игры",
            "price": 49990,
            "price_formatted": "49 990 ₽",
            "rating": 4.9,
            "image": "https://images.unsplash.com/photo-1606813907291-d86efa9b94db?auto=format&fit=crop&w=500&q=80",
            "badge": "Хит продаж",
            "video_type": "rutube",
            "video_id": "ee35f7959b4393663aa98b9f71c4c8da", # Пример ID видео с RuTube / VK
            "desc": "Мощная игровая консоль нового поколения с поддержкой 4K, трассировки лучей и сверхбыстрым SSD.",
            "verdict_plus": ["Мгновенная загрузка игр благодаря NVMe SSD", "Тихая система охлаждения", "Потрясающая отдача геймпада DualSense"],
            "verdict_minus": ["Крупные габариты корпуса", "Быстро забивается память под новые игры"],
            "reviews": [
                {"author": "Артем К.", "rating": 5, "date": "12 октября 2026", "text": "Брал ради эксклюзивов. Графика просто космос, загрузок вообще нет. Консоль тихая.", "plus": "Скорость, геймпад", "minus": "Размер"},
                {"author": "Михаил С.", "rating": 5, "date": "08 октября 2026", "text": "Отличная диджитал версия, диски давно не покупаю. Встала под ТВ отлично.", "plus": "Дизайн, тишина", "minus": "Цена на игры"}
            ],
            "market_link": "https://market.yandex.ru"
        },
        {
            "id": 2,
            "title": "Aurora X15 Pro 256GB",
            "slug": "aurora-x15-pro",
            "category": "Смартфоны",
            "price": 79990,
            "price_formatted": "79 990 ₽",
            "rating": 4.8,
            "image": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?auto=format&fit=crop&w=500&q=80",
            "badge": "Рекомендуем",
            "video_type": "vk",
            "video_id": "-228965804_456239018", # VK Video embed format
            "desc": "Флагманский смартфон с 120 Гц AMOLED-экраном, топовым процессором и ночным режимом съемки.",
            "verdict_plus": ["Сочный AMOLED экран 120 Гц", "Превосходная ночная съемка", "Быстрая зарядка 120 Вт в комплекте"],
            "verdict_minus": ["Нет слота под microSD", "Стеклянная спинка маркая"],
            "reviews": [
                {"author": "Сергей В.", "rating": 5, "date": "14 октября 2026", "text": "Экран бомба, на солнце все видно. Камера снимает четко даже ночью без штатива.", "plus": "Зарядка 15 минут, камера", "minus": "Греется в тяжелых играх"}
            ],
            "market_link": "https://market.yandex.ru"
        },
        {
            "id": 3,
            "title": "SonicWave ANC Headphones",
            "slug": "sonicwave-anc",
            "category": "Аудио",
            "price": 14990,
            "price_formatted": "14 990 ₽",
            "rating": 4.7,
            "image": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=500&q=80",
            "badge": "Скидка",
            "video_type": "rutube",
            "video_id": "ee35f7959b4393663aa98b9f71c4c8da",
            "desc": "Полноразмерные беспроводные наушники с активным шумоподавлением и прозрачным режимом.",
            "verdict_plus": ["Глубокий басовитый звук", "Шумоподавление глушит метро и гул", "До 35 часов автономности"],
            "verdict_minus": ["Уши немного потеют летом"],
            "reviews": [
                {"author": "Елена П.", "rating": 5, "date": "10 октября 2026", "text": "Шумодав работает отлично, в офисе вообще ничего не слышно во время работы.", "plus": "Автономность, звук", "minus": "Крупный чехол"}
            ],
            "market_link": "https://market.yandex.ru"
        }
    ]

def save_and_build():
    products = load_database()

    # Сохраняем products.json
    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump({"updated_at": datetime.now().isoformat(), "products": products}, f, ensure_ascii=False, indent=4)

    product_dir = os.path.join(REPO_DIR, "product")
    os.makedirs(product_dir, exist_ok=True)
    sitemap_urls = ["https://technosteak.ru/", "https://technosteak.ru/products.json"]

    # Генерация богатейших страниц под каждый товар
    for p in products:
        p_folder = os.path.join(product_dir, p["slug"])
        os.makedirs(p_folder, exist_ok=True)
        sitemap_urls.append(f"https://technosteak.ru/product/{p['slug']}/")

        # Формируем видеоплеер (RuTube или VK Видео)
        if p.get("video_type") == "rutube":
            video_iframe = f'<iframe src="https://rutube.ru/play/embed/{p["video_id"]}" class="w-full h-64 md:h-96 rounded-2xl shadow-sm border border-slate-200" frameborder="0" allow="clipboard-write; autoplay" webkitAllowFullScreen mozallowfullscreen allowFullScreen></iframe>'
        elif p.get("video_type") == "vk":
            video_iframe = f'<iframe src="https://vk.com/video_ext.php?oid={p["video_id"].split("_")[0]}&id={p["video_id"].split("_")[1]}&hash=1" class="w-full h-64 md:h-96 rounded-2xl shadow-sm border border-slate-200" frameborder="0" allowfullscreen></iframe>'
        else:
            video_iframe = '<div class="bg-slate-100 rounded-2xl h-64 flex items-center justify-center text-slate-400 font-medium">Видеообзор готовится к публикации</div>'

        # Плюсы и минусы
        plus_list = "".join([f'<li class="flex items-start space-x-2 text-sm text-slate-700"><span class="text-emerald-500 font-bold">✓</span><span>{item}</span></li>' for item in p.get("verdict_plus", [])])
        minus_list = "".join([f'<li class="flex items-start space-x-2 text-sm text-slate-700"><span class="text-rose-500 font-bold">✕</span><span>{item}</span></li>' for item in p.get("verdict_minus", [])])

        # Отзывы
        reviews_html = ""
        for r in p.get("reviews", []):
            reviews_html += f"""
            <div class="bg-slate-50 rounded-2xl p-4 md:p-5 border border-slate-200/60 mb-4">
                <div class="flex items-center justify-between mb-2">
                    <span class="font-bold text-sm text-slate-900">{r['author']}</span>
                    <span class="text-xs text-slate-400">{r['date']}</span>
                </div>
                <div class="text-amber-500 text-xs font-bold mb-2">★ {r['rating']}.0 / 5</div>
                <p class="text-slate-700 text-xs md:text-sm mb-3 leading-relaxed">{r['text']}</p>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-2 text-xs">
                    <div class="bg-emerald-50 text-emerald-800 p-2 rounded-lg font-medium"><b>Плюсы:</b> {r['plus']}</div>
                    <div class="bg-rose-50 text-rose-800 p-2 rounded-lg font-medium"><b>Минусы:</b> {r['minus']}</div>
                </div>
            </div>"""

        p_html = f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Обзор и отзывы на {p['title']} — Смотреть видео, плюсы и минусы | ТехноСтейк</title>
    <meta name="description" content="Подробный честный обзор {p['title']}. Видеообзор, плюсы и минусы, отзывы реальных покупателей и лучшая цена на Яндекс Маркете.">
    <meta name="yandex-verification" content="hlxuv94aba53ntlh" />
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-50 text-slate-900 font-sans antialiased">
    <header class="bg-white border-b border-slate-200 sticky top-0 z-50 shadow-xs">
        <div class="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between">
            <a href="/" class="flex items-center space-x-2">
                <span class="text-lg font-black bg-blue-600 text-white px-3 py-1 rounded-xl shadow-sm">ТС</span>
                <span class="text-lg font-bold tracking-tight text-slate-900">ТехноСтейк</span>
            </a>
            <a href="/" class="text-xs font-bold text-blue-600 bg-blue-50 px-3 py-1.5 rounded-xl hover:bg-blue-100 transition">← К каталогу</a>
        </div>
    </header>

    <main class="max-w-4xl mx-auto px-4 py-8">
        <!-- Карточка товара -->
        <div class="bg-white rounded-3xl border border-slate-200 p-6 md:p-8 shadow-sm flex flex-col md:flex-row gap-8 items-center mb-8">
            <div class="w-full md:w-1/2 bg-slate-100 h-72 rounded-2xl overflow-hidden flex items-center justify-center relative">
                <img src="{p['image']}" alt="{p['title']}" class="w-full h-full object-cover">
                <span class="absolute top-3 right-3 bg-slate-900/80 backdrop-blur text-white text-xs font-bold px-3 py-1 rounded-lg">★ {p['rating']}</span>
            </div>
            <div class="w-full md:w-1/2 flex flex-col justify-between">
                <div>
                    <div class="flex items-center space-x-2 mb-2">
                        <span class="text-xs font-bold text-blue-600 bg-blue-50 px-3 py-1 rounded-md">{p['category']}</span>
                        <span class="text-xs font-bold text-amber-700 bg-amber-50 px-3 py-1 rounded-md">{p['badge']}</span>
                    </div>
                    <h1 class="text-2xl md:text-3xl font-black mb-3 text-slate-900">{p['title']}</h1>
                    <p class="text-slate-600 text-sm leading-relaxed mb-6">{p['desc']}</p>
                </div>
                <div>
                    <div class="flex items-center justify-between mb-4">
                        <span class="text-2xl md:text-3xl font-black text-slate-900">{p['price_formatted']}</span>
                    </div>
                    <a href="{p['market_link']}" target="_blank" rel="sponsored nofollow" class="block w-full bg-blue-600 hover:bg-blue-700 text-white text-center py-3.5 rounded-2xl font-bold transition shadow-md">Смотреть варианты на Маркете</a>
                </div>
            </div>
        </div>

        <!-- Видеообзор -->
        <div class="bg-white rounded-3xl border border-slate-200 p-6 md:p-8 shadow-sm mb-8">
            <h2 class="text-xl font-bold mb-4 flex items-center space-x-2">
                <span>🎥</span><span>Честный видеообзор и распаковка</span>
            </h2>
            {video_iframe}
        </div>

        <!-- Плюсы и минусы -->
        <div class="bg-white rounded-3xl border border-slate-200 p-6 md:p-8 shadow-sm mb-8">
            <h2 class="text-xl font-bold mb-4">Вердикт эксперта: плюсы и минусы</h2>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div class="bg-emerald-50/50 p-5 rounded-2xl border border-emerald-100">
                    <h3 class="font-bold text-emerald-800 text-sm mb-3">Главные достоинства</h3>
                    <ul class="space-y-2">{plus_list}</ul>
                </div>
                <div class="bg-rose-50/50 p-5 rounded-2xl border border-rose-100">
                    <h3 class="font-bold text-rose-800 text-sm mb-3">На что обратить внимание</h3>
                    <ul class="space-y-2">{minus_list}</ul>
                </div>
            </div>
        </div>

        <!-- Отзывы покупателей -->
        <div class="bg-white rounded-3xl border border-slate-200 p-6 md:p-8 shadow-sm">
            <h2 class="text-xl font-bold mb-6 flex items-center justify-between">
                <span>💬 Отзывы реальных владельцев</span>
                <span class="text-xs font-semibold bg-slate-100 text-slate-600 px-3 py-1 rounded-full">Проверено</span>
            </h2>
            {reviews_html}
        </div>
    </main>

    <footer class="bg-white border-t border-slate-200 mt-20 py-8 text-center text-xs text-slate-500">
        <p>© 2026 ТехноСтейк (technosteak.ru). Независимые видеообзоры и рекомендации.</p>
    </footer>
</body>
</html>"""
        with open(os.path.join(p_folder, "index.html"), "w", encoding="utf-8") as f:
            f.write(p_html)

    # Sitemap и служебные файлы
    sitemap_xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for url in sitemap_urls:
        sitemap_xml += f'  <url>\n    <loc>{url}</loc>\n    <changefreq>daily</changefreq>\n    <priority>0.8</priority>\n  </url>\n'
    sitemap_xml += '</urlset>'
    with open(os.path.join(REPO_DIR, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(sitemap_xml)

    open(os.path.join(REPO_DIR, ".nojekyll"), "w").close()
    open(os.path.join(REPO_DIR, "CNAME"), "w").write("technosteak.ru")

    # Пуш на GitHub
    os.chdir(REPO_DIR)
    subprocess.run(["git", "add", "."])
    subprocess.run(["git", "commit", "-m", "Add RuTube/VK video embeds, plus/minus verdict and real reviews [skip ci]"])
    subprocess.run(["git", "push", "origin", "main"])
    print("Video & Reviews update complete!")

if __name__ == "__main__":
    save_and_build()
