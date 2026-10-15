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
            "price_status": "Скидка -25%",
            "rating": 4.9,
            "image": "https://images.unsplash.com/photo-1606813907291-d86efa9b94db?auto=format&fit=crop&w=500&q=80",
            "badge": "Хит продаж",
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
            "price_status": "Скидка -30%",
            "rating": 4.8,
            "image": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=500&q=80",
            "badge": "Скидка",
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

    # 1. ГЕНЕРАЦИЯ СТРАНИЦ ТОВАРОВ В КЛАССИЧЕСКОМ СИНЕМ СТИЛЕ
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
    <meta name="description" content="{p['desc']} Актуальная цена {p['price_formatted']}, рейтинг ★{p['rating']} и партнерские предложения на Яндекс Маркете.">
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
        <div class="bg-white rounded-3xl border border-slate-200 p-6 md:p-8 shadow-sm flex flex-col md:flex-row gap-8 items-center mb-8">
            <div class="w-full md:w-1/2 bg-slate-100 h-72 rounded-2xl overflow-hidden flex items-center justify-center relative">
                <img src="{p['image']}" alt="{p['title']}" class="w-full h-full object-cover">
                <span class="absolute top-3 right-3 bg-slate-900/80 backdrop-blur text-white text-xs font-bold px-3 py-1 rounded-lg">★ {p['rating']}</span>
            </div>
            <div class="w-full md:w-1/2 flex flex-col justify-between">
                <div>
                    <div class="flex items-center space-x-2 mb-2">
                        <span class="text-xs font-bold text-blue-600 bg-blue-50 px-3 py-1 rounded-md">{p['category']}</span>
                        <span class="text-xs font-bold text-slate-600 bg-slate-100 px-3 py-1 rounded-md">{p['badge']}</span>
                    </div>
                    <h1 class="text-2xl md:text-3xl font-black mb-2 text-slate-900">{p['title']}</h1>
                    <p class="text-slate-600 text-sm mb-4">{p['desc']}</p>
                </div>
                <div>
                    <div class="flex items-center justify-between mb-4">
                        <span class="text-2xl md:text-3xl font-black text-slate-900">{p['price_formatted']}</span>
                    </div>
                    <a href="{p['market_link']}" target="_blank" class="block w-full bg-blue-600 hover:bg-blue-700 text-white text-center py-3.5 rounded-2xl font-bold transition shadow-md mb-2">Смотреть на Маркете</a>
                    <a href="https://t.me/technosteak" target="_blank" class="block w-full bg-slate-100 hover:bg-slate-200 text-slate-700 text-center py-2.5 rounded-2xl font-bold text-xs transition">📢 Канал со скидками в Telegram</a>
                </div>
            </div>
        </div>
    </main>
