"""Generate all v2.8 hero bitmaps (+ manifest) into watchface/src/main/res/drawable: the new rig (bending arms, real hands, crouch),
eased keyframed taps at 20 fps, and every mood redrawn with the new arms.
Usage: python3 gen28.py [--only prefix,...] [--norender]"""
import asyncio, json, math, os, random, sys
sys.path.insert(0, 'tools')
import v27 as A, retriever as RT, dog3 as D, dog2 as D2, render_v2 as R, real_guy as G, coffee_guy as C, rig28 as M
import clip28 as CL
from PIL import Image, ImageChops, ImageEnhance, ImageFilter, ImageDraw, ImageFont
import preview_compositor as F

S = 1.35
B = 'watchface/src/main/'
OUT = B + 'res/drawable/'
RAW = 'build/raw28/'
os.makedirs(OUT, exist_ok=True); os.makedirs(RAW, exist_ok=True)
R.OUT = RAW
BW, BH = round(A.VB[2] * S), round(A.VB[3] * S)
DDX = 14
K = A.K
ease, lerp = D.ease, D.lerp
FPS = 20


def rig2px(p): return (50 + (p[0] + 40) * K, (p[1] + 26.667) * K)
def px2rig(p): return ((p[0] - 50) / K - 40, p[1] / K - 26.667)
def px2box(p): return ((p[0] - A.VB[0]) * S, (p[1] - A.VB[1]) * S)


def dog_head_px(local, head_a, dx=DDX, dk=1.08):
    a = math.radians(head_a)
    lx, ly = local[0] * RT.HEAD_K, local[1] * RT.HEAD_K
    ux = 106 + lx * math.cos(a) - ly * math.sin(a)
    uy = 6 + lx * math.sin(a) + ly * math.cos(a)
    return (dx + 0.4 * dk * ux, A.GROUND + 0.4 * dk * (uy - 112))


SVGS = {}
def reg(name, body):
    SVGS[name] = body
    return name


def man(**p): return M.man(p)
def man_only(name, body): return reg(name, A.scene(body, None))
def dog_only(name, dog, dog_dx=DDX, dk=1.08): return reg(name, A.scene('', dog, dog_dx=dog_dx, dk=dk))
RIGK = 1.2

STILLS, SEQS = {}, {}

# ------------------------------------------------------------------ base pose = the first frame of every tap
BASE_M, BASE_D, _ = CL.pat(0.0)
BASE_M = dict(BASE_M, breathe=0.5)
BASE_D = dict(BASE_D, breathe=0.0, sweep=0.0)
HANG_L = dict(kind='reach', wrist=CL.HANG_L[:2], z=CL.HANG_L[2], hand='relax')
CUP = dict(kind='cup', wrist=CL.CUP_R[:2], z=CL.CUP_R[2])


def base_man(**over):
    p = dict(BASE_M); p.update(over); return M.man(p)


def sit(**over):
    d = dict(BASE_D); d.update(over); d.setdefault('head_a', -20); return RT.sit(**d)


STILLS['base'] = (reg('sc_base', A.scene(base_man(), sit(), dog_dx=DDX)), ('day', 'am', 'pm', 'night'))


# ------------------------------------------------------------------ taps (eased keyframes, 20 fps)
def tap_seq(name, fn, dur):
    n = round(dur * FPS)
    frames = []
    for i in range(n + 1):
        t = min(dur, i / FPS)
        env = min(1.0, t / 0.3, (dur - t) / 0.3)
        m, d, props = fn(t)
        m = dict(m, breathe=0.5)
        if props: m['props'] = props
        d = dict(d, breathe=0.0, sweep=d.get('sweep', 0.0) * max(0.0, env))
        frames.append(reg(f'sc_{name}_{i:03d}', A.scene(M.man(m), RT.sit(**{'head_a': -20, **d}), dog_dx=DDX)))
    return frames + ['sc_base']


