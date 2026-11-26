#!/usr/bin/env python3
"""EMC Studio site generator.
python3 _atelier/build.py seances _site _atelier/assets
seances/courses.json lists the courses. Every folder holding a .md anywhere under seances/
(directly, or in sub-folders by theme) is a session, named AAAA-MM-JJ-slug, unique across the tree.
Its courses come from the .md header: `cours: e-music-ma, e-music-ba` (first = main course).
Page address: <site>/<AAAA-MM-JJ-slug>/, whatever the folder layout. Folders starting with _ or . are ignored."""
import json, re, math, html, shutil, sys, hashlib
from pathlib import Path
import markdown, yaml

SRC = Path(sys.argv[1]); OUT = Path(sys.argv[2]); ASSETS = Path(sys.argv[3])
FONTS = ''
CC0 = '<a href="https://creativecommons.org/publicdomain/zero/1.0/deed.fr">CC0 1.0</a> · domaine public'
MONTHS = ['janvier','février','mars','avril','mai','juin','juillet','août','septembre','octobre','novembre','décembre']
esc = lambda s: html.escape(str(s), quote=True)
md = lambda s: markdown.markdown(re.sub(r'([^\n])\n(- |\d+\. )', r'\1\n\n\2', s), extensions=['fenced_code'])
mdi = lambda s: re.sub(r'^<p>|</p>$', '', md(s).strip())

LEVELS = {'MA': 'master', 'BA': 'bachelor'}
def clabel(cs):
    """Musique électronique MA · BA  /  Interfaces MA · Musique électronique BA"""
    if len({c['title'] for c in cs}) == 1: return f"{cs[0]['title']} {' · '.join(c['level'] for c in cs)}".strip()
    return ' · '.join(f"{c['title']} {c['level']}".strip() for c in cs)
def nlabel(cs):
    out = []
    for c in cs:
        for l in c['level'].split(' · '):
            l = LEVELS.get(l.strip(), l.strip())
            if l and l not in out: out.append(l)
    return ' · '.join(out)

def dshort(d): return f'{d.day:02d}.{d.month:02d}.{d.year}'

def trace(seed, W=1152, H=180):
    h = int(hashlib.md5(seed.encode()).hexdigest()[:8], 16)
    k = 9 + h % 7; m = 1.5 + (h >> 4) % 5 * 0.5; ph = (h >> 8) % 100 / 100 * math.pi
    f = lambda x: H/2 - H*0.34 * (0.3 + 0.7*math.sin(math.pi*x/W)) * math.sin(x/W*math.pi*k + ph) * math.cos(x/W*math.pi*m)
    d = ''.join(('L' if x else 'M') + f'{x} {f(x):.1f}' for x in range(0, W+1, 3))
    return d, f

def scope(seed, H=180, taps=(), label='2 ms / div'):
    d, f = trace(seed, H=H)
    marks = ''.join(f'<span class="tap" style="left:{x/1152*100:.3f}%;top:{f(x):.1f}px"></span><span class="dot" style="left:{x/1152*100:.3f}%;top:{f(x):.1f}px"></span>' for x in taps)
    return (f'<div class="scope" style="--h:{H}px" aria-hidden="true"><div class="axis"></div>'
            f'<svg viewBox="0 0 1152 {H}" preserveAspectRatio="none"><path class="tr" d="{d}"/></svg>{marks}<span class="div">{label}</span></div>')

def shell(title, depth, top_right, body, script=''):
    r = '../' * depth
    return f'''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
{FONTS}
<link rel="stylesheet" href="{r}assets/emc.css">
</head>
<body>
<div class="wrap">
<header class="top"><a href="{r}index.html">emc<span class="tilde">~</span> studio</a><nav class="topnav"><span class="crumb">{top_right}</span><a class="nl" href="{r}notions/index.html">Notions &amp; objets</a></nav></header>
{body}
<footer><span>EMC Studio · Electronic &amp; Multimedia Composition</span><span>{CC0}</span></footer>
</div>
{script}
</body>
</html>
'''

