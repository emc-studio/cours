#!/usr/bin/env python3
"""Render every session page (<site>/<AAAA-MM-JJ-slug>/) of the built site to a PDF next to it: python3 _atelier/pdf.py _site"""
import sys, http.server, threading, functools
from pathlib import Path
from playwright.sync_api import sync_playwright
root = Path(sys.argv[1]).resolve()
class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
H = functools.partial(Quiet, directory=str(root))
srv = http.server.ThreadingHTTPServer(('127.0.0.1', 8765), H); threading.Thread(target=srv.serve_forever, daemon=True).start()
with sync_playwright() as p:
    pg = p.chromium.launch().new_page(viewport={'width': 1100, 'height': 900})
    for f in sorted(root.glob('*/index.html')):
        if 'id="data"' not in f.read_text(): continue      # session pages only (not courses, notions)
        rel = f.parent.relative_to(root)
        pg.goto(f'http://127.0.0.1:8765/{rel}/'); pg.wait_for_timeout(800); pg.emulate_media(media='print')
        pg.pdf(path=str(f.parent / f'{f.parent.name}.pdf'), format='A4', print_background=True)
        pg.emulate_media(media='screen'); print('pdf', rel)
srv.shutdown()
