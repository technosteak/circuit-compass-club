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
            "old_price_formatted": "54 990 ₽",
            "price_status": "Исторический минимум (-9%)",
            "rating": 4.9,
            "image": "https://images.unsplash.com/photo-1606813907291-d86efa9b94db?auto=format&fit=crop&w=500&q=80",
            "badge": "Хит продаж",
            "video_type": "rutube",
            "video_id": "ee35f7959b4393663aa98b9f71c4c8da",
            "desc": "Мощная игровая консоль нового поколения с поддержкой 4K, трассировки лучей и сверхбыстрым SSD.",
            "verdict_plus": ["Мгновенная загрузка игр благодаря NVMe SSD", "Тихая система охлаждения", "Потрясающая отдача геймпада DualSense"],
            "verdict_minus": ["Крупные габариты корпуса", "Быстро забивается память под новые игры"],
            "cross_sell": ["Второй геймпад DualSense", "Зарядная станция", "Подписка PlayStation Plus 12 мес"],
            "versus_target": "xbox-series-x",
            "versus_title": "Xbox Series X 1TB",
            "reviews": [
                {"author": "Артем К.", "rating": 5, "date": "12 октября 2026", "text": "Брал ради эксклюзивов. Графика просто космос, загрузок вообще нет.", "plus": "Скорость, геймпад", "minus": "Размер"}
            ],
            "market_link": "https://market.yandex.ru"
        },
        {
            "id": 2,
            "title": "Xbox Series X 1TB",
            "slug": "xbox-series-x",
            "category": "Игры",
            "price": 48990,
            "price_formatted": "48 990 ₽",
            "old_price_formatted": "52 990 ₽",
            "price_status": "Лучшая цена за 3 месяца",
            "rating": 4.8,
            "image": "https://images.unsplash.com/photo-1621259182978-fbf93132d53d?auto=format&fit=crop&w=500&q=80",
            "badge": "Хит",
            "video_type": "rutube",
            "video_id": "ee35f7959b4393663aa98b9f71c4c8da",
            "desc": "Самая быстрая и мощная консоль Xbox с нативным разрешением 4K и подпиской Game Pass.",
            "verdict_plus": ["Обратная совместимость", "Тихая работа", "Удобная подписка Game Pass"],
            "verdict_minus": ["Мало эксклюзивов на старте"],
            "cross_sell": ["Аккумулятор для геймпада", "Беспроводная гарнитура Xbox"],
            "versus_target": "playbox-5-digital",
            "versus_title": "PlayBox 5 Digital",
            "reviews": [
                {"author": "Игорь М.", "rating": 5, "date": "10 октября 2026", "text": "Game Pass полностью окупает консоль. Мощная и тихая.", "plus": "Производительность", "minus": "Дизайн колонка"}
            ],
            "market_link": "https://market.yandex.ru"
        },
        {
            "id": 3,
            "title": "Aurora X15 Pro 256GB",
            "slug": "aurora-x15-pro",
            "category": "Смартфоны",
            "price": 79990,
            "price_formatted": "79 990 ₽",
            "old_price_formatted": "85 990 ₽",
            "price_status": "Скидка недели (-7%)",
            "rating": 4.8,
            "image": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?auto=format&fit=crop&w=500&q=80",
            "badge": "Рекомендуем",
            "video_type": "vk",
            "video_id": "-228965804_456239018",
            "desc": "Флагманский смартфон с 120 Гц AMOLED-экраном, топовым процессором и ночной съемкой.",
            "verdict_plus": ["Сочный AMOLED экран 120 Гц", "Превосходная ночная съемка", "Зарядка 120 Вт в комплекте"],
            "verdict_minus": ["Нет слота под microSD"],
            "cross_sell": ["Защитное стекло 9H", "Чехол MagSafe", "Быстрая беспроводная зарядка"],
            "versus_target": "",
            "versus_title": "",
            "reviews": [
                {"author": "Сергей В.", "rating": 5, "date": "14 октября 2026", "text": "Экран бомба, на солнце все видно. Камера снимает четко.", "plus": "Зарядка 15 минут", "minus": "Греется в играх"}
            ],
            "market_link": "https://market.yandex.ru"
        }
    ]

