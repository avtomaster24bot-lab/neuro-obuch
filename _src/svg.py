# -*- coding: utf-8 -*-
"""Схемы-иллюстрации SVG (рисуются кодом, подписаны «Схема», это не скриншоты приложений)."""
from html import escape as e
F = "font-family=\"Manrope, 'Segoe UI', Arial, sans-serif\""
DEFS = '''<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#8b5cf6"/><stop offset="1" stop-color="#22d3ee"/></linearGradient>
<filter id="gl"><feGaussianBlur stdDeviation="6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>'''

def wrap(w, h, body, label="Схема"):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">{DEFS}'
            f'<rect width="{w}" height="{h}" rx="22" fill="#0b0b26"/>'
            f'<text x="{w-20}" y="30" text-anchor="end" {F} font-size="14" fill="#6b6b99">{label}</text>{body}</svg>')

LS = 1
def txt(x, y, s, size=18, fill="#e9e9ff", weight=600, anchor="middle"):
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" {F} font-size="{round(size*LS)}" font-weight="{weight}" fill="{fill}">{e(s)}</text>'

def pipeline(steps, accent):
    n = len(steps); w = 1000; h = 230; bw = 160; gap = (w - 40 - n*bw)/(n-1)
    b = ""
    for i, s in enumerate(steps):
        x = 20 + i*(bw+gap)
        b += f'<rect x="{x}" y="70" width="{bw}" height="96" rx="18" fill="#141441" stroke="{accent if i==n-1 else "#3b3b77"}" stroke-width="2"/>'
        b += f'<circle cx="{x+bw/2}" cy="70" r="16" fill="url(#g)"/>' + txt(x+bw/2, 76, str(i+1), 15, "#0a0a1f", 800)
        words = s.split(" ")
        if len(s) > 13 and len(words) > 1:
            mid = len(words)//2 or 1
            b += txt(x+bw/2, 116, " ".join(words[:mid]), 17) + txt(x+bw/2, 140, " ".join(words[mid:]), 17)
        else:
            b += txt(x+bw/2, 126, s, 17)
        if i < n-1:
            ax = x+bw+6; b += f'<path d="M{ax} 118 L{ax+gap-12} 118" stroke="url(#g)" stroke-width="3"/><path d="M{ax+gap-12} 111 L{ax+gap-4} 118 L{ax+gap-12} 125 z" fill="#22d3ee"/>'
    b += txt(20, 208, "Как это работает в курсе", 15, "#8a8ab8", 500, "start")
    return wrap(w, h, b)

def chat():
    b = '<rect x="40" y="50" width="920" height="420" rx="18" fill="#121238" stroke="#2f2f66"/>'
    b += '<rect x="40" y="50" width="200" height="420" rx="18" fill="#17174a"/>'
    b += '<rect x="60" y="80" width="160" height="40" rx="12" fill="url(#g)"/>' + txt(140, 106, "+ Новый чат", 16, "#0a0a1f", 800)
    for i in range(4): b += f'<rect x="60" y="{140+i*36}" width="{150-i*15}" height="14" rx="7" fill="#2a2a60"/>'
    b += txt(600, 200, "Чем я могу помочь?", 30, "#e9e9ff", 700)
    b += '<rect x="290" y="380" width="620" height="60" rx="30" fill="#1d1d55" stroke="#22d3ee" stroke-width="2" filter="url(#gl)"/>'
    b += txt(320, 417, "Введите запрос…", 18, "#8a8ab8", 500, "start")
    b += '<circle cx="878" cy="410" r="20" fill="url(#g)"/><path d="M870 410 L888 410 M880 402 L888 410 L880 418" stroke="#0a0a1f" stroke-width="3" fill="none"/>'
    b += '<path d="M600 330 L600 372" stroke="#fbbf24" stroke-width="3" stroke-dasharray="6 5"/>' + txt(600, 318, "Сюда пишем промпт", 18, "#fbbf24", 700)
    b += '<path d="M140 140 L140 136" stroke="none"/>' + txt(140, 450, "← история чатов", 14, "#8a8ab8", 500)
    return wrap(1000, 500, b, "Схема интерфейса чат-бота")

