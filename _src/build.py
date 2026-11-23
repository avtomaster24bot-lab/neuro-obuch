# -*- coding: utf-8 -*-
"""Сборка сайта: python3 _src/build.py (из корня репозитория). Генерирует HTML-страницы и SVG-схемы."""
import os, sys, json, html
sys.path.insert(0, os.path.dirname(__file__))
from data import BRAND, TAGLINE, BASE_URL, COURSES, BUNDLE, FAQ
import svg
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V = "4"
E = html.escape

def rub(n): return f"{n:,}".replace(",", " ") + " ₽"

def write(path, s):
    p = os.path.join(ROOT, path); os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8").write(s)

def page(path, title, desc, body, root, mbar=True, og="assets/img/hero.jpg"):
    url = BASE_URL + path.replace("index.html", "")
    nav = f'''<a href="{root}kursy/">Курсы</a><a href="{root}urok/formula-prompta/">Бесплатный урок</a><a href="{root}novoe/">Новое каждый день</a><a href="{root}gaydy/">Гайды</a><a href="{root}#faq">Вопросы</a><a class="btn sm tg" data-link="channel" href="#">Telegram-канал</a>'''
    mb = f'<div class="mbar"><a class="btn ghost" href="{root}urok/formula-prompta/">Бесплатный урок</a><a class="btn" href="{root}kursy/">Выбрать курс</a></div>' if mbar else ""
    return f'''<!doctype html>
<html lang="ru"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{E(title)}</title><meta name="description" content="{E(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website"><meta property="og:locale" content="ru_RU"><meta property="og:site_name" content="{BRAND}">
<meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE_URL}{og}"><meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#07071a">
<link rel="icon" href="{root}assets/img/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&family=Unbounded:wght@500;600;700&display=swap&subset=cyrillic" rel="stylesheet">
<link rel="stylesheet" href="{root}assets/css/style.css?v={V}">
</head><body>
<header class="top"><div class="wrap">
<a class="logo" href="{root}"><span class="logo-mark" aria-hidden="true">✦</span><span>{BRAND}<small>{TAGLINE}</small></span></a>
<button class="burger" aria-label="Меню" aria-expanded="false">☰</button>
<nav class="nav">{nav}</nav></div></header>
<main>{body}</main>
<footer><div class="wrap cols">
<div><a class="logo" href="{root}" style="opacity:1"><span class="logo-mark">✦</span><span>{BRAND}<small>{TAGLINE}</small></span></a>
<p style="margin-top:12px">Учим пользоваться нейросетями с нуля до дохода: тексты, картинки, видео, голос, учёт и свои ИИ-помощники.</p>
<div class="soc"><a data-link="channel" href="#">Telegram</a><a data-link="youtube" data-social href="#">YouTube</a><a data-link="instagram" data-social href="#">Instagram</a><a data-link="tiktok" data-social href="#">TikTok</a><a data-link="vk" data-social href="#">VK</a></div></div>
<div><b style="color:var(--txt)">Курсы</b><br><br>{"".join(f'<a href="{root}kursy/{c["slug"]}/">{E(c["title"])}</a>' for c in COURSES[:4])}</div>
<div><b style="color:var(--txt)">&nbsp;</b><br><br>{"".join(f'<a href="{root}kursy/{c["slug"]}/">{E(c["title"])}</a>' for c in COURSES[4:])}<a href="{root}kursy/#tarify">Тарифы</a></div>
<div><b style="color:var(--txt)">Бесплатно</b><br><br><a href="{root}urok/formula-prompta/">Урок «Формула промпта»</a><a href="{root}gaydy/">Гайды PDF</a><a href="{root}novoe/">Новое каждый день</a><a data-link="contact" href="#">Написать нам</a></div>
</div><div class="wrap"><p class="small" style="margin-top:26px">© 2026 {BRAND}. Цены на сайте предварительные, сайт не является публичной офертой. Названия сервисов принадлежат их владельцам; школа не аффилирована с ними. Доступность зарубежных сервисов зависит от страны.</p></div></footer>
{mb}
<script src="{root}config.js?v={V}"></script><script src="{root}assets/js/app.js?v={V}"></script>
</body></html>'''

def ccard(c, root):
    return f'''<a class="card ccard glow reveal" href="{root}kursy/{c["slug"]}/"><img src="{root}assets/img/{c["img"]}.webp" alt="Иллюстрация к курсу «{E(c["title"])}»" loading="lazy" width="1152" height="864">
<div class="body"><div class="meta"><span class="tag">{c["level"]}</span><span class="tag">{c["weeks"]} нед.</span><span class="tag">{c["lessons"]} уроков</span></div>
<h3>{E(c["title"])}</h3><p class="muted small">{E(c["short"])}</p>
<div class="price">{rub(c["price"])}<span>Подробнее →</span></div></div></a>'''

def lead_block(root):
    return f'''<section id="gift"><div class="wrap"><div class="lm reveal">
<div><span class="eyebrow">Подарок</span><h2>Напиши слово <span class="kw" data-keyword>ИИ</span> в Telegram —<br>пришлём «Карту нейросетей 2026»</h2>
<p class="muted">35+ проверенных инструментов по задачам: тексты, картинки, видео, голос, таблицы и боты. Плюс 30 готовых промптов для контента. Подпишитесь на канал — каждый день там новая фишка ИИ с видео-инструкцией.</p>
<div class="btns"><a class="btn tg" data-link="bot" href="#">Написать слово в Telegram</a><a class="btn ghost" data-link="channel" href="#">Подписаться на канал</a></div></div>
<div class="card" style="background:rgba(0,0,0,.25)"><b>Или скачайте прямо сейчас:</b><br><br>
<a class="btn sm block" href="{root}gaydy/karta-neyrosetey/">📘 Карта нейросетей 2026</a><br>
<a class="btn sm ghost block" href="{root}gaydy/30-promptov/">✍️ 30 промптов для контента</a>
<p class="small muted" style="margin:12px 0 0">Есть версия для чтения на телефоне и PDF для печати.</p></div>
</div></div></section>'''