# ---------- session parsing ----------
def parse_session(folder):
    mdf = next(folder.glob('*.md'))
    text = mdf.read_text()
    fm = {}
    m = re.match(r'---\n(.*?)\n---\n', text, re.S)
    if m: fm = yaml.safe_load(m.group(1)); text = text[m.end():]
    text = re.sub(r'<!--.*?-->', '', text, flags=re.S)
    parts = re.split(r'^## (.+)$', text, flags=re.M)
    head = parts[0]
    title = re.search(r'^# (.+)$', head, re.M).group(1).strip()
    lead = re.sub(r'^# .+$', '', head, flags=re.M).strip()
    sections = [(parts[i].strip(), parts[i+1].strip()) for i in range(1, len(parts), 2)]
    cfg = json.loads((folder / 'config.json').read_text()) if (folder / 'config.json').exists() else {}
    return dict(fm=fm, title=title, lead=lead, sections=sections, cfg=cfg, folder=folder)

def subs(body):
    p = re.split(r'^### (.+)$', body, flags=re.M)
    return p[0].strip(), [(p[i].strip(), p[i+1].strip()) for i in range(1, len(p), 2)]

def quotes(body):
    out = []
    for blk in re.split(r'\n\s*\n', body):
        lines = blk.strip().splitlines()
        if lines and all(l.startswith('>') for l in lines):
            out.append('\n'.join(re.sub(r'^> ?', '', l) for l in lines))
    return out

def keyed(q):
    m = re.match(r'\*\*(.+?)\*\*\s*(.*)', q, re.S)
    return (m.group(1), m.group(2)) if m else ('', q)

def slug(s):
    import unicodedata
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode()
    return re.sub(r'[^a-z0-9]+', '-', s.lower().replace('~', '')).strip('-') or 'x'

def code_block(c):
    return f'<div class="code"><div class="bar"><button class="ghost copy" type="button">Copier</button></div><pre><code>{esc(c)}</code></pre></div>'

def render_rich(body):
    """paragraphs + fenced code with copy buttons"""
    out = []
    for i, chunk in enumerate(re.split(r'```\n?(.*?)```', body, flags=re.S)):
        if i % 2: out.append(code_block(chunk.rstrip('\n')))
        elif chunk.strip(): out.append(md(chunk))
    return ''.join(out)

def sec_steps(body):
    intro, ss = subs(body)
    cells = ''
    for h, b in ss:
        m = re.match(r'(\d+)\.\s*(.+)', h); n, t = (m.group(1), m.group(2)) if m else ('', h)
        cells += f'<div class="step" tabindex="0" data-s="{n}"><span class="n">{int(n):02d}</span><h3>{mdi(t)}</h3>{md(b)}</div>'
    return (md(intro) if intro else '') + f'<div class="grid1" id="steps">{cells}</div>'

def sec_notes(body):
    rows = ''
    for q in quotes(body):
        k, v = keyed(q)
        if k.lower().startswith('attention'):
            k = re.sub(r'^attention\s*:?\s*', '', k, flags=re.I)
            k = k[:1].upper() + k[1:]
            rows += f'<div class="note warn"><span class="k"><svg class="warn-i" width="26" height="26" viewBox="0 0 20 20" role="img" aria-label="Attention"><path d="M10 2 L18.5 17 H1.5 Z" fill="none" stroke="var(--acc)" stroke-width="1.5" stroke-linejoin="round"/><rect x="9.25" y="7" width="1.5" height="5.5" fill="var(--acc)"/><rect x="9.25" y="13.8" width="1.5" height="1.5" fill="var(--acc)"/></svg><span>{mdi(k)}</span></span><div>{md(v)}</div></div>'
        else: rows += f'<div class="note"><span class="k">{mdi(k)}</span><div>{md(v)}</div></div>'
    return f'<div class="notes">{rows}</div>'

