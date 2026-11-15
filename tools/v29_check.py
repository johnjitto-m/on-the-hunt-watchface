"""v2.9 preview: v28 states + the two lit-window towers (date / pulse) and the dot-font time, placed as in the XML."""
import json, math, os, sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont
sys.path.insert(0, 'tools')
import v28_check as C
import v25_check as V

B = 'watchface/src/main/'
GEO = json.load(open('tools/towers29.json'))
FD = B + 'res/font/'
CY, RD = (70, 235, 255), (255, 60, 90)
PI, GY0 = GEO['pitch'], GEO['gy0']
SS = 4
CTX = {}


def F(name, size): return ImageFont.truetype(FD + name + '.ttf', int(size * SS))


def ov(): return Image.new('RGBA', (480 * SS, 480 * SS), (0, 0, 0, 0))


def ctext(d, box, s, font, col):
    """WFF PartText, align CENTER, line box = 0.7*size, 7 rows from the top"""
    x, y, w = box
    adv = font.getlength(s)
    d.text(((x + w / 2) * SS - adv / 2, y * SS), s, font=font, fill=col, anchor='la')


def glowed(layer, r, k=0.75):
    g = layer.filter(ImageFilter.GaussianBlur(r * SS))
    a = g.split()[3].point(lambda v: int(min(255, v * 1.6 * k)))
    g.putalpha(a)
    out = ov(); out.alpha_composite(g); out.alpha_composite(g); out.alpha_composite(layer)
    return out


def tower_text():
    hr, (day, mon, wd), dow = CTX['hr'], CTX['date'], CTX['dow']
    t = ov(); d = ImageDraw.Draw(t)
    f, fh = F('dots', 40), F('dots_heart', 40)
    xl, xr = GEO['x0']['l'] - 4 * PI, GEO['x0']['r'] - 4 * PI
    W = 36 * PI
    ctext(d, (xl, GY0 + 1 * PI, W), f'{day} {mon}', f, CY + (255,))
    ctext(d, (xl, GY0 + 8 * PI, W), wd, f, CY + (255,))
    wr, wc0, wst = GEO['week']
    wx = GEO['x0']['l'] + (wc0 + (dow - 1) * wst) * PI; wy = GY0 + wr * PI
    for k in range(7):
        x = GEO['x0']['l'] + (wc0 + k * wst) * PI
        d.rectangle([(x + 0.5) * SS, (wy + 0.5) * SS, (x + 3.5) * SS - 1, (wy + 3.5) * SS - 1], fill=CY + (110,))
    d.rectangle([(wx + 0.5) * SS, (wy + 0.5) * SS, (wx + 3.5) * SS - 1, (wy + 3.5) * SS - 1], fill=CY + (255,))
    s = '♥' + (str(hr) if hr > 0 else '--')
    ctext(d, (xr, GY0 + 1 * PI, W), s, f, RD + (255,))
    ctext(d, (xr, GY0 + 1 * PI, W), s, fh, RD + (255,))
    st = 'RUSH' if hr >= 140 else ('ALERT' if hr >= 100 else 'CALM')
    ctext(d, (xr, GY0 + 8 * PI, W), st, f, RD + (255,))
    sh = Image.new('RGBA', t.size, (0, 0, 0, 0)); sh.putalpha(t.split()[3].point(lambda v: int(v * 0.8)))
    out = ov(); out.alpha_composite(sh.filter(ImageFilter.GaussianBlur(5 * SS))); out.alpha_composite(glowed(t, 3))
    return out


def put_towers(bg, night):
    bg.alpha_composite(tower_text().resize((960, 960), Image.LANCZOS))


_orig_bg = V.background
def background(h, mins, wx=None, night=None, moonk=1):
    im = _orig_bg(h, mins, wx, night, moonk)
    n = night if night is not None else (h >= 18 or h < 6)
    put_towers(im, n)
    return im
V.background = background


def dot_time(im, hhmm, y=73, size=90, col=(244, 244, 242), glow=True, family='dots_time'):
    f = F(family, size)
    t = ov(); ImageDraw.Draw(t).text((240 * SS - f.getlength(hhmm) / 2, y * SS), hhmm, font=f, fill=col + (255,), anchor='la')
    out = im.copy()
    if glow:
        sh = Image.new('RGBA', t.size, (0, 0, 0, 0)); sh.putalpha(t.split()[3].point(lambda v: int(v * 0.9)))
        sh = sh.transform(sh.size, Image.AFFINE, (1, 0, 0, 0, 1, -2 * SS)).filter(ImageFilter.GaussianBlur(9 * SS / 2))
        out.alpha_composite(sh.resize((480, 480), Image.LANCZOS))
        t = glowed(t, 5 / 2, 0.45)
    out.alpha_composite(t.resize((480, 480), Image.LANCZOS))
    return out


