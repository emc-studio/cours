#!/usr/bin/env python3
"""Render every session page of the built site to a PDF next to it: python3 pdf.py out/v2"""
import sys, http.server, threading, functools
from pathlib import Path
from playwright.sync_api import sync_playwright
root = Path(sys.argv[1]).resolve()
H = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(root))
H.log_message = lambda *a: None
srv = http.server.ThreadingHTTPServer(('127.0.0.1', 8765), H); threading.Thread(target=srv.serve_forever, daemon=True).start()
with sync_playwright() as p:
    pg = p.chromium.launch().new_page(viewport={'width': 1100, 'height': 900})
    for f in root.glob('*/*/index.html'):
        rel = f.parent.relative_to(root)
        if rel.parts[0] == 'notions': continue
        pg.goto(f'http://127.0.0.1:8765/{rel}/'); pg.wait_for_timeout(800); pg.emulate_media(media='print')
        pg.pdf(path=str(f.parent / f'{f.parent.name}.pdf'), format='A4', print_background=True)
        pg.emulate_media(media='screen'); print('pdf', rel)
srv.shutdown()
