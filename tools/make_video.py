"""Short cinematic demo of the 'On the Hunt' watch face (1080x1920, 30 fps)."""
import math, os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

D = 'build/art/'
FONTS = {'bebas': 'watchface/src/main/res/font/bebas_neue.ttf', 'om': 'watchface/src/main/res/font/oswald_medium.ttf',
         'or': 'watchface/src/main/res/font/oswald_regular.ttf'}
W, H, FPS = 1080, 1920, 30
S = 2                     # face drawn at 960 px (2x the watch's 480)
FACE = 900                # on-screen face size
FX, FY = (W - FACE) // 2, 430
OUT = 'build/'
_cache = {}


def asset(name):
    if name not in _cache:
        im = Image.open(D + name + '.png').convert('RGBA')
        _cache[name] = im.resize((im.width * S, im.height * S), Image.LANCZOS)
    return _cache[name]


def font(k, size):
    key = (k, size)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(FONTS[k], size)
    return _cache[key]


def txt(dr, box, s, fn, size, color, align='CENTER', sp=0.0):
    x, y, w, h = box
    f = font(fn, size)
    asc, desc = f.getmetrics()
    ws = [f.getlength(c) for c in s]
    tot = sum(ws) + sp * size * (len(s) - 1)
    cx = x + (w - tot) / 2 if align == 'CENTER' else (x + w - tot if align == 'END' else x)
    ty = y + (h - (asc + desc)) / 2
    for c, cw in zip(s, ws):
        dr.text((cx, ty), c, font=f, fill=color)
        cx += cw + sp * size


def sb(b): return tuple(v * S for v in b)


MASK = Image.new('L', (480 * S, 480 * S), 0)
ImageDraw.Draw(MASK).ellipse([0, 0, 480 * S - 1, 480 * S - 1], fill=255)


