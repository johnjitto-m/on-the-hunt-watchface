"""v2.7 extras: fireworks, diyas, festival string lights, wet-ground reflections, AOD silhouette, masks."""
import json, math, os, random, shutil
from PIL import Image, ImageDraw, ImageFilter, ImageChops

B8 = os.environ.get('PREV_RES', 'build/prev_res/')   # res/ folder of the previous version, to carry assets over
B9 = 'watchface/src/main/'
OUT = B9 + 'res/drawable/'
M = json.load(open('tools/art28.json'))
BW, BH = 248, 202

# ---------------- carry over the scene assets from v2.6 (no old character sprites)
OLD_CHAR = ('duo_', 'dw_', 'mw_', 'g_', 'dog3_', 'dog_lie', 'preview', 'mask_duo')
for f in os.listdir(B8 + 'drawable'):
    if not f.startswith(OLD_CHAR):
        shutil.copy(B8 + 'drawable/' + f, OUT + f)
for d in ('font', 'values', 'xml'):
    shutil.copytree(B8 + d, B9 + 'res/' + d, dirs_exist_ok=True)
os.makedirs(B9 + 'res/raw', exist_ok=True)

# ---------------- masks for the walk-on-wake
Image.new('RGBA', (BW, BH), (0, 0, 0, 0)).save(OUT + 'mask_duo_clear.png')
Image.new('RGBA', (BW, BH), (255, 255, 255, 255)).save(OUT + 'mask_duo_solid.png')


