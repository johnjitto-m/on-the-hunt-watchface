"""Composite v2.6 states from the final build8 bitmaps (same layer order as the XML)."""
import json, os
from PIL import Image
import preview_compositor as F
import v25_check as V
V.D = D = 'watchface/src/main/res/drawable/'
V._c.clear()
LISTS = json.load(open('tools/duo_lists.json'))
L = lambda n: Image.open(D + n + '.png').convert('RGBA')
WIDE = dict(dxb=-42, dxh=43, nodiv=True)
fxw = lambda s: 24 + 2.3 * min(100, s * 100 / 15000)
duox = lambda s: max(fxw(s) - 50, 30)


def state(h, m, steps, layers_fn, wx=None, night=None, moonk=1, done=False, **kw):
    dx = duox(steps)
    layers = [(L('pool'), 184 if done else dx - 20, 205)] + layers_fn(dx)
    n = night if night is not None else (h >= 18 or h < 6)
    st = dict(time=f'{h:02d}:{m:02d}', bat=kw.pop('bat', 75), hr=kw.pop('hr', 72), temp=kw.pop('temp', 27), steps=steps, night=n,
              bg=V.background(h, m, wx, night, moonk), layers=layers, **WIDE, **kw)
    return F.face(st, 0.4, 480)


duo = lambda name: (lambda dx: [(L(name), dx, 241)])
states = {
    'sunrise': state(6, 40, 600, duo('duo_base')),
    'morning': state(9, 10, 3400, lambda dx: [(L(LISTS['dog_wake'][20]), dx, 311), (L(LISTS['man_wake'][20]), dx + 50, 241)]),
    'noon': state(12, 20, 6900, duo('duo_base')),
    'coin': state(15, 30, 9900, duo(LISTS['coin'][14])),
    'sunset': state(17, 30, 12300, duo(LISTS['nuzzle'][24])),
    'night': state(20, 15, 14200, duo('duo_base'), moonk=1),
    'pat': state(16, 5, 11000, duo(LISTS['pat'][20])),
    'rain': state(10, 5, 5200, duo(LISTS['sip'][10]), wx='rain', temp=23),
    'notif': state(13, 22, 9800, duo(LISTS['notif'][14])),
    'lean': state(15, 10, 4200, lambda dx: [(L('dog_lie_up'), dx, 241 + 85), (L('g_lean'), dx + 50, 241)], hr=64),
    'fullmoon': state(23, 40, 300, duo('duo_base'), moonk=4),
    'done': state(19, 5, 15120, lambda dx: [(L('dog3_happy_02'), 204, 311), (L('g_cheer_00'), 254, 241)], done=True, bat=54, hr=128),
}
os.makedirs('build/v26', exist_ok=True)
for k, im in states.items(): im.save(f'build/v26/{k}.png')
states['noon'].save(D + 'preview.png')
c = Image.new('RGB', (480 * 4, 480 * 3), (16, 16, 20))
for i, n in enumerate(states): c.paste(states[n], ((i % 4) * 480, (i // 4) * 480), states[n])
c.resize((1600, 1200)).save('/tmp/v26.png'); print('ok')
