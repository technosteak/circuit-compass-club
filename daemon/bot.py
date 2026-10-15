import json
import os
import random
import subprocess
from datetime import datetime

REPO_DIR = "/var/www/technosteak"
JSON_PATH = os.path.join(REPO_DIR, "products.json")

# Четкие базы данных без пересечений мусора
CATALOG_POOL = [
    {"title": "PlayBox 5 Digital Edition", "slug": "playbox-5-digital", "category": "Игры", "price": 49990, "image": "https://images.unsplash.com/photo-1606813907291-d86efa9b94db?auto=format&fit=crop&w=500&q=80", "desc": "Мощная игровая консоль нового поколения с поддержкой 4K и SSD."},
    {"title": "Xbox Series X 1TB", "slug": "xbox-series-x", "category": "Игры", "price": 52990, "image": "https://images.unsplash.com/photo-1621259182978-fbf93132d53d?auto=format&fit=crop&w=500&q=80", "desc": "Флагманская консоль Microsoft с высокой производительностью."},
    {"title": "SonicWave ANC Headphones", "slug": "sonicwave-anc", "category": "Аудио", "price": 13990, "image": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=500&q=80", "desc": "Беспроводные наушники с активным шумоподавлением и чистым басом."},
    {"title": "JBL Charge 5 Speaker", "slug": "jbl-charge-5", "category": "Аудио", "price": 14990, "image": "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?auto=format&fit=crop&w=500&q=80", "desc": "Мощная влагозащищенная портативная колонка."},
    {"title": "Aurora X15 Pro 256GB", "slug": "aurora-x15-pro", "category": "Смартфоны", "price": 79990, "image": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?auto=format&fit=crop&w=500&q=80", "desc": "Флагманский смартфон с 120 Гц AMOLED-экраном."},
    {"title": "Xiaomi Redmi Note 13 Pro", "slug": "redmi-note-13-pro", "category": "Смартфоны", "price": 28990, "image": "https://images.unsplash.com/photo-1598327105666-5b89351aff97?auto=format&fit=crop&w=500&q=80", "desc": "Народный смартфон с камерой 200 Мп и быстрой зарядкой."},
    {"title": "MacBook Air 13 M2", "slug": "macbook-air-13-m2", "category": "Ноутбуки", "price": 114990, "image": "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?auto=format&fit=crop&w=500&q=80", "desc": "Легкий и невероятно быстрый ноутбук на базе чипа M2."},
    {"title": "Asus TUF Gaming A15", "slug": "asus-tuf-gaming-a15", "category": "Ноутбуки", "price": 89990, "image": "https://images.unsplash.com/photo-1603302576837-37561b2e2302?auto=format&fit=crop&w=500&q=80", "desc": "Надежный игровой ноутбук с мощной видеокартой."},
    {"title": "Yandex Station Midi", "slug": "yandex-station-midi", "category": "Умный дом", "price": 14990, "image": "https://images.unsplash.com/photo-1543512214-318c7553f230?auto=format&fit=crop&w=500&q=80", "desc": "Умная колонка с голосовым помощником Алисой и LED-дисплеем."},
    {"title": "Robot Vacuum Cleaner S10", "slug": "robot-vacuum-s10", "category": "Умный дом", "price": 22990, "image": "https://images.unsplash.com/photo-1518640467707-6811f4a6ab73?auto=format&fit=crop&w=500&q=80", "desc": "Робот-пылесос с лазерной навигацией и влажной уборкой."}
]

def load_database():
    if os.path.exists(JSON_PATH):
        try:
            with open(JSON_PATH, "r", encoding="utf-8") as f:
                return json.load(f).get("products", [])
        except:
            pass
    return CATALOG_POOL[:4]

def save_and_build():
    products = load_database()
    existing_slugs = {p["slug"] for p in products}

    # Добавляем следующий логичный товар из пула, если есть новые
    for item in CATALOG_POOL:
        if item["slug"] not in existing_slugs:
            new_p = item.copy()
            new_p["id"] = max([p["id"] for p in products], default=0) + 1
            is_juicy = random.choice([True, False])
            discount = random.randint(15, 30) if is_juicy else 0
            old_price = int(new_p["price"] * (1 + discount / 100)) if is_juicy else new_p["price"]
            
            new_p["is_juicy_discount"] = is_juicy
            new_p["discount_percent"] = discount
            new_p["price_formatted"] = f"{new_p['price']:,}".replace(",", " ") + " ₽"
            new_p["old_price_formatted"] = f"{old_price:,}".replace(",", " ") + " ₽"
            new_p["price_status"] = f"🔥 Скидка -{discount}%" if is_juicy else "Лучшая цена"
            new_p["rating"] = round(random.uniform(4.7, 5.0), 1)
            new_p["badge"] = f"-{discount}%" if is_juicy else "Хит"
            new_p["market_link"] = "https://market.yandex.ru"
            products.append(new_p)
            break

    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump({"updated_at": datetime.now().isoformat(), "products": products}, f, ensure_ascii=False, indent=4)

    # Генерация SEO-страниц
    product_dir = os.path.join(REPO_DIR, "product")
    os.makedirs(product_dir, exist_ok=True)
    sitemap_urls = ["https://technosteak.ru/", "https://technosteak.ru/products.json"]

    for p in products:
        p_folder = os.path.join(product_dir, p["slug"])
        os.makedirs(p_folder, exist_ok=True)
        sitemap_urls.append(f"https://technosteak.ru/product/{p['slug']}/")

        p_html = f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Купить {p['title']} — Обзор и цена | ТехноСтейк</title>
    <meta name="description" content="{p['desc']} Цена: {p['price_formatted']}.">
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-50 text-slate-900 font-sans antialiased">
    <header class="bg-white border-b border-slate-200 sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between">
            <a href="/" class="flex items-center space-x-2">
                <span class="text-lg font-black bg-blue-600 text-white px-3 py-1 rounded-xl">ТС</span>
                <span class="text-lg font-bold">ТехноСтейк</span>
            </a>
            <a href="https://t.me/technosteak" target="_blank" class="text-xs font-bold text-white bg-blue-500 px-3.5 py-2 rounded-xl">✈️ Telegram</a>
        </div>
    </header>
    <main class="max-w-4xl mx-auto px-4 py-8">
        <div class="bg-white rounded-3xl border border-slate-200 p-6 md:p-8 shadow-sm flex flex-col md:flex-row gap-8 items-center">
            <img src="{p['image']}" class="w-full md:w-1/2 h-72 object-cover rounded-2xl">
            <div class="w-full md:w-1/2">
                <span class="text-xs font-bold text-blue-600 bg-blue-50 px-3 py-1 rounded-md">{p['category']}</span>
                <h1 class="text-2xl font-black mt-2 mb-2">{p['title']}</h1>
                <p class="text-slate-600 text-sm mb-4">{p['desc']}</p>
                <div class="text-2xl font-black text-slate-900 mb-4">{p['price_formatted']}</div>
                <a href="{p['market_link']}" target="_blank" class="block w-full bg-blue-600 text-white text-center py-3 rounded-xl font-bold">Смотреть на Маркете</a>
            </div>
        </div>
    </main>
</body>
</html>"""
        with open(os.path.join(p_folder, "index.html"), "w", encoding="utf-8") as f:
            f.write(p_html)

    # Главная страница (Классический синий стиль + Бургер-меню + Категории)
    index_html = """<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ТехноСтейк — Каталог техники, честные обзоры и лучшие цены</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-50 text-slate-900 font-sans antialiased">
    <!-- Шапка с бургером -->
    <header class="bg-white border-b border-slate-200 sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between">
            <div class="flex items-center space-x-3">
                <button onclick="toggleMenu()" class="p-2 rounded-xl bg-slate-100 text-slate-700 hover:bg-slate-200 transition">☰</button>
                <a href="/" class="flex items-center space-x-2">
                    <span class="text-lg font-black bg-blue-600 text-white px-3 py-1 rounded-xl">ТС</span>
                    <span class="text-lg font-bold">ТехноСтейк</span>
                </a>
            </div>
            <a href="https://t.me/technosteak" target="_blank" class="text-xs font-bold text-white bg-blue-500 px-3.5 py-2 rounded-xl">✈️ Telegram</a>
        </div>
    </header>

    <!-- Выдвижное бургер-меню -->
    <div id="mobileMenu" class="fixed inset-0 z-50 bg-slate-900/50 hidden">
        <div class="bg-white w-4/5 max-w-xs h-full p-6 shadow-2xl flex flex-col justify-between">
            <div>
                <div class="flex items-center justify-between mb-6">
                    <span class="font-bold text-lg">Категории</span>
                    <button onclick="toggleMenu()" class="text-slate-500 font-bold text-lg">✕</button>
                </div>
                <div class="flex flex-col space-y-2">
                    <button onclick="filterCategory('all'); toggleMenu();" class="text-left px-4 py-2.5 rounded-xl font-bold bg-blue-50 text-blue-600">🔥 Все товары</button>
                    <button onclick="filterCategory('juicy'); toggleMenu();" class="text-left px-4 py-2.5 rounded-xl font-semibold text-slate-700 hover:bg-slate-100">💥 Сочные скидки</button>
                    <button onclick="filterCategory('Смартфоны'); toggleMenu();" class="text-left px-4 py-2.5 rounded-xl font-semibold text-slate-700 hover:bg-slate-100">📱 Смартфоны</button>
                    <button onclick="filterCategory('Игры'); toggleMenu();" class="text-left px-4 py-2.5 rounded-xl font-semibold text-slate-700 hover:bg-slate-100">🎮 Игры и приставки</button>
                    <button onclick="filterCategory('Аудио'); toggleMenu();" class="text-left px-4 py-2.5 rounded-xl font-semibold text-slate-700 hover:bg-slate-100">🎧 Аудио</button>
                    <button onclick="filterCategory('Ноутбуки'); toggleMenu();" class="text-left px-4 py-2.5 rounded-xl font-semibold text-slate-700 hover:bg-slate-100">💻 Ноутбуки</button>
                    <button onclick="filterCategory('Умный дом'); toggleMenu();" class="text-left px-4 py-2.5 rounded-xl font-semibold text-slate-700 hover:bg-slate-100">🏠 Умный дом</button>
                </div>
            </div>
            <div class="text-xs text-slate-400 text-center">technosteak.ru • 2026</div>
        </div>
    </div>

    <main class="max-w-7xl mx-auto px-4 py-6">
        <div class="bg-gradient-to-r from-blue-600 to-indigo-700 rounded-3xl p-6 md:p-8 text-white mb-6 shadow-md">
            <h1 class="text-2xl md:text-3xl font-black mb-2">Выбирайте технику с умом</h1>
            <p class="text-blue-100 text-sm mb-4">Качественные гаджеты, проверенные обзоры и лучшие цены.</p>
            <input type="text" id="searchInput" placeholder="Поиск по каталогу..." class="w-full px-4 py-3 rounded-2xl text-slate-900 bg-white placeholder-slate-400 text-sm focus:outline-none">
        </div>

        <!-- Кнопки быстрого фильтра -->
        <div class="flex items-center space-x-2 overflow-x-auto pb-4 no-scrollbar">
            <button onclick="filterCategory('all')" class="cat-btn px-4 py-2 rounded-xl text-xs font-bold bg-blue-600 text-white whitespace-nowrap">Все товары</button>
            <button onclick="filterCategory('juicy')" class="cat-btn px-4 py-2 rounded-xl text-xs font-semibold bg-white border border-slate-200 text-slate-700 whitespace-nowrap">💥 Скидки</button>
            <button onclick="filterCategory('Смартфоны')" class="cat-btn px-4 py-2 rounded-xl text-xs font-semibold bg-white border border-slate-200 text-slate-700 whitespace-nowrap">Смартфоны</button>
            <button onclick="filterCategory('Игры')" class="cat-btn px-4 py-2 rounded-xl text-xs font-semibold bg-white border border-slate-200 text-slate-700 whitespace-nowrap">Игры</button>
            <button onclick="filterCategory('Аудио')" class="cat-btn px-4 py-2 rounded-xl text-xs font-semibold bg-white border border-slate-200 text-slate-700 whitespace-nowrap">Аудио</button>
            <button onclick="filterCategory('Ноутбуки')" class="cat-btn px-4 py-2 rounded-xl text-xs font-semibold bg-white border border-slate-200 text-slate-700 whitespace-nowrap">Ноутбуки</button>
            <button onclick="filterCategory('Умный дом')" class="cat-btn px-4 py-2 rounded-xl text-xs font-semibold bg-white border border-slate-200 text-slate-700 whitespace-nowrap">Умный дом</button>
        </div>

        <div class="grid grid-cols-2 md:grid-cols-4 gap-4" id="productsGrid"></div>
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
            render();
        }

        function filterCategory(cat) {
            currentCat = cat;
            render();
        }

        function render() {
            const grid = document.getElementById('productsGrid');
            let list = products.filter(p => {
                let matchCat = currentCat === 'all' || (currentCat === 'juicy' ? p.is_juicy_discount : p.category === currentCat);
                let matchSearch = p.title.toLowerCase().includes(searchQuery.toLowerCase());
                return matchCat && matchSearch;
            });

            grid.innerHTML = list.map(item => `
                <div class="bg-white rounded-2xl border border-slate-200 p-4 shadow-sm flex flex-col justify-between">
                    <div>
                        <a href="product/${item.slug}/"><img src="${item.image}" class="w-full h-36 object-cover rounded-xl mb-2"></a>
                        <span class="text-[10px] font-bold text-blue-600 bg-blue-50 px-2 py-0.5 rounded-md">${item.category}</span>
                        <a href="product/${item.slug}/" class="block font-bold text-sm mt-1 text-slate-800 line-clamp-2">${item.title}</a>
                    </div>
                    <div class="mt-4">
                        <div class="text-base font-black text-slate-900 mb-2">${item.price_formatted}</div>
                        <a href="${item.market_link}" target="_blank" class="block w-full bg-blue-600 text-white text-center py-2 rounded-xl text-xs font-bold">На Маркет</a>
                    </div>
                </div>
            `).join('');
        }

        document.getElementById('searchInput').addEventListener('input', (e) => {
            searchQuery = e.target.value;
            render();
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
    subprocess.run(["git", "commit", "-m", "Fix product data consistency and restore burger menu [skip ci]"])
    subprocess.run(["git", "push", "origin", "main"])
    print("Fixed! Burger menu and clean product catalog restored.")

if __name__ == "__main__":
    save_and_build()
