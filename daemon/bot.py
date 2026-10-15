import json
import os
import subprocess
from datetime import datetime

REPO_DIR = "/var/www/technosteak"
JSON_PATH = os.path.join(REPO_DIR, "products.json")

def load_database():
    if os.path.exists(JSON_PATH):
        try:
            with open(JSON_PATH, "r", encoding="utf-8") as f:
                return json.load(f).get("products", [])
        except:
            pass
    return []

def save_and_build():
    products = load_database()
    
    # Большой пул заготовок для автоматического расширения каталога
    expansion_pool = [
        {"title": "PlayBox 5 Digital Edition", "slug": "playbox-5-digital", "category": "Игры", "is_juicy_discount": True, "discount_percent": 25, "price": 49990, "old_price_formatted": "66 500 ₽", "price_status": "Скидка -25%", "rating": 4.9, "image": "https://images.unsplash.com/photo-1606813907291-d86efa9b94db?auto=format&fit=crop&w=500&q=80", "badge": "Хит", "desc": "Мощная игровая консоль нового поколения с поддержкой 4K и SSD."},
        {"title": "SonicWave ANC Headphones", "slug": "sonicwave-anc", "category": "Аудио", "is_juicy_discount": True, "discount_percent": 30, "price": 13990, "old_price_formatted": "19 990 ₽", "price_status": "Скидка -30%", "rating": 4.8, "image": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=500&q=80", "badge": "Скидка", "desc": "Беспроводные наушники с активным шумоподавлением и чистым басом."},
        {"title": "Aurora X15 Pro 256GB", "slug": "aurora-x15-pro", "category": "Смартфоны", "is_juicy_discount": False, "discount_percent": 0, "price": 79990, "old_price_formatted": "85 990 ₽", "price_status": "Скидка недели", "rating": 4.8, "image": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?auto=format&fit=crop&w=500&q=80", "badge": "Флагман", "desc": "Флагманский смартфон с 120 Гц AMOLED-экраном и топовой камерой."},
        {"title": "Nintendo Switch OLED", "slug": "nintendo-switch-oled", "category": "Игры", "is_juicy_discount": True, "discount_percent": 15, "price": 31990, "old_price_formatted": "37 990 ₽", "price_status": "Скидка -15%", "rating": 4.7, "image": "https://images.unsplash.com/photo-1578303512597-81e6cc155b3e?auto=format&fit=crop&w=500&q=80", "badge": "Хит", "desc": "Яркий 7-дюймовый OLED-экран для портативного гейминга."},
        {"title": "JBL Charge 5 Speaker", "slug": "jbl-charge-5", "category": "Аудио", "is_juicy_discount": False, "discount_percent": 0, "price": 13990, "old_price_formatted": "15 990 ₽", "price_status": "Популярное", "rating": 4.9, "image": "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?auto=format&fit=crop&w=500&q=80", "badge": "Топ", "desc": "Мощная влагозащищенная портативная колонка с PowerBank."},
        {"title": "Robot Vacuum S10", "slug": "robot-vacuum-s10", "category": "Умный дом", "is_juicy_discount": True, "discount_percent": 20, "price": 22990, "old_price_formatted": "28 990 ₽", "price_status": "Скидка -20%", "rating": 4.6, "image": "https://images.unsplash.com/photo-1518640467707-6811f4a6ab73?auto=format&fit=crop&w=500&q=80", "badge": "Акция", "desc": "Робот-пылесос с лазерной навигацией и влажной уборкой."},
        {"title": "MacBook Air 13 M2", "slug": "macbook-air-13-m2", "category": "Смартфоны", "is_juicy_discount": False, "discount_percent": 0, "price": 114990, "old_price_formatted": "124 990 ₽", "price_status": "Новинка", "rating": 5.0, "image": "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?auto=format&fit=crop&w=500&q=80", "badge": "Премиум", "desc": "Легкий и невероятно быстрый ноутбук на базе чипа M2."},
        {"title": "Sony WH-1000XM5", "slug": "sony-wh-1000xm5", "category": "Аудио", "is_juicy_discount": True, "discount_percent": 18, "price": 32990, "old_price_formatted": "39 990 ₽", "price_status": "Скидка -18%", "rating": 4.9, "image": "https://images.unsplash.com/photo-1546435770-a3e426bf472b?auto=format&fit=crop&w=500&q=80", "badge": "Топ звук", "desc": "Наушники с эталонным активным шумоподавлением."}
    ]

    existing_slugs = {p["slug"] for p in products}
    added_count = 0
    for item in expansion_pool:
        if item["slug"] not in existing_slugs:
            new_p = item.copy()
            new_p["id"] = max([p["id"] for p in products], default=0) + 1
            new_p["price_formatted"] = f"{new_p['price']:,}".replace(",", " ") + " ₽"
            new_p["market_link"] = "https://market.yandex.ru"
            new_p["video_type"] = "rutube"
            new_p["video_id"] = "ee35f7959b4393663aa98b9f71c4c8da"
            new_p["verdict_plus"] = ["Отличное соотношение цены и качества", "Надежная сборка", "Положительные отзывы"]
            new_p["verdict_minus"] = ["Быстро раскупают по акции"]
            new_p["reviews"] = [{"author": "Покупатель", "rating": 5, "date": "Сегодня", "text": "Отличный товар, доставили быстро.", "plus": "Качество", "minus": "Нет"}]
            products.append(new_p)
            added_count += 1
            break # Добавляем по одному за цикл, чтобы каталог рос плавно каждый час

    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump({"updated_at": datetime.now().isoformat(), "products": products}, f, ensure_ascii=False, indent=4)

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
    <title>Купить {p['title']} — Обзор, цена и характеристики | ТехноСтейк</title>
    <meta name="description" content="{p['desc']} Актуальная цена {p['price_formatted']}, рейтинг ★{p['rating']} и партнерские предложения.">
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
            <a href="https://t.me/technosteak" target="_blank" class="text-xs font-bold text-white bg-blue-500 hover:bg-blue-600 px-3.5 py-2 rounded-xl transition">✈️ Наш Telegram</a>
        </div>
    </header>
    <main class="max-w-4xl mx-auto px-4 py-8">
        <div class="bg-white rounded-3xl border border-slate-200 p-6 md:p-8 shadow-sm flex flex-col md:flex-row gap-8 items-center mb-8">
            <div class="w-full md:w-1/2 bg-slate-100 h-72 rounded-2xl overflow-hidden flex items-center justify-center relative">
                <img src="{p['image']}" alt="{p['title']}" class="w-full h-full object-cover">
                <span class="absolute top-3 right-3 bg-slate-900/80 text-white text-xs font-bold px-3 py-1 rounded-lg">★ {p['rating']}</span>
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
                </div>
            </div>
        </div>
    </main>
</body>
</html>"""
        with open(os.path.join(p_folder, "index.html"), "w", encoding="utf-8") as f:
            f.write(p_html)

    # Главная страница (оставляем твой любимый синий стиль с бургером)
    with open(os.path.join(REPO_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write("""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ТехноСтейк — Каталог техники, честные обзоры и лучшие цены</title>
    <meta name="yandex-verification" content="hlxuv94aba53ntlh" />
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-50 text-slate-900 font-sans antialiased">
    <header class="bg-white border-b border-slate-200 sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between">
            <div class="flex items-center space-x-3">
                <button onclick="toggleMenu()" class="p-2 rounded-xl bg-slate-100 text-slate-700">☰</button>
                <a href="/" class="flex items-center space-x-2">
                    <span class="text-lg font-black bg-blue-600 text-white px-3 py-1 rounded-xl">ТС</span>
                    <span class="text-lg font-bold">ТехноСтейк</span>
                </a>
            </div>
            <a href="https://t.me/technosteak" target="_blank" class="text-xs font-bold text-white bg-blue-500 px-3.5 py-2 rounded-xl">Telegram</a>
        </div>
    </header>
    <div id="mobileMenu" class="fixed inset-0 z-50 bg-slate-900/50 hidden">
        <div class="bg-white w-4/5 max-w-xs h-full p-6" id="menuPanel">
            <button onclick="toggleMenu()" class="mb-4 font-bold">✕ Закрыть</button>
            <div class="flex flex-col space-y-3">
                <a href="/" class="font-bold text-blue-600">🔥 Все товары</a>
                <a href="https://t.me/technosteak" target="_blank" class="font-semibold text-slate-700">✈️ Наш канал</a>
            </div>
        </div>
    </div>
    <main class="max-w-7xl mx-auto px-4 py-6">
        <div class="bg-gradient-to-r from-blue-600 to-indigo-700 rounded-3xl p-8 text-white mb-6">
            <h1 class="text-2xl md:text-4xl font-black mb-2">Выбирайте технику с умом</h1>
            <p class="text-blue-100 text-sm">Актуальные тренды, обзоры и лучшие цены.</p>
        </div>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4" id="productsGrid"></div>
    </main>
    <script>
        function toggleMenu() {
            const m = document.getElementById('mobileMenu');
            m.classList.toggle('hidden');
        }
        async function load() {
            const res = await fetch('products.json?' + new Date().getTime());
            const data = await res.json();
            const grid = document.getElementById('productsGrid');
            grid.innerHTML = (data.products || []).map(item => `
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
        load();
    </script>
</body>
</html>""")

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
    subprocess.run(["git", "commit", "-m", f"Auto-expand catalog, added new items [skip ci]"])
    subprocess.run(["git", "push", "origin", "main"])
    print(f"Build complete. Total products: {len(products)}")

if __name__ == "__main__":
    save_and_build()
