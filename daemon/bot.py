import json
import os
import subprocess
from datetime import datetime

REPO_DIR = "/var/www/technosteak"
JSON_PATH = os.path.join(REPO_DIR, "products.json")

# Четкий список только РЕАЛЬНЫХ товаров с корректными фотографиями и описаниями
REAL_PRODUCTS = [
    {
        "id": 1,
        "title": "PlayStation 5 Digital Edition",
        "slug": "playstation-5-digital",
        "category": "Игры",
        "is_juicy_discount": True,
        "discount_percent": 25,
        "price": 49990,
        "price_formatted": "49 990 ₽",
        "old_price_formatted": "66 500 ₽",
        "price_status": "Скидка -25%",
        "rating": 4.9,
        "image": "https://images.unsplash.com/photo-1606813907291-d86efa9b94db?auto=format&fit=crop&w=600&q=80",
        "badge": "Хит продаж",
        "desc": "Игровая консоль Sony с ультраскоростным SSD, поддержкой 4K и отдачей DualSense.",
        "market_link": "https://market.yandex.ru"
    },
    {
        "id": 2,
        "title": "Беспроводные наушники Sony WH-1000XM4",
        "slug": "sony-wh-1000xm4",
        "category": "Аудио",
        "is_juicy_discount": True,
        "discount_percent": 30,
        "price": 24990,
        "price_formatted": "24 990 ₽",
        "old_price_formatted": "35 990 ₽",
        "price_status": "Скидка -30%",
        "rating": 4.9,
        "image": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=600&q=80",
        "badge": "Выбор экспертов",
        "desc": "Полноразмерные наушники с лучшим в классе активным шумоподавлением и LDAC.",
        "market_link": "https://market.yandex.ru"
    },
    {
        "id": 3,
        "title": "Apple iPhone 15 Pro 128GB",
        "slug": "iphone-15-pro-128gb",
        "category": "Смартфоны",
        "is_juicy_discount": False,
        "discount_percent": 0,
        "price": 98990,
        "price_formatted": "98 990 ₽",
        "old_price_formatted": "109 990 ₽",
        "price_status": "Лучшая цена",
        "rating": 4.8,
        "image": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?auto=format&fit=crop&w=600&q=80",
        "badge": "Флагман",
        "desc": "Флагманский смартфон в титановом корпусе с процессором A17 Pro и кнопкой Action.",
        "market_link": "https://market.yandex.ru"
    },
    {
        "id": 4,
        "title": "Портативная колонка JBL Charge 5",
        "slug": "jbl-charge-5",
        "category": "Аудио",
        "is_juicy_discount": True,
        "discount_percent": 15,
        "price": 14990,
        "price_formatted": "14 990 ₽",
        "old_price_formatted": "17 990 ₽",
        "price_status": "Скидка -15%",
        "rating": 4.9,
        "image": "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?auto=format&fit=crop&w=600&q=80",
        "badge": "Влагозащита",
        "desc": "Мощный звук, защита IP67 от воды и пыли, работа до 20 часов от одного заряда.",
        "market_link": "https://market.yandex.ru"
    },
    {
        "id": 5,
        "title": "Ноутбук Apple MacBook Air 13 M2",
        "slug": "macbook-air-13-m2",
        "category": "Ноутбуки",
        "is_juicy_discount": False,
        "discount_percent": 0,
        "price": 109990,
        "price_formatted": "109 990 ₽",
        "old_price_formatted": "119 990 ₽",
        "price_status": "Популярное",
        "rating": 5.0,
        "image": "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?auto=format&fit=crop&w=600&q=80",
        "badge": "Тонкий и легкий",
        "desc": "Ультратонкий ноутбук на процессоре M2 с дисплеем Liquid Retina и бесшумным охлаждением.",
        "market_link": "https://market.yandex.ru"
    },
    {
        "id": 6,
        "title": "Умная колонка Яндекс Станция Миди",
        "slug": "yandex-station-midi",
        "category": "Умный дом",
        "is_juicy_discount": True,
        "discount_percent": 20,
        "price": 13990,
        "price_formatted": "13 990 ₽",
        "old_price_formatted": "16 990 ₽",
        "price_status": "Скидка -20%",
        "rating": 4.8,
        "image": "https://images.unsplash.com/photo-1543512214-318c7553f230?auto=format&fit=crop&w=600&q=80", "badge": "С Алисой",
        "desc": "Компактная умная колонка со встроенным хабом Zigbee, мощным звуком 24 Вт и LED-экраном.",
        "market_link": "https://market.yandex.ru"
    }
]