def sec_figure(body, folder):
    m = re.search(r'!\[(.*?)\]\((.*?)\)', body)
    cap = re.sub(r'!\[.*?\]\(.*?\)', '', body)
    cap = re.sub(r'^\*\(.*?\)\*$', '', cap, flags=re.M).strip()
    img = f'<img src="{esc(m.group(2))}" alt="{esc(m.group(1))}">' if m else ''
    return f'<div class="figure">{img}<div>{md(cap)}</div></div>'

def sec_objects(body):
    _, ss = subs(body); cards = ''; tokmap = {}; gl = []
    for h, b in ss:
        role = ''
        toks = [c.split()[0] for c in re.findall(r'`([^`]+)`', h)]
        fid = 'f-' + slug(toks[0] if toks else h)
        for t in toks: tokmap.setdefault(t, fid)
        dl = ''
        for item in re.findall(r'^- (.+)$', b, re.M):
            mm = re.match(r'\*\*(.+?)\s*:\*\*\s*(.*)', item)
            if mm:
                k = mm.group(1)
                if 'piège' in k.lower(): dl += f'<dd class="trap"><svg class="warn-i" width="26" height="26" viewBox="0 0 20 20" role="img" aria-label="Piège"><path d="M10 2 L18.5 17 H1.5 Z" fill="none" stroke="var(--acc)" stroke-width="1.5" stroke-linejoin="round"/><rect x="9.25" y="7" width="1.5" height="5.5" fill="var(--acc)"/><rect x="9.25" y="13.8" width="1.5" height="1.5" fill="var(--acc)"/></svg><span>{mdi(mm.group(2))}</span></dd>'
                else: dl += f'<dt>{esc(k)}</dt><dd>{mdi(mm.group(2))}</dd>'
                if k.lower().startswith('rôle'): role = mm.group(2)
            else: dl += f'<dd>{mdi(item)}</dd>'
        cards += f'<article class="card" id="{fid}"><span class="obj">{mdi(h)}</span><dl>{dl}</dl></article>'
        gl.append(dict(toks=toks, fid=fid, head=mdi(h), role=mdi(role)))
    return f'<div class="cards">{cards}</div>', tokmap, gl

def sec_try(body, key):
    items = re.findall(r'^(?:- \[[ x]\]|\d+\.|-)\s+(.+)$', body, re.M)
    li = ''.join(f'<li><span class="i">{i+1:02d}</span><span>{mdi(t)}</span></li>' for i, t in enumerate(items))
    return f'<ol class="try">{li}</ol>'

def sec_further(body):
    intro, ss = subs(body); top = ''
    for q in quotes(intro):
        k, v = keyed(q)
        due = ' due' if k.lower().startswith('à rendre') else ''
        top += f'<div class="notation{due}"><p class="k">{mdi(k)}</p><div>{md(v)}</div></div>'
    cards = ''
    for h, b in ss:
        t, _, lv = h.partition(' · ')
        cards += f'<article class="card"><span class="lv">{esc(lv)}</span><h3>{mdi(t)}</h3>{render_rich(b)}</article>'
    return top + f'<div class="cards">{cards}</div>'

# ---------- session page ----------
SESSION_JS = Path(__file__).with_name('session.js').read_text()

def meta(cs, sname, S):
    course = cs[0]
    fm, cfg = S['fm'], S['cfg']
    tags = [n.strip() for n in str(fm.get('notions', '')).split(',') if n.strip()]
    objs = []
    if cfg.get('patch'):
        for o in json.loads((S['folder'] / cfg['patch']).read_text())['patcher']['boxes']:
            bx = o['box']; c = bx['maxclass']
            t = str(bx.get('text', '')).split(' ')[0] if c == 'newobj' else (None if c in ('comment', 'message') else c)
            if t and t not in objs: objs.append(t)
    asl = lambda v: [k.strip().split('/')[-1] for k in (v.split(',') if isinstance(v, str) else (v or []))]
    return dict(date=fm['date'], title=S['title'], key=sname, course=course, courses=cs, label=clabel(cs),
                tags=tags, objs=sorted(objs), avant=asl(fm.get('avant')), apres=asl(fm.get('apres')), gl=[])

