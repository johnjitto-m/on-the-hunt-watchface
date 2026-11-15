"""Composite v2.7 states from the final watch face bitmaps (same placement as the XML)."""
import json, os, sys
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, 'tools')
import preview_compositor as F
import v25_check as V

B9 = 'watchface/src/main/'
V.D = D = B9 + 'res/drawable/'
V._c.clear()
ART = json.load(open('tools/art28.json'))
L = lambda n: Image.open(D + n + '.png').convert('RGBA')
WIDE = dict(dxb=-42, dxh=43, nodiv=True, hide_bat=True, bat_arc=True)
GY = 180
FONT = ImageFont.truetype(B9 + 'res/font/oswald_medium.ttf', 15)


def duox(steps): return 63 + 0.97 * min(100, steps * 100 / 15000)


def S(name): x, y, w, h = ART['stills'][name]; return (L(name), x, y)
def Q(seq, i):
    s = ART['seqs'][seq]; x, y, w, h = s['box']
    return (L(s['frames'][i if i >= 0 else len(s['frames']) + i]), x, y)


def state(h, m, steps, parts, wx=None, night=None, moonk=1, fest=None, comp='3:30 PM  TEAM SYNC', fw=False, extra_pre=None, fixed_gx=None, **kw):
    dx = duox(steps); gx = dx - 32 if fixed_gx is None else fixed_gx
    n = night if night is not None else (h >= 18 or h < 6)
    bg = V.background(h, m, wx, night, moonk)
    def put(im, x, y): bg.alpha_composite(im.resize((im.width * 2, im.height * 2), Image.LANCZOS), (int(x * 2), int(y * 2)))
    if fw:
        for (x, y, c, f) in ((24, 24, 'gold', 6), (300, 6, 'rose', 4), (170, 92, 'teal', 9), (370, 96, 'gold', 2)):
            put(L(f'fw_{c}_{f:02d}'), x, y)
    if fest:
        put(L(f'lights_{fest}_a'), 0, 176); put(L(f'lights_{fest}_b'), 0, 176)
    layers = []
    if fest == 'dw':
        layers += [(L('diya_1'), x, 356) for x in (44, 96, 208, 268, 330, 412)]
    layers.append((L('pool'), round(dx - 19), 205))
    for im, x, y in parts:
        layers.append((im, round(gx + x), GY + y))
    st = dict(time=f'{h:02d}:{m:02d}', bat=kw.pop('bat', 75), hr=kw.pop('hr', 72), temp=kw.pop('temp', 27), steps=steps, night=n,
              bg=bg, layers=layers, **WIDE, **kw)
    im = F.face(st, 0.4, 480)
    if comp:
        d = ImageDraw.Draw(im); tw = d.textlength(comp, font=FONT)
        d.text((240 - tw / 2 + 1, 152 + 1), comp, font=FONT, fill=(0, 0, 0, 200)); d.text((240 - tw / 2, 152), comp, font=FONT, fill=(232, 217, 168, 255))
    return im


def aod(steps=9800):
    im = Image.new('RGBA', (480, 480), (0, 0, 0, 255)); d = ImageDraw.Draw(im)
    fb = ImageFont.truetype('tools/fonts/bebas_neue.ttf', 116); fs = ImageFont.truetype(B9 + 'res/font/oswald_medium.ttf', 18)
    fc = ImageFont.truetype(B9 + 'res/font/oswald_medium.ttf', 22)
    def ctext(y, s, f, col):
        tw = d.textlength(s, font=f); d.text((240 - tw / 2, y), s, font=f, fill=col)
    ctext(94, 'WED  ·  11  NOV', fs, (140, 140, 148)); ctext(114, '12:20', fb, (201, 201, 206)); ctext(238, f'{steps:,} / 15,000', fc, (138, 122, 72))
    x, y, w, h = ART['stills']['aod_duo']; a = L('aod_duo').resize((round(w * 0.62), round(h * 0.62)), Image.LANCZOS)
    im.alpha_composite(a, (round(240 - w * 0.62 / 2 + 10), round(388 - h * 0.62)))
    d.rectangle([150, 388, 330, 389], fill=(58, 58, 64))
    m = Image.new('L', (480, 480), 0); ImageDraw.Draw(m).ellipse([0, 0, 479, 479], fill=255)
    out = Image.new('RGBA', (480, 480), (0, 0, 0, 0)); out.paste(im, (0, 0), m)
    return out


if __name__ == '__main__':
    st = {
        'morning': state(7, 10, 900, [S('h_morning_man_am'), Q('steam_none', 3), Q('yawn_am', 7)], temp=19),
        'day': state(12, 20, 6900, [S('h_base_day')]),
        'golden': state(17, 25, 11200, [S('h_base_pm')], night=False, bat=42),
        'hot': state(14, 30, 8600, [S('h_hot_man_day'), Q('pant_day', 2)], temp=34),
        'rain': state(10, 5, 4200, [(L('h_refl_rain_day'), 0, 195), Q('shake_day', -1), S('h_rain_man_day')], wx='rain', temp=22),
        'storm': state(21, 15, 7400, [(L('h_refl_storm_night'), 0, 195), S('h_storm_night')], wx='storm', temp=21),
        'snow': state(9, 30, 2600, [S('h_snow_day'), Q('breath_none', 3)], wx='snow', temp=-2),
        'late': state(23, 40, 13900, [Q('sleep_night', 2), S('h_night_man_night')], moonk=3, bat=33, charging=True),
        'notif': state(13, 22, 9800, [S('h_notif_man_day'), Q('bark_day', 1)]),
        'workout': state(18, 10, 11800, [Q('jog_day', 3)], hr=134, night=False),
        'pat': state(16, 5, 11000, [Q('pat_day', 30)]),
        'coin': state(15, 30, 9900, [Q('coin_day', 19)]),
        'behind': state(15, 10, 4200, [S('h_behind_day')], hr=64, label='BEHIND PACE · TIME TO MOVE'),
        'low': state(20, 40, 8000, [S('h_low_night')], bat=14),
        'done': state(19, 5, 15120, [Q('cheer_night', 1)], bat=54, hr=128, fixed_gx=104),
        'diwali': state(20, 30, 10200, [S('h_diwali_dog_night'), S('h_diwali_man_night'), Q('sparks_none', 2)], fest='dw', fw=True, label='HAPPY DIWALI', label_color='#ffc14d'),
        'xmas': state(11, 0, 5400, [S('h_xmas_day')], fest='xm', label='MERRY CHRISTMAS', label_color='#ff6b74'),
        'nye': state(23, 50, 12000, [S('h_nye_night')], fw=True),
    }
    st['aod'] = aod()
    out = 'build/v28/'
    os.makedirs(out, exist_ok=True)
    for k, im in st.items(): im.save(out + k + '.png')
    st['day'].save(D + 'preview.png')
    keys = list(st)
    c = Image.new('RGB', (480 * 5, 480 * 4), (16, 16, 20))
    for i, k in enumerate(keys): c.paste(st[k], ((i % 5) * 480, (i // 5) * 480), st[k])
    c.save('build/v28_all.png')
    print('ok', len(keys))
