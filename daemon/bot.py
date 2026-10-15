import json
import os
import random
import subprocess
from datetime import datetime

REPO_DIR = "/var/www/technosteak"
JSON_PATH = os.path.join(REPO_DIR, "products.json")

# Категории и шаблоны для генерации сотен товаров
BRANDS = ["Xiaomi", "Samsung", "Apple", "Sony", "JBL", "Yandex", "PlayStation", "Xbox", "Asus", "Lenovo", "Honor", "Realme", "Dyson", "Dreame", "LG"]
CATEGORIES = ["Смартфоны", "Игры", "Аудио", "Умный дом", "Ноутбуки", "ТВ и Видео", "Автотовары", "Аксессуары"]

NOOTBOOK_MODELS = ["ProBook 15", "Gaming Nitro 5", "Air Ultra 14", "Legion 5", "ZenBook OLED"]
PHONE_MODELS = ["Redmi Note 13 Pro", "Galaxy A55 5G", "iPhone 15 Pro", "Poco X6 Pro", "Magic 6 Pro"]
AUDIO_MODELS = ["Tune 510BT", "AirPods Pro 2", "WH-1000XM4", "Boombox 3", "Buds FE"]
GAME_MODELS = ["DualSense Edge", "GamePass Ultimate", "Steam Deck OLED", "VR Headset 2", "Racing Wheel G29"]
HOME_MODELS = ["Станция Миди", "Робот-пылесос X10", "Умная лампочка RGB", "Даччик протечки", "Умная розетка"]

def load_database():
    if os.path.exists(JSON_PATH):
        try:
            with open(JSON_PATH, "r", encoding="utf-8") as f:
                return json.load(f).get("products", [])
        except:
            pass
    return []

def generate_next_product(existing_slugs, current_count):
    # Генератор случайных реалистичных моделей
    cat = random.choice(CATEGORIES)
    brand = random.choice(BRANDS)
    
    if cat == "Смартфоны":
        model = random.choice(PHONE_MODELS) + f" {random.choice(['128GB', '256GB', '512GB'])}"
        price = random.randint(15000, 120000)
        img = "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?auto=format&fit=crop&w=500&q=80"
    elif cat == "Игры":
        model = random.choice(GAME_MODELS)
        price = random.randint(4000, 60000)
        img = "https://images.unsplash.com/photo-1606813907291-d86efa9b94db?auto=format&fit=crop&w=500&q=80"
    elif cat == "Аудио":
        model = random.choice(AUDIO_MODELS)
        price = random.randint(2500, 45000)
        img = "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=500&q=80"
    elif cat == "Умный дом":
        model = random.choice(HOME_MODELS)
        price = random.randint(1500, 35000)
        img = "https://images.unsplash.com/photo-1558089687-f282ffcbc126?auto=format&fit=crop&w=500&q=80"
    else:
        model = random.choice(NOOTBOOK_MODELS)
        price = random.randint(35000, 150000)
        img = "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?auto=format&fit=crop&w=500&q=80"

    title = f"{brand} {model}"
    slug = f"{brand.lower()}-{model.lower().replace(' ', '-').replace('/', '')}-{current_count + 1}"

    if slug in existing_slugs:
        slug = f"{slug}-{random.randint(100, 999)}"

    is_juicy = random.choice([True, False, False])
    discount = random.randint(15, 35) if is_juicy else 0
    old_price = int(price * (1 + discount / 100)) if is_juicy else price

    return {
        "id": current_count + 1,
        "title": title,
        "slug": slug,
        "category": cat,
        "is_juicy_discount": is_juicy,
        "discount_percent": discount,
        "price": price,
        "price_formatted": f"{price:,}".replace(",", " ") + " ₽",
        "old_price_formatted": f"{old_price:,}".replace(",", " ") + " ₽",
        "price_status": f"🔥 Скидка -{discount}%" if is_juicy else "Выгодная цена",
        "rating": round(random.uniform(4.5, 5.0), 1),
        "image": img,
        "badge": f"-{discount}%" if is_juicy else "Хит",
        "video_type": "rutube",
        "video_id": "ee35f7959b4393663aa98b9f71c4c8da",
        "desc": f"Официальный гаджет {title} с гарантией и быстрой доставкой по всей России.",
        "verdict_plus": ["Официальная гарантия", "Высокий рейтинг покупателей", "Быстрая доставка"],
        "verdict_minus": ["Ограниченное количество по акции"],
        "market_link": "https://market.yandex.ru"
    }

def save_and_build():
    products = load_database()
    existing_slugs = {p["slug"] for p in products}

    # При каждом запуске добавляем 1-2 новых товара в каталог
    new_product = generate_next_product(existing_slugs, len(products))
    products.append(new_product)

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
    <title>Купить {p['title']} — Обзор и лучшая цена | ТехноСтейк</title>
    <meta name="description" content="{p['desc']} Цена: {p['price_formatted']}.">
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-50 text-slate-900 font-sans antialiased">
    <header class="bg-white border-b border-slate-200 sticky top-0 z-50 shadow-xs">
        <div class="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between">
            <a href="/" class="flex items-center space-x-2">
                <span class="text-lg font-black bg-blue-600 text-white px-3 py-1 rounded-xl">ТС</span>
                <span class="text-lg font-bold text-slate-900">ТехноСтейк</span>
            </a>
            <a href="https://t.me/technosteak" target="_blank" class="text-xs font-bold text-white bg-blue-500 px-3.5 py-2 rounded-xl">✈️ Telegram</a>
        </div>
    </header>
    <main class="max-w-4xl mx-auto px-4 py-8">
        <div class="bg-white rounded-3xl border border-slate-200 p-6 shadow-sm flex flex-col md:flex-row gap-8 items-center">
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

    # Главная страница (Синяя тема)
    index_html = """<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ТехноСтейк — Каталог техники и лучшие цены</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-50 text-slate-900 font-sans antialiased">
    <header class="bg-white border-b border-slate-200 sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between">
            <a href="/" class="flex items-center space-x-2">
                <span class="text-lg font-black bg-blue-600 text-white px-3 py-1 rounded-xl">ТС</span>
                <span class="text-lg font-bold">ТехноСтейк</span>
            </a>
            <a href="https://t.me/technosteak" target="_blank" class="text-xs font-bold text-white bg-blue-500 px-3.5 py-2 rounded-xl">Telegram</a>
        </div>
    </header>
    <main class="max-w-7xl mx-auto px-4 py-6">
        <div class="bg-gradient-to-r from-blue-600 to-indigo-700 rounded-3xl p-8 text-white mb-6">
            <h1 class="text-2xl md:text-4xl font-black mb-2">Выбирайте технику с умом</h1>
            <p class="text-blue-100 text-sm">Сотни проверенных товаров с ценами и обзорами.</p>
        </div>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4" id="productsGrid"></div>
    </main>
    <script>
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
    subprocess.run(["git", "commit", "-m", f"Auto-add new product. Total: {len(products)} [skip ci]"])
    subprocess.run(["git", "push", "origin", "main"])
    print(f"Build complete. Total products: {len(products)}")

if __name__ == "__main__":
    save_and_build()