def face(st, t):
    """Draw the watch face (960x960) for state dict st at time t (seconds into scene)."""
    im = Image.new('RGBA', (480 * S, 480 * S), (0, 0, 0, 255))
    dr = ImageDraw.Draw(im)
    night, wx = st.get('night', False), st.get('wx')
    rainy = wx in ('rain', 'storm')
    im.alpha_composite(asset(('bg_rain_' if rainy else 'bg_noir_') + ('night' if night else 'day')), (0, 176 * S))
    if rainy:
        tile = asset('wx_rain'); y = int(((t % 3) * 120 - 360) * S)
        im.alpha_composite(tile, (0, y))
    if wx == 'snow':
        tile = asset('wx_snow'); y = int((((t % 12) * 30) - 360) * S)
        im.alpha_composite(tile, (0, y))
    if wx in ('cloudy', 'fog'):
        im.alpha_composite(asset('wx_' + wx), (int((-40 + 40 * math.sin(t * 0.8)) * S), 0))
    if wx == 'storm':
        ph = t % 2.2
        if ph < 0.12 or 0.22 < ph < 0.32:
            im.alpha_composite(asset('wx_storm'), (0, 0))
    if wx in ('rain', 'storm', 'snow'):
        dr.rectangle([0, 380 * S, 480 * S, 480 * S], fill=(0, 0, 0, 255))
    acc = '#c8102e' if night else '#d4af37'
    lab = '#ff7a8a' if night else '#ecd27a'
    txt(dr, sb((0, 32, 480, 30)), st.get('date', 'WED · 11 NOV'), 'om', 21 * S, '#d6d6da', sp=0.24)
    txt(dr, sb((0, 56, 480, 140)), st.get('time', '12:59'), 'bebas', 136 * S, '#f4f4f2')
    bat = st.get('bat', 75)
    txt(dr, sb((60, 214, 102, 44)), str(bat), 'om', 36 * S, '#ffffff', 'END')
    txt(dr, sb((163, 222, 40, 32)), '%', 'om', 24 * S, '#ffffff', 'START')
    if st.get('charging'):
        im.alpha_composite(asset('ic_bolt'), (186 * S, 210 * S))
    on = round(bat / 10)
    for i in range(10):
        lit = i < on
        col = '#e0213b' if lit else '#2a2a2e'
        if st.get('charging') and i == on and int(t * 2) % 2 == 0: col = '#ffd36b'
        if bat < 20 and lit and int(t * 2.5) % 2: col = '#3a1a10'
        dr.rectangle(sb((79 + i * 14, 260, 79 + i * 14 + 10, 272)), fill=col)
    status = 'RELOADING…' if st.get('charging') else ('CRITICAL' if bat < 20 else ('WOUNDED' if bat < 50 else 'COMBAT READY'))
    scol = '#ffd36b' if st.get('charging') else ('#ff9a4a' if bat < 20 else '#ff7a8a')
    txt(dr, sb((60, 276, 175, 20)), status, 'om', 14 * S, scol, sp=0.12)
    dr.rectangle(sb((239, 210, 240, 273)), fill='#2a2a2e')
    hr = st.get('hr', 75)
    beat = int((t * hr / 60) * 6) % 6
    im.alpha_composite(asset(f'heart_{beat}'), (266 * S, 218 * S))
    txt(dr, sb((290, 215, 62, 44)), str(hr), 'om', 36 * S, '#ffffff')
    txt(dr, sb((354, 229, 50, 22)), 'BPM', 'om', 15 * S, '#d6d6da', 'START', 0.1)
    im.alpha_composite(asset('ecg'), (277 * S, 261 * S))
    txt(dr, sb((245, 277, 175, 20)), 'ADRENALINE' if hr >= 140 else ('ON EDGE' if hr >= 100 else 'CALM'), 'om', 14 * S, '#ff7a8a', sp=0.12)
    steps, goal = st.get('steps', 10281), 15000
    p = min(100, steps * 100 / goal)
    im.alpha_composite(asset('track_dash'), (70 * S, 374 * S))
    dr.rectangle(sb((70, 374, 70 + 3.2 * p, 377)), fill=acc)
    done = steps >= goal
    if done:
        im.alpha_composite(asset('coin_done'), (386 * S, 360 * S))
        im.alpha_composite(asset('fig_aim'), (292 * S, 278 * S))
        im.alpha_composite(asset(f'dog_happy_{int(t * 10) % 8:02d}'), (262 * S, 343 * S))
        bi = int(t * 12)
        if 0 <= bi < 40:
            im.alpha_composite(asset(f'blast_{bi % 20:02d}'), (290 * S, 252 * S))
        txt(dr, sb((0, 392, 480, 32)), 'CONTRACT FULFILLED', 'om', 23 * S, '#f4f4f2', sp=0.17)
        dr.rectangle(sb((150, 427, 329, 428)), fill='#e0213b')
        txt(dr, sb((0, 432, 480, 26)), f'+{steps - goal} OVERTIME', 'om', 17 * S, '#ecd27a', sp=0.12)
    else:
        im.alpha_composite(asset('coin_red' if night else 'coin_gold'), (386 * S, 360 * S))
        fx = 37 + 2.76 * p
        mode = st.get('fig', 'stand')
        if mode == 'walk':
            fig = f'walk_{int(t * 8) % 12:02d}'
        elif mode == 'reload':
            fig = f'reload_{int(t * 5) % 8:02d}'
        elif mode == 'kneel':
            fig = 'fig_kneel'
        else:
            fig = 'fig_front'
        im.alpha_composite(asset(fig), (int(fx * S), 278 * S))
        dx = fx - 30 if fx >= 72 else fx + 62
        if st.get('notif'):
            im.alpha_composite(asset(f'dog_alert_{int(t * 8) % 8:02d}'), (int(dx * S), 333 * S))
        elif mode == 'walk':
            im.alpha_composite(asset(f'dog_walk_{int(t * 13) % 6:02d}'), (int(dx * S), 347 * S))
        else:
            im.alpha_composite(asset('dog_sit'), (int(dx * S), 347 * S))
        txt(dr, sb((0, 390, 480, 22)), "TONIGHT'S BOUNTY" if night else "TODAY'S BOUNTY", 'om', 16 * S, lab, sp=0.2)
        txt(dr, sb((0, 410, 480, 46)), f'{steps} / {goal}', 'om', 36 * S, '#ffffff')
    out = Image.new('RGBA', im.size, (0, 0, 0, 0))
    out.paste(im, (0, 0), MASK)
    return out.resize((FACE, FACE), Image.LANCZOS)


def backdrop(glow):
    bg = Image.new('RGB', (W, H), (8, 8, 10))
    g = Image.new('RGB', (W, H), (0, 0, 0))
    ImageDraw.Draw(g).ellipse([FX - 220, FY - 220, FX + FACE + 220, FY + FACE + 220], fill=glow)
    g = g.filter(ImageFilter.GaussianBlur(180))
    bg = Image.blend(bg, Image.eval(g, lambda v: v), 0.55)
    d = ImageDraw.Draw(bg)
    # watch bezel
    d.ellipse([FX - 34, FY - 34, FX + FACE + 34, FY + FACE + 34], fill=(26, 26, 30))
    d.ellipse([FX - 22, FY - 22, FX + FACE + 22, FY + FACE + 22], fill=(12, 12, 14))
    d.ellipse([FX - 34, FY - 34, FX + FACE + 34, FY + FACE + 34], outline=(60, 60, 66), width=3)
    return bg


BACK = {}


