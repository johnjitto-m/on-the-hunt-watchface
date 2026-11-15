"""Pillow compositor for the v2.4 mock-ups (draws at 2x = 960 px)."""
import math, random
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance, ImageChops
import make_video as m

D = 'build/art/'
S = 2
_c = {}


def asset(n):
    if n not in _c:
        im = Image.open(D + n + '.png').convert('RGBA')
        _c[n] = im.resize((im.width * S, im.height * S), Image.LANCZOS)
    return _c[n]


def hexc(h): h = h.lstrip('#'); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


SKIES = {   # top, middle(y=200), horizon(y=330), horizon glow
    'dawn': ('#0a0a10', '#2a2232', '#9a6440', '#e0904a'),
    'day': ('#111924', '#33404e', '#6c7a88', None),
    'dusk': ('#0a0910', '#3a1c2c', '#b4552e', '#ff7a3a'),
    'night': ('#000000', '#06070c', '#10131c', None),
    'rain': ('#0a0d12', '#1f2934', '#3c4955', None),
    'storm': ('#06060b', '#171628', '#2b2a46', None),
    'snow': ('#0d0f13', '#2c333c', '#727c88', None),
    'cloudy': ('#0c0e11', '#2a2f36', '#5c636c', None),
}


def sky(kind, moon=True):
    key = ('sky', kind, moon)
    if key in _c: return _c[key]
    top, mid, hor, glow = SKIES[kind]
    W = 480 * S
    im = Image.new('RGBA', (W, W), (0, 0, 0, 255))
    px = ImageDraw.Draw(im)
    a, b, c = hexc(top), hexc(mid), hexc(hor)
    for y in range(380 * S):
        yy = y / S
        if yy < 200:
            u = (yy / 200) ** 1.4; col = tuple(int(a[i] + (b[i] - a[i]) * u) for i in range(3))
        else:
            u = min(1, (yy - 200) / 130); col = tuple(int(b[i] + (c[i] - b[i]) * u) for i in range(3))
        px.line([(0, y), (W, y)], fill=col + (255,))
    if glow:
        gl = Image.new('RGBA', im.size, (0, 0, 0, 0))
        ImageDraw.Draw(gl).ellipse([60 * S, 260 * S, 420 * S, 420 * S], fill=hexc(glow) + (150,))
        im.alpha_composite(gl.filter(ImageFilter.GaussianBlur(40 * S)))
    if kind == 'night':
        random.seed(3); d = ImageDraw.Draw(im)
        for _ in range(70):
            x, y = random.randint(20, 460), random.randint(20, 250); r = random.choice([0.6, 0.9, 1.2]) * S
            d.ellipse([x * S - r, y * S - r, x * S + r, y * S + r], fill=(230, 230, 240, random.choice([90, 140, 200])))
    if kind == 'night' and moon:
        d.ellipse([392 * S, 92 * S, 414 * S, 114 * S], fill=(217, 214, 207, 255))
        d.ellipse([385 * S, 89 * S, 407 * S, 111 * S], fill=hexc('#06070c') + (255,))
    _c[key] = im
    return im


def sb(b): return tuple(v * S for v in b)


def arc_pos(t):
    return 240 - 205 * math.cos(math.pi * t), 318 - 262 * math.sin(math.pi * t)


def sun_img(low, part):
    key = ('sun', round(low, 2), part)
    if key in _c: return _c[key]
    n = 200 * S; im = Image.new('RGBA', (n, n), (0, 0, 0, 0)); c = n // 2
    core = tuple(int(a + (b - a) * low) for a, b in zip((255, 250, 232), (255, 168, 80)))
    halo = tuple(int(a + (b - a) * low) for a, b in zip((255, 238, 180), (255, 130, 60)))
    if part == 'disc':
        g = Image.new('RGBA', (n, n), (0, 0, 0, 0)); gd = ImageDraw.Draw(g)
        gd.ellipse([c - 30 * S, c - 30 * S, c + 30 * S, c + 30 * S], fill=halo + (150,))
        im.alpha_composite(g.filter(ImageFilter.GaussianBlur(9 * S)))
        r = (14 + 3 * low) * S
        ImageDraw.Draw(im).ellipse([c - r, c - r, c + r, c + r], fill=core + (255,))
    else:
        g = Image.new('RGBA', (n, n), (0, 0, 0, 0)); gd = ImageDraw.Draw(g)
        for r, a in ((95, 30 + 30 * low), (60, 45 + 25 * low), (34, 60)):
            gd.ellipse([c - r * S, c - r * S, c + r * S, c + r * S], fill=halo + (int(a),))
        im.alpha_composite(g.filter(ImageFilter.GaussianBlur(18 * S)))
        r = (9 + 2 * low) * S
        ImageDraw.Draw(im).ellipse([c - r, c - r, c + r, c + r], fill=core + (150,))
    _c[key] = im
    return im