def links_html(m, allm):
    by = {x['key']: x for x in allm}
    row = lambda x: f'<a class="row" href="../{x["key"]}/"><span class="d">{dshort(x["date"])}</span><span class="t">{esc(x["title"])}</span><span class="c">{esc(x["label"])} →</span></a>'
    out = ''
    for lab, keys in (('Avant cette séance', m['avant']), ('Pour la suite', m['apres'])):
        xs = [by[k] for k in keys if k in by]
        if xs: out += f'<span>{lab}</span><div>{"".join(row(x) for x in xs)}</div>'
    skip = set(m['avant'] + m['apres'] + [m['key']])
    rel = sorted(((len(set(x['tags']) & set(m['tags'])) * 2 + len(set(x['objs']) & set(m['objs'])), x) for x in allm if x['key'] not in skip), key=lambda t: -t[0])
    rel = [x for s, x in rel if s >= 3][:4]
    if rel: out += f'<span>Sur des notions proches</span><div>{"".join(row(x) for x in rel)}</div>'
    return f'<section class="s" id="liens"><h2>Dans la bibliothèque</h2><div class="links">{out}</div></section>' if out else ''

def build_session(sname, S, m, allm, depth=1):
    fm, cfg, folder = S['fm'], S['cfg'], S['folder']; course = m['course']
    d = fm['date']; out = OUT / sname; out.mkdir(parents=True, exist_ok=True)
    for f in folder.iterdir():
        if f.suffix in ('.png', '.jpg', '.jpeg', '.svg', '.maxpat', '.gif', '.webp'): shutil.copy(f, out / f.name)
    crumb = f'<a href="../index.html">EMC Studio</a><span>›</span><a href="../{course["slug"]}/index.html">{esc(course["title"])} {esc(course["level"])}</a><span>›</span><span>{dshort(d)}</span>'
    tags = m['tags']
    from urllib.parse import quote
    notions = ''.join(f'<a href="../index.html?q={quote(n)}#recherche" title="Tous les cours avec « {esc(n)} »">{esc(n)}</a>' for n in tags)
    patchf = cfg.get('patch')
    actions = ''
    if patchf:
        actions = (f'<div class="actions"><div class="seg"><button id="copyPatch" type="button">Copier le patch</button>'
                   f'<a class="btn ghost" href="{esc(patchf)}" download><span class="hide-s">Télécharger le </span>.maxpat</a>'
                   f'<a class="btn ghost" href="{esc(sname)}.pdf" download>PDF</a></div>'
                   f'<span class="small">Après « Copier le patch » : dans Max, <b>File › New From Clipboard</b></span></div>')
    due = any(h.lower().startswith('aller plus loin') and '**À rendre' in bd for h, bd in S['sections'])
    if due: actions = f'<a class="due-link" href="#{slug("Aller plus loin")}">Exercices à rendre <span aria-hidden="true">↓</span></a>' + actions
    body = (f'<div class="shead"><div class="meta"><span>{dshort(d)}</span><span class="lvl">{esc(nlabel(m["courses"]))}</span><span>{esc(m["label"])}</span></div>'
            f'<h1>{esc(S["title"])}</h1><div class="lead">{md(S["lead"])}</div>'
            f'<div class="notions">{notions}</div>{actions}</div>')
    if patchf:
        body += ('<div class="canvas"><svg id="patch" viewBox="' + esc(cfg.get('viewBox', '0 0 720 440')) + '" role="img" aria-label="Le patch redessiné"></svg></div>'
                 '<div class="legend"><span><i></i>câble signal (audio)</span><span><i class="c"></i>câble de contrôle (messages)</span><span>Cliquer sur une pastille pour suivre le parcours, sur un objet pour lire sa fiche</span></div>')
    tokmap = {}; demo_done = False
    for h, b in S['sections']:
        hl = h.lower()
        if hl.startswith('le parcours') or hl.startswith('le patch'): inner = sec_steps(b)
        elif hl.startswith('avant de commencer'): inner = sec_notes(b)
        elif '![' in b: inner = sec_figure(b, folder)
        elif hl.startswith('les objets'): inner, tokmap, m['gl'] = sec_objects(b)
        elif hl.startswith('à essayer'): inner = sec_try(b, sname)
        elif hl.startswith('aller plus loin'): inner = sec_further(b)
        elif hl.startswith('ressources'): inner = f'<div class="res">{md(b)}</div>'
        else: inner = f'<div class="prose">{render_rich(b)}</div>'
        body += f'<section class="s" id="{slug(h)}"><h2>{esc(h)}</h2>{inner}</section>'
        if not demo_done and ('![' in b) and cfg.get('demos'):
            body += demos_html(cfg['demos']); demo_done = True
    if cfg.get('demos') and not demo_done: body += demos_html(cfg['demos'])
    body += links_html(m, allm)
    data = {'patch': json.loads((folder / patchf).read_text()) if patchf else None,
            'zones': cfg.get('zones', {}), 'pins': cfg.get('pins', {}), 'tok': tokmap, 'key': sname}
    script = ('<div class="toast" id="toast">Copié</div><script type="application/json" id="data">'
              + json.dumps(data, ensure_ascii=False).replace('</', '<\\/') + '</script><script>' + SESSION_JS + '</script>')
    (out / 'index.html').write_text(shell(f'{S["title"].split(":")[0].strip()} · EMC Studio', depth, crumb, body, script))
    return m