SEQS['pat'] = (tap_seq('pat', CL.pat, 3.4), ('day', 'night'), FPS)
SEQS['coin'] = (tap_seq('coin', CL.coin, 2.4), ('day', 'night'), FPS)
SEQS['sip'] = (tap_seq('sip', CL.sip, 2.6), ('day', 'night'), FPS)

# ------------------------------------------------------------------ wake: walk in (side view), then turn to face you
WALK_N = 28
bm = man_only('sc_base_man', base_man())
bd = dog_only('sc_base_dog', sit())
walk_frames = [man_only(f'sc_walk_{i:02d}', G.walk(A.O, i / 12)) for i in range(12)]
man_wake = [walk_frames[i % 12] for i in range(WALK_N)] + [('blend', walk_frames[WALK_N % 12], bm, u) for u in (0.25, 0.5, 0.75)] + [bm]
trot_frames = [dog_only(f'sc_trot_{i:02d}', D.trot(i / 12), dk=RIGK) for i in range(12)]
stand = dog_only('sc_stand', D.stand_pose(head_a=-6), dk=RIGK)
dog_wake = [trot_frames[i % 12] for i in range(WALK_N)] + [stand, ('blend', stand, bd, 0.4), ('blend', stand, bd, 0.75), bd]
SEQS['wake_man'] = (man_wake, ('day', 'night'), 12)
SEQS['wake_dog'] = (dog_wake, ('day', 'night'), 12)

# ------------------------------------------------------------------ moods
STILLS['morning_man'] = (man_only('sc_morning_man', base_man(R=dict(CUP, steam=0.0), lids=0.45, smile=0.9, look=(0.0, 0.3))), ('am',))
yawn = []
for k in range(14):
    v = ease(k / 4) if k < 4 else 1.0 if k < 9 else 1 - ease((k - 8) / 5)
    yawn.append(dog_only(f'sc_yawn_{k:02d}', sit(head_a=round(-20 - 6 * v), mouth='yawn' if v > 0.35 else 'closed', eyes_closed=v > 0.5, ears=-0.4 * v)))
SEQS['yawn'] = (yawn + [bd], ('am',), 8)

STILLS['hot_man'] = (man_only('sc_hot_man', base_man(outfit='tee', shades=True, smile=0.5, R=dict(CUP, cup='iced'))), ('day', 'pm'))
SEQS['pant'] = ([dog_only(f'sc_pant_{k}', sit(head_a=-4 + b, mouth='pant', breathe=b, sweep=0.25 * math.sin(k * 1.6))) for k, b in enumerate((0, 0.8, 1.3, 0.7))], ('day', 'pm'), 6)

HANDLE = (-6.0, 128.0)
def umbrella_man(top, r, **kw):
    return base_man(L=dict(kind='reach', wrist=HANDLE, z=18, hand='fist', pole=(-0.6, 0.3, -0.6)), props_back=A.umbrella(HANDLE, top, r=r),
                    wet=True, look=(-1.3, 0.7), tilt=-5, R=dict(CUP, steam=0.0), **kw)
STILLS['rain_man'] = (man_only('sc_rain_man', umbrella_man((-44, 76), 82)), ('day', 'night'))
RAIN_DX = 12
rain_sit = dog_only('sc_rain_sit', sit(head_a=-26, ears=-0.4, extra_body=A.WET), RAIN_DX)
def spray(k):
    random.seed(k)
    return ''.join(f'<circle cx="{70 + 46 * math.cos(t) * r:.1f}" cy="{52 + 26 * math.sin(t) * r:.1f}" r="{1 + random.random():.1f}" fill="#eaf4ff" fill-opacity="{0.8 - 0.5 * r:.2f}"/>'
                   for t, r in ((random.uniform(0, 6.28), random.uniform(0.7, 1.25)) for _ in range(22)))
shake = []
for k in range(10):
    w = math.sin(k * 2.1)
    shake.append(dog_only(f'sc_shake_{k:02d}', D.pose(theta=2 * w, head_a=-6 + 14 * w, ears=-0.6 + 1.2 * abs(w), tail_a=18 * w) + spray(k), RAIN_DX, dk=RIGK))
