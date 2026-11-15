"""v2.8 motion test: pat, coin flip and sip with the new rig, eased keyframes, follow-through and secondary motion."""
import asyncio, math, os, subprocess, sys
sys.path.insert(0, 'tools')
import rig28 as M, v27 as A, retriever as RT, render_v2 as R
from rig28 import Track as T
from PIL import Image, ImageDraw, ImageFont

FPS = 24
S = 1.35
OUT = 'build/clip28/'
RAW = OUT + 'raw/'
os.makedirs(RAW, exist_ok=True)
R.OUT = RAW
DDX = 14
HANG_L = (45.0, 153.0, 6.0)
CUP_R = (98.0, 118.0, 34.0)


def wrist_track(keys):
    """keys: (t, (x, y, z), ease) -> Track over tuples"""
    return T(keys)


def blink_at(t, times, dur=0.13):
    for b in times:
        if b <= t <= b + dur:
            u = (t - b) / dur
            return 1 - abs(2 * u - 1)
    return 0.0


def ears_spring(head, t, base=0.0, k=0.045):
    v = (head(t) - head(t - 3 / FPS))
    return max(-1.0, min(1.0, base + k * v * 8))


# ---------------------------------------------------------------- PAT (3.4 s)
def pat(t):
    drop = T([(0.25, 0.0), (0.9, 0.72, 'io'), (2.5, 0.72), (3.1, 0.0, 'io')])(t)
    lean = T([(0.25, 0.0), (0.9, -9.0, 'io'), (2.5, -9.0), (3.05, 1.2, 'io'), (3.3, 0.0, 'io')])(t)
    spread = 0.0
    # wrist path in world space; hand lands on the head then strokes it
    base = T([(0.0, HANG_L), (0.35, (47.0, 150.0, 10.0), 'io'), (0.65, (18.0, 140.0, 24.0), 'io'), (0.92, (-6.0, 171.0, 6.0), 'back'),
              (2.3, (-6.0, 171.0, 6.0)), (2.55, (6.0, 152.0, 16.0), 'out'), (3.0, (49.0, 156.0, 2.0), 'io'), (3.3, HANG_L, 'io')])(t)
    if 1.0 <= t <= 2.3:
        w = math.sin((t - 1.0) / 0.43 * 2 * math.pi)
        base = (base[0] + 3.2 * w, base[1] - 1.6 * abs(w), base[2])
    curl = T([(0.0, 0.38), (0.6, 0.06, 'io'), (1.0, 0.06), (2.3, 0.06), (2.6, 0.38, 'io')])(t)
    if 1.0 <= t <= 2.3:
        curl = 0.08 + 0.18 * (0.5 + 0.5 * math.sin((t - 1.0) / 0.43 * 2 * math.pi + 1.2))
    man = dict(drop=drop, lean=lean, spread=spread,
               L=dict(kind='reach', wrist=base[:2], z=base[2], hand='open', curl=curl, pole=(-0.6, -0.15, -0.55), wbend=T([(0.6, 0), (0.95, -25.0, 'io'), (2.4, -25.0), (2.7, 0.0, 'io')])(t)),
               R=dict(kind='cup', wrist=(98.0, 118.0 + 0.0), z=34.0),
               look=T([(0.0, (0.0, 0.0)), (0.25, (-1.4, 1.2), 'io'), (2.6, (-1.4, 1.2)), (3.0, (0.0, 0.0), 'io')])(t),
               tilt=T([(0.0, 0.0), (0.4, -6.0, 'io'), (2.6, -6.0), (3.1, 0.0, 'io')])(t),
               smile=T([(0.0, 0.4), (0.5, 0.9, 'io'), (2.8, 0.9), (3.3, 0.4, 'io')])(t),
               blink=blink_at(t, (1.6, 3.2)), breathe=0.5 + 0.5 * math.sin(t * 2.4))
    head = T([(0.0, -20.0), (0.85, -22.0, 'io'), (1.05, -31.0, 'back'), (2.3, -31.0), (2.55, -24.0, 'io'), (3.4, -20.0, 'io')])
    ha = head(t) + (2.4 * math.sin((t - 1.0) / 0.43 * 2 * math.pi + 0.6) if 1.0 <= t <= 2.3 else 0.0)
    eyes = 0.95 <= t <= 2.4
    wag_amp = T([(0.0, 0.2), (0.9, 0.3), (1.2, 1.0, 'io'), (2.6, 1.0), (3.4, 0.3, 'io')])(t)
    dog = dict(head_a=ha, eyes_closed=eyes, ears=ears_spring(head, t, -0.35 if eyes else 0.0), mouth='pant' if 1.3 <= t <= 2.2 else 'closed',
               sweep=wag_amp * math.sin(t * 2 * math.pi * 2.2), lean=T([(0.9, 0.0), (1.2, 3.0, 'io'), (2.3, 3.0), (2.6, 0.0, 'io')])(t),
               breathe=0.6 * math.sin(t * 3.0))
    return man, dog, ''