# ---------------- fireworks (14 frames, 3 colours)
def firework(col, seed, n=14, size=120, ss=3):
    random.seed(seed)
    W = size * ss; c = W / 2
    rays = [(random.uniform(0, 6.283), random.uniform(0.75, 1.0)) for _ in range(34)]
    frames = []
    for f in range(n):
        u = (f + 1) / n
        im = Image.new('RGBA', (W, W), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        R = (0.12 + 0.88 * (1 - (1 - u) ** 2.4)) * (W * 0.44)
        fade = 1.0 if u < 0.45 else max(0.0, 1 - (u - 0.45) / 0.55)
        grav = 26 * ss * u * u
        for t, k in rays:
            x1, y1 = c + R * k * math.cos(t), c + R * k * math.sin(t) + grav
            x0, y0 = c + R * k * 0.62 * math.cos(t), c + R * k * 0.62 * math.sin(t) + grav * 0.6
            a = int(255 * fade)
            d.line([(x0, y0), (x1, y1)], fill=col + (int(a * 0.55),), width=int(1.6 * ss))
            d.ellipse([x1 - 1.8 * ss, y1 - 1.8 * ss, x1 + 1.8 * ss, y1 + 1.8 * ss], fill=(255, 250, 230, a))
            if u > 0.55 and random.random() < 0.4:
                d.ellipse([x1 - ss, y1 + 4 * ss, x1 + ss, y1 + 6 * ss], fill=col + (int(a * 0.8),))
        if u < 0.25:
            d.ellipse([c - 10 * ss, c - 10 * ss, c + 10 * ss, c + 10 * ss], fill=(255, 250, 220, int(220 * (1 - u / 0.25))))
        glow = im.filter(ImageFilter.GaussianBlur(5 * ss)); glow.alpha_composite(im)
        frames.append(glow.resize((size, size), Image.LANCZOS))
    return frames


for name, col, seed in (('gold', (255, 200, 90), 1), ('rose', (255, 90, 120), 2), ('teal', (90, 230, 210), 3)):
    for i, fr in enumerate(firework(col, seed)):
        fr.save(OUT + f'fw_{name}_{i:02d}.png')


# ---------------- diya (clay oil lamp) with a flickering flame, 3 frames
def diya(f, ss=6):
    W, H = 24 * ss, 22 * ss
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    glow = Image.new('RGBA', (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(glow)
    gd.ellipse([2 * ss, 0, 22 * ss, 18 * ss], fill=(255, 170, 60, 120))
    glow = glow.filter(ImageFilter.GaussianBlur(3 * ss))
    im.alpha_composite(glow)
    d.pieslice([2 * ss, 6 * ss, 22 * ss, 26 * ss], 0, 180, fill=(170, 74, 30, 255))          # clay bowl
    d.ellipse([2 * ss, 13 * ss, 22 * ss, 19 * ss], fill=(214, 110, 50, 255))
    d.ellipse([4 * ss, 14 * ss, 20 * ss, 17.6 * ss], fill=(90, 40, 16, 255))
    d.arc([2 * ss, 6 * ss, 22 * ss, 26 * ss], 20, 160, fill=(255, 190, 120, 200), width=ss)
    sway = (-0.8, 0.0, 0.9)[f]; tall = (1.0, 1.15, 0.92)[f]
    fx, fy = 12 * ss + sway * ss, 15 * ss
    d.polygon([(fx - 2.6 * ss, fy), (fx + sway * ss * 0.6, fy - 9 * ss * tall), (fx + 2.6 * ss, fy)], fill=(255, 150, 40, 255))
    d.ellipse([fx - 2.6 * ss, fy - 3 * ss, fx + 2.6 * ss, fy + 1.4 * ss], fill=(255, 150, 40, 255))
    d.polygon([(fx - 1.2 * ss, fy), (fx + sway * ss * 0.4, fy - 6 * ss * tall), (fx + 1.2 * ss, fy)], fill=(255, 238, 160, 255))
    return im.resize((24, 22), Image.LANCZOS)


for f in range(3):
    diya(f).save(OUT + f'diya_{f}.png')


# ---------------- festival string lights over the rooftops of the city layer (two alternating sets)
city = Image.open(B8 + 'drawable/city_day.png').getchannel('A')
tops = []
for x in range(0, 480):
    col = [city.getpixel((x, y)) for y in range(204)]
    tops.append(next((y for y, v in enumerate(col) if v > 140), 203))


def lights(colors, seed):
    random.seed(seed)
    ss = 3
    A = Image.new('RGBA', (480 * ss, 204 * ss), (0, 0, 0, 0)); Bm = A.copy()
    da, db = ImageDraw.Draw(A), ImageDraw.Draw(Bm)
    xs = list(range(4, 480, 30))
    k = 0
    for x0, x1 in zip(xs, xs[1:]):
        y0 = min(tops[x0 - 2:x0 + 3]) + 3 if x0 > 2 else tops[x0] + 3
        y1 = min(tops[x1 - 2:x1 + 3]) + 3
        if max(y0, y1) > 160 or abs(y1 - y0) > 26: continue
        sag = 7 + random.uniform(0, 5)
        pts = [(x0 + (x1 - x0) * t, y0 + (y1 - y0) * t + sag * 4 * t * (1 - t)) for t in [i / 40 for i in range(41)]]
        for d in (da, db):
            d.line([(p[0] * ss, p[1] * ss) for p in pts], fill=(40, 34, 30, 200), width=ss)
        for i in range(2, 40, 5):
            px, py = pts[i]; col = colors[k % len(colors)]; k += 1
            d = da if k % 2 else db
            d.ellipse([(px - 1.6) * ss, (py - 0.4) * ss, (px + 1.6) * ss, (py + 2.8) * ss], fill=col + (255,))
    out = []
    for im in (A, Bm):
        g = im.filter(ImageFilter.GaussianBlur(3 * ss))
        g = Image.eval(g, lambda v: v)
        g.alpha_composite(im)
        out.append(g.resize((480, 204), Image.LANCZOS))
    return out


for name, cols, seed in (('dw', [(255, 196, 70), (255, 140, 40), (255, 226, 140)], 5), ('xm', [(255, 60, 70), (80, 220, 110), (255, 230, 150), (240, 244, 255)], 6)):
    a, b = lights(cols, seed)
    a.save(OUT + f'lights_{name}_a.png'); b.save(OUT + f'lights_{name}_b.png')


# ---------------- wet-ground reflections (rain / storm), relative to the duo box
def reflection(layers, name, h=26):
    box = Image.new('RGBA', (BW, BH), (0, 0, 0, 0))
    for n in layers:
        x, y, w, hh = M['stills'][n]
        box.alpha_composite(Image.open(OUT + n + '.png').convert('RGBA'), (x, y))
    ground = round((134.75 + 10) * 1.35)
    fig = box.crop((0, 0, BW, ground)).transpose(Image.FLIP_TOP_BOTTOM)
    fig = fig.resize((BW, max(1, int(fig.height * 0.45))), Image.LANCZOS).crop((0, 0, BW, h))
    fig = fig.filter(ImageFilter.GaussianBlur(0.9))
    a = fig.getchannel('A')
    grad = Image.linear_gradient('L').resize((BW, h)).point(lambda v: int((255 - v) * 0.36))
    fig.putalpha(ImageChops.multiply(a, grad))
    # broken by ripples
    d = ImageDraw.Draw(fig)
    for yy in range(3, h, 4):
        d.line([(0, yy), (BW, yy)], fill=(0, 0, 0, 0), width=1)
    fig.save(OUT + name + '.png')


for g in ('day', 'night'):
    reflection([f'h_rain_man_{g}', f'h_rain_dog_{g}'], f'h_refl_rain_{g}')
    reflection([f'h_storm_{g}'], f'h_refl_storm_{g}')


# ---------------- always-on silhouette: dim fill + soft rim
def aod():
    x, y, w, h = M['stills']['h_base_night']
    im = Image.open(OUT + 'h_base_night.png').convert('RGBA')
    a = im.getchannel('A').point(lambda v: 255 if v > 90 else 0)
    er = a.filter(ImageFilter.MinFilter(3))
    edge = ImageChops.subtract(a, er)
    fill = Image.new('RGBA', im.size, (34, 34, 40, 0)); fill.putalpha(a.point(lambda v: int(v * 0.9)))
    rim = Image.new('RGBA', im.size, (150, 150, 162, 0)); rim.putalpha(edge)
    fill.alpha_composite(rim)
    fill.save(OUT + 'aod_duo.png')
    return [x, y, w, h]


M['stills']['aod_duo'] = aod()
json.dump(M, open('tools/art28.json', 'w'), indent=1)
print('extras ok', len(os.listdir(OUT)))