SEQS['shake'] = (shake + [('blend', shake[-1], rain_sit, 0.33), ('blend', shake[-1], rain_sit, 0.66), rain_sit], ('day', 'night'), 12)
STILLS['rain_dog'] = (rain_sit, ('day', 'night'))
STILLS['storm'] = (reg('sc_storm', A.scene(base_man(L=dict(kind='reach', wrist=(-4.0, 128.0), z=18, hand='fist', pole=(-0.6, 0.3, -0.6)),
                                                    props_back=A.umbrella((-4.0, 128.0), (-26, 74), r=80), wet=True, look=(-1.5, 0.8), tilt=-6, R=dict(CUP, steam=0.0)),
                                           sit(head_a=6, ears=-1.0, extra_body=A.WET, sweep=-0.4), dog_dx=28)), ('day', 'night'))

POCKET_L = dict(kind='reach', wrist=(52.0, 150.0), z=10, hand='hidden')
POCKET_R = dict(kind='reach', wrist=(98.0, 150.0), z=10, hand='hidden')
STILLS['snow'] = (reg('sc_snow', A.scene(base_man(scarf=True, snow=True, L=POCKET_L, smile=0.3, R=dict(CUP, steam=1.2)),
                                         sit(head_a=-10, extra_body=A.SNOW_BACK, extra_head=A.SNOW_HEAD), dog_dx=DDX)), ('day', 'night'))
STILLS['cold'] = (reg('sc_cold', A.scene(base_man(scarf=True, L=POCKET_L, smile=0.3, R=dict(CUP, steam=1.2)), sit(head_a=-10), dog_dx=DDX)), ('day', 'night'))
STILLS['night_man'] = (man_only('sc_night_man', base_man(L=POCKET_L, R=POCKET_R, look=(0.7, -1.1), tilt=4, smile=0.35, brows=0.6)), ('night',))
SEQS['sleep'] = ([dog_only(f'sc_sleep_{k}', A.dog_sleep(b), -16) for k, b in enumerate((0, 0.7, 1.2, 0.7))], ('night',), 3)

STILLS['notif_man'] = (man_only('sc_notif_man', base_man(L=dict(kind='reach', wrist=(62.0, 98.0), z=30, hand='relax', watch=True, wbend=-20),
                                                         look=(-1.4, 1.1), tilt=-6, lids=0.15, R=dict(CUP, steam=0.4))), ('day', 'am', 'pm', 'night'))
bark = {m: dog_only(f'sc_bark_{m}', D.pose(head_a=-16, mouth=('open' if m else 'closed'), ears=1.0, tail_a=-6 + 10 * m), DDX - 6, dk=RIGK) for m in (0, 1)}
B1 = ('bubble', bark[1])
SEQS['bark'] = ([bark[0], B1, B1, bark[0], B1, B1, bark[0], bark[0]], ('day', 'night'), 6)

STILLS['low'] = (reg('sc_low', A.scene(base_man(R=dict(kind='cup', wrist=(104.0, 152.0), z=8, steam=0.0, cup_rot=8), lids=0.6, tilt=7, look=(0.0, 1.0), smile=-0.4, breathe=-0.5),
                                       A.dog_sleep(0, awake=True, head_up=0.6), dog_dx=-16)), ('day', 'night'))
STILLS['behind'] = (reg('sc_behind', A.scene(C.lean_pose(), A.dog_sleep(0, awake=True, head_up=1.0), dog_dx=-18)), ('day', 'night'))
SEQS['jog'] = ([reg(f'sc_jog_{i:02d}', A.scene(A.jog(i / 12), D.trot((i / 12 * 2) % 1, head_a=-4), dog_dx=88, dog_front=True, dk=RIGK)) for i in range(12)], ('day', 'night'), 12)


def happy(i):
    u = i / 8; hop = abs(math.sin(2 * math.pi * u))
    return D.pose(fl=(-30 * hop, 0.7 * hop), ff=(-24 * hop, 0.6 * hop), hl=(8 * hop, 0.2), hf=(4 * hop, 0.1), head_a=-18, mouth='open', ears=0.6,
                  tail_a=-20 + 24 * math.sin(4 * math.pi * u), bob=-8 * hop, theta=-10 * hop)