def faq_html(items):
    return "".join(f'<details class="faq"><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q, a in items)

# ---------------- Главная ----------------
def home():
    r = ""
    know = [("🧾", "Фото чека → строка в таблице", "Сфотографировали чек — ИИ сам разнёс сумму, дату и категорию в учёт."),
            ("🎙️", "Голосовое → протокол и задачи", "Часовой созвон превращается в краткий конспект и список дел за минуту."),
            ("🎬", "Рилс без съёмок", "Сценарий, сцены, озвучка и субтитры — ролик из одного текста."),
            ("🤖", "Бот отвечает клиентам 24/7", "Telegram-бот на ваших материалах: консультирует и собирает заявки."),
            ("📊", "Формулы Excel словами", "«Посчитай выручку по менеджерам за март» — и формула готова."),
            ("🖼️", "Фото товара без студии", "Предметная съёмка и карточка для маркетплейса из снимка на телефон.")]
    know_html = "".join(f'<div class="card glow reveal"><div class="ico">{i}</div><h3>{t}</h3><p class="muted small" style="margin:0">{d}</p></div>' for i, t, d in know)
    body = f'''
<section class="hero"><div class="wrap hero-grid">
<div><span class="eyebrow">Школа нейросетей · онлайн</span>
<h1>Нейросети — <span class="grad">с нуля до дохода</span></h1>
<p class="lead">Научим создавать контент, картинки, видео и голос с ИИ, вести учёт и автоматизировать бизнес, собрать своего ИИ-помощника. Простым языком, с картинками, аудио и новыми фишками каждый день.</p>
<div class="chips"><span class="chip">✍️ Тексты</span><span class="chip">🎨 Картинки</span><span class="chip">🎬 Видео</span><span class="chip">🎙️ Голос</span><span class="chip">📊 Учёт и таблицы</span><span class="chip">🤖 ИИ-боты</span></div>
<div class="btns"><a class="btn" href="urok/formula-prompta/">Пройти бесплатный урок</a><a class="btn ghost" href="kursy/">Смотреть курсы</a></div>
<div class="stats"><div class="stat"><b>7</b><span>направлений обучения</span></div><div class="stat"><b>120+</b><span>уроков в программах</span></div><div class="stat"><b>ежедневно</b><span>новые возможности ИИ</span></div></div>
</div>
<div class="hero-img"><img src="assets/img/hero.webp" alt="Нейросеть над ноутбуком: текст, картинки, видео, звук и таблицы" width="1280" height="720" fetchpriority="high"></div>
</div></section>

<section style="padding-top:0"><div class="wrap"><div class="audio reveal">
<div class="wave">🎧</div><div><h3 style="margin-bottom:4px">Аудио-презентация школы · 1,5 минуты</h3>
<p class="muted small" style="margin:0">Послушайте, чему и как мы учим, — можно в дороге. Голос синтезирован нейросетью, как и всё, чему вы научитесь.</p>
<audio controls preload="none" src="assets/audio/prezentaciya.mp3"></audio></div></div></div></section>

<section><div class="wrap"><div class="sec-head"><span class="eyebrow">О чём многие не знают</span><h2>ИИ умеет гораздо больше, чем «написать текст»</h2><p class="muted">Вот что вы будете делать уже после первых уроков — без программирования.</p></div>
<div class="grid g3">{know_html}</div></div></section>

<section id="kursy"><div class="wrap"><div class="sec-head"><span class="eyebrow">Направления</span><h2>Курсы-пакеты: выберите, с чего начать</h2><p class="muted">Каждый курс — это видео-уроки, пошаговые тексты с картинками, аудио-версии, шаблоны и домашние задания с разбором.</p></div>
<div class="grid g3">{"".join(ccard(c, r) for c in COURSES)}
<a class="card ccard glow reveal" href="kursy/#tarify" style="justify-content:center;padding:28px;background:linear-gradient(160deg,rgba(139,92,246,.25),rgba(34,211,238,.12))"><span class="eyebrow" style="align-self:flex-start">Выгодно</span><h3 style="font-size:24px">{BUNDLE["title"]}</h3><p class="muted">{BUNDLE["note"]}</p><div class="price" style="border:0">{rub(BUNDLE["price"])}<span>Тарифы →</span></div></a>
</div></div></section>

<section><div class="wrap"><div class="sec-head"><span class="eyebrow">Как проходит обучение</span><h2>Учиться легко, даже если вы «не технарь»</h2></div>
<div class="grid g4 steps4">
<div class="card reveal"><h3>Видео + текст + аудио</h3><p class="muted small" style="margin:0">Каждый урок в трёх форматах: смотрите, читайте со скриншотами или слушайте.</p></div>
<div class="card reveal"><h3>Практика сразу</h3><p class="muted small" style="margin:0">После каждого урока — задание на 10–20 минут и готовые шаблоны промптов.</p></div>
<div class="card reveal"><h3>Свежие фишки</h3><p class="muted small" style="margin:0">ИИ меняется каждую неделю — новые уроки добавляем в курс без доплаты.</p></div>
<div class="card reveal"><h3>Сообщество</h3><p class="muted small" style="margin:0">Закрытый Telegram-чат, разборы работ и ответы на вопросы.</p></div>
</div></div></section>

<section><div class="wrap"><div class="lm reveal" style="background:linear-gradient(135deg,#101040,#0b0b26);border-color:rgba(34,211,238,.35)">
<div><span class="eyebrow">Бесплатный урок</span><h2>Формула сильного промпта: первый пост с ИИ за 10 минут</h2>
<p class="muted">Пошагово, с картинками и аудио. Оцените качество обучения до покупки — это урок из курса «Нейросети с нуля».</p>
<a class="btn" href="urok/formula-prompta/">Открыть урок бесплатно →</a></div>
<img src="assets/img/urok/formula.svg" alt="Схема: формула Р-З-К-Ф" loading="lazy" style="border-radius:16px">
</div></div></section>

<section id="novoe"><div class="wrap"><div class="sec-head"><span class="eyebrow">Новое каждый день</span><h2>Свежие возможности нейросетей</h2><p class="muted">Каждый день разбираем новую функцию: что появилось и как применить. Короткие видео — в Telegram, YouTube Shorts, Reels и TikTok.</p></div>
<div class="grid g3" id="feed" data-limit="6" data-root=""><p class="muted">Загружаем ленту…</p></div>
<div class="btns" style="margin-top:22px"><a class="btn ghost" href="novoe/">Все новинки →</a><a class="btn tg" data-link="channel" href="#">Получать каждый день в Telegram</a></div></div></section>

{lead_block(r)}

<section id="otzyvy"><div class="wrap"><div class="sec-head"><span class="eyebrow">Отзывы</span><h2>Здесь появятся отзывы первых учеников</h2><p class="muted">Мы не публикуем выдуманные отзывы. Ниже — макет того, как будут выглядеть настоящие отзывы после первого потока.</p></div>
<div class="grid g3">{"".join(f'<div class="card reveal" style="opacity:.75"><span class="ph">ПРИМЕР</span><p>«Текст настоящего отзыва ученика появится здесь после первого потока курса «{E(c)}».»</p><p class="small muted" style="margin:0">Имя ученика · город · курс</p></div>' for c in ["Нейросети с нуля", "Контент и посты с ИИ", "ИИ для бизнеса"])}</div></div></section>

<section id="faq"><div class="wrap" style="max-width:820px"><div class="sec-head"><span class="eyebrow">Вопросы</span><h2>Частые вопросы</h2></div>{faq_html(FAQ)}</div></section>

<section><div class="wrap" style="text-align:center;max-width:760px"><h2>Начните с бесплатного — <span class="grad">а дальше решите сами</span></h2>
<p class="muted">Бесплатный урок, гайды и ежедневные фишки в Telegram. Когда будете готовы — выберите курс.</p>
<div class="btns" style="justify-content:center"><a class="btn" href="urok/formula-prompta/">Бесплатный урок</a><a class="btn tg" data-link="channel" href="#">Telegram-канал</a></div></div></section>'''
    write("index.html", page("index.html", f"{BRAND} — школа нейросетей: от нуля до дохода", "Онлайн-школа нейросетей: контент, картинки, видео, голос, учёт и автоматизация бизнеса, свои ИИ-боты. Бесплатный урок, гайды и новые возможности ИИ каждый день.", body, ""))

# ---------------- Каталог ----------------
def catalog():
    r = "../"
    tar = [("Самостоятельно", "Любой курс", "от " + rub(min(c["price"] for c in COURSES)), ["Все уроки курса: видео, текст, аудио", "Шаблоны и промпты", "Обновления курса 12 месяцев"], "default", False),
           ("С куратором", "Курс + проверка заданий", "+40% к цене курса", ["Всё из тарифа «Самостоятельно»", "Проверка домашних заданий", "Закрытый чат с куратором", "Сертификат"], "default", True),
           (BUNDLE["title"], "Все 7 направлений", rub(BUNDLE["price"]), ["Все курсы школы", "Куратор и разборы работ", "Новые курсы без доплаты 12 месяцев", "Личная консультация по внедрению ИИ"], "bundle", False)]
    th = "".join(f'''<div class="card tariff {"hot" if hot else ""} reveal">{'<span class="ph" style="color:#22d3ee;border-color:#22d3ee">ПОПУЛЯРНЫЙ</span>' if hot else ""}<h3>{t}</h3><p class="muted small">{s}</p><div class="big">{p}</div><ul class="check">{"".join(f"<li>{x}</li>" for x in li)}</ul><br><a class="btn block" data-link="pay" data-course="{k}" href="#">Оформить</a></div>''' for t, s, p, li, k, hot in tar)
    body = f'''<div class="wrap"><p class="crumbs"><a href="../">Главная</a> / Курсы</p></div>
<section style="padding-top:26px"><div class="wrap"><div class="sec-head"><span class="eyebrow">Каталог</span><h1 style="font-size:clamp(26px,6vw,46px)">Курсы по нейросетям</h1><p class="muted">7 направлений — от первого запроса в чат-бот до собственного ИИ-ассистента для бизнеса. Не знаете, с чего начать? Начните с «Нейросети с нуля» или с <a href="../urok/formula-prompta/">бесплатного урока</a>.</p></div>
<div class="grid g3">{"".join(ccard(c, r) for c in COURSES)}</div></div></section>
<section id="tarify"><div class="wrap"><div class="sec-head"><span class="eyebrow">Тарифы</span><h2>Формат участия</h2><p class="note">Цены предварительные и могут измениться до старта продаж.</p></div><div class="grid g3">{th}</div></div></section>
{lead_block(r)}'''
    write("kursy/index.html", page("kursy/index.html", f"Курсы по нейросетям — {BRAND}", "Каталог курсов: нейросети с нуля, контент, картинки, видео, голос, ИИ для бизнеса и свой ИИ-бот. Тарифы и программы.", body, r))

# ---------------- Страница курса ----------------
def course(c):
    r = "../../"
    write(f"assets/img/kursy/{c['slug']}.svg", svg.pipeline(c["pipeline"], c["accent"]))
    mods = "".join(f'''<details class="mod" {"open" if i==0 else ""}><summary><span class="n">{i+1}</span>{E(t)}</summary><div class="in"><p class="muted">{E(d)}</p><ol>{"".join(f"<li>{E(l)}</li>" for l in ls)}</ol></div></details>''' for i, (t, d, ls) in enumerate(c["modules"]))
    n_less = sum(len(m[2]) for m in c["modules"])
    others = [x for x in COURSES if x["slug"] != c["slug"]][:3]
    body = f'''<div class="wrap"><p class="crumbs"><a href="{r}">Главная</a> / <a href="{r}kursy/">Курсы</a> / {E(c["title"])}</p>
<div class="chero"><div><span class="eyebrow">Курс · {c["level"]} · {c["weeks"]} недели</span><h1 style="font-size:clamp(27px,6.4vw,50px)">{E(c["title"])}</h1><p class="lead" style="font-size:18px;color:#cfd0ef">{E(c["short"])}</p>
<div class="btns"><a class="btn" data-link="pay" data-course="{c["slug"]}" href="#">Купить курс · {rub(c["price"])}</a><a class="btn ghost" href="#programma">Программа</a></div></div>
<img src="{r}assets/img/{c["img"]}.webp" alt="Иллюстрация к курсу «{E(c["title"])}»" width="1152" height="864"></div></div>
<section><div class="wrap layout"><div>
<h2>Для кого</h2><ul class="check">{"".join(f"<li>{E(x)}</li>" for x in c["for"])}</ul>
<h2 style="margin-top:40px">Чему вы научитесь</h2><div class="grid g2">{"".join(f'<div class="card"><b class="grad" style="font:700 22px var(--hf)">0{i+1}</b><p style="margin:6px 0 0">{E(x)}</p></div>' for i, x in enumerate(c["outcomes"]))}</div>
<h2 style="margin-top:40px">Как это работает</h2><img class="pipe" src="{r}assets/img/kursy/{c["slug"]}.svg" alt="Схема: {" → ".join(c["pipeline"])}" loading="lazy">
<h2 id="programma" style="margin-top:40px">Программа: {len(c["modules"])} модуля</h2><p class="muted">В каждом уроке — видео, текст с пошаговыми картинками, аудио-версия и практическое задание. Здесь — основные уроки, полный курс включает {c["lessons"]} уроков с практикумами{"" if n_less >= c["lessons"] else " и разборами"}.</p>{mods}
<h2 style="margin-top:40px">Инструменты курса</h2><div class="tools">{"".join(f'<span class="chip">{E(t)}</span>' for t in c["tools"])}</div><p class="small muted" style="margin-top:10px">Набор инструментов обновляется: если появляется сервис лучше — добавляем урок. Для каждого зарубежного сервиса показываем доступную альтернативу.</p>
<h2 style="margin-top:40px">Попробуйте бесплатно</h2><div class="card"><p>Не уверены? Пройдите бесплатный урок «Формула сильного промпта» — так устроены все уроки школы.</p><a class="btn sm" href="{r}urok/formula-prompta/">Открыть бесплатный урок →</a></div>
</div>
<aside class="buy"><span class="tag">{c["lessons"]} уроков · {c["weeks"]} нед.</span><div class="big" style="margin:12px 0 4px">{rub(c["price"])}</div><p class="note">Цена предварительная</p>
<ul class="check small"><li>Видео, текст с картинками и аудио</li><li>Шаблоны и промпты</li><li>Домашние задания</li><li>Обновления 12 месяцев</li><li>Чат участников</li></ul><br>
<a class="btn block" data-link="pay" data-course="{c["slug"]}" href="#">Купить курс</a><br><a class="btn ghost block" data-link="contact" href="#">Задать вопрос</a>
<p class="small muted" style="margin:12px 0 0">Оплата через Telegram. Доступ открывается сразу после оплаты.</p></aside></div></section>
<section><div class="wrap"><h2>Другие курсы</h2><div class="grid g3">{"".join(ccard(x, r) for x in others)}</div></div></section>
{lead_block(r)}'''
    write(f"kursy/{c['slug']}/index.html", page(f"kursy/{c['slug']}/index.html", f"{c['title']} — курс {BRAND}", c["short"], body, r, og=f"assets/img/hero.jpg"))

# ---------------- Бесплатный урок ----------------
LESSON_PROMPT = """Ты — опытный SMM-копирайтер кофейни.
Задача: напиши пост для Instagram о нашем новом напитке — лавандовом рафе.
Контекст: аудитория — мамы в декрете 25–35 лет из Алматы, гуляют с колясками днём. Наша фишка — тихий зал и детский уголок. Цель поста — чтобы пришли в будни с 11 до 15.
Формат: до 600 знаков, дружеский тон на «ты», 3 эмодзи, в конце — призыв прийти и промокод LAVANDA.
Если чего-то не хватает — сначала задай мне до 3 уточняющих вопросов."""

def lesson():
    r = "../../"
    svg.LS = 1.3
    for name, fn in [("chat", svg.chat), ("compare", svg.compare), ("formula", svg.formula), ("loop", svg.loop), ("check", svg.checklist)]:
        write(f"assets/img/urok/{name}.svg", fn())
    svg.LS = 1
    P = E(LESSON_PROMPT)
    body = f'''<div class="wrap"><p class="crumbs"><a href="{r}">Главная</a> / <a href="{r}kursy/s-nulya/">Нейросети с нуля</a> / Бесплатный урок</p></div>
<section style="padding-top:20px"><div class="wrap lesson">
<span class="eyebrow">Бесплатный урок · 10 минут</span>
<h1 style="font-size:clamp(26px,6vw,44px)">Формула сильного промпта: первый пост с ИИ за 10 минут</h1>
<p class="lead" style="color:#cfd0ef;font-size:18px">Почему одни получают от нейросети шедевры, а другие — «воду»? Дело не в сервисе, а в запросе. За этот урок вы освоите формулу, которой пользуются профессионалы, и напишете готовый пост.</p>
<div class="audio" style="margin:20px 0"><div class="wave">🎧</div><div><b>Аудио-версия урока</b><p class="small muted" style="margin:0">Слушайте, пока выполняете шаги.</p><audio controls preload="none" src="{r}assets/audio/urok-formula-prompta.mp3"></audio></div></div>
<div class="card"><b>Что понадобится:</b><ul style="margin:8px 0 0"><li>Телефон или компьютер</li><li>Любой чат-бот с ИИ: ChatGPT, Gemini, Claude, GigaChat или Алиса (YandexGPT) — бесплатной версии достаточно</li><li>10 минут</li></ul></div>

<div class="step"><span class="n">1</span><h2>Откройте чат с нейросетью</h2></div>
<p>Зайдите на сайт или в приложение выбранного чат-бота и войдите в аккаунт. Нажмите «Новый чат» — так ИИ не будет путать вашу задачу с прошлыми разговорами. Внизу экрана есть поле ввода: туда мы и будем писать запрос (его называют <b>промпт</b>).</p>
<figure><img src="{r}assets/img/urok/chat.svg" alt="Схема интерфейса чат-бота: кнопка нового чата, поле ввода и кнопка отправки" loading="lazy"><figcaption>Схема: так выглядит почти любой чат-бот — история слева, поле ввода внизу.</figcaption></figure>

<div class="step"><span class="n">2</span><h2>Посмотрите, почему «напиши пост» не работает</h2></div>
<p>Нейросеть не знает ни вас, ни ваших клиентов. Если написать «Напиши пост про кофе», она выдаст среднестатистический текст «для всех» — гладкий и бесполезный. Чем больше нужного контекста вы дадите, тем точнее результат.</p>
<figure><img src="{r}assets/img/urok/compare.svg" alt="Схема: слабый промпт против сильного промпта" loading="lazy"><figcaption>Схема: слева запрос без деталей, справа — по формуле.</figcaption></figure>

<div class="step"><span class="n">3</span><h2>Запомните формулу Р-З-К-Ф</h2></div>
<p>Любой сильный промпт состоит из четырёх частей:</p>
<ul><li><b>Р — Роль.</b> Кем быть нейросети: копирайтером, юристом, репетитором. Это задаёт уровень и стиль.</li>
<li><b>З — Задача.</b> Что конкретно сделать: пост, письмо, план, таблицу.</li>
<li><b>К — Контекст.</b> Для кого, зачем, какие факты важны, чего избегать.</li>
<li><b>Ф — Формат.</b> Объём, тон, структура, эмодзи, призыв к действию.</li></ul>
<figure><img src="{r}assets/img/urok/formula.svg" alt="Схема: формула Р-З-К-Ф — роль, задача, контекст, формат" loading="lazy"><figcaption>Схема: четыре кирпича любого запроса.</figcaption></figure>

<div class="step"><span class="n">4</span><h2>Скопируйте и отправьте готовый промпт</h2></div>
<p>Вот пример для кофейни. Скопируйте его, отправьте в чат — а потом замените детали на свои: ваш продукт, вашу аудиторию, ваш город.</p>
<div class="prompt" id="pr"><button class="btn sm copy" onclick="navigator.clipboard.writeText(document.getElementById('prt').innerText);this.textContent='Скопировано ✓'">Копировать</button><span id="prt">{P}</span></div>
<div class="tip">💡 <b>Секретный приём:</b> последняя строка «задай мне уточняющие вопросы» превращает ИИ из исполнителя в партнёра. Он спросит то, о чём вы не подумали, — и текст станет точнее.</div>

<div class="step"><span class="n">5</span><h2>Доведите текст за 2–3 уточнения</h2></div>
<p>Первый ответ — это черновик. Не начинайте заново, а уточняйте в том же чате. Работают короткие команды:</p>
<ul><li>«Сделай первую строку цепляющей — вопрос к маме, которая устала»</li><li>«Убери канцелярит и слова "уникальный", "незабываемый"»</li><li>«Дай 3 варианта заголовка, разных по настроению»</li><li>«Сократи на треть, сохрани призыв»</li></ul>
<figure><img src="{r}assets/img/urok/loop.svg" alt="Схема цикла: черновик, оценка, уточнение, новая версия" loading="lazy"><figcaption>Схема: цикл доработки — обычно хватает 2–3 кругов.</figcaption></figure>

<div class="step"><span class="n">6</span><h2>Проверьте перед публикацией</h2></div>
<p>Нейросеть иногда уверенно ошибается — придумывает цифры, адреса, факты. Это называется «галлюцинации». Перед публикацией пройдитесь по чек-листу:</p>
<figure><img src="{r}assets/img/urok/check.svg" alt="Схема: чек-лист перед публикацией" loading="lazy"><figcaption>Схема: 5 пунктов проверки — 1 минута, которая спасает репутацию.</figcaption></figure>

<h2>Домашнее задание</h2>
<div class="card"><ol style="margin:0;padding-left:20px"><li>Напишите промпт по формуле Р-З-К-Ф для своего продукта, услуги или блога.</li><li>Получите текст и сделайте 2 уточнения.</li><li>Сравните с ответом на запрос «напиши пост про …» без формулы. Почувствуйте разницу.</li></ol></div>

<div class="lm" style="margin-top:34px"><div><h2>Понравилось? Это 1 из 14 уроков курса «Нейросети с нуля»</h2><p class="muted">Дальше — шаблоны промптов на каждый день, ИИ-репетитор, разбор документов и фото, безопасность данных.</p>
<div class="btns"><a class="btn" href="{r}kursy/s-nulya/">Смотреть программу курса</a><a class="btn tg" data-link="bot" href="#">Получить ещё 30 промптов</a></div></div>
<img src="{r}assets/img/c-nul.webp" alt="Иллюстрация к курсу «Нейросети с нуля»" loading="lazy" style="border-radius:16px"></div>
</div></section>'''
    write("urok/formula-prompta/index.html", page("urok/formula-prompta/index.html", f"Бесплатный урок: формула сильного промпта — {BRAND}", "Пошаговый бесплатный урок с картинками и аудио: формула Р-З-К-Ф и первый пост с нейросетью за 10 минут.", body, r))

# ---------------- Лента ----------------
def novoe():
    r = "../"
    body = f'''<div class="wrap"><p class="crumbs"><a href="../">Главная</a> / Новое каждый день</p></div>
<section style="padding-top:26px"><div class="wrap"><div class="sec-head"><span class="eyebrow">Новое каждый день</span><h1 style="font-size:clamp(26px,6vw,46px)">Новые возможности нейросетей</h1><p class="muted">Что появилось в мире ИИ и как это применить. У каждой новости — ссылка на первоисточник. Видео-разборы выходят в Telegram, YouTube Shorts, Reels и TikTok.</p>
<div class="btns"><a class="btn tg" data-link="channel" href="#">Получать в Telegram каждый день</a></div></div>
<div class="grid g3" id="feed" data-root="../"><p class="muted">Загружаем ленту…</p></div></div></section>
{lead_block(r)}'''
    write("novoe/index.html", page("novoe/index.html", f"Новое каждый день — возможности нейросетей · {BRAND}", "Ежедневная лента новых возможностей ИИ: видео, картинки, голос, агенты и бизнес — с источниками и советами, как применить.", body, r))

# ---------------- Гайды ----------------
GUIDE_CSS = '''<style>.guide{max-width:820px;margin:0 auto}.guide table{width:100%;border-collapse:collapse;font-size:15px;margin:10px 0 26px}.guide td,.guide th{border-bottom:1px solid var(--line);padding:9px 8px;text-align:left;vertical-align:top}.guide th{color:var(--c);font-size:13px;text-transform:uppercase;letter-spacing:.06em}.guide .prompt{margin:8px 0 18px;font-size:14px}
@media print{body:before,.top,.mbar,footer,.noprint{display:none!important}body{background:#fff;color:#111;font-size:12px}.guide h1,.guide h2{color:#3b1d8f}.guide .prompt{background:#f4f3ff;color:#111;border-color:#c4b5fd}.guide td,.guide th{border-color:#ddd}.grad{color:#5b21b6;-webkit-text-fill-color:#5b21b6}.card{border-color:#ddd;background:#fafafa}a{color:#111}section{padding:0}}</style>'''

MAP = [
 ("Тексты и ассистенты", [("ChatGPT", "Универсальный помощник: тексты, анализ файлов, картинки, голос"), ("Gemini", "Ассистент Google, связан с Gmail, Документами и Таблицами"), ("Claude", "Длинные документы, аккуратная редактура, сложные тексты"), ("GigaChat", "Российский ассистент от Сбера, работает без VPN в РФ"), ("Алиса (YandexGPT)", "Ассистент Яндекса: тексты, пересказ видео и статей"), ("Perplexity", "Поиск с ответом и ссылками на источники"), ("NotebookLM", "Конспекты и аудио-обзоры по вашим документам")]),
 ("Картинки и дизайн", [("Midjourney", "Художественные изображения высокого качества"), ("ChatGPT (изображения)", "Картинки по описанию и правки словами, текст на картинке"), ("Gemini (изображения)", "Генерация и редактирование фото в чате"), ("Шедеврум", "Генерация картинок от Яндекса"), ("Kandinsky", "Генерация картинок от Сбера"), ("Ideogram", "Логотипы и постеры с текстом"), ("Canva", "Дизайн-шаблоны со встроенными ИИ-функциями"), ("Leonardo", "Изображения и стили для игр, персонажей и рекламы")]),
 ("Видео", [("Kling", "Генерация видео из текста и фото"), ("Runway", "Генерация и ИИ-монтаж видео"), ("Google Veo / Flow", "Видео со звуком и сценами по описанию"), ("HeyGen", "Говорящие ИИ-аватары и перевод видео"), ("CapCut", "Монтаж, авто-субтитры, ИИ-эффекты"), ("Hailuo (MiniMax)", "Короткие видео по тексту и картинке")]),
 ("Голос и музыка", [("ElevenLabs", "Реалистичная озвучка и клонирование голоса (с согласия)"), ("Suno", "Песни и музыка по текстовому описанию"), ("Яндекс SpeechKit", "Синтез и распознавание русской речи"), ("Adobe Podcast", "Чистка звука «как в студии»"), ("Whisper", "Расшифровка аудио в текст, открытая модель")]),
 ("Таблицы, учёт, автоматизация", [("Gemini в Google Таблицах", "Формулы, анализ и заполнение таблиц"), ("Copilot в Excel", "Анализ данных и формулы словами"), ("n8n", "Автоматизации и ИИ-агенты, можно на своём сервере"), ("Make", "Конструктор автоматизаций без кода"), ("Zapier", "Связка сотен сервисов по триггерам")]),
 ("Боты и свои ассистенты", [("Custom GPTs / Projects", "Ассистент на ваших инструкциях и файлах"), ("Telegram BotFather", "Создание Telegram-бота за 2 минуты"), ("Gems в Gemini", "Свои мини-ассистенты в Gemini"), ("Voiceflow", "Конструктор чат- и голосовых ботов")]),
]

PROMPTS = [
 ("Стратегия", ["Ты — маркетолог. Составь портрет моей аудитории: [ниша, город, продукт]. Опиши 5 болей, 5 желаний и 5 возражений, словами самих клиентов.", "Составь контент-план на 30 дней для [площадка] по нише [ниша]. Рубрики: польза, личное, кейсы, продажа. Формат: таблица дата | рубрика | тема | хук.", "Дай 20 тем постов, которые вызовут споры в комментариях в нише [ниша], без токсичности.", "Проанализируй 3 поста конкурентов (вставлю ниже): что в них цепляет, что слабо, как сделать лучше."]),
 ("Посты", ["Напиши пост по формуле Р-З-К-Ф: Роль — [кто], Задача — [что], Контекст — [для кого и зачем], Формат — [объём, тон, CTA].", "Вот 3 моих поста. Опиши мой стиль в 10 правилах (лексика, длина фраз, юмор). Дальше пиши строго по этим правилам.", "Перепиши текст: убери канцелярит, штампы и слова «уникальный», «незабываемый». Сохрани смысл.", "Дай 10 вариантов первой строки к этому посту: вопрос, цифра, провокация, история, боль.", "Напиши историю из моей жизни [факты] в формате: проблема → поворот → вывод → вопрос подписчикам.", "Сделай из этого текста карусель на 8 слайдов: заголовок слайда + 1–2 строки, последний слайд — призыв."]),
 ("Продажи", ["Составь прогрев на 7 дней к продукту [продукт, цена]: по дню — тема, цель, формат (пост/сторис/рилс).", "Напиши продающий пост по схеме: боль → цена бездействия → решение → доказательство → оффер → дедлайн.", "Перечисли 10 возражений к [продукт] и ответь на каждое коротко и без давления.", "Придумай 5 лид-магнитов для [ниша], которые можно выдавать по кодовому слову в Telegram.", "Напиши текст автоответа бота: человек написал кодовое слово, получает гайд и мягкое приглашение на консультацию."]),
 ("Видео и рилс", ["Напиши сценарий рилс на 30 секунд о [тема]: хук до 2 секунд, 3 факта, призыв. Отметь, что показывать в кадре.", "Дай 15 хуков для коротких видео в нише [ниша] по формулам: «Я не знал…», «Перестань…», «3 ошибки…».", "Сделай раскадровку из 6 сцен для этого сценария: план, движение камеры, текст на экране.", "Перепиши сценарий для озвучки: короткие фразы, паузы обозначь «…», ударения — заглавной буквой."]),
 ("Картинки", ["Создай промпт для картинки: [объект], стиль [стиль], свет [мягкий/контровой], ракурс [сверху/крупный план], фон [какой], без текста.", "Предложи 5 визуальных концепций обложки для поста на тему [тема] в едином стиле для ленты.", "Опиши фото товара для маркетплейса: [товар], 3 варианта сцены, которые повышают кликабельность.", "Придумай персонажа-маскота для бренда [ниша]: внешность, характер, цвета. Дай промпт для генерации в 3 позах.", "Сравни эти 2 картинки (прикреплю) как арт-директор: что сильнее, что улучшить в следующей генерации."]),
 ("Рутина", ["Сделай из этой расшифровки созвона: краткое резюме, решения, задачи с ответственными и сроками.", "Ответь клиенту на отзыв [текст] вежливо, по делу, без шаблонных извинений, предложи решение.", "Напиши формулу для Google Таблиц: [что посчитать]. Столбцы: [описание]. Объясни, как она работает.", "Составь чек-лист запуска [проект] по шагам с ориентировочным временем на каждый.", "Превращу голосовое в текст и вставлю ниже — сделай из него пост в моём стиле и 3 сторис.", "Составь шаблон еженедельного отчёта для руководителя: показатели, выводы, риски, план — по данным, которые я вставлю."]),
]

def guides():
    r = "../../"
    rows = "".join(f'<h2>{E(sec)}</h2><table><tr><th style="width:34%">Сервис</th><th>Для чего</th></tr>{"".join(f"<tr><td><b>{E(n)}</b></td><td>{E(d)}</td></tr>" for n, d in items)}</table>' for sec, items in MAP)
    total = sum(len(i) for _, i in MAP)
    body = f'''{GUIDE_CSS}<div class="wrap noprint"><p class="crumbs"><a href="{r}">Главная</a> / <a href="../">Гайды</a> / Карта нейросетей</p></div>
<section style="padding-top:20px"><div class="wrap guide"><span class="eyebrow">Бесплатный гайд · {BRAND}</span><h1 style="font-size:clamp(26px,6vw,42px)">Карта нейросетей 2026: <span class="grad">{total} инструментов по задачам</span></h1>
<p class="muted">Шпаргалка: какой сервис взять под конкретную задачу. Сверено в ноябре 2026. Тарифы, лимиты и доступность в разных странах меняются — проверяйте на сайте сервиса. Для пользователей из России и Казахстана отмечены российские альтернативы (GigaChat, Алиса, Шедеврум, Kandinsky, SpeechKit).</p>
<div class="btns noprint"><a class="btn" href="../karta-neyrosetey.pdf" download>Скачать PDF</a><a class="btn ghost" href="javascript:print()">Распечатать</a></div>
{rows}
<div class="card"><h3>Как выбрать с чего начать</h3><ol style="margin:0;padding-left:20px"><li>Возьмите один универсальный ассистент (ChatGPT, Gemini или GigaChat) и пользуйтесь им каждый день неделю.</li><li>Добавьте один инструмент под вашу главную задачу: картинки, видео или таблицы.</li><li>Только потом — автоматизации и боты.</li></ol></div>
<div class="card noprint" style="margin-top:18px"><b>Хотите разбор каждого инструмента с видео?</b> Подпишитесь на <a data-link="channel" href="#">Telegram-канал</a> — каждый день новая фишка, или загляните в <a href="{r}kursy/">курсы</a>.</div>
</div></section>'''
    write("gaydy/karta-neyrosetey/index.html", page("gaydy/karta-neyrosetey/index.html", f"Карта нейросетей 2026 — бесплатный гайд {BRAND}", "Шпаргалка: 35+ нейросетей по задачам — тексты, картинки, видео, голос, таблицы, боты. Скачайте PDF бесплатно.", body, r, mbar=False))
    n = 0; ph = ""
    for sec, ps in PROMPTS:
        ph += f"<h2>{E(sec)}</h2>"
        for p in ps:
            n += 1; ph += f'<p style="margin:0"><b>{n}.</b></p><div class="prompt">{E(p)}</div>'
    body = f'''{GUIDE_CSS}<div class="wrap noprint"><p class="crumbs"><a href="{r}">Главная</a> / <a href="../">Гайды</a> / 30 промптов</p></div>
<section style="padding-top:20px"><div class="wrap guide"><span class="eyebrow">Бесплатный гайд · {BRAND}</span><h1 style="font-size:clamp(26px,6vw,42px)">{n} промптов для контента, <span class="grad">которые работают</span></h1>
<p class="muted">Копируйте, замените [скобки] на свои данные и отправляйте в любой чат-бот: ChatGPT, Gemini, Claude, GigaChat или Алису. Лучший результат — если в начале диалога рассказать о себе и своей аудитории.</p>
<div class="btns noprint"><a class="btn" href="../30-promptov.pdf" download>Скачать PDF</a><a class="btn ghost" href="javascript:print()">Распечатать</a></div>
{ph}
<div class="card noprint"><b>Как писать такие промпты самому?</b> Пройдите <a href="{r}urok/formula-prompta/">бесплатный урок «Формула сильного промпта»</a>.</div></div></section>'''
    write("gaydy/30-promptov/index.html", page("gaydy/30-promptov/index.html", f"{n} промптов для контента — бесплатный гайд {BRAND}", "Готовые промпты для постов, прогревов, рилс, картинок и рутины. Скачайте PDF бесплатно.", body, r, mbar=False))
    body = f'''<div class="wrap"><p class="crumbs"><a href="../">Главная</a> / Гайды</p></div>
<section style="padding-top:26px"><div class="wrap"><div class="sec-head"><span class="eyebrow">Бесплатно</span><h1 style="font-size:clamp(26px,6vw,46px)">Гайды и шпаргалки</h1><p class="muted">Скачивайте бесплатно. Новые гайды сначала появляются в нашем Telegram-канале.</p></div>
<div class="grid g2"><a class="card glow" href="karta-neyrosetey/"><div class="ico">📘</div><h3>Карта нейросетей 2026</h3><p class="muted small">{total} инструментов по задачам + российские альтернативы.</p><span class="btn sm">Открыть</span></a>
<a class="card glow" href="30-promptov/"><div class="ico">✍️</div><h3>{n} промптов для контента</h3><p class="muted small">Посты, прогревы, рилс, картинки и рутина.</p><span class="btn sm">Открыть</span></a></div></div></section>
{lead_block("../")}'''
    write("gaydy/index.html", page("gaydy/index.html", f"Бесплатные гайды по нейросетям — {BRAND}", "Карта нейросетей 2026 и промпты для контента — скачайте бесплатно.", body, "../"))

def misc():
    write("assets/img/favicon.svg", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#8b5cf6"/><stop offset="1" stop-color="#22d3ee"/></linearGradient></defs><rect width="64" height="64" rx="16" fill="url(#g)"/><path d="M32 12l5 15 15 5-15 5-5 15-5-15-15-5 15-5z" fill="#0a0a1f"/></svg>')
    body = '<section><div class="wrap" style="text-align:center"><h1>404</h1><p class="muted">Такой страницы нет. Возможно, нейросеть её ещё не придумала 🙂</p><a class="btn" href="/neuro-obuch/">На главную</a></div></section>'
    s = page("404.html", f"Страница не найдена — {BRAND}", "Страница не найдена", body, "/neuro-obuch/")
    write("404.html", s)
    urls = ["", "kursy/", "urok/formula-prompta/", "novoe/", "gaydy/", "gaydy/karta-neyrosetey/", "gaydy/30-promptov/"] + [f"kursy/{c['slug']}/" for c in COURSES]
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + "".join(f"<url><loc>{BASE_URL}{u}</loc></url>" for u in urls) + "</urlset>\n")
    write("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {BASE_URL}sitemap.xml\n")
    write(".nojekyll", "")

if __name__ == "__main__":
    home(); catalog(); [course(c) for c in COURSES]; lesson(); novoe(); guides(); misc()
    print("OK: страницы собраны")