def demos_html(which):
    parts = []
    if 'spat' in which:
        parts.append('''<div class="demo"><h3>Placer la source</h3><p class="small">Déplacer le point. Le message affiché est celui que le patch envoie à <code>spat5.oper</code>.</p>
<svg id="room" viewBox="0 0 400 400" aria-label="Vue du dessus : source et quatre haut-parleurs"></svg>
<span class="msg" id="adMsg">/source/1/ad 0.0 1.0</span>
<div class="ctrl"><label for="az">azimut</label><input type="range" id="az" min="-180" max="180" step="1" value="0"><output id="azO">0°</output></div>
<div class="ctrl"><label for="di">distance</label><input type="range" id="di" min="0.2" max="3.2" step="0.1" value="1"><output id="diO">1.0 m</output></div>
<div class="meters" id="meters"></div>
<p class="small">Calcul simplifié (panoramique à puissance constante entre deux haut-parleurs voisins, −6 dB par doublement de distance) : Spat y ajoute la réverbération et l'absorption de l'air. Schéma non à l'échelle.</p></div>''')
    if 'adsr' in which:
        parts.append('''<div class="demo"><h3>Façonner l'enveloppe</h3><p class="small">En gris : quand le toggle vaut 1. La courbe : la sortie de <code>adsr~</code> sur 2 secondes.</p>
<div class="fig"><svg id="env" aria-label="Courbe d'enveloppe ADSR"></svg></div>
<span class="msg" id="adsrMsg">adsr~ 5 50 0.5 200 · metro 500</span>
<div class="ctrl"><label for="eA">attack</label><input type="range" id="eA" min="1" max="600" value="5"><output id="eAO">5 ms</output></div>
<div class="ctrl"><label for="eD">decay</label><input type="range" id="eD" min="1" max="600" value="50"><output id="eDO">50 ms</output></div>
<div class="ctrl"><label for="eS">sustain</label><input type="range" id="eS" min="0" max="1" step="0.05" value="0.5"><output id="eSO">0.5</output></div>
<div class="ctrl"><label for="eR">release</label><input type="range" id="eR" min="1" max="1200" value="200"><output id="eRO">200 ms</output></div>
<div class="ctrl"><label for="eM">metro</label><input type="range" id="eM" min="50" max="1000" step="10" value="500"><output id="eMO">500 ms</output></div></div>''')
    return '<section class="s" id="jouer"><h2>Jouer avec, sans ouvrir Max</h2><div class="demos">' + ''.join(parts) + '</div></section>'