SEQS['cheer'] = ([reg(f'sc_cheer_{i}', A.scene(C.cheer_pose(i % 2), happy(i), dog_dx=-4, dk=RIGK)) for i in range(8)], ('day', 'night'), 8)

# ------------------------------------------------------------------ festivals
SPARK_TIP = A.SPARK_TIP
spark_w = (104.0, 92.0)
stick = (f'<path d="M{spark_w[0] - 1:.1f} {spark_w[1] + 2:.1f} L{SPARK_TIP[0]:.1f} {SPARK_TIP[1]:.1f}" stroke="#4a4a50" stroke-width="1.6"/>'
         f'<path d="M{spark_w[0] + 6:.1f} {spark_w[1] - 16:.1f} L{SPARK_TIP[0]:.1f} {SPARK_TIP[1]:.1f}" stroke="#9a9aa4" stroke-width="2.6" stroke-linecap="round"/>')
STILLS['diwali_man'] = (man_only('sc_diwali_man', base_man(R=dict(kind='reach', wrist=spark_w, z=30, hand='fist', wbend=30), props_back=stick,
                                                           smile=0.9, look=(1.0, -0.8), tilt=3)), ('night',))
MARIGOLD = ''.join(f'<circle cx="{103 + 12 * math.cos(t):.1f}" cy="{27 + 7 * math.sin(t) + 4:.1f}" r="2.3" fill="{c}"/>'
                   for t, c in ((0.3 + i * 0.42, ('#f28c18', '#ffc21a', '#e8611a')[i % 3]) for i in range(8)))
STILLS['diwali_dog'] = (dog_only('sc_diwali_dog', sit(head_a=-32, sweep=0.5, extra_body=MARIGOLD)), ('night',))
ANTLERS = ('<path d="M2 -14 Q-2 -26 -8 -30 M-3 -24 Q-8 -24 -10 -20 M-5 -28 Q-6 -34 -2 -36" stroke="#6a4020" stroke-width="2.2" fill="none" stroke-linecap="round"/>'
           '<path d="M10 -16 Q12 -28 18 -32 M13 -25 Q18 -26 20 -22 M15 -29 Q16 -35 12 -37" stroke="#6a4020" stroke-width="2.2" fill="none" stroke-linecap="round"/>'
           '<path d="M0 -14 Q6 -18 12 -16" stroke="#b3121f" stroke-width="2" fill="none"/>')
STILLS['xmas'] = (reg('sc_xmas', A.scene(base_man(hat='santa', smile=0.9), sit(sweep=0.6, extra_head=ANTLERS), dog_dx=DDX)), ('day', 'night'))
STILLS['nye'] = (reg('sc_nye', A.scene(base_man(L=POCKET_L, R=POCKET_R, look=(0.6, -1.3), tilt=3, smile=0.8, brows=0.5), sit(head_a=-40, ears=0.5, look=-1.0), dog_dx=DDX)), ('night',))


# ------------------------------------------------------------------ overlay loops (no grading)
def steam_svg(f, n=8):
    out = A.mdefs()
    for j, off in enumerate((0.0, 0.37, 0.71)):
        u = ((f / n) + off) % 1.0
        y0 = 93 - 30 * u; x0 = 85 + 3 * j - 2 + 2.5 * math.sin(u * 6 + j)
        a = 0.42 * math.sin(math.pi * u)
        out += (f'<path d="M{x0:.1f} {y0:.1f} Q{x0 - 3:.1f} {y0 - 5:.1f} {x0:.1f} {y0 - 10:.1f} Q{x0 + 3:.1f} {y0 - 15:.1f} {x0 - 0.5:.1f} {y0 - 20:.1f}" '
                f'stroke="#ffffff" stroke-opacity="{a:.2f}" stroke-width="{1.8 - 0.4 * j:.1f}" fill="none" stroke-linecap="round"/>')
    return out + '<ellipse cx="86" cy="74" rx="8" ry="11" fill="#ffffff" fill-opacity="0.06" filter="url(#puff)"/>'
