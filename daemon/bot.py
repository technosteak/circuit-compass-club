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
            "is_juicy_discount": True,
            "discount_percent": 25,
            "price": 49990,
            "price_formatted": "49 990 ₽",
            "old_price_formatted": "66 500 ₽",
            "price_status": "🔥 СОЧНАЯ СКИДКА -25%",
            "rating": 4.9,
            "image": "https://images.unsplash.com/photo-1606813907291-d86efa9b94db?auto=format&fit=crop&w=500&q=80",
            "badge": "🔥 -25% СКИДКА",
            "video_type": "rutube",
            "video_id": "ee35f7959b4393663aa98b9f71c4c8da",
            "desc": "Мощная игровая консоль нового поколения с поддержкой 4K, трассировки лучей и SSD.",
            "verdict_plus": ["Мгновенная загрузка", "Тихое охлаждение", "Отдача DualSense"],
            "verdict_minus": ["Крупные габариты"],
            "cross_sell": ["Второй геймпад", "Зарядка"],
            "versus_target": "xbox-series-x",
            "versus_title": "Xbox Series X 1TB",
            "reviews": [{"author": "Артем К.", "rating": 5, "date": "12 октября 2026", "text": "Взял по акции со скидкой, огонь!", "plus": "Скорость", "minus": "Размер"}],
            "market_link": "https://market.yandex.ru"
        },
        {
            "id": 2,
            "title": "SonicWave ANC Headphones",
            "slug": "sonicwave-anc",
            "category": "Аудио",
            "is_juicy_discount": True,
            "discount_percent": 30,
            "price": 13990,
            "price_formatted": "13 990 ₽",
            "old_price_formatted": "19 990 ₽",
            "price_status": "🔥 СОЧНАЯ СКИДКА -30%",
            "rating": 4.8,
            "image": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=500&q=80",
            "badge": "🔥 -30% СКИДКА",
            "video_type": "rutube",
            "video_id": "ee35f7959b4393663aa98b9f71c4c8da",
            "desc": "Беспроводные наушники с активным шумоподавлением и басом.",
            "verdict_plus": ["Шумодав", "Автономность 35ч"],
            "verdict_minus": ["Чехол крупный"],
            "cross_sell": ["Кабель AUX", "Адаптер"],
            "versus_target": "",
            "versus_title": "",
            "reviews": [{"author": "Елена П.", "rating": 5, "date": "10 октября 2026", "text": "Супер цена со скидкой!", "plus": "Звук", "minus": "Чехол"}],
            "market_link": "https://market.yandex.ru"
        },
        {
            "id": 3,
            "title": "Aurora X15 Pro 256GB",
            "slug": "aurora-x15-pro",
            "category": "Смартфоны",
            "is_juicy_discount": False,
            "discount_percent": 0,
            "price": 79990,
            "price_formatted": "79 990 ₽",
            "old_price_formatted": "85 990 ₽",
            "price_status": "Скидка недели (-7%)",
            "rating": 4.8,
            "image": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?auto=format&fit=crop&w=500&q=80",
            "badge": "Рекомендуем",
            "video_type": "vk",
            "video_id": "-228965804_456239018",
            "desc": "Флагманский смартфон с 120 Гц AMOLED-экраном и ночной съемкой.",
            "verdict_plus": ["AMOLED 120Гц", "Зарядка 120Вт"],
            "verdict_minus": ["Нет microSD"],
            "cross_sell": ["Стекло 9H", "Чехол"],
            "versus_target": "",
            "versus_title": "",
            "reviews": [{"author": "Сергей В.", "rating": 5, "date": "14 октября 2026", "text": "Камера отличная", "plus": "Зарядка", "minus": "Греется"}],
            "market_link": "https://market.yandex.ru"
        }
    ]

