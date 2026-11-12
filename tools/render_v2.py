"""Render all v2 watch-face bitmaps with headless Chrome (transparent PNGs)."""
import math, os, re, sys, asyncio, random
sys.path.insert(0, 'tools')
import color_poses as P, backdrops as B, styles
from playwright.async_api import async_playwright

OUT = 'build/art'
os.makedirs(OUT, exist_ok=True)
tpl = open('tools/hunt2_template.html').read()
STYLE = tpl[tpl.index('<style>') + 7: tpl.index('</style>')]
FONTS = ''


def fix(s):
    return re.sub(r'<(path|circle|ellipse|polyline|line|rect|polygon|text|stop)([^>]*?)/>', r'<\1\2></\1>', s)


def fig(inner, w=72, h=116):
    return (f'<svg width="{w}" height="{h}" viewBox="0 0 {w / 0.3:.3f} {h / 0.3:.3f}" style="display:block; overflow: hidden">'
            f'<g transform="translate(40 26.667)">{fix(inner)}</g></svg>')


def subs(s, vals):
    for k, v in vals.items():
        s = s.replace('{{' + k + '}}', str(v))
    return s


JOBS = []   # (name, html, width, height, times[list of seconds or None])


def job(name, body, w, h, times=None):
    JOBS.append((name, body, w, h, times))


# ---------- character
job('fig_front', fig(P.front()), 72, 116)
job('fig_aim', fig(P.aim_static(42)), 72, 116)
job('fig_kneel', fig(P.kneel()), 72, 116)
job('walk', fig(P.walk()), 72, 116, [i * 1.8 / 12 for i in range(12)])
job('reload', fig(P.reload()), 72, 116, [i * 1.6 / 8 for i in range(8)])
aod_fig = styles.ink()
for a, b in (('#e9e4d8', '#8c8c92'), ('stroke-width="1.5"', 'stroke-width="3.4"'), ('stroke-width="1.3"', 'stroke-width="2.6"'),
             ('stroke-width="1.2"', 'stroke-width="2.4"'), ('stroke-width="0.6"', 'stroke-width="1"'), ('stroke-width="0.8"', 'stroke-width="1.6"')):
    aod_fig = aod_fig.replace(a, b)
aod_fig = re.sub(r'<path d="M\d+(\.\d+)? \d+(\.\d+)? L[^"]*" stroke="#8c8c92" stroke-width="1" opacity="0.7"></path>', '', aod_fig)
job('fig_aod', fig(aod_fig), 72, 116)

# ---------- dog
def dogbox(svg, w=34, h=30):
    return f'<div style="width:{w}px;height:{h}px;padding-top:4px;box-sizing:border-box">{svg}</div>'
job('dog_sit', dogbox(B.DOG), 34, 30)
job('dog_walk', dogbox(B.DOGWALK), 34, 30, [i * 0.45 / 6 for i in range(6)])
job('dog_alert', dogbox(B.DOGALERT, 34, 44).replace('padding-top:4px', 'padding-top:18px'), 34, 44, [i * 1.2 / 8 for i in range(8)])
job('dog_happy', dogbox(B.DOGHAPPY, 34, 34).replace('padding-top:4px', 'padding-top:8px'), 34, 34, [i * 0.8 / 8 for i in range(8)])
dog_aod = B.DOG.replace('#cfcac0', '#77777d').replace('#26221f', '#000000').replace('stroke="#c8102e"', 'stroke="#5a1f26"')
job('dog_aod', dogbox(dog_aod), 34, 30)

