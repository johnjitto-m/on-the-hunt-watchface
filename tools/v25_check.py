"""Composite v2.5 states from the final build6 bitmaps (same layer order as the XML)."""
import math
from PIL import Image, ImageDraw
import preview_compositor as F
D = 'build/v25/'
S = 2
_c = {}
def A(n):
    if n not in _c:
        im = Image.open(D + n + '.png').convert('RGBA'); _c[n] = im.resize((im.width * S, im.height * S), Image.LANCZOS)
    return _c[n]
def put(im, n, x, y, alpha=1.0):
    a = A(n)
    if alpha < 1: a = a.copy(); a.putalpha(a.getchannel('A').point(lambda v: int(v * alpha)))
    im.alpha_composite(a, (int(x * S), int(y * S)))

def background(h, mins, wx=None, night=None, moonk=1):
    hh = h + mins / 60
    if night is None: night = h >= 18 or h < 6
    skyk = 'storm' if wx == 'storm' else 'night' if night else (wx if wx in ('rain', 'snow') else 'cloudy' if wx in ('cloudy', 'fog') else 'dawn' if 5 <= h < 7 else 'dusk' if 17 <= h < 19 else 'day')
    im = Image.new('RGBA', (480 * S, 480 * S), (0, 0, 0, 255))
    put(im, f'sky_{skyk}', 0, 0)
    precip = wx in ('rain', 'storm', 'snow'); dim = 90 / 255 if wx in ('cloudy', 'fog') else 1
    def bodies(part):
        if 6 <= h < 18 and not night and not precip:
            t = (hh - 6) / 12; x = 240 - 205 * math.cos(math.pi * t); y = 318 - 262 * math.sin(math.pi * t)
            low = 1 - min(1, max(0, math.sin(math.pi * t) * 2.2))
            put(im, f'sun_{part}_high', x - 100, y - 100, (1 - low) * dim); put(im, f'sun_{part}_low', x - 100, y - 100, low * dim)
        if (h >= 18 or h < 6) and not precip:
            t = ((hh + 6) % 24) / 12; x = 240 - 205 * math.cos(math.pi * t); y = 318 - 262 * math.sin(math.pi * t)
            if part == 'disc': put(im, f'moon_{moonk}', x - 40, y - 40, dim)
            else: put(im, 'moon_glow', x - 40, y - 40, dim * (1 - math.cos(moonk * 0.7854)) / 2)
    bodies('disc')
    put(im, 'towers_night' if night else 'towers_day', 0, 0)
    bodies('glow')
    put(im, 'city_night' if night else 'city_day', 0, 176)
    if wx in ('rain', 'storm'): put(im, 'wx_rain', 0, -300)
    if wx == 'snow': put(im, 'wx_snow', 0, -250)
    if wx in ('cloudy', 'fog'): put(im, 'wx_' + wx, -30, 0)
    if wx == 'storm': put(im, 'wx_storm', 0, 0)
    ImageDraw.Draw(im).rectangle([0, 380 * S, 480 * S, 480 * S], fill=(0, 0, 0, 255))
    return im

L = lambda n: Image.open(D + n + '.png').convert('RGBA')
WIDE = dict(dxb=-42, dxh=43, nodiv=True)
fxw = lambda s: 24 + 2.3 * min(100, s * 100 / 15000)

def state(h, m, steps, hero, dog, wx=None, night=None, moonk=1, extra=None, done=False, **kw):
    fx = fxw(steps); hn, hx = hero if isinstance(hero, tuple) else (hero, fx)
    dn, dx, dy = dog
    layers = [(L('pool'), (184 if done else fx - 70), 205), (L(dn), dx if dx is not None else (fx - 30 if fx >= 60 else fx + 72), dy), (L(hn), hx, 241)]
    if extra: layers += extra
    n = night if night is not None else (h >= 18 or h < 6)
    st = dict(time=f'{h:02d}:{m:02d}', bat=kw.pop('bat', 75), hr=kw.pop('hr', 72), temp=kw.pop('temp', 27), steps=steps, night=n,
              bg=background(h, m, wx, night, moonk), layers=layers, **WIDE, **kw)
    return F.face(st, 0.4, 480)

SIT, WALK = ('dog_sit_tall', None, 292), ('dog_walk_04', None, 326)
if __name__ == '__main__':
    states = {
        'sunrise': state(6, 40, 600, 'g_front', SIT),
        'morning': state(9, 10, 3400, 'g_walk_06', WALK),
        'noon': state(12, 20, 6900, 'g_front', SIT),
        'afternoon': state(15, 30, 9900, 'g_sip_14', SIT),
        'sunset': state(17, 30, 12300, 'g_walk_14', WALK),
        'night': state(20, 15, 14200, 'g_front', SIT, moonk=1),
        'fullmoon': state(23, 40, 300, 'g_front', SIT, moonk=4),
        'rain': state(10, 5, 5200, 'g_coin_18', SIT, wx='rain', temp=23),
        'pat': state(16, 5, 11000, ('g_patm_22', fxw(11000) - 30), SIT),
        'notif': state(13, 22, 9800, 'g_front', ('dog_alert_02', None, 305)),
        'lean': state(15, 10, 4200, 'g_lean', SIT, hr=64),
        'done': state(19, 5, 15120, ('g_cheer_00', 254), ('dog_happy_02', 224, 320), done=True, bat=54, hr=128),
    }
    import os; os.makedirs('build/v25', exist_ok=True)
    for k, im in states.items(): im.save(f'build/v25/{k}.png')
    states['noon'].save('build/v25/preview.png')
    names = list(states)
    c = Image.new('RGB', (480 * 4, 480 * 3), (16, 16, 20))
    for i, n in enumerate(names): c.paste(states[n], ((i % 4) * 480, (i // 4) * 480), states[n])
    c.resize((1600, 1200)).save('/tmp/v25.png')
    print('ok')