def state(h, m, steps, parts, hr=72, date=('11', 'NOV', 'WED'), dow=4, h24=True, **kw):
    CTX.update(hr=hr, date=date, dow=dow)
    im = C.state(h, m, steps, parts, hr=hr, temp=None, hide_date=True, hide_time=True, hide_hr=True, no_bounty=True, **kw)
    hh = h if h24 else (h % 12 or 12)
    return dot_time(im, f'{hh:02d}:{m:02d}')


def aod(steps=9800):
    im = Image.new('RGBA', (480, 480), (0, 0, 0, 255)); d = ImageDraw.Draw(im)
    fs = ImageFont.truetype(FD + 'oswald_medium.ttf', 18); fc = ImageFont.truetype(FD + 'oswald_medium.ttf', 22)
    def ct(y, s, f, col):
        tw = d.textlength(s, font=f); d.text((240 - tw / 2, y), s, font=f, fill=col)
    ct(94, 'WED  ·  11  NOV', fs, (140, 140, 148)); ct(238, f'{steps:,} / 15,000', fc, (138, 122, 72))
    im = dot_time(im, '12:20', y=124, size=90, col=(189, 189, 194), glow=False, family='dots')
    x, y, w, h = C.ART['stills']['aod_duo']; a = C.L('aod_duo').resize((round(w * 0.62), round(h * 0.62)), Image.LANCZOS)
    im.alpha_composite(a, (round(240 - w * 0.62 / 2 + 10), round(388 - h * 0.62)))
    ImageDraw.Draw(im).rectangle([150, 388, 330, 389], fill=(58, 58, 64))
    mk = Image.new('L', (480, 480), 0); ImageDraw.Draw(mk).ellipse([0, 0, 479, 479], fill=255)
    out = Image.new('RGBA', (480, 480), (0, 0, 0, 0)); out.paste(im, (0, 0), mk)
    return out


if __name__ == '__main__':
    S, Q, L = C.S, C.Q, C.L
    which = sys.argv[1:] or None
    st = {
        'day': lambda: state(12, 20, 6900, [S('h_base_day')]),
        'morning': lambda: state(7, 10, 900, [S('h_morning_man_am'), Q('steam_none', 3), Q('yawn_am', 7)], date=('3', 'MAR', 'TUE'), dow=3),
        'golden': lambda: state(17, 25, 11200, [S('h_base_pm')], night=False, bat=42, date=('28', 'MAY', 'THU'), dow=5),
        'rain': lambda: state(10, 5, 4200, [(L('h_refl_rain_day'), 0, 195), Q('shake_day', -1), S('h_rain_man_day')], wx='rain'),
        'storm': lambda: state(21, 15, 7400, [(L('h_refl_storm_night'), 0, 195), S('h_storm_night')], wx='storm', hr=0),
        'late': lambda: state(23, 40, 13900, [Q('sleep_night', 2), S('h_night_man_night')], moonk=3, bat=33, charging=True, hr=58, date=('20', 'SEP', 'SUN'), dow=1),
        'workout': lambda: state(18, 10, 11800, [Q('jog_day', 3)], hr=134, night=False),
        'rush': lambda: state(19, 5, 15120, [Q('cheer_night', 1)], bat=54, hr=146, fixed_gx=104),
        'notif': lambda: state(13, 22, 9800, [S('h_notif_man_day'), Q('bark_day', 1)], h24=False),
        'diwali': lambda: state(20, 30, 10200, [S('h_diwali_dog_night'), S('h_diwali_man_night'), Q('sparks_none', 2)], fest='dw', fw=True, label='HAPPY DIWALI', label_color='#ffc14d', date=('8', 'NOV', 'SUN'), dow=1),
        'snow': lambda: state(9, 30, 2600, [S('h_snow_day'), Q('breath_none', 3)], wx='snow', date=('24', 'DEC', 'THU'), dow=5),
        'behind': lambda: state(15, 10, 4200, [S('h_behind_day')], hr=64, label='BEHIND PACE · TIME TO MOVE'),
        'pat': lambda: state(16, 5, 11000, [Q('pat_day', 30)]),
        'coin': lambda: state(15, 30, 9900, [Q('coin_day', 19)]),
        'aod': lambda: aod(),
    }
    keys = [k for k in st if not which or k in which]
    out = 'build/v29/'
    os.makedirs(out, exist_ok=True)
    ims = {}
    for k in keys:
        ims[k] = st[k](); ims[k].save(out + k + '.png')
    if 'day' in ims: ims['day'].save(B + 'res/drawable/preview.png')
    n = len(keys); cols = 4 if n > 4 else n; rows = math.ceil(n / cols)
    c = Image.new('RGB', (480 * cols, 480 * rows), (16, 16, 20))
    for i, k in enumerate(keys): c.paste(ims[k], ((i % cols) * 480, (i // cols) * 480), ims[k])
    c.save('build/v29_all.png')
    print('ok', keys)