</body>
</html>"""
        with open(os.path.join(p_folder, "index.html"), "w", encoding="utf-8") as f:
            f.write(p_html)

    # 2. ГЛАВНАЯ СТРАНИЦА В СИНЕМ ДИЗАЙНЕ С БУРГЕРОМ
    index_html = """<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ТехноСтейк — Каталог техники, честные обзоры и лучшие цены</title>
    <meta name="description" content="Независимый каталог техники с актуальными ценами, рейтингами и партнерскими предложениями Яндекс Маркета.">
    <meta name="yandex-verification" content="hlxuv94aba53ntlh" />
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-50 text-slate-900 font-sans antialiased">
    <!-- Шапка -->
    <header class="bg-white border-b border-slate-200 sticky top-0 z-50 shadow-xs">
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
    <div id="mobileMenu" class="fixed inset-0 z-50 bg-slate-900/50 backdrop-blur-sm hidden transition-opacity">
        <div class="bg-white w-4/5 max-w-xs h-full shadow-2xl p-6 flex flex-col justify-between transform -translate-x-full transition-transform duration-300" id="menuPanel">
            <div>
                <div class="flex items-center justify-between mb-8">
                    <div class="flex items-center space-x-2">
                        <span class="text-base font-black bg-blue-600 text-white px-2.5 py-1 rounded-lg">ТС</span>
                        <span class="font-bold text-lg">Категории</span>
                    </div>
                    <button onclick="toggleMenu()" class="p-2 text-slate-400 hover:text-slate-600">
                        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                        </svg>
                    </button>
                </div>
                <div class="flex flex-col space-y-2">
                    <button onclick="selectCategoryFromMenu('all')" class="text-left px-4 py-3 rounded-xl font-bold bg-blue-50 text-blue-600 transition">🔥 Все товары</button>
                    <button onclick="selectCategoryFromMenu('juicy')" class="text-left px-4 py-3 rounded-xl font-semibold text-slate-700 hover:bg-slate-100 transition">💥 Сочные скидки</button>
                    <button onclick="selectCategoryFromMenu('Смартфоны')" class="text-left px-4 py-3 rounded-xl font-semibold text-slate-700 hover:bg-slate-100 transition">📱 Смартфоны и гаджеты</button>
                    <button onclick="selectCategoryFromMenu('Игры')" class="text-left px-4 py-3 rounded-xl font-semibold text-slate-700 hover:bg-slate-100 transition">🎮 Игры и консоли</button>
                    <button onclick="selectCategoryFromMenu('Аудио')" class="text-left px-4 py-3 rounded-xl font-semibold text-slate-700 hover:bg-slate-100 transition">🎧 Аудио и звук</button>
                </div>
            </div>
            <div class="text-xs text-slate-400 text-center py-4 border-t border-slate-100">
                technosteak.ru • 2026
            </div>
        </div>
    </div>

    <!-- Главный баннер (Сине-фиолетовый) -->
    <main class="max-w-7xl mx-auto px-4 py-6">
        <div class="bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-700 rounded-3xl p-6 md:p-10 text-white mb-6 shadow-xl relative overflow-hidden">
            <div class="relative z-10">
                <h1 class="text-2xl md:text-4xl font-black mb-3 tracking-tight">Выбирайте технику с умом, а не наугад</h1>
                <p class="text-blue-100 max-w-xl text-sm md:text-base leading-relaxed mb-5">Актуальные тренды, честные видеообзоры и прямые партнерские ссылки.</p>
                <div class="max-w-md">
                    <input type="text" id="searchInput" placeholder="Поиск по технике, брендам, моделям..." class="w-full px-4 py-3 rounded-2xl text-slate-900 bg-white/95 backdrop-blur placeholder-slate-400 text-sm focus:outline-none focus:ring-4 focus:ring-blue-400/50 shadow-lg">
                </div>
            </div>
        </div>

        <!-- Кнопки категорий -->
        <div class="flex items-center space-x-2 overflow-x-auto pb-4 no-scrollbar">
            <button onclick="filterCategory('all')" class="cat-btn px-4 py-2 rounded-xl text-xs md:text-sm font-bold bg-blue-600 text-white transition shadow-sm whitespace-nowrap">Все товары</button>
            <button onclick="filterCategory('juicy')" class="cat-btn px-4 py-2 rounded-xl text-xs md:text-sm font-semibold bg-white border border-slate-200 text-slate-700 hover:bg-slate-100 transition whitespace-nowrap">💥 Скидки</button>
            <button onclick="filterCategory('Смартфоны')" class="cat-btn px-4 py-2 rounded-xl text-xs md:text-sm font-semibold bg-white border border-slate-200 text-slate-700 hover:bg-slate-100 transition whitespace-nowrap">Смартфоны</button>
            <button onclick="filterCategory('Игры')" class="cat-btn px-4 py-2 rounded-xl text-xs md:text-sm font-semibold bg-white border border-slate-200 text-slate-700 hover:bg-slate-100 transition whitespace-nowrap">Игры и консоли</button>
            <button onclick="filterCategory('Аудио')" class="cat-btn px-4 py-2 rounded-xl text-xs md:text-sm font-semibold bg-white border border-slate-200 text-slate-700 hover:bg-slate-100 transition whitespace-nowrap">Аудио</button>
        </div>

        <!-- Сетка товаров -->
        <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3 md:gap-6" id="productsGrid"></div>
    </main>

    <footer class="bg-white border-t border-slate-200 mt-20 py-8 text-center text-xs text-slate-500">
        <p>© 2026 ТехноСтейк (technosteak.ru). Все права защищены.</p>
    </footer>

    <script>
        let products = [];
        let currentCategory = 'all';
        let searchQuery = '';

        async function loadProducts() {
            try {
                const res = await fetch('products.json?' + new Date().getTime());
                const data = await res.json();
                products = data.products || [];
                renderProducts();
            } catch (e) { console.error(e); }
        }

        function toggleMenu() {
            const menu = document.getElementById('mobileMenu');
            const panel = document.getElementById('menuPanel');
            if (menu.classList.contains('hidden')) {
                menu.classList.remove('hidden');
                setTimeout(() => panel.classList.remove('-translate-x-full'), 10);
            } else {
                panel.classList.add('-translate-x-full');
                setTimeout(() => menu.classList.add('hidden'), 300);
            }
        }

        function selectCategoryFromMenu(cat) { filterCategory(cat); toggleMenu(); }

        function filterCategory(cat) {
            currentCategory = cat;
            document.querySelectorAll('.cat-btn').forEach(btn => {
                if (btn.textContent.includes(cat) || (cat === 'all' && btn.textContent.includes('Все'))) {
                    btn.className = "cat-btn px-4 py-2 rounded-xl text-xs md:text-sm font-bold bg-blue-600 text-white transition shadow-sm whitespace-nowrap";
                } else {
                    btn.className = "cat-btn px-4 py-2 rounded-xl text-xs md:text-sm font-semibold bg-white border border-slate-200 text-slate-700 hover:bg-slate-100 transition whitespace-nowrap";
                }
            });
            renderProducts();
        }

        function renderProducts() {
            const grid = document.getElementById('productsGrid');
            let filtered = products.filter(p => {
                let matchesCat = currentCategory === 'all' || p.category === currentCategory;
                if (currentCategory === 'juicy') matchesCat = p.is_juicy_discount;
                const matchesSearch = p.title.toLowerCase().includes(searchQuery.toLowerCase()) || p.desc.toLowerCase().includes(searchQuery.toLowerCase());
                return matchesCat && matchesSearch;
            });

            if (filtered.length === 0) {
                grid.innerHTML = '<div class="col-span-full py-16 text-center text-slate-400 font-medium">Ничего не найдено</div>';
                return;
            }

            grid.innerHTML = filtered.map(item => `
                <div class="bg-white rounded-2xl border border-slate-200 p-3 md:p-4 shadow-sm hover:shadow-md transition flex flex-col justify-between">
                    <div>
                        <a href="product/${item.slug}/" class="block bg-slate-100 h-36 md:h-48 rounded-xl mb-3 overflow-hidden relative">
                            <img src="${item.image}" alt="${item.title}" class="w-full h-full object-cover">
                            <span class="absolute top-2 right-2 bg-slate-900/70 backdrop-blur text-white text-[10px] font-bold px-2 py-0.5 rounded-md">★ ${item.rating}</span>
                        </a>
                        <span class="text-[10px] md:text-xs font-bold text-blue-600 bg-blue-50 px-2.5 py-1 rounded-md">${item.category}</span>
                        <a href="product/${item.slug}/" class="block font-bold text-sm md:text-base mt-2 mb-1 text-slate-800 line-clamp-2 hover:text-blue-600 transition">${item.title}</a>
                        <p class="text-slate-500 text-xs line-clamp-2 mb-3">${item.desc}</p>
                    </div>
                    <div>
                        <div class="flex items-center justify-between mb-3">
                            <span class="text-base md:text-xl font-black text-slate-900">${item.price_formatted}</span>
                        </div>
                        <a href="${item.market_link}" target="_blank" class="block w-full bg-blue-600 hover:bg-blue-700 text-white text-center py-2.5 rounded-xl text-xs md:text-sm font-bold transition shadow-sm">Смотреть на Маркете</a>
                    </div>
                </div>
            `).join('');
        }

        document.getElementById('searchInput').addEventListener('input', (e) => { searchQuery = e.target.value; renderProducts(); });
        loadProducts();
    </script>
</body>
</html>
"""
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
    subprocess.run(["git", "commit", "-m", "Restore original blue theme with burger menu and clean UI [skip ci]"])
    subprocess.run(["git", "push", "origin", "main"])
    print("Original blue theme restored successfully!")

if __name__ == "__main__":
    save_and_build()