def moon_img(phase, part='disc'):
    key = ('moon', round(phase, 3), part)
    if key in _c: return _c[key]
    n = 80 * S; c = n // 2; r = 13 * S
    if part == 'glow':
        g = Image.new('RGBA', (n, n), (0, 0, 0, 0))
        lit = 1 - (math.cos(2 * math.pi * phase) + 1) / 2
        ImageDraw.Draw(g).ellipse([c - 30 * S, c - 30 * S, c + 30 * S, c + 30 * S], fill=(210, 220, 240, int(70 * lit)))
        _c[key] = g.filter(ImageFilter.GaussianBlur(10 * S)); return _c[key]
    disc = Image.new('RGBA', (n, n), (0, 0, 0, 0)); d = ImageDraw.Draw(disc)
    d.ellipse([c - r, c - r, c + r, c + r], fill=(232, 230, 222, 255))
    for (dx, dy, rr) in ((-4, -3, 2.6), (3, 2, 2), (-1, 5, 1.6), (5, -4, 1.3)):
        d.ellipse([c + (dx - rr) * S, c + (dy - rr) * S, c + (dx + rr) * S, c + (dy + rr) * S], fill=(200, 198, 190, 255))
    # phase mask: lit fraction via terminator ellipse
    mask = Image.new('L', (n, n), 0); md = ImageDraw.Draw(mask)
    k = math.cos(2 * math.pi * phase)            # 1 new .. -1 full
    waxing = phase < 0.5
    md.ellipse([c - r, c - r, c + r, c + r], fill=255)
    tw = abs(k) * r
    if k > 0:                                      # crescent: remove most of the disc
        md.rectangle([c - r, c - r, c, c + r] if waxing else [c, c - r, c + r, c + r], fill=0)
        md.ellipse([c - tw, c - r, c + tw, c + r], fill=0)
    else:                                          # gibbous: add bulge on the dark side
        md.rectangle([c - r, c - r, c, c + r] if waxing else [c, c - r, c + r, c + r], fill=0)
        md.ellipse([c - tw, c - r, c + tw, c + r], fill=255)
    lit = Image.new('RGBA', (n, n), (0, 0, 0, 0)); lit.paste(disc, (0, 0), mask)
    dark = disc.copy(); dark.putalpha(disc.getchannel('A').point(lambda v: int(v * 0.12)))
    out = Image.new('RGBA', (n, n), (0, 0, 0, 0))
    g = Image.new('RGBA', (n, n), (0, 0, 0, 0)); ImageDraw.Draw(g).ellipse([c - 26 * S, c - 26 * S, c + 26 * S, c + 26 * S], fill=(220, 225, 240, int(60 * (1 - max(0, k)))))
    out.alpha_composite(g.filter(ImageFilter.GaussianBlur(8 * S))); out.alpha_composite(dark); out.alpha_composite(lit)
    _c[key] = out
    return out


def celestial(im, st, part='disc'):
    h = st['hour']; wx = st.get('wx')
    if wx in ('rain', 'storm', 'snow'): return
    dim = 0.35 if wx in ('cloudy', 'fog') else 1.0
    if 6 <= h < 18:
        t = (h - 6) / 12; x, y = arc_pos(t); low = 1 - min(1, math.sin(math.pi * t) * 2.2)
        sp = sun_img(max(0, low), part)
    else:
        t = ((h - 18) % 24) / 12; x, y = arc_pos(t); sp = moon_img(st.get('moon', 0.6), part)
    if dim < 1:
        sp = sp.copy(); sp.putalpha(sp.getchannel('A').point(lambda v: int(v * dim)))
    im.alpha_composite(sp, (int(x * S - sp.width / 2), int(y * S - sp.height / 2)))


def calm(im, color=0.5, bright=0.7, blur=1.2):
    key = ('calm', id(im), color, bright)
    if key in _c: return _c[key]
    rgb = im.convert('RGB'); a = im.getchannel('A')
    hsv = rgb.convert('HSV'); _, sat, val = hsv.split()
    keep = ImageChops.multiply(sat.point(lambda v: 255 if v > 110 else 0), val.point(lambda v: 255 if v > 120 else 0)).filter(ImageFilter.GaussianBlur(2))
    c = ImageEnhance.Brightness(ImageEnhance.Color(rgb).enhance(color)).enhance(bright).filter(ImageFilter.GaussianBlur(blur))
    out = Image.composite(rgb, c, keep).convert('RGBA'); out.putalpha(a)
    _c[key] = out
    return out