def save_and_build():
    products = load_database()

    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump({"updated_at": datetime.now().isoformat(), "products": products}, f, ensure_ascii=False, indent=4)

    product_dir = os.path.join(REPO_DIR, "product")
    os.makedirs(product_dir, exist_ok=True)
    sitemap_urls = ["https://technosteak.ru/", "https://technosteak.ru/products.json"]

    # 1. СТРАНИЦЫ ТОВАРОВ С КНОПКОЙ ТЕЛЕГРАМ
    for p in products:
        p_folder = os.path.join(product_dir, p["slug"])
        os.makedirs(p_folder, exist_ok=True)
        sitemap_urls.append(f"https://technosteak.ru/product/{p['slug']}/")

        badge_color = "bg-rose-600 text-white font-black" if p.get("is_juicy_discount") else "bg-amber-50 text-amber-700 font-bold"

        p_html = f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Сочная скидка! {p['title']} — Купить по акции | ТехноСтейк</title>
    <meta name="description" content="{p['title']} со скидкой! Актуальная цена {p['price_formatted']}. Честный обзор, отзывы и где купить дешевле.">
    <meta name="yandex-verification" content="hlxuv94aba53ntlh" />
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-50 text-slate-900 font-sans antialiased">
    <header class="bg-white border-b border-slate-200 sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between">
            <a href="/" class="flex items-center space-x-2"><span class="text-lg font-black bg-blue-600 text-white px-3 py-1 rounded-xl">ТС</span><span class="text-lg font-bold">ТехноСтейк</span></a>
            <a href="https://t.me/technosteak" target="_blank" class="text-xs font-bold text-white bg-blue-500 hover:bg-blue-600 px-3.5 py-2 rounded-xl transition flex items-center space-x-1.5 shadow-sm">
                <span>✈️ Наш Telegram</span>
            </a>
        </div>
    </header>

    <main class="max-w-4xl mx-auto px-4 py-8">
        <div class="bg-white rounded-3xl border border-slate-200 p-6 md:p-8 shadow-sm flex flex-col md:flex-row gap-8 items-center mb-8">
            <div class="w-full md:w-1/2 bg-slate-100 h-72 rounded-2xl overflow-hidden flex items-center justify-center relative">
                <img src="{p['image']}" alt="{p['title']}" class="w-full h-full object-cover">
                <span class="absolute top-3 right-3 bg-slate-900/80 backdrop-blur text-white text-xs font-bold px-3 py-1 rounded-lg">★ {p['rating']}</span>
            </div>
            <div class="w-full md:w-1/2 flex flex-col justify-between">
                <div>
                    <div class="flex items-center space-x-2 mb-2">
                        <span class="text-xs font-bold text-blue-600 bg-blue-50 px-3 py-1 rounded-md">{p['category']}</span>
                        <span class="text-xs px-3 py-1 rounded-md shadow-xs {badge_color}">{p['badge']}</span>
                    </div>
                    <h1 class="text-2xl md:text-3xl font-black mb-2 text-slate-900">{p['title']}</h1>
                    <p class="text-slate-600 text-sm mb-4">{p['desc']}</p>
                </div>
                <div>
                    <div class="bg-rose-50 border border-rose-200 rounded-2xl p-3 mb-4">
                        <div class="flex items-center justify-between mb-1">
                            <span class="text-xs font-bold text-rose-700">{p['price_status']}</span>
                            <span class="text-xs line-through text-slate-400">{p.get('old_price_formatted', '')}</span>
                        </div>
                        <div class="text-2xl font-black text-rose-600">{p['price_formatted']}</div>
                    </div>
                    <a href="{p['market_link']}" target="_blank" class="block w-full bg-rose-600 hover:bg-rose-700 text-white text-center py-3.5 rounded-2xl font-bold transition shadow-md mb-3">Забрать со скидкой на Маркете</a>
                    <a href="https://t.me/technosteak" target="_blank" class="block w-full bg-slate-100 hover:bg-slate-200 text-slate-700 text-center py-2.5 rounded-2xl font-bold text-xs transition">📢 Получать скидки дня в Telegram</a>
                </div>
            </div>
        </div>
    </main>