SEQS['steam'] = ([man_only(f'sc_steam_{f}', steam_svg(f)) for f in range(8)], ('none',), 8)


def breath_svg(f, n=8, dog_head_a=-10):
    def puff(cx, cy, u, dx, dy, scale):
        a = 0.42 * math.sin(math.pi * u)
        return ''.join(f'<ellipse cx="{cx + dx * u * k:.1f}" cy="{cy + dy * u * k:.1f}" rx="{(2 + 4 * u) * scale * (0.7 + 0.3 * k):.1f}" ry="{(1.6 + 3 * u) * scale * (0.7 + 0.3 * k):.1f}" '
                       f'fill="#ffffff" fill-opacity="{a * (1 - 0.25 * k):.2f}" filter="url(#bpuff)"/>' for k in (0.6, 1.0))
    u1 = (f / n) % 1.0; u2 = (f / n + 0.5) % 1.0
    mx, my = rig2px((79, 44)); dx_, dy_ = dog_head_px((40, 1), dog_head_a)
    body = ('<defs><filter id="bpuff" x="-80%" y="-80%" width="260%" height="260%"><feGaussianBlur stdDeviation="1.3"/></filter></defs>'
            + (puff(mx, my, u1, 9, -4, 1.0) if u1 < 0.75 else '') + (puff(dx_ + 1, dy_, u2, 8, -3, 0.8) if u2 < 0.75 else ''))
    return reg(f'sc_breath_{f}', A.scene('', None, extra=body))
SEQS['breath'] = ([breath_svg(f) for f in range(8)], ('none',), 6)


def sparks_svg(f):
    random.seed(100 + f)
    tx, ty = SPARK_TIP
    out = A.mdefs() + (f'<circle cx="{tx}" cy="{ty}" r="16" fill="#ffd27a" fill-opacity="0.22" filter="url(#puff)"/>'
                       f'<circle cx="{tx}" cy="{ty}" r="4.2" fill="#fff6d8"/><circle cx="{tx}" cy="{ty}" r="7" fill="#ffd27a" fill-opacity="0.45"/>')
    for _ in range(26):
        t = random.uniform(0, 6.283); r0 = random.uniform(3, 6); r1 = r0 + random.uniform(6, 20)
        x0, y0 = tx + r0 * math.cos(t), ty + r0 * math.sin(t); x1, y1 = tx + r1 * math.cos(t), ty + r1 * math.sin(t)
        col = random.choice(('#fff3c0', '#ffd27a', '#ffb347', '#ffffff'))
        out += f'<path d="M{x0:.1f} {y0:.1f} L{x1:.1f} {y1:.1f}" stroke="{col}" stroke-width="{random.uniform(0.6, 1.3):.1f}" stroke-linecap="round"/>'
    return out
SEQS['sparks'] = ([man_only(f'sc_sparks_{f}', sparks_svg(f)) for f in range(8)], ('none',), 12)


# ------------------------------------------------------------------ grading + output (same as v2.7)
def grade(im, g):
    if g == 'none': return im
    a = im.getchannel('A')
    if g == 'day':
        out = F.rim(im, (215, 228, 245), 190, side=-1)
    elif g in ('am', 'pm'):
        rgb = ImageChops.multiply(im.convert('RGB'), Image.new('RGB', im.size, (255, 236, 206)))
        rgb = ImageEnhance.Brightness(rgb).enhance(1.04)
        base = rgb.convert('RGBA'); base.putalpha(a)
        out = F.rim(base, (255, 190, 110), 255, side=-1 if g == 'am' else 1)
        out = F.rim(out, (255, 214, 160), 110, side=-1 if g == 'am' else 1)
    else:
        rgb = ImageChops.multiply(im.convert('RGB'), Image.new('RGB', im.size, (196, 206, 236)))
        base = rgb.convert('RGBA'); base.putalpha(a)
        out = F.rim(base, (150, 178, 255), 200, side=-1)
        top = Image.new('RGBA', im.size, (255, 200, 130, 0))
        top.putalpha(ImageChops.subtract(a, ImageChops.offset(a, 0, 1)).point(lambda v: int(v * 0.5))); out.alpha_composite(top)
    out.putalpha(a)
    return out


