# -*- coding: utf-8 -*-
"""python3 _src/tools.py pdf  — PDF гайдов;  python3 _src/tools.py shots <url> <outdir> — скриншоты."""
import sys, os, http.server, threading, functools
from playwright.sync_api import sync_playwright
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def serve():
    h = functools.partial(http.server.SimpleHTTPRequestHandler, directory=os.path.dirname(ROOT))
    s = http.server.ThreadingHTTPServer(("127.0.0.1", 0), h); threading.Thread(target=s.serve_forever, daemon=True).start()
    return f"http://127.0.0.1:{s.server_address[1]}/" + os.path.basename(ROOT) + "/"

def pdf():
    base = serve()
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page()
        for g in ["karta-neyrosetey", "30-promptov"]:
            pg.goto(base + f"gaydy/{g}/", wait_until="networkidle"); pg.emulate_media(media="print")
            pg.pdf(path=os.path.join(ROOT, f"gaydy/{g}.pdf"), format="A4", print_background=True, margin={"top": "14mm", "bottom": "14mm", "left": "12mm", "right": "12mm"})
            print("PDF", g)
        b.close()

def shots(base, out):
    os.makedirs(out, exist_ok=True)
    pages = {"home": "", "kurs-s-nulya": "kursy/s-nulya/", "kurs-biznes": "kursy/biznes/", "urok": "urok/formula-prompta/", "katalog": "kursy/", "novoe": "novoe/"}
    with sync_playwright() as p:
        b = p.chromium.launch()
        m = b.new_page(viewport={"width": 390, "height": 844}, device_scale_factor=2, is_mobile=True, has_touch=True)
        d = b.new_page(viewport={"width": 1440, "height": 900})
        for k, u in pages.items():
            for pg, tag in [(m, "mobile"), (d, "desktop")]:
                pg.goto(base + u, wait_until="networkidle"); pg.wait_for_timeout(800)
                pg.add_style_tag(content='.reveal{opacity:1!important;transform:none!important;transition:none!important}'); pg.evaluate("document.querySelectorAll('img[loading=lazy]').forEach(i=>i.loading='eager')"); pg.wait_for_timeout(1500)
                pg.screenshot(path=f"{out}/{k}-{tag}.png", full_page=(tag == "mobile" and k in ("home", "urok", "kurs-s-nulya", "katalog")) or tag == "desktop")
                pg.screenshot(path=f"{out}/{k}-{tag}-top.png") if tag == "mobile" else None
        sw = m.evaluate("document.documentElement.scrollWidth"); print("mobile scrollWidth", sw)
        b.close()

if __name__ == "__main__":
    if sys.argv[1] == "pdf": pdf()
    else: shots(sys.argv[2], sys.argv[3])