def save_and_build():
    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump({"updated_at": datetime.now().isoformat(), "products": REAL_PRODUCTS}, f, ensure_ascii=False, indent=4)

    product_dir = os.path.join(REPO_DIR, "product")
    os.makedirs(product_dir, exist_ok=True)
    sitemap_urls = ["https://technosteak.ru/", "https://technosteak.ru/products.json"]

    # SEO Страницы товаров
    for p in REAL_PRODUCTS:
        p_folder = os.path.join(product_dir, p["slug"])
        os.makedirs(p_folder, exist_ok=True)
        sitemap_urls.append(f"https://technosteak.ru/product/{p['slug']}/")

        p_html = f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Купить {p['title']} — Характеристики и цена | ТехноСтейк</title>
    <meta name="description" content="{p['desc']} Актуальная цена {p['price_formatted']} на Яндекс Маркете.">
    <meta name="yandex-verification" content="hlxuv94aba53ntlh" />
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-50 text-slate-900 font-sans antialiased">
    <header class="bg-white border-b border-slate-200 sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between">
            <a href="/" class="flex items-center space-x-2">
                <span class="text-lg font-black bg-blue-600 text-white px-3 py-1 rounded-xl shadow-sm">ТС</span>
                <span class="text-lg font-bold text-slate-900">ТехноСтейк</span>
            </a>
            <a href="/" class="text-xs font-bold text-blue-600 bg-blue-50 px-3 py-1.5 rounded-xl hover:bg-blue-100 transition">← На главную</a>
        </div>
    </header>

    <main class="max-w-4xl mx-auto px-4 py-8">
        <div class="bg-white rounded-3xl border border-slate-200 p-6 md:p-8 shadow-sm flex flex-col md:flex-row gap-8 items-center">
            <div class="w-full md:w-1/2 bg-slate-100 h-72 rounded-2xl overflow-hidden relative">
                <img src="{p['image']}" alt="{p['title']}" class="w-full h-full object-cover">
                <span class="absolute top-3 right-3 bg-slate-900/80 backdrop-blur text-white text-xs font-bold px-3 py-1 rounded-lg">★ {p['rating']}</span>
            </div>
            <div class="w-full md:w-1/2 flex flex-col justify-between">
                <div>
                    <span class="text-xs font-bold text-blue-600 bg-blue-50 px-3 py-1 rounded-md">{p['category']}</span>
                    <h1 class="text-2xl md:text-3xl font-black mt-2 mb-2 text-slate-900">{p['title']}</h1>
                    <p class="text-slate-600 text-sm mb-4">{p['desc']}</p>
                </div>
                <div>
                    <div class="text-2xl md:text-3xl font-black text-slate-900 mb-4">{p['price_formatted']}</div>
                    <a href="{p['market_link']}" target="_blank" class="block w-full bg-blue-600 hover:bg-blue-700 text-white text-center py-3.5 rounded-2xl font-bold transition shadow-md mb-2">Смотреть на Маркете</a>
                    <a href="https://t.me/technosteak" target="_blank" class="block w-full bg-slate-100 hover:bg-slate-200 text-slate-700 text-center py-2.5 rounded-2xl font-bold text-xs transition">📢 Канал в Telegram</a>
                </div>
            </div>
        </div>
    </main>