# ---------------------------------------------------------------- COIN (2.4 s)
def coin(t):
    T_FLICK, T_CATCH = 0.45, 1.42
    wr = T([(0.0, HANG_L), (0.32, (56.0, 101.0, 32.0), 'io'), (0.42, (56.0, 106.0, 30.0), 'io'), (0.5, (58.0, 93.0, 33.0), 'out'),
            (0.75, (58.0, 97.0, 32.0), 'io'), (1.3, (59.0, 95.0, 32.0)), (1.45, (59.0, 92.0, 33.0), 'out'), (1.56, (58.0, 100.0, 32.0), 'back'),
            (2.15, HANG_L, 'io')])(t)
    hand = 'relax' if t < 0.2 else 'pinch' if t < T_FLICK else 'flick' if t < 1.38 else 'fist' if t < 1.9 else 'relax'
    # coin flight
    props, h = '', 0.0
    hx, hy = wr[0] + 2, wr[1] - 9
    if t < T_FLICK:
        cx, cy, rx = hx, hy, 6.0
    elif t < T_CATCH:
        u = (t - T_FLICK) / (T_CATCH - T_FLICK)
        cx = 60 + 2 * u; cy = (100 - 9) - 122 * 4 * u * (1 - u); rx = 1.0 + 5.4 * abs(math.cos(t * 26))
        h = 4 * u * (1 - u)
    else:
        cx = None
    if cx is not None and t < 1.5:
        props = (f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="11" fill="#f0c85a" fill-opacity="0.22" filter="url(#soft)"/>'
                 f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{rx:.1f}" ry="6" fill="#d9b04a" stroke="#7a5a18" stroke-width="1.1"/>'
                 + (f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{rx * 0.5:.1f}" ry="3.1" fill="none" stroke="#fff1b0" stroke-width="0.9"/>' if rx > 2.6 else ''))
    hh = T([(0.0, 0.0), (T_FLICK, 0.0), (0.95, 1.0, 'out'), (T_CATCH, 0.05, 'in'), (1.6, 0.0)])
    look_up = M.spring(hh, t, 1 / FPS, 0.3, 2)
    man = dict(L=dict(kind='reach', wrist=wr[:2], z=wr[2], hand=hand, wbend=T([(0.2, 0.0), (0.4, -40.0, 'io'), (1.6, -40.0), (2.0, 0.0, 'io')])(t)),
               look=T([(0.0, (0.0, 0.0)), (0.3, (-0.4, 0.6), 'io'), (0.45, (-0.4, 0.6))])(t) if t < 0.45 else ((-0.4 * (1 - look_up), 0.6 - 2.0 * look_up) if t < 1.7 else T([(1.7, (-0.4, 0.6)), (2.3, (0.0, 0.0), 'io')])(t)), tilt=-2.0 * look_up, smile=T([(0.0, 0.4), (1.45, 0.4), (1.65, 0.9, 'io'), (2.0, 0.9), (2.4, 0.4, 'io')])(t),
               drop=0.04 * math.sin(math.pi * max(0.0, min(1.0, (t - 0.3) / 0.2))) if t < 0.5 else 0.0,
               blink=blink_at(t, (2.05,)), breathe=0.5 + 0.5 * math.sin(t * 2.4))
    head = T([(0.0, -20.0), (0.3, -24.0, 'io'), (T_FLICK, -24.0), (0.98, -50.0, 'out'), (T_CATCH, -22.0, 'in'), (1.7, -26.0, 'back'), (2.4, -20.0, 'io')])
    dhead = lambda tt: head(tt - 2 / FPS)
    dog = dict(head_a=dhead(t), ears=ears_spring(dhead, t, 0.5 if 0.2 < t < 1.6 else 0.0), look=-1.0 * h,
               sweep=(0.3 + 0.7 * (1.45 < t < 2.3)) * math.sin(t * 2 * math.pi * 2.4), mouth='pant' if 1.5 < t < 2.2 else 'closed',
               breathe=0.6 * math.sin(t * 3.0), eyes_closed=blink_at(t, (0.15,)) > 0.5)
    return man, dog, props


# ---------------------------------------------------------------- SIP (2.6 s)
def sip(t):
    wr = T([(0.0, CUP_R), (0.25, (98.0, 123.0, 32.0), 'io'), (0.55, (104.0, 94.0, 38.0), 'io'), (0.85, (88.0, 66.0, 30.0), 'out'),
            (1.45, (88.0, 64.0, 30.0)), (1.75, (102.0, 96.0, 36.0), 'io'), (2.05, CUP_R, 'back')])(t)
    rot = T([(0.0, 0.0), (0.55, -4.0), (0.85, -28.0, 'io'), (1.1, -33.0, 'io'), (1.45, -33.0), (1.75, -6.0, 'io'), (2.05, 0.0, 'io')])(t)
    steam = T([(0.0, 0.8), (0.4, 0.0, 'io'), (1.9, 0.0), (2.6, 0.8, 'io')])(t)
    man = dict(R=dict(kind='cup', wrist=wr[:2], z=wr[2], cup_rot=rot, steam=steam),
               tilt=T([(0.0, 0.0), (0.25, -1.5, 'io'), (0.85, 4.5, 'io'), (1.45, 5.0), (1.9, -1.0, 'io'), (2.3, 0.0, 'io')])(t),
               look=T([(0.0, (0.0, 0.0)), (0.25, (0.8, 0.9), 'io'), (0.6, (0.4, -0.6), 'io'), (1.6, (0.0, 0.0), 'io')])(t),
               blink=max(T([(0.0, 0.0), (0.7, 0.0), (0.85, 1.0, 'io'), (1.45, 1.0), (1.6, 0.0, 'io')])(t), blink_at(t, (2.35,))),
               smile=T([(0.0, 0.4), (1.5, 0.3), (1.8, 1.0, 'back'), (2.6, 0.4, 'io')])(t),
               breathe=0.5 + 0.5 * math.sin(t * 2.4) + T([(1.6, 0.0), (1.8, 1.0, 'io'), (2.1, 0.0, 'io')])(t))
    cup_h = (118.0 - wr[1]) / 54.0
    head = lambda tt: -20.0 - 12.0 * max(0.0, (118.0 - T([(0.0, CUP_R), (0.25, (98.0, 123.0, 32.0), 'io'), (0.55, (104.0, 94.0, 38.0), 'io'),
                                                          (0.85, (88.0, 66.0, 30.0), 'out'), (1.45, (88.0, 64.0, 30.0)), (1.75, (102.0, 96.0, 36.0), 'io'),
                                                          (2.05, CUP_R, 'back')])(tt - 3 / FPS)[1]) / 54.0)
    dog = dict(head_a=head(t), ears=ears_spring(head, t, 0.35 * min(1.0, max(0.0, cup_h))), sweep=0.35 * math.sin(t * 2 * math.pi * 1.6),
               breathe=0.6 * math.sin(t * 3.0), eyes_closed=blink_at(t, (1.9,)) > 0.5)
    return man, dog, ''


def idle(t):
    man = dict(breathe=0.5 + 0.5 * math.sin(t * 2.4), blink=blink_at(t, (0.55,)), smile=0.45)
    dog = dict(head_a=-20 + 1.2 * math.sin(t * 1.7), breathe=0.6 * math.sin(t * 3.0), sweep=0.2 * math.sin(t * 2 * math.pi * 0.9),
               eyes_closed=blink_at(t, (0.3,)) > 0.5)
    return man, dog, ''


PLAN = [('idle', idle, 1.0), ('pat', pat, 3.4), ('idle', idle, 0.6), ('coin', coin, 2.4), ('idle', idle, 0.6), ('sip', sip, 2.6), ('idle', idle, 0.8)]


def frame_svg(fn, t):
    man, dog, props = fn(t)
    man = dict(man)
    if props: man['props'] = props
    return A.scene(M.man(man), RT.sit(**{'head_a': -20, **dog}), dog_dx=DDX)


if __name__ == '__main__':
    import v27_check as VC
    names = []
    R.JOBS.clear()
    k = 0
    for name, fn, dur in PLAN:
        for i in range(round(dur * FPS)):
            t = i / FPS
            s, W, H = A.svg(frame_svg(fn, t), S, 2)
            nm = f'f{k:04d}'; R.job(nm, s, W * 2, H * 2); names.append((nm, name)); k += 1
    print('frames', k)
    asyncio.run(R.main())
    import gen27 as GN
    bg = VC.state(12, 20, 6900, [], comp=None)
    gx = VC.duox(6900) - 32
    FONT = ImageFont.truetype('watchface/src/main/res/font/oswald_medium.ttf', 30)
    BWH = (round(A.VB[2] * S), round(A.VB[3] * S))
    for nm, label in names:
        im = Image.open(RAW + nm + '.png').convert('RGBA').resize(BWH, Image.LANCZOS)
        im = GN.grade(im, 'day')
        f = bg.copy(); f.alpha_composite(im, (round(gx), 180))
        big = Image.new('RGB', (1080, 1080), (12, 12, 15))
        big.paste(f.resize((960, 960), Image.LANCZOS), (60, 30), f.resize((960, 960), Image.LANCZOS))
        d = ImageDraw.Draw(big)
        cap = {'idle': 'breathing · blinking', 'pat': 'TAP 1 · crouches and pats', 'coin': 'TAP 2 · coin flip', 'sip': 'TAP 3 · coffee sip'}[label]
        tw = d.textlength(cap, font=FONT); d.text((540 - tw / 2, 1000), cap, font=FONT, fill=(214, 195, 130))
        big.save(OUT + nm + '.png')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-framerate', str(FPS), '-i', OUT + 'f%04d.png', '-c:v', 'libx264', '-crf', '18', '-preset', 'veryfast',
                    '-pix_fmt', 'yuv420p', '-movflags', '+faststart', OUT + 'tmp.mp4'], check=True)
    os.replace(OUT + 'tmp.mp4', 'build/motion-test-v28.mp4')
    print('done')