def save_and_build():
    products = load_database()

    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump({"updated_at": datetime.now().isoformat(), "products": products}, f, ensure_ascii=False, indent=4)

    product_dir = os.path.join(REPO_DIR, "product")
    versus_dir = os.path.join(REPO_DIR, "versus")
    os.makedirs(product_dir, exist_ok=True)
    os.makedirs(versus_dir, exist_ok=True)

    sitemap_urls = ["https://technosteak.ru/", "https://technosteak.ru/products.json"]

    # 1. ГЕНЕРАЦИЯ СТРАНИЦ ТОВАРОВ (с динамикой цен, доп. товарами и ссылками на Versus)
    for p in products:
        p_folder = os.path.join(product_dir, p["slug"])
        os.makedirs(p_folder, exist_ok=True)
        sitemap_urls.append(f"https://technosteak.ru/product/{p['slug']}/")

        if p.get("video_type") == "rutube":
            video_iframe = f'<iframe src="https://rutube.ru/play/embed/{p["video_id"]}" class="w-full h-64 md:h-96 rounded-2xl shadow-sm border border-slate-200" frameborder="0" allowfullscreen></iframe>'
        elif p.get("video_type") == "vk":
            video_iframe = f'<iframe src="https://vk.com/video_ext.php?oid={p["video_id"].split("_")[0]}&id={p["video_id"].split("_")[1]}&hash=1" class="w-full h-64 md:h-96 rounded-2xl shadow-sm border border-slate-200" frameborder="0" allowfullscreen></iframe>'
        else:
            video_iframe = '<div class="bg-slate-100 rounded-2xl h-64 flex items-center justify-center text-slate-400 font-medium">Видеообзор готовится</div>'

        plus_list = "".join([f'<li class="flex items-start space-x-2 text-sm text-slate-700"><span class="text-emerald-500 font-bold">✓</span><span>{item}</span></li>' for item in p.get("verdict_plus", [])])
        minus_list = "".join([f'<li class="flex items-start space-x-2 text-sm text-slate-700"><span class="text-rose-500 font-bold">✕</span><span>{item}</span></li>' for item in p.get("verdict_minus", [])])
        cross_sell_html = "".join([f'<span class="bg-slate-100 border border-slate-200 text-slate-700 text-xs font-semibold px-3 py-1.5 rounded-xl">+ {item}</span>' for item in p.get("cross_sell", [])])

        versus_block = ""
        if p.get("versus_target"):
            v_url = f"/versus/{p['slug']}-vs-{p['versus_target']}/"
            versus_block = f"""
            <div class="bg-gradient-to-r from-purple-900 to-indigo-900 rounded-3xl p-6 text-white mb-8 shadow-lg flex items-center justify-between">
                <div>
                    <span class="text-xs text-purple-300 uppercase tracking-widest font-bold">Сравнение моделей</span>
                    <h3 class="text-lg font-bold mt-1">{p['title']} VS {p['versus_title']}</h3>
                    <p class="text-xs text-purple-200 mt-1">Что лучше выбрать в 2026 году? Сравнили характеристики и цены.</p>
                </div>
                <a href="{v_url}" class="bg-white text-purple-900 px-4 py-2.5 rounded-xl font-bold text-xs whitespace-nowrap hover:bg-purple-100 transition shadow-sm">Смотреть сравнение →</a>
            </div>"""

        reviews_html = ""
        for r in p.get("reviews", []):
            reviews_html += f"""
            <div class="bg-slate-50 rounded-2xl p-4 border border-slate-200/60 mb-3">
                <div class="flex items-center justify-between mb-1"><span class="font-bold text-sm text-slate-900">{r['author']}</span><span class="text-xs text-slate-400">{r['date']}</span></div>
                <div class="text-amber-500 text-xs font-bold mb-2">★ {r['rating']}.0 / 5</div>
                <p class="text-slate-700 text-xs md:text-sm mb-2">{r['text']}</p>
            </div>"""

        p_html = f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Обзор и цена {p['title']} — История цен и отзывы | ТехноСтейк</title>
    <meta name="description" content="Честный обзор {p['title']}. Динамика цен, видеообзор, плюсы и минусы, отзывы. Покупка на Яндекс Маркете.">
    <meta name="yandex-verification" content="hlxuv94aba53ntlh" />
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-50 text-slate-900 font-sans antialiased">
    <header class="bg-white border-b border-slate-200 sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between">
            <a href="/" class="flex items-center space-x-2"><span class="text-lg font-black bg-blue-600 text-white px-3 py-1 rounded-xl">ТС</span><span class="text-lg font-bold">ТехноСтейк</span></a>
            <a href="/" class="text-xs font-bold text-blue-600 bg-blue-50 px-3 py-1.5 rounded-xl">← Главная</a>
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
                        <span class="text-xs font-bold text-amber-700 bg-amber-50 px-3 py-1 rounded-md">{p['badge']}</span>
                    </div>
                    <h1 class="text-2xl md:text-3xl font-black mb-2 text-slate-900">{p['title']}</h1>
                    <p class="text-slate-600 text-sm mb-4">{p['desc']}</p>
                </div>
                <div>
                    <!-- Динамика цен -->
                    <div class="bg-emerald-50 border border-emerald-200 rounded-2xl p-3 mb-4">
                        <div class="flex items-center justify-between mb-1">
                            <span class="text-xs font-bold text-emerald-800">🔥 {p['price_status']}</span>
                            <span class="text-xs line-through text-slate-400">{p.get('old_price_formatted', '')}</span>
                        </div>
                        <div class="text-2xl font-black text-slate-900">{p['price_formatted']}</div>
                    </div>
                    <a href="{p['market_link']}" target="_blank" rel="sponsored nofollow" class="block w-full bg-blue-600 hover:bg-blue-700 text-white text-center py-3.5 rounded-2xl font-bold transition shadow-md">Смотреть на Маркете</a>
                </div>
            </div>
        </div>

        {versus_block}

        <!-- Видеообзор -->
        <div class="bg-white rounded-3xl border border-slate-200 p-6 md:p-8 shadow-sm mb-8">
            <h2 class="text-xl font-bold mb-4">🎥 Честный видеообзор</h2>
            {video_iframe}
        </div>

        <!-- Экспертный вердикт -->
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

        <!-- Доп. товары / Аксессуары -->
        <div class="bg-white rounded-3xl border border-slate-200 p-6 md:p-8 shadow-sm mb-8">
            <h3 class="text-base font-bold text-slate-900 mb-3">🛒 С этим товаром чаще всего берут:</h3>
            <div class="flex flex-wrap gap-2">{cross_sell_html}</div>
        </div>

        <!-- Отзывы -->
        <div class="bg-white rounded-3xl border border-slate-200 p-6 md:p-8 shadow-sm">
            <h2 class="text-xl font-bold mb-4">💬 Отзывы покупателей</h2>
            {reviews_html}
        </div>
    </main>
    <footer class="bg-white border-t border-slate-200 mt-20 py-8 text-center text-xs text-slate-500">
        <p>© 2026 ТехноСтейк (technosteak.ru). Независимый гид по технике.</p>
    </footer>