</body>
</html>"""
        with open(os.path.join(p_folder, "index.html"), "w", encoding="utf-8") as f:
            f.write(p_html)

    # Главная страница (Строгий синий дизайн, бургер-меню, поиск, категории)
    index_html = """<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ТехноСтейк — Каталог техники, честные обзоры и лучшие цены</title>
    <meta name="description" content="Независимый каталог техники с актуальными ценами, рейтингами и предложением проверенных гаджетов.">
    <meta name="yandex-verification" content="hlxuv94aba53ntlh" />
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-50 text-slate-900 font-sans antialiased">
    <header class="bg-white border-b border-slate-200 sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between">
            <div class="flex items-center space-x-3">
                <button onclick="toggleMenu()" class="p-2 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-700 transition focus:outline-none">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path>
                    </svg>
                </button>
                <a href="/" class="flex items-center space-x-2">
                    <span class="text-lg font-black bg-blue-600 text-white px-3 py-1 rounded-xl shadow-sm">ТС</span>
                    <span class="text-lg font-bold tracking-tight text-slate-900">ТехноСтейк</span>
                </a>
            </div>
            <div class="flex items-center space-x-2">
                <a href="https://t.me/technosteak" target="_blank" class="text-xs font-bold text-white bg-blue-500 hover:bg-blue-600 px-3 py-1.5 rounded-xl transition shadow-xs hidden sm:inline-block">Telegram</a>
                <span class="text-[11px] bg-emerald-50 text-emerald-700 border border-emerald-200 px-2.5 py-1 rounded-full font-semibold">Яндекс Партнер</span>
            </div>
        </div>
    </header>

    <!-- Бургер Меню -->
    <div id="mobileMenu" class="fixed inset-0 z-50 bg-slate-900/50 backdrop-blur-sm hidden">
        <div class="bg-white w-4/5 max-w-xs h-full shadow-2xl p-6 flex flex-col justify-between">
            <div>
                <div class="flex items-center justify-between mb-8">
                    <div class="flex items-center space-x-2">
                        <span class="text-base font-black bg-blue-600 text-white px-2.5 py-1 rounded-lg">ТС</span>
                        <span class="font-bold text-lg">Категории</span>
                    </div>
                    <button onclick="toggleMenu()" class="p-2 text-slate-400 hover:text-slate-600">✕</button>
                </div>
                <div class="flex flex-col space-y-2">
                    <button onclick="filterCategory('all'); toggleMenu();" class="text-left px-4 py-3 rounded-xl font-bold bg-blue-50 text-blue-600">🔥 Все товары</button>
                    <button onclick="filterCategory('juicy'); toggleMenu();" class="text-left px-4 py-3 rounded-xl font-semibold text-slate-700 hover:bg-slate-100">💥 Сочные скидки</button>
                    <button onclick="filterCategory('Смартфоны'); toggleMenu();" class="text-left px-4 py-3 rounded-xl font-semibold text-slate-700 hover:bg-slate-100">📱 Смартфоны</button>
                    <button onclick="filterCategory('Игры'); toggleMenu();" class="text-left px-4 py-3 rounded-xl font-semibold text-slate-700 hover:bg-slate-100">🎮 Игры и консоли</button>
                    <button onclick="filterCategory('Аудио'); toggleMenu();" class="text-left px-4 py-3 rounded-xl font-semibold text-slate-700 hover:bg-slate-100">🎧 Аудио</button>
                    <button onclick="filterCategory('Ноутбуки'); toggleMenu();" class="text-left px-4 py-3 rounded-xl font-semibold text-slate-700 hover:bg-slate-100">💻 Ноутбуки</button>
                    <button onclick="filterCategory('Умный дом'); toggleMenu();" class="text-left px-4 py-3 rounded-xl font-semibold text-slate-700 hover:bg-slate-100">🏠 Умный дом</button>
                </div>
            </div>
            <div class="text-xs text-slate-400 text-center py-4 border-t border-slate-100">technosteak.ru • 2026</div>
        </div>
    </div>

    <main class="max-w-7xl mx-auto px-4 py-6">
        <div class="bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-700 rounded-3xl p-6 md:p-10 text-white mb-6 shadow-xl relative overflow-hidden">
            <h1 class="text-2xl md:text-4xl font-black mb-3 tracking-tight">Выбирайте технику с умом, а не наугад</h1>
            <p class="text-blue-100 max-w-xl text-sm md:text-base leading-relaxed mb-5">Актуальные тренды, честные видеообзоры и прямые партнерские ссылки.</p>
            <div class="max-w-md">
                <input type="text" id="searchInput" placeholder="Поиск по технике, брендам, моделям..." class="w-full px-4 py-3 rounded-2xl text-slate-900 bg-white placeholder-slate-400 text-sm focus:outline-none focus:ring-4 focus:ring-blue-400/50 shadow-lg">
            </div>
        </div>

        <div class="flex items-center space-x-2 overflow-x-auto pb-4 no-scrollbar">
            <button onclick="filterCategory('all')" class="cat-btn px-4 py-2 rounded-xl text-xs md:text-sm font-bold bg-blue-600 text-white shadow-sm whitespace-nowrap">Все товары</button>
            <button onclick="filterCategory('juicy')" class="cat-btn px-4 py-2 rounded-xl text-xs md:text-sm font-semibold bg-white border border-slate-200 text-slate-700 hover:bg-slate-100 whitespace-nowrap">💥 Скидки</button>
            <button onclick="filterCategory('Смартфоны')" class="cat-btn px-4 py-2 rounded-xl text-xs md:text-sm font-semibold bg-white border border-slate-200 text-slate-700 hover:bg-slate-100 whitespace-nowrap">Смартфоны</button>
            <button onclick="filterCategory('Игры')" class="cat-btn px-4 py-2 rounded-xl text-xs md:text-sm font-semibold bg-white border border-slate-200 text-slate-700 hover:bg-slate-100 whitespace-nowrap">Игры и консоли</button>
            <button onclick="filterCategory('Аудио')" class="cat-btn px-4 py-2 rounded-xl text-xs md:text-sm font-semibold bg-white border border-slate-200 text-slate-700 hover:bg-slate-100 whitespace-nowrap">Аудио</button>
            <button onclick="filterCategory('Ноутбуки')" class="cat-btn px-4 py-2 rounded-xl text-xs md:text-sm font-semibold bg-white border border-slate-200 text-slate-700 hover:bg-slate-100 whitespace-nowrap">Ноутбуки</button>
            <button onclick="filterCategory('Умный дом')" class="cat-btn px-4 py-2 rounded-xl text-xs md:text-sm font-semibold bg-white border border-slate-200 text-slate-700 hover:bg-slate-100 whitespace-nowrap">Умный дом</button>
        </div>

        <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4" id="productsGrid"></div>
    </main>

    <script>
        let products = [];
        let currentCat = 'all';
        let searchQuery = '';

        function toggleMenu() {
            document.getElementById('mobileMenu').classList.toggle('hidden');
        }

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
            let list = products.filter(p => {
                let matchCat = currentCat === 'all' || (currentCat === 'juicy' ? p.is_juicy_discount : p.category === currentCat);
                let matchSearch = p.title.toLowerCase().includes(searchQuery.toLowerCase());
                return matchCat && matchSearch;
            });

            grid.innerHTML = list.map(item => `
                <div class="bg-white rounded-2xl border border-slate-200 p-4 shadow-sm flex flex-col justify-between">
                    <div>
                        <a href="product/${item.slug}/" class="block bg-slate-100 h-40 rounded-xl mb-3 overflow-hidden relative">
                            <img src="${item.image}" alt="${item.title}" class="w-full h-full object-cover">
                            <span class="absolute top-2 right-2 bg-slate-900/80 text-white text-[10px] font-bold px-2 py-0.5 rounded-md">★ ${item.rating}</span>
                        </a>
                        <span class="text-[10px] font-bold text-blue-600 bg-blue-50 px-2 py-0.5 rounded-md">${item.category}</span>
                        <a href="product/${item.slug}/" class="block font-bold text-sm mt-2 mb-1 text-slate-800 line-clamp-2 hover:text-blue-600">${item.title}</a>
                        <p class="text-slate-500 text-xs line-clamp-2 mb-3">${item.desc}</p>
                    </div>
                    <div>
                        <div class="text-base md:text-lg font-black text-slate-900 mb-2">${item.price_formatted}</div>
                        <a href="${item.market_link}" target="_blank" class="block w-full bg-blue-600 hover:bg-blue-700 text-white text-center py-2.5 rounded-xl text-xs font-bold transition shadow-sm">Смотреть на Маркете</a>
                    </div>
                </div>
            `).join('');
        }

        document.getElementById('searchInput').addEventListener('input', (e) => {
            searchQuery = e.target.value;
            renderProducts();
        });

        loadProducts();
    </script>
</body>
</html>"""
    with open(os.path.join(REPO_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(index_html)

    # Sitemap
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
    subprocess.run(["git", "commit", "-m", "Clean solid database, restore blue UI and burger [skip ci]"])
    subprocess.run(["git", "push", "origin", "main"])
    print("Done! Clean catalog restored.")

if __name__ == "__main__":
    save_and_build()