# ---------- backgrounds (480 x 204 placed at y=176)
def city(kind, night):
    vals = dict(winColor='#e3c463' if night else '#3a3424', neonColor='#e0213b', neonGlow=0.8 if night else 0.4,
                lampGlow=0.35 if night else 0.15)
    if kind == 'noir':
        far, near = B.noir()
        signs = B.noir_signs()
        band = (f'<div style="position:absolute;left:0;top:30px;width:480px;height:168px">'
                f'<svg width="480" height="168" viewBox="0 0 480 168" style="position:absolute;left:0;top:0;overflow:visible">{far}</svg>'
                + ('<div style="position:absolute;left:392px;top:-10px;width:22px;height:22px;border-radius:50%;background:#d9d6cf;box-shadow:inset -7px -3px 0 0 #000,0 0 12px rgba(217,214,207,.35)"></div>' if night else '')
                + f'<svg width="480" height="168" viewBox="0 0 480 168" style="position:absolute;left:0;top:0;overflow:visible">{near}</svg>'
                f'<svg width="480" height="168" viewBox="0 0 480 168" style="position:absolute;left:0;top:0;overflow:visible">{signs}</svg></div>')
    else:
        far, near = B.rain()
        band = (f'<div style="position:absolute;left:0;top:102px;width:480px;height:96px">'
                f'<svg width="480" height="96" viewBox="0 0 480 96" style="position:absolute;left:0;top:0;overflow:visible">{far}</svg>'
                f'<svg width="480" height="96" viewBox="0 0 480 96" style="position:absolute;left:0;top:0;overflow:visible">{near}</svg></div>')
    html = (f'<div style="position:relative;width:480px;height:204px;overflow:hidden">{band}'
            '<div style="position:absolute;left:0;top:0;width:480px;height:110px;background:linear-gradient(180deg,#000 0%,rgba(0,0,0,.55) 55%,rgba(0,0,0,0) 100%)"></div>'
            '<div style="position:absolute;left:0;top:180px;width:480px;height:24px;background:linear-gradient(180deg,rgba(0,0,0,0) 0%,#000 90%)"></div></div>')
    return subs(fix(html), vals)

for kind in ('noir', 'rain'):
    for night in (False, True):
        job(f'bg_{kind}_{"night" if night else "day"}', city(kind, night), 480, 204)
aod_far, aod_near = B.noir()
aod_html = (f'<div style="position:relative;width:480px;height:204px;overflow:hidden">'
            f'<div style="position:absolute;left:0;top:30px;width:480px;height:168px;opacity:.32;filter:grayscale(1)"><svg width="480" height="168" viewBox="0 0 480 168" style="overflow:visible">{aod_far}</svg></div>'
            f'<div style="position:absolute;left:0;top:30px;width:480px;height:168px;opacity:.4;filter:grayscale(1)"><svg width="480" height="168" viewBox="0 0 480 168" style="overflow:visible">{aod_near}</svg></div>'
            '<div style="position:absolute;left:0;top:0;width:480px;height:110px;background:linear-gradient(180deg,#000 0%,rgba(0,0,0,.6) 55%,rgba(0,0,0,0) 100%)"></div></div>')
job('bg_aod', subs(fix(aod_html), dict(winColor='#3a3a40', neonColor='#5a1f26', neonGlow=0.0, lampGlow=0.04)), 480, 204)

# ---------- weather tiles (480 x 720, period 360 vertically)
random.seed(8)
drops = [(random.randint(-10, 500), random.randint(0, 360), random.choice([0.9, 1.1]), random.choice([0.18, 0.25, 0.33])) for _ in range(85)]
rain = ''.join(f'<line x1="{x}" y1="{y + k * 360}" x2="{x - 2}" y2="{y + k * 360 + 12}" stroke="#b6c0d2" stroke-width="{w}" stroke-linecap="round" opacity="{o}"></line>'
               for k in (0, 1) for x, y, w, o in drops)
job('wx_rain', f'<svg width="480" height="720" viewBox="0 0 480 720">{rain}</svg>', 480, 720)
random.seed(4)
fl = [(random.randint(-10, 490), random.randint(0, 360), random.choice([1, 1.3, 1.8]), random.choice([0.4, 0.6, 0.8])) for _ in range(90)]
snow = ''.join(f'<circle cx="{x}" cy="{y + k * 360}" r="{r}" fill="#eef2f7" opacity="{o}"></circle>' for k in (0, 1) for x, y, r, o in fl)
job('wx_snow', f'<svg width="480" height="720" viewBox="0 0 480 720">{snow}</svg>', 480, 720)
def clouds(spec, color):
    return ('<div style="position:relative;width:560px;height:374px">' + ''.join(
        f'<div style="position:absolute;left:{x + 40}px;top:{y}px;width:{w}px;height:{h}px;border-radius:50%;background:{color};opacity:{o};filter:blur(15px)"></div>'
        for x, y, w, h, o in spec) + '</div>')