def compare():
    b = '<rect x="30" y="60" width="455" height="360" rx="18" fill="#1a0f22" stroke="#f87171" stroke-width="2"/>'
    b += '<rect x="515" y="60" width="455" height="360" rx="18" fill="#0d1f1a" stroke="#4ade80" stroke-width="2"/>'
    b += txt(257, 100, "✗ Слабый промпт", 22, "#f87171", 800) + txt(742, 100, "✓ Сильный промпт", 22, "#4ade80", 800)
    b += '<rect x="60" y="130" width="395" height="60" rx="12" fill="#2a1630"/>' + txt(257, 168, "«Напиши пост про кофе»", 19)
    for i, s in enumerate(["Шаблонный текст «для всех»", "Нет цели и аудитории", "Непонятный объём и формат", "Приходится переделывать 5 раз"]):
        b += txt(70, 235+i*42, "— " + s, 17, "#fca5a5", 500, "start")
    rows = [("Роль", "ты SMM-копирайтер кофейни"), ("Задача", "пост о новом рафе"), ("Контекст", "мамы в декрете, Алматы"), ("Формат", "до 600 знаков, 3 эмодзи, CTA")]
    for i, (k, v) in enumerate(rows):
        y = 130 + i*58
        b += f'<rect x="545" y="{y}" width="395" height="48" rx="12" fill="#12332a"/>' + txt(560, y+31, k + ":", 17, "#4ade80", 800, "start") + txt(692, y+31, v, 13, "#d1fae5", 500, "start")
        if False: pass
    b += txt(742, 395, "Результат с 1–2 попыток", 18, "#4ade80", 700)
    return wrap(1000, 450, b)

def formula():
    parts = [("Р", "Роль", "Кем быть ИИ", "#8b5cf6"), ("З", "Задача", "Что сделать", "#d946ef"), ("К", "Контекст", "Для кого и зачем", "#22d3ee"), ("Ф", "Формат", "Как оформить", "#22c55e")]
    b = ""
    for i, (l, t, d, c) in enumerate(parts):
        x = 30 + i*240
        b += f'<rect x="{x}" y="70" width="220" height="250" rx="22" fill="#141441" stroke="{c}" stroke-width="2"/>'
        b += f'<circle cx="{x+110}" cy="140" r="44" fill="{c}" filter="url(#gl)"/>' + txt(x+110, 156, l, 44, "#0a0a1f", 800)
        b += txt(x+110, 230, t, 24, "#fff", 800) + txt(x+110, 266, d, 16, "#b7b7dd", 500)
        if i < 3: b += txt(x+230, 205, "+", 30, "#6b6b99", 800)
    b += txt(500, 370, "Формула Р-З-К-Ф: четыре кирпича любого запроса", 20, "#e9e9ff", 700)
    return wrap(1000, 400, b)

def loop():
    b = ""
    nodes = [(500, 110, "Черновик ИИ"), (790, 270, "Ваша оценка"), (500, 420, "Уточнение"), (210, 270, "Новая версия")]
    b += '<circle cx="500" cy="265" r="155" fill="none" stroke="url(#g)" stroke-width="3" stroke-dasharray="10 8"/>'
    for x, y, s in nodes:
        b += f'<rect x="{x-105}" y="{y-30}" width="210" height="60" rx="16" fill="#141441" stroke="#8b5cf6" stroke-width="2"/>' + txt(x, y+7, s, 18)
    b += txt(500, 262, "2–3 круга", 26, "#22d3ee", 800) + txt(500, 292, "и текст готов", 17, "#b7b7dd", 500)
    return wrap(1000, 480, b)

def checklist():
    items = ["Факты и цифры проверены по источнику", "Звучит как вы, а не как робот", "Есть одна главная мысль", "Понятный призыв к действию", "Нет личных данных клиентов"]
    b = '<rect x="130" y="50" width="740" height="370" rx="22" fill="#141441" stroke="#3b3b77"/>' + txt(500, 95, "Чек-лист перед публикацией", 22, "#fff", 800)
    for i, s in enumerate(items):
        y = 140 + i*56
        b += f'<rect x="170" y="{y-22}" width="30" height="30" rx="8" fill="url(#g)"/>' + txt(185, y, "✓", 18, "#0a0a1f", 800) + txt(220, y, s, 17, "#e9e9ff", 500, "start")
    return wrap(1000, 460, b)