# ---------- course + home ----------
def build_course(course, sessions):
    out = OUT / course['slug']; out.mkdir(parents=True, exist_ok=True)
    rows = ''.join(f'<a class="row" href="../{esc(s["key"])}/"><span class="d">{dshort(s["date"])}</span><span class="t">{esc(s["title"])}</span><span class="c">→</span></a>'
                   for s in sorted(sessions, key=lambda s: s['date'], reverse=True))
    crumb = f'<a href="../index.html">EMC Studio</a><span>›</span><span>{esc(course["title"])} {esc(course["level"])}</span>'
    body = (f'<div class="ctitle"><span class="lvl">{esc(course["level"])}</span><h1>{esc(course["title"])}</h1></div>'
            + scope(course['slug'], H=120, label='')
            + (f'<div class="thread">{rows}</div>' if rows else ''))
    (out / 'index.html').write_text(shell(f'{course["title"]} {course["level"]} · EMC Studio', 1, crumb, body))

def build_home(courses, latest, allsess):
    n = len(courses); taps = [i * 1152 / n + 24 for i in range(n)]
    cols = ''.join(f'<a class="col" href="{c["slug"]}/"><span class="lvl">{esc(c["level"])}</span><span class="t">{esc(c["title"])}</span><span class="go"><span>Supports de cours</span><span>→</span></span></a>' for c in courses)
    lat = ''
    if latest:
        s = latest
        lat = (f'<section class="latest"><p class="label">Dernière séance</p><a class="row" href="{s["key"]}/">'
               f'<span class="d">{dshort(s["date"])}</span><span class="t">{esc(s["title"])}</span><span class="c">{esc(s["label"])} →</span></a></section>')
    idx = [dict(d=dshort(s['date']), iso=str(s['date']), t=s['title'], c=s['label'], h=f"{s['key']}/", tags=s['tags'], objs=s['objs']) for s in sorted(allsess, key=lambda s: s['date'], reverse=True)]
    srch = ('<section class="search" id="recherche"><p class="label">Rechercher une notion, un objet, un patch</p>'
            '<input id="q" type="search" placeholder="OSC, adsr~, spatialisation…" aria-label="Rechercher">'
            '<div class="tags" id="tags"></div><div class="hits" id="hits"></div></section>'
            '<script type="application/json" id="idx">' + json.dumps(idx, ensure_ascii=False).replace('</', '<\\/') + '</script>'
            '<script>' + Path(__file__).with_name('search.js').read_text() + '</script>')
    body = ('<div class="hero"><h1 class="giant">EMC</h1><div class="sub"><i></i><p>Electronic &amp; Multimedia Composition</p></div></div>'
            + scope('emc-home', taps=taps) + f'<div class="cols">{cols}</div>' + lat + srch)
    (OUT / 'index.html').write_text(shell('EMC Studio', 0, '<span>Supports de cours</span>', body))

def build_index(allm):
    out = OUT / 'notions'; out.mkdir(parents=True, exist_ok=True)
    srt = lambda xs: sorted(xs, key=lambda s: s.lower())
    row = lambda x, frag='': f'<li><a href="../{x["key"]}/{frag}">{dshort(x["date"])} · {esc(x["title"].split(":")[0].strip())}</a> <span>({esc(x["label"])})</span></li>'
    tags = srt({t for x in allm for t in x['tags']})
    ncards = ''.join(f'<div id="n-{slug(t)}"><h3>{esc(t)}</h3><ul>{"".join(row(x) for x in allm if t in x["tags"])}</ul></div>' for t in tags)
    objs = srt({o for x in allm for o in x['objs']} | {t for x in allm for g in x['gl'] for t in g['toks']})
    ocards = ''
    for o in objs:
        fiches = [(x, g) for x in allm for g in x['gl'] if o in g['toks']]
        role = next((g['role'] for x, g in fiches if g['role']), '')
        users = [x for x in allm if o in x['objs']]
        lis = ''.join(row(x, f'#{g["fid"]}') for x, g in fiches) + ''.join(row(x) for x in users if x not in [f[0] for f in fiches])
        ocards += f'<div id="o-{slug(o)}"><span class="o">{esc(o)}</span>{f"<p>{role}</p>" if role else ""}<ul>{lis}</ul></div>'
    jn = ''.join(f'<a href="#n-{slug(t)}">{esc(t)}</a>' for t in tags)
    jo = ''.join(f'<a href="#o-{slug(o)}">{esc(o)}</a>' for o in objs)
    body = ('<div class="ctitle"><span class="lvl">index</span><h1>Notions &amp; objets</h1></div>'
            f'<section class="s" style="padding-top:24px" id="notions"><h2>Notions</h2><div class="jump">{jn}</div><div class="idx">{ncards}</div></section>'
            f'<section class="s" id="objets"><h2>Objets</h2><p class="label">Chaque objet renvoie à sa fiche, ou aux patchs qui l\'utilisent.</p><div class="jump">{jo}</div><div class="idx">{ocards}</div></section>')
    (out / 'index.html').write_text(shell('Notions & objets · EMC Studio', 1, '<a href="../index.html">EMC Studio</a>', body))