def pool(im, cx, cy, warm=(255, 196, 120)):
    lay = Image.new('RGBA', im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for r, a in ((95, 26), (70, 30), (48, 34)):
        d.ellipse([(cx - r * 0.75) * S, (cy - r) * S, (cx + r * 0.75) * S, (cy + r) * S], fill=warm + (a,))
    d.ellipse([(cx - 52) * S, (372 - 7) * S, (cx + 52) * S, (372 + 7) * S], fill=warm + (70,))
    im.alpha_composite(lay.filter(ImageFilter.GaussianBlur(18 * S)))


def rim(sprite, col=(205, 222, 245), strength=200, side=-1):
    a = sprite.getchannel('A')
    sh = ImageChops.offset(a, -side * 1, 0)
    edge = ImageChops.subtract(a, sh).point(lambda v: min(255, int(v * strength / 255)))
    lay = Image.new('RGBA', sprite.size, col + (0,)); lay.putalpha(edge)
    out = sprite.copy()
    out = ImageEnhance.Contrast(out.convert('RGB')).enhance(1.12).convert('RGBA'); out.putalpha(a)
    out.alpha_composite(lay)
    return out


MASK = Image.new('L', (480 * S, 480 * S), 0)
ImageDraw.Draw(MASK).ellipse([0, 0, 480 * S - 1, 480 * S - 1], fill=255)
GOLD, GOLDL, RED = '#d4af37', '#ecd27a', '#e0213b'
GOAL = 15000


def face(st, t=0.0, size=960):
    night = st.get('night', False); wx = st.get('wx')
    skyk = wx if wx in ('rain', 'storm', 'snow', 'cloudy') else st.get('sky', 'night' if night else 'day')
    if st.get('bg') is not None:
        im = st['bg'].copy(); dr = ImageDraw.Draw(im)
        return _hud(im, dr, st, t, size, night, wx)
    im = sky(skyk, 'hour' not in st).copy()
    if st.get('calm'):
        im = ImageEnhance.Brightness(ImageEnhance.Color(im.convert('RGB')).enhance(0.8)).enhance(0.86).convert('RGBA')
    if 'hour' in st: celestial(im, st, 'disc')
    if st.get('towers'):
        tw = Image.open('build/frames/' + ('towers_night' if night else 'towers_day') + '.png').convert('RGBA')
        im.alpha_composite(tw.resize((480 * S, 380 * S), Image.LANCZOS), (0, 0))
    if 'hour' in st: celestial(im, st, 'glow')
    dr = ImageDraw.Draw(im)
    city = asset('city_night' if night else 'city_day')
    if st.get('calm'): city = calm(city, bright=0.62 if not night else 0.75)
    im.alpha_composite(city, (0, 176 * S))
    if wx in ('rain', 'storm'):
        im.alpha_composite(asset('wx_rain'), (0, int(((t % 3) * 120 - 360) * S)))
    if wx == 'snow':
        im.alpha_composite(asset('wx_snow'), (0, int(((t % 12) * 30 - 360) * S)))
    if wx == 'cloudy':
        im.alpha_composite(asset('wx_cloudy'), (int((-40 + 40 * math.sin(t * 0.8)) * S), 0))
    if wx == 'storm' and st.get('flash', True):
        im.alpha_composite(asset('wx_storm'), (0, 0))
    dr.rectangle([0, 380 * S, 480 * S, 480 * S], fill=(0, 0, 0, 255))
    return _hud(im, dr, st, t, size, night, wx)


def _hud(im, dr, st, t, size, night, wx):
    acc = RED if night else GOLD
    lab = '#ff7a8a' if night else GOLDL
    temp = st.get('temp')
    date = st.get('date', 'WED · 11 NOV') + (f'  ·  {temp}°' if temp is not None else '')
    if not st.get('hide_date'): m.txt(dr, sb((0, 26, 480, 26)), date, 'om', 19 * S, '#d6d6da', sp=0.22)
    if st.get('towers'):
        sh = Image.new('RGBA', im.size, (0, 0, 0, 0))
        m.txt(ImageDraw.Draw(sh), sb((0, 48, 480, 124)), st.get('time', '12:59'), 'bebas', 120 * S, (0, 0, 0, 200))
        m.txt(ImageDraw.Draw(sh), sb((0, 27, 480, 26)), date, 'om', 19 * S, (0, 0, 0, 220), sp=0.22)
        im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(5 * S))); dr = ImageDraw.Draw(im)
    if not st.get('hide_time'): m.txt(dr, sb((0, 46, 480, 124)), st.get('time', '12:59'), 'bebas', 120 * S, '#f4f4f2')
    if st.get('towers'): m.txt(dr, sb((0, 26, 480, 26)), date, 'om', 19 * S, '#d6d6da', sp=0.22)
    # health
    bat = st.get('bat', 75); chg = st.get('charging')
    B, Hh = st.get('dxb', 0), st.get('dxh', 0)
    if not st.get('hide_bat'):
        m.txt(dr, sb((60 + B, 176, 100, 40)), str(bat), 'om', 32 * S, '#ffffff', 'END')
        m.txt(dr, sb((161 + B, 184, 40, 28)), '%', 'om', 21 * S, '#ffffff', 'START')
    if chg and not st.get('hide_bat'): im.alpha_composite(asset('ic_bolt'), ((184 + B) * S, 184 * S))
    low = bat < 20
    on = round(bat / 10)
    blk = '#ff6a3d' if low else (RED if night else GOLD)
    for i in (range(10) if not st.get('hide_bat') else []):
        lit = i < on; col = blk if lit else '#2a2a2e'
        if chg and i == on: col = '#ffe08a'
        if low and lit and st.get('blink'): col = '#3a1a10'
        dr.rectangle(sb((79 + B + i * 14, 218, 79 + B + i * 14 + 10, 228)), fill=col)
    status = 'RELOADING…' if chg else ('CRITICAL' if low else ('WOUNDED' if bat < 50 else 'COMBAT READY'))
    scol = '#ffe08a' if chg else ('#ff8a4a' if low else ('#ff7a8a' if night else '#e8d9a8'))
    if not st.get('hide_bat') and not st.get('hide_status'): m.txt(dr, sb((60 + B, 232, 175, 18)), status, 'om', 13 * S, scol, sp=0.12)
    if not st.get('nodiv'): dr.rectangle(sb((239, 178, 240, 246)), fill='#3a3a40')
    hr = st.get('hr', 75)
    if st.get('bat_arc'):
        col = (255, 75, 75) if low else ((245, 197, 66) if bat < 50 else (61, 220, 132))
        r = 226 * S; box = [240 * S - r, 240 * S - r, 240 * S + r, 240 * S + r]
        for i in range(10):
            a0 = 242 + i * 5.8 + 0.8; a1 = 242 + (i + 1) * 5.8 - 0.8
            lit = bat > i * 10
            c = col if lit else (52, 52, 58)
            if chg and i * 10 < bat <= (i + 1) * 10: c = (200, 255, 224)
            dr.arc(box, a0 - 90, a1 - 90, fill=c, width=7 * S)
    if not st.get('hide_hr'):
        im.alpha_composite(asset('heart_2'), ((264 + Hh) * S, 184 * S))
        m.txt(dr, sb((288 + Hh, 176, 62, 40)), str(hr), 'om', 32 * S, '#ffffff')
        m.txt(dr, sb((352 + Hh, 189, 50, 20)), 'BPM', 'om', 14 * S, '#d6d6da', 'START', 0.1)
        im.alpha_composite(asset('ecg'), ((277 + Hh) * S, 216 * S))
        hs = 'ADRENALINE' if hr >= 140 else ('ON EDGE' if hr >= 100 else 'CALM')
        m.txt(dr, sb((245 + Hh, 232, 175, 18)), hs, 'om', 13 * S, '#ff7a8a' if (night or hr >= 100) else '#e8d9a8', sp=0.12)
    # trail
    steps = st.get('steps', 10281); p = min(100, steps * 100 / GOAL)
    TX0, TX1 = 70, 352
    for x in range(TX0, TX1, 8):
        dr.rectangle(sb((x, 374, x + 4, 376)), fill='#55555c')
    dr.rectangle(sb((TX0, 373, TX0 + (TX1 - TX0) * p / 100, 377)), fill=acc)
    for mk in (25, 50, 75):                        # milestone ticks (lit once passed)
        mx = TX0 + (TX1 - TX0) * mk / 100
        dr.rectangle(sb((mx - 1, 368, mx + 1, 382)), fill=acc if p >= mk else '#55555c')
    done = steps >= GOAL
    CX = 352
    fx = 24 + 2.3 * p
    pose = st.get('fig', 'stand')
    if done:
        im.alpha_composite(asset('coin_done'), (CX * S, 360 * S))
        if st.get('layers'):
            for lim, lx, ly in st['layers']:
                im.alpha_composite(lim.resize((lim.width * S, lim.height * S), Image.LANCZOS), (int(lx * S), int(ly * S)))
        else:
            im.alpha_composite(asset('fig_aim'), (226 * S, 248 * S))
            im.alpha_composite(asset('dog_happy_03'), (186 * S, 333 * S))
        bf = st.get('blast')
        if st.get('notext'):
            pass
        elif bf is not None:
            k = .7; b = asset(f'blast_{bf:02d}'); b = b.resize((int(b.width * k), int(b.height * k)), Image.LANCZOS)
            im.alpha_composite(b, (int((367 - 111 * k) * S), int((375 - 123 * k) * S)))
        else:
            m.txt(dr, sb((0, 390, 480, 32)), 'CONTRACT FULFILLED', 'om', 22 * S, '#f4f4f2', sp=0.17)
            dr.rectangle(sb((152, 424, 328, 425)), fill=RED)
            m.txt(dr, sb((0, 428, 480, 26)), f'+{steps - GOAL} OVERTIME', 'om', 16 * S, GOLDL, sp=0.12)
    else:
        im.alpha_composite(asset('coin_red' if night else 'coin_gold'), (CX * S, 360 * S))
        if st.get('layers'):
            if st.get('pool'): pool(im, *st['pool'])
            for lim, lx, ly in st['layers']:
                im.alpha_composite(lim.resize((lim.width * S, lim.height * S), Image.LANCZOS), (int(lx * S), int(ly * S)))
            pose = '_layers'
        if pose == '_layers': pass
        elif pose == 'walk': fig = f'walk_{int(t * 8) % 12:02d}'
        elif pose == 'reload': fig = 'reload_03'
        elif pose == 'kneel': fig = 'fig_kneel'
        elif pose == 'lean': fig = 'fig_lean'
        else: fig = 'fig_front'
        if pose != '_layers': im.alpha_composite(asset(fig), (int(fx * S), 248 * S))
        dx = fx - 34 if fx >= 60 else fx + 80
        if pose == 'lean': dx = fx + 62
        if pose == '_layers': pass
        elif st.get('notif'):
            im.alpha_composite(asset('dog_alert_03'), (int(dx * S), 320 * S))
        elif pose == 'walk':
            im.alpha_composite(asset(f'dog_walk_{int(t * 13) % 6:02d}'), (int(dx * S), 338 * S))
        else:
            im.alpha_composite(asset('dog_sit'), (int(dx * S), 338 * S))
        if st.get('label'):
            m.txt(dr, sb((0, 390, 480, 22)), st['label'], 'om', 15 * S, st.get('label_color', '#ffb347'), sp=0.16)
        elif pose == 'lean':
            m.txt(dr, sb((0, 390, 480, 22)), 'BEHIND PACE · TIME TO MOVE', 'om', 15 * S, '#ffb347', sp=0.16)
        else:
            if not st.get('no_bounty'): m.txt(dr, sb((0, 390, 480, 22)), "TONIGHT'S BOUNTY" if night else "TODAY'S BOUNTY", 'om', 15 * S, lab, sp=0.2)
        m.txt(dr, sb((0, 408, 480, 44)), f'{steps:,} / {GOAL:,}', 'om', 34 * S, '#ffffff')
        if st.get('dossier'):
            x0, y0 = int(fx + 92), 256
            card = Image.new('RGBA', im.size, (0, 0, 0, 0)); cd = ImageDraw.Draw(card)
            cd.rounded_rectangle(sb((x0, y0, x0 + 150, y0 + 84)), radius=8 * S, fill=(8, 8, 10, 230), outline=hexc(GOLD) + (255,), width=2 * S)
            im.alpha_composite(card); dr = ImageDraw.Draw(im)
            m.txt(dr, sb((x0 + 12, y0 + 8, 130, 16)), 'DOSSIER · TODAY', 'om', 11 * S, GOLDL, 'START', 0.18)
            m.txt(dr, sb((x0 + 12, y0 + 26, 130, 26)), f'{steps:,} STEPS', 'om', 20 * S, '#ffffff', 'START')
            m.txt(dr, sb((x0 + 12, y0 + 54, 130, 22)), f'{GOAL - steps:,} TO GO · {round(p)}%', 'om', 13 * S, '#d6d6da', 'START', 0.06)
            dr.polygon(sb((x0, y0 + 30, x0 - 8, y0 + 38, x0, y0 + 46)), fill=GOLD)
    if st.get('post'): st['post'](im)
    out = Image.new('RGBA', im.size, (0, 0, 0, 0))
    out.paste(im, (0, 0), MASK)
    return out if size == 960 else out.resize((size, size), Image.LANCZOS)