</body>
</html>"""
        with open(os.path.join(p_folder, "index.html"), "w", encoding="utf-8") as f:
            f.write(p_html)

    # 2. ГЕНЕРАЦИЯ VERSUS-СТРАНИЦ (Сравнения)
    for p in products:
        if p.get("versus_target"):
            target_p = next((x for x in products if x["slug"] == p["versus_target"]), None)
            if target_p:
                v_slug = f"{p['slug']}-vs-{target_p['slug']}"
                v_folder = os.path.join(versus_dir, v_slug)
                os.makedirs(v_folder, exist_ok=True)
                sitemap_urls.append(f"https://technosteak.ru/versus/{v_slug}/")

                v_html = f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{p['title']} против {target_p['title']} — Что лучше выбрать в 2026? | ТехноСтейк</title>
    <meta name="description" content="Сравнение {p['title']} и {target_p['title']}. Подробный разбор характеристик, цен, плюсов и минусов. Выбираем лучшую покупку.">
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-50 text-slate-900 font-sans antialiased">
    <header class="bg-white border-b border-slate-200 sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between">
            <a href="/" class="flex items-center space-x-2"><span class="text-lg font-black bg-blue-600 text-white px-3 py-1 rounded-xl">ТС</span><span class="text-lg font-bold">ТехноСтейк</span></a>
            <a href="/" class="text-xs font-bold text-blue-600 bg-blue-50 px-3 py-1.5 rounded-xl">← Главная</a>
        </div>
    </header>

    <main class="max-w-5xl mx-auto px-4 py-8">
        <div class="text-center mb-8">
            <span class="text-xs font-bold uppercase tracking-widest text-blue-600 bg-blue-50 px-3 py-1 rounded-full">Битва устройств</span>
            <h1 class="text-2xl md:text-4xl font-black mt-3 text-slate-900">{p['title']} <span class="text-rose-600">VS</span> {target_p['title']}</h1>
            <p class="text-slate-500 text-sm mt-2">Сравнение цен, характеристик и пользовательского опыта</p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
            <!-- Товар A -->
            <div class="bg-white rounded-3xl border border-slate-200 p-6 shadow-sm flex flex-col justify-between">
                <div>
                    <img src="{p['image']}" alt="{p['title']}" class="w-full h-48 object-cover rounded-2xl mb-4">
                    <span class="text-xs font-bold text-blue-600 bg-blue-50 px-2.5 py-1 rounded-md">{p['category']}</span>
                    <h2 class="text-xl font-bold mt-2 text-slate-900">{p['title']}</h2>
                    <p class="text-xs text-slate-500 mt-2 leading-relaxed">{p['desc']}</p>
                </div>
                <div class="mt-6 border-t border-slate-100 pt-4">
                    <div class="text-xl font-black mb-3 text-slate-900">{p['price_formatted']}</div>
                    <a href="{p['market_link']}" target="_blank" class="block w-full bg-blue-600 hover:bg-blue-700 text-white text-center py-3 rounded-xl font-bold text-xs">Купить {p['title']}</a>
                </div>
            </div>

            <!-- Товар B -->
            <div class="bg-white rounded-3xl border border-slate-200 p-6 shadow-sm flex flex-col justify-between">
                <div>
                    <img src="{target_p['image']}" alt="{target_p['title']}" class="w-full h-48 object-cover rounded-2xl mb-4">
                    <span class="text-xs font-bold text-purple-600 bg-purple-50 px-2.5 py-1 rounded-md">{target_p['category']}</span>
                    <h2 class="text-xl font-bold mt-2 text-slate-900">{target_p['title']}</h2>
                    <p class="text-xs text-slate-500 mt-2 leading-relaxed">{target_p['desc']}</p>
                </div>
                <div class="mt-6 border-t border-slate-100 pt-4">
                    <div class="text-xl font-black mb-3 text-slate-900">{target_p['price_formatted']}</div>
                    <a href="{target_p['market_link']}" target="_blank" class="block w-full bg-purple-600 hover:bg-purple-700 text-white text-center py-3 rounded-xl font-bold text-xs">Купить {target_p['title']}</a>
                </div>
            </div>
        </div>
    </main>

    <footer class="bg-white border-t border-slate-200 py-8 text-center text-xs text-slate-500">
        <p>© 2026 ТехноСтейк (technosteak.ru). Интерактивные сравнения гаджетов.</p>
    </footer>
</body>
</html>"""
                with open(os.path.join(v_folder, "index.html"), "w", encoding="utf-8") as f:
                    f.write(v_html)

    # 3. ГЛАВНАЯ СТРАНИЦА C AI-КВИЗОМ
    index_html = """<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ТехноСтейк — Честные обзоры, сравнения и подбор техники</title>
    <meta name="description" content="Независимый экспертный гид по технике. Умный подбор устройств, динамика цен и честные отзывы.">
    <meta name="yandex-verification" content="hlxuv94aba53ntlh" />
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-50 text-slate-900 font-sans antialiased">
    <header class="bg-white border-b border-slate-200 sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between">
            <a href="/" class="flex items-center space-x-2"><span class="text-lg font-black bg-blue-600 text-white px-3 py-1 rounded-xl">ТС</span><span class="text-lg font-bold">ТехноСтейк</span></a>
            <span class="text-[11px] bg-emerald-50 text-emerald-700 border border-emerald-200 px-2.5 py-1 rounded-full font-semibold">Яндекс Партнер</span>
        </div>
    </header>

    <main class="max-w-7xl mx-auto px-4 py-6">
        <!-- AI КВИЗ И БАННЕР -->
        <div class="bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-700 rounded-3xl p-6 md:p-10 text-white mb-8 shadow-xl">
            <div class="max-w-2xl">
                <span class="text-xs bg-white/20 text-white font-bold px-3 py-1 rounded-full uppercase tracking-widest">AI Помощник 2026</span>
                <h1 class="text-2xl md:text-4xl font-black mt-3 mb-3">Не знаете, что выбрать? Подберем за 10 секунд!</h1>
                <p class="text-blue-100 text-sm mb-6">Укажите категорию и бюджет, а мы подберем лучшее устройство с честным рейтингом.</p>
                
                <div class="bg-white/10 backdrop-blur-md p-4 rounded-2xl flex flex-col md:flex-row gap-3">
                    <select id="quizBudget" class="bg-white text-slate-900 text-xs font-bold rounded-xl px-3 py-2.5 focus:outline-none">
                        <option value="all">Любой бюджет</option>
                        <option value="50000">До 50 000 ₽</option>
                        <option value="100000">До 100 000 ₽</option>
                    </select>
                    <button onclick="runQuiz()" class="bg-amber-400 hover:bg-amber-300 text-slate-900 font-black text-xs px-5 py-2.5 rounded-xl transition shadow-md">✨ Подобрать идеальное устройство</button>
                </div>
            </div>
        </div>

        <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4" id="productsGrid"></div>
    </main>

    <script>
        let products = [];
        async function loadProducts() {
            const res = await fetch('products.json?' + new Date().getTime());
            const data = await res.json();
            products = data.products || [];
            renderProducts(products);
        }

        function runQuiz() {
            const maxB = document.getElementById('quizBudget').value;
            let filtered = products;
            if (maxB !== 'all') {
                filtered = products.filter(p => p.price <= parseInt(maxB));
            }
            renderProducts(filtered);
        }

        function renderProducts(list) {
            const grid = document.getElementById('productsGrid');
            grid.innerHTML = list.map(item => `
                <div class="bg-white rounded-2xl border border-slate-200 p-4 shadow-sm hover:shadow-md transition flex flex-col justify-between">
                    <div>
                        <a href="product/${item.slug}/" class="block bg-slate-100 h-40 rounded-xl mb-3 overflow-hidden relative">
                            <img src="${item.image}" alt="${item.title}" class="w-full h-full object-cover">
                            <span class="absolute top-2 right-2 bg-slate-900/80 text-white text-[10px] font-bold px-2 py-0.5 rounded-md">★ ${item.rating}</span>
                        </a>
                        <span class="text-[10px] font-bold text-blue-600 bg-blue-50 px-2 py-0.5 rounded-md">${item.category}</span>
                        <a href="product/${item.slug}/" class="block font-bold text-sm mt-2 mb-1 text-slate-800 line-clamp-2 hover:text-blue-600">${item.title}</a>
                        <span class="text-[10px] font-bold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded-md block w-fit mb-3">${item.price_status || 'Отличная цена'}</span>
                    </div>
                    <div>
                        <div class="text-lg font-black text-slate-900 mb-2">${item.price_formatted}</div>
                        <a href="${item.market_link}" target="_blank" class="block w-full bg-blue-600 hover:bg-blue-700 text-white text-center py-2.5 rounded-xl text-xs font-bold">Смотреть на Маркете</a>
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

    # Sitemap
    sitemap_xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for url in sitemap_urls:
        sitemap_xml += f'  <url>\n    <loc>{url}</loc>\n    <changefreq>daily</changefreq>\n    <priority>0.8</priority>\n  </url>\n'
    sitemap_xml += '</urlset>'
    with open(os.path.join(REPO_DIR, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(sitemap_xml)

    open(os.path.join(REPO_DIR, ".nojekyll"), "w").close()
    open(os.path.join(REPO_DIR, "CNAME"), "w").write("technosteak.ru")

    # Git push
    os.chdir(REPO_DIR)
    subprocess.run(["git", "add", "."])
    subprocess.run(["git", "commit", "-m", "Mega-Update: AI Quiz, Price Dynamics, Versus pages & Cross-sell [skip ci]"])
    subprocess.run(["git", "push", "origin", "main"])
    print("Mega update successfully pushed to GitHub!")

if __name__ == "__main__":
    save_and_build()