def make_bubble(w=56, h=33):
    FONT = ImageFont.truetype('tools/fonts/bebas_neue.ttf', 56)
    W, H = w * 4, h * 4
    b = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(b)
    d.rounded_rectangle([6, 6, W - 6, H - 36], radius=34, fill=(250, 246, 236, 255), outline=(30, 26, 20, 255), width=7)
    d.polygon([(W - 48, H - 40), (W - 28, H - 4), (W - 86, H - 40)], fill=(250, 246, 236, 255))
    d.line([(W - 48, H - 37), (W - 28, H - 4), (W - 86, H - 37)], fill=(30, 26, 20, 255), width=7)
    tw = d.textlength('WOOF', font=FONT); d.text(((W - tw) / 2, 16), 'WOOF', font=FONT, fill=(176, 28, 40, 255))
    return b.resize((w, h), Image.LANCZOS)
BUBBLE = make_bubble()


def load(scene): return Image.open(RAW + scene + '.png').convert('RGBA').resize((BW, BH), Image.LANCZOS)


_cache = {}
def frame_img(spec, g):
    key = (spec if isinstance(spec, str) else tuple(spec), g)
    if key in _cache: return _cache[key]
    if isinstance(spec, str):
        im = grade(load(spec), g)
    elif spec[0] == 'bubble':
        im = frame_img(spec[1], g).copy()
        bx, by = px2box((9, 40)); im.alpha_composite(BUBBLE, (round(bx), round(by)))
    else:
        _, a, b, u = spec
        im = Image.blend(frame_img(a, g), frame_img(b, g), u)
    _cache[key] = im
    return im


if __name__ == '__main__':
    only = sys.argv[sys.argv.index('--only') + 1].split(',') if '--only' in sys.argv else None
    if '--norender' not in sys.argv:
        R.JOBS.clear()
        for name, body in SVGS.items():
            s, W, H = A.svg(body, S, 2)
            R.job(name, s, W * 2, H * 2)
        print('rendering', len(R.JOBS))
        asyncio.run(R.main())
    man_ = {'stills': {}, 'seqs': {}}
    for name, (scene, grades) in STILLS.items():
        if only and not any(name.startswith(o) for o in only): continue
        for g in grades:
            im = frame_img(scene, g); bb = im.getchannel('A').getbbox()
            nm = f'h_{name}_{g}'; im.crop(bb).save(OUT + nm + '.png')
            man_['stills'][nm] = [bb[0], bb[1], bb[2] - bb[0], bb[3] - bb[1]]
    for name, (frames, grades, fps) in SEQS.items():
        if only and not any(name.startswith(o) for o in only): continue
        for g in grades:
            ims = [frame_img(f, g) for f in frames]
            bb = None
            for im in ims:
                b = im.getchannel('A').getbbox()
                bb = b if bb is None else (min(bb[0], b[0]), min(bb[1], b[1]), max(bb[2], b[2]), max(bb[3], b[3]))
            names, seen = [], {}
            for f, im in zip(frames, ims):
                key = f if isinstance(f, str) else tuple(f)
                if key not in seen:
                    seen[key] = f'h_{name}_{g}_{len(seen):02d}'
                    im.crop(bb).save(OUT + seen[key] + '.png')
                names.append(seen[key])
            man_['seqs'][f'{name}_{g}'] = dict(box=[bb[0], bb[1], bb[2] - bb[0], bb[3] - bb[1]], frames=names, fps=fps)
    path = 'tools/art28.json'
    old = json.load(open(path)) if (only and os.path.exists(path)) else {'stills': {}, 'seqs': {}}
    for k in ('stills', 'seqs'): old[k].update(man_[k])
    json.dump(old, open(path, 'w'), indent=1)
    print('stills', len(old['stills']), 'seqs', len(old['seqs']), 'box', BW, BH)