def frame(scene, t):
    glow = scene.get('glow', (60, 48, 20))
    if glow not in BACK:
        BACK[glow] = backdrop(glow)
    img = BACK[glow].copy()
    if scene.get('face') is not None:
        st = scene['face'](t) if callable(scene['face']) else scene['face']
        f = face(st, t + scene.get('t0', 0))
        img.paste(f, (FX, FY), f)
    d = ImageDraw.Draw(img)
    dur = scene['dur']
    # caption fade
    a = max(0, min(1, (t - 0.25) / 0.45)) * max(0, min(1, (dur - t - 0.15) / 0.35))
    if scene.get('title'):
        col = tuple(int(c * a) for c in (233, 228, 216))
        gold = tuple(int(c * a) for c in (217, 178, 90))
        if scene.get('face') is None:
            txt(d, (0, 760, W, 170), scene['title'], 'bebas', 168, col, sp=0.06)
            d.rectangle([W // 2 - 90, 952, W // 2 + 90, 955], fill=gold)
            txt(d, (0, 980, W, 60), scene.get('sub', ''), 'or', 34, tuple(int(c * a) for c in (160, 160, 168)), sp=0.18)
        else:
            txt(d, (0, 1430, W, 110), scene['title'], 'bebas', 92, col, sp=0.08)
            d.rectangle([W // 2 - 60, 1548, W // 2 + 60, 1550], fill=gold)
            txt(d, (0, 1570, W, 60), scene.get('sub', ''), 'or', 32, tuple(int(c * a) for c in (160, 160, 168)), sp=0.16)
    # dip to black at the edges of every scene
    fade = min(1, t / 0.3, (dur - t) / 0.3)
    if fade < 1:
        img = Image.blend(Image.new('RGB', (W, H), (0, 0, 0)), img, max(0, fade))
    return img


def render(name, scene):
    tmp = OUT + name + '.tmp.mp4'
    n = int(scene['dur'] * FPS)
    p = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', tmp], stdin=subprocess.PIPE)
    for i in range(n):
        p.stdin.write(frame(scene, i / FPS).tobytes())
    p.stdin.close()
    if p.wait() == 0:
        os.replace(tmp, OUT + name + '.mp4')


day = dict(time='12:59', bat=75, hr=75, steps=10281)
SCENES = [
    ('s01', dict(dur=2.6, title='ON THE HUNT', sub='A NOIR WATCH FACE FOR WEAR OS')),
    ('s02', dict(dur=3.6, face=dict(day, fig='walk'), title='RAISE YOUR WRIST', sub='HE MOVES. THE DOG FOLLOWS.')),
    ('s03', dict(dur=2.6, face=dict(day, notif=True), title='NEW INTEL', sub='UNREAD NOTIFICATIONS — THE DOG PERKS UP')),
    ('s04', dict(dur=3.0, face=dict(day, time='17:42', wx='rain', bat=88, hr=92, steps=6120), glow=(30, 45, 70), title='REAL WEATHER', sub='RAIN FALLS WHEN IT RAINS ON YOU')),
    ('s05', dict(dur=2.6, face=dict(day, time='18:06', wx='storm', night=True, bat=86, hr=104, steps=6480), glow=(40, 40, 80), title='THUNDERSTORM', sub='LIGHTNING OVER THE CITY')),
    ('s06', dict(dur=2.6, face=dict(day, time='22:31', wx='snow', night=True, bat=58, hr=70, steps=11200), glow=(50, 55, 70), title='SNOW', sub='THE CITY GOES QUIET')),
    ('s07', dict(dur=2.6, face=dict(day, time='21:14', night=True, bat=61, hr=68, steps=12450), glow=(80, 10, 20), title='AFTER SUNSET', sub="GOLD TURNS RED · TONIGHT'S BOUNTY")),
    ('s08', dict(dur=2.6, face=dict(day, time='23:48', night=True, bat=46, hr=66, steps=12900, charging=True, fig='reload'), glow=(70, 55, 15), title='CHARGING', sub='HE RELOADS')),
    ('s09', dict(dur=2.6, face=dict(day, time='07:12', bat=14, hr=88, steps=13400, fig='kneel'), glow=(80, 30, 10), title='LOW BATTERY', sub='WOUNDED — BUT NOT DONE')),
    ('s10', dict(dur=3.2, face=lambda t: dict(day, time='18:58', bat=58, hr=118, steps=int(13600 + min(1, t / 2.8) * 1399), fig='walk'), title='EVERY STEP COUNTS', sub='THE BOUNTY GETS CLOSER')),
    ('s11', dict(dur=4.2, face=dict(day, time='19:05', bat=54, hr=128, steps=15120), glow=(90, 40, 10), title='CONTRACT FULFILLED', sub='GOAL REACHED · OVERTIME BEGINS')),
    ('s12', dict(dur=3.0, title='ON THE HUNT', sub='GITHUB.COM/JOHNJITTO-M/ON-THE-HUNT-WATCHFACE')),
]

if __name__ == '__main__':
    only = sys.argv[1:]
    for name, sc in SCENES:
        if not only or name in only:
            render(name, sc)
    print('scenes done')