def fail(folder, msg):
    sys.exit(f'\nERREUR dans {folder} :\n  {msg}\n')

def as_list(v):
    return [x.strip() for x in (v.split(',') if isinstance(v, str) else (v or [])) if str(x).strip()]

def discover(courses):
    """Every folder holding a .md under seances/ (any depth) is a session; check what the page needs."""
    bys = {c['slug']: c for c in courses}
    skip = lambda p: any(part[0] in '._' for part in p.relative_to(SRC).parts)
    found, seen = [], {}
    for folder in sorted({f.parent for f in SRC.rglob('*.md')} - {SRC}):
        if skip(folder): continue
        mds = sorted(folder.glob('*.md'))
        if len(mds) > 1: fail(folder, f'un seul fichier .md par séance (trouvés : {", ".join(m.name for m in mds)})')
        if not re.match(r'\d{4}-\d{2}-\d{2}-[a-z0-9-]+$', folder.name):
            fail(folder, 'le nom du dossier d\'une séance doit être de la forme AAAA-MM-JJ-mots-en-minuscules (ex. 2026-12-01-granular-01)')
        if folder.name in seen: fail(folder, f'une autre séance porte déjà ce nom : {seen[folder.name]}')
        seen[folder.name] = folder
        try: S = parse_session(folder)
        except yaml.YAMLError as e: fail(mds[0], f'en-tête illisible (entre les deux lignes ---) : {e}')
        except json.JSONDecodeError as e: fail(folder / 'config.json', f'JSON invalide : {e}')
        except AttributeError: fail(mds[0], 'il manque le titre de la page (une ligne « # Titre » avant la première section ##)')
        if 'date' not in S['fm']: fail(mds[0], 'il manque « date: AAAA-MM-JJ » dans l\'en-tête')
        p = S['cfg'].get('patch')
        if p and not (folder / p).exists(): fail(folder / 'config.json', f'le patch « {p} » n\'est pas dans le dossier')
        cs = as_list(S['fm'].get('cours'))
        if not cs: fail(mds[0], f'il manque la ligne « cours: … » dans l\'en-tête (cours possibles : {", ".join(bys)})')
        for c in cs:
            if c not in bys: fail(mds[0], f'« cours: {c} » : cours inconnu (cours possibles : {", ".join(bys)} ; voir courses.json)')
        found.append(([bys[c] for c in cs], folder.name, S))
    return found

courses = json.loads((SRC / 'courses.json').read_text())['courses']
found = discover(courses)
if OUT.exists(): shutil.rmtree(OUT)
OUT.mkdir(parents=True); shutil.copytree(ASSETS, OUT / 'assets')
(OUT / '.nojekyll').write_text('')
allsess = [meta(cs, s, S) for cs, s, S in found]
for (cs, s, S), m in zip(found, allsess): build_session(s, S, m, allsess)
for c in courses: build_course(c, [m for m in allsess if c in m['courses']])
build_index(allsess)
build_home(courses,max(allsess, key=lambda s: s['date']) if allsess else None, allsess)
print('built', len(allsess), 'session(s)')