</body>
</html>"""
        with open(os.path.join(p_folder, "index.html"), "w", encoding="utf-8") as f:
            f.write(p_html)

    # 2. ГЛАВНАЯ СТРАНИЦА С БАННЕРОМ И КНОПКОЙ ТЕЛЕГРАМ
    index_html = """<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ТехноСтейк — Сочные скидки и независимый выбор техники</title>
    <meta name="description" content="Каталог товаров с максимальными скидками. Честные обзоры, подбор техники и акции на Яндекс Маркете.">
    <meta name="yandex-verification" content="hlxuv94aba53ntlh" />
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-50 text-slate-900 font-sans antialiased">
    <header class="bg-white border-b border-slate-200 sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between">
            <a href="/" class="flex items-center space-x-2"><span class="text-lg font-black bg-rose-600 text-white px-3 py-1 rounded-xl shadow-sm">ТС</span><span class="text-lg font-bold">ТехноСтейк</span></a>
            <a href="https://t.me/technosteak" target="_blank" class="text-xs font-bold text-white bg-blue-500 hover:bg-blue-600 px-3.5 py-2 rounded-xl transition flex items-center space-x-1.5 shadow-sm">
                <span>✈️ Канал в Telegram</span>
            </a>
        </div>
    </header>

    <main class="max-w-7xl mx-auto px-4 py-6">
        <div class="bg-gradient-to-r from-rose-600 via-red-600 to-orange-600 rounded-3xl p-6 md:p-10 text-white mb-6 shadow-xl relative overflow-hidden flex flex-col md:flex-row justify-between items-start md:items-center gap-6">
            <div class="max-w-2xl relative z-10">
                <span class="text-xs bg-white/20 text-white font-bold px-3 py-1 rounded-full uppercase tracking-widest">Максимальный дисконт</span>
                <h1 class="text-2xl md:text-4xl font-black mt-3 mb-2">🔥 Сочные скидки дня</h1>
                <p class="text-rose-100 text-sm mb-4">Самые глубокие скидки на популярные гаджеты с прямой выгодой до 30%.</p>
                <a href="https://t.me/technosteak" target="_blank" class="inline-flex items-center space-x-2 bg-white text-rose-600 px-4 py-2.5 rounded-xl font-black text-xs hover:bg-rose-50 transition shadow-md">
                    <span>🔥 Подписаться на закрытые скидки в Telegram →</span>
                </a>
            </div>
        </div>

        <!-- Категории -->
        <div class="flex items-center space-x-2 overflow-x-auto pb-4 no-scrollbar">
            <button onclick="filterCategory('juicy')" class="cat-btn px-4 py-2.5 rounded-xl text-xs md:text-sm font-black bg-rose-600 text-white transition shadow-sm whitespace-nowrap">🔥 Сочные скидки</button>
            <button onclick="filterCategory('all')" class="cat-btn px-4 py-2.5 rounded-xl text-xs md:text-sm font-semibold bg-white border border-slate-200 text-slate-700 transition whitespace-nowrap">Все товары</button>
            <button onclick="filterCategory('Смартфоны')" class="cat-btn px-4 py-2.5 rounded-xl text-xs md:text-sm font-semibold bg-white border border-slate-200 text-slate-700 transition whitespace-nowrap">Смартфоны</button>
            <button onclick="filterCategory('Игры')" class="cat-btn px-4 py-2.5 rounded-xl text-xs md:text-sm font-semibold bg-white border border-slate-200 text-slate-700 transition whitespace-nowrap">Игры</button>
            <button onclick="filterCategory('Аудио')" class="cat-btn px-4 py-2.5 rounded-xl text-xs md:text-sm font-semibold bg-white border border-slate-200 text-slate-700 transition whitespace-nowrap">Аудио</button>
        </div>

        <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4" id="productsGrid"></div>
    </main>

    <script>
        let products = [];
        let currentCat = 'juicy';

        async function loadProducts() {
            const res = await fetch('products.json?' + new Date().getTime());
            const data = await res.json();
            products = data.products || [];
            renderProducts();
        }

        function filterCategory(cat) {
            currentCat = cat;
            renderProducts();
        }

        function renderProducts() {
            const grid = document.getElementById('productsGrid');
            let list = products;
            if (currentCat === 'juicy') {
                list = products.filter(p => p.is_juicy_discount);
            } else if (currentCat !== 'all') {
                list = products.filter(p => p.category === currentCat);
            }

            grid.innerHTML = list.map(item => `
                <div class="bg-white rounded-2xl border border-slate-200 p-4 shadow-sm hover:shadow-md transition flex flex-col justify-between">
                    <div>
                        <a href="product/${item.slug}/" class="block bg-slate-100 h-40 rounded-xl mb-3 overflow-hidden relative">
                            <img src="${item.image}" alt="${item.title}" class="w-full h-full object-cover">
                            ${item.is_juicy_discount ? `<span class="absolute top-2 left-2 bg-rose-600 text-white text-[10px] font-black px-2 py-0.5 rounded-md shadow-sm">-${item.discount_percent}%</span>` : ''}
                            <span class="absolute top-2 right-2 bg-slate-900/80 text-white text-[10px] font-bold px-2 py-0.5 rounded-md">★ ${item.rating}</span>
                        </a>
                        <span class="text-[10px] font-bold text-blue-600 bg-blue-50 px-2 py-0.5 rounded-md">${item.category}</span>
                        <a href="product/${item.slug}/" class="block font-bold text-sm mt-2 mb-1 text-slate-800 line-clamp-2 hover:text-rose-600">${item.title}</a>
                    </div>
                    <div>
                        <div class="text-xs line-through text-slate-400 font-medium">${item.old_price_formatted || ''}</div>
                        <div class="text-lg font-black text-rose-600 mb-2">${item.price_formatted}</div>
                        <a href="${item.market_link}" target="_blank" class="block w-full bg-rose-600 hover:bg-rose-700 text-white text-center py-2.5 rounded-xl text-xs font-bold transition shadow-sm">Купить со скидкой</a>
                    </div>
                </div>
            `).join('');
        }
        loadProducts();
    </script>
</body>
</html>"""
    with open(os.path.join(REPO_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(index_html)

    # Sitemap и CNAME
    sitemap_xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for url in sitemap_urls:
        sitemap_xml += f'  <url>\n    <loc>{url}</loc>\n    <changefreq>daily</changefreq>\n    <priority>0.8</priority>\n  </url>\n'
    sitemap_xml += '</urlset>'
    with open(os.path.join(REPO_DIR, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(sitemap_xml)

    open(os.path.join(REPO_DIR, ".nojekyll"), "w").close()
    open(os.path.join(REPO_DIR, "CNAME"), "w").write("technosteak.ru")

    os.chdir(REPO_DIR)
    subprocess.run(["git", "add", "."])
    subprocess.run(["git", "commit", "-m", "Add Telegram channel buttons and cross-links [skip ci]"])
    subprocess.run(["git", "push", "origin", "main"])
    print("Site updated with Telegram integration!")

if __name__ == "__main__":
    save_and_build()