job('wx_cloudy', clouds([(-40, 30, 220, 46, .5), (200, 10, 260, 52, .45), (380, 70, 200, 44, .4), (40, 150, 240, 40, .32), (280, 190, 230, 40, .3)], '#3c4049'), 560, 374)
job('wx_fog', clouds([(-60, 40, 240, 48, .38), (190, 20, 260, 50, .34), (360, 90, 220, 46, .32), (-20, 170, 250, 44, .30), (250, 200, 260, 46, .30), (60, 270, 280, 40, .34), (320, 300, 220, 36, .36)], '#565a63'), 560, 374)
job('wx_storm', '<div style="position:relative;width:480px;height:374px;background:radial-gradient(circle at 80% 25%, rgba(220,230,255,.55), rgba(220,230,255,.12) 55%, rgba(0,0,0,0) 85%)">'
    '<svg width="70" height="230" viewBox="0 0 40 130" style="position:absolute;left:380px;top:20px"><path d="M24 0 L10 52 L19 52 L6 96 L13 96 L4 130 L30 82 L22 82 L33 42 L24 42 L32 0 Z" fill="#e9f0ff"></path></svg>'
    '<svg width="40" height="120" viewBox="0 0 40 120" style="position:absolute;left:50px;top:60px"><path d="M22 0 L10 46 L18 46 L8 120 L30 38 L21 38 L30 0 Z" fill="#dfe8ff"></path></svg></div>', 480, 374)
job('glow', '<div style="width:120px;height:120px;border-radius:50%;background:radial-gradient(circle, rgba(224,33,59,.6) 0%, rgba(224,33,59,.2) 45%, rgba(224,33,59,0) 70%)"></div>', 120, 120)

# ---------- coins
def coin(bg, mark, crack=False):
    c = ('<svg width="30" height="30" viewBox="0 0 30 30" style="position:absolute;left:0;top:0"><g fill="none" stroke="#ff3b2b" stroke-width="1.4"><polyline points="15,2 13,10 17,14 12,20 15,28"></polyline><polyline points="17,14 24,12 28,15"></polyline><polyline points="13,10 6,8"></polyline></g></svg>' if crack else '')
    return (f'<div style="position:relative;width:30px;height:30px;box-sizing:border-box;border-radius:50%;background:{bg};border:2px solid rgba(0,0,0,.45);display:flex;align-items:center;justify-content:center">'
            f'<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="{mark}" stroke-width="2.4"><circle cx="12" cy="12" r="7"></circle><line x1="12" y1="1" x2="12" y2="7"></line><line x1="12" y1="17" x2="12" y2="23"></line><line x1="1" y1="12" x2="7" y2="12"></line><line x1="17" y1="12" x2="23" y2="12"></line></svg>{c}</div>')
job('coin_gold', coin('#d4af37', '#1a1408'), 30, 30)
job('coin_red', coin('#c8102e', '#1a1408'), 30, 30)
job('coin_done', coin('#2a0b10', '#e0213b', True), 30, 30)


async def main():
    async with async_playwright() as p:
        br = await p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
        pg = await br.new_page(device_scale_factor=1)
        for name, body, w, h, times in JOBS:
            html = (f'<!doctype html><html><head><meta charset="utf-8">{FONTS}<style>{STYLE} html,body{{margin:0;background:transparent}}</style></head>'
                    f'<body><div id="t" style="width:{w}px;height:{h}px;overflow:hidden;position:relative">{body}</div></body></html>')
            await pg.set_viewport_size({'width': max(w, 100), 'height': max(h, 100)})
            await pg.set_content(html, wait_until='load')
            el = await pg.query_selector('#t')
            if times is None:
                await pg.evaluate('document.getAnimations().forEach(a => { a.pause(); a.currentTime = 0; })')
                await el.screenshot(path=f'{OUT}/{name}.png', omit_background=True)
            else:
                for i, t in enumerate(times):
                    await pg.evaluate(f'document.getAnimations().forEach(a => {{ a.pause(); a.currentTime = {t * 1000}; }})')
                    await el.screenshot(path=f'{OUT}/{name}_{i:02d}.png', omit_background=True)
        await br.close()

if __name__ == "__main__":
    asyncio.run(main())
print('rendered', len(os.listdir(OUT)))
