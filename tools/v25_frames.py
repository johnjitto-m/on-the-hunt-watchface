"""v2.5 character frames: detailed coffee guy (guy2 patch) + golden dog, smoother frame counts, rim light."""
import asyncio, math, os, sys
sys.path.insert(0, 'tools'); sys.path.insert(0, 'tools')
import render_v2 as R
import guy2                      # patches real_guy in place
import real_guy as G
import coffee_guy as C
import dog2 as DG
from PIL import Image, ImageOps

OUT = 'build/v25/'
RAW = 'build/raw/'
os.makedirs(RAW, exist_ok=True)
R.OUT = RAW
J = R.job


def box(body, w=100, h=161, vbw=240):
    return C.svgbox(body, w, h, vbw=vbw)


def lerp(a, b, u): return a + (b - a) * u


def coin_frame_f(fi):
    i0 = int(math.floor(fi)); i1 = min(29, i0 + 1); u = fi - i0
    if u < 1e-6 or i0 == i1:
        return C.coin_frame(i0)
    # interpolate the arm keyframes, keep the coin path continuous
    def arm(i):
        seq = {0: -4, 1: -8, 2: -10, 3: -12, 4: -16}
        ua = seq.get(i, -12 if i < 23 else (-12 + (i - 22) * 6 if i < 26 else 6))
        fa = -70 if i < 24 else (-70 + (i - 23) * 25 if i < 26 else -6)
        if i == 4: fa = -84
        return ua, fa
    a0, a1 = arm(i0), arm(i1)
    ua, fa = lerp(a0[0], a1[0], u), lerp(a0[1], a1[1], u)
    hp = C.hand_pos(ua, fa, pt=(76, 168))
    h0 = C.hand_pos(-16, -84, pt=(76, 168)); h1 = C.hand_pos(-12, -70, pt=(76, 168))
    if 4 <= fi <= 22:
        v = (fi - 4) / 18
        cx = lerp(h0[0], h1[0], v); cy = lerp(h0[1], h1[1], v) - 112 * 4 * v * (1 - v)
    elif fi <= 24:
        cx, cy = hp
    else:
        cx = None
    extra = ''
    if cx is not None:
        rx = 1.4 + 6.2 * abs(math.cos(fi * 1.15))
        glow = f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="13" fill="#f0c85a" fill-opacity="0.25" filter="url(#soft)"/>' if 4 <= fi <= 22 else ''
        extra = (glow + f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{rx:.1f}" ry="7.4" fill="#d9b04a" stroke="#7a5a18" stroke-width="1.2"/>'
                 + (f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{rx * 0.5:.1f}" ry="3.8" fill="none" stroke="#fff1b0" stroke-width="1"/>' if rx > 3 else ''))
    tilt = -10 * math.sin((fi - 6) / 14 * math.pi) if 6 <= fi <= 20 else 0
    return C.side(_free=True, _cupback=True, _arm=(ua, fa), ua_b=8, fa_b=-60, tilt=tilt, _extra=extra)


N_WALK, N_SIP, N_COIN, N_PAT = 24, 32, 40, 44

if __name__ == '__main__':
    R.JOBS.clear()
    J('g_front', box(C.front()), 100, 161)
    for i in range(N_WALK):
        J(f'g_walk_{i:02d}', box(G.walk(C.O, i / N_WALK)), 100, 161)
    for k in range(N_SIP):
        J(f'g_sip_{k:02d}', box(C.sip_frame(k * 23 / (N_SIP - 1))), 100, 161)
    for k in range(N_COIN):
        J(f'g_coin_{k:02d}', box(coin_frame_f(k * 29 / (N_COIN - 1))), 100, 161)
    # pat: two targets (dog on the left -> mirrored set, dog on the right -> direct set)
    for name, target in (('patm_src', (171.2, 169.2)), ('pat', (233.6, 169.2))):
        C.PAT_TARGET = target
        best = None
        for dx in range(-30, 41, 2):
            b = C.solve_reach(target, C.KNEEL['lean'], dx, C.KNEEL['bob'])
            if best is None or b[0] < best[0][0] - 0.5: best = (b, dx)
        base, C.KNEEL['dx'] = best
        print(name, 'reach', base)
        for k in range(N_PAT):
            J(f'g_{name}_{k:02d}', C.svgbox(C.pat_frame(k * 29 / (N_PAT - 1), base), 130, 161, vbx=0, vbw=312), 130, 161)
    J('g_lean', box(C.lean_pose()), 100, 161)
    J('g_tired', box(C.tired_pose()), 100, 161)
    J('g_cheer_00', box(C.cheer_pose(0)), 100, 161); J('g_cheer_01', box(C.cheer_pose(1)), 100, 161)
    # golden dog
    DG.set_palette('golden')
    J('dog_sit', DG.svg(DG.sitting(), DG.SIT_W, DG.SIT_H, DG.SIT_VB), DG.SIT_W, DG.SIT_H)
    for i in range(12):
        J(f'dog_walk_{i:02d}', DG.svg(DG.standing(ph=i / 12, tail_a=5 * math.sin(i / 12 * 4 * math.pi), bob=-0.8 * abs(math.cos(i / 12 * 4 * math.pi))),
                                      DG.WALK_W, DG.WALK_H, DG.WALK_VB), DG.WALK_W, DG.WALK_H)
    for i in range(8):
        pulse = 0.5 + 0.5 * math.sin(i / 8 * 2 * math.pi)
        J(f'dog_alert_{i:02d}', DG.svg(DG.sitting(ears=1, look_up=1, tail_a=-5 * pulse) + DG.BADGE.format(r=f'{9 + 3 * pulse:.1f}'), DG.SIT_W, DG.ALERT_H, DG.ALERT_VB), DG.SIT_W, DG.ALERT_H)
    for i in range(8):
        u = i / 8; hop = abs(math.sin(math.pi * 2 * u))
        sw = ((10 * hop, 0.2 * hop), (-30 * hop, 0.6 * hop), (6 * hop, 0.1), (-24 * hop, 0.5 * hop))
        J(f'dog_happy_{i:02d}', DG.svg(DG.standing(swings=sw, tail_a=-28 + 22 * math.sin(4 * math.pi * u), bob=-7 * hop, mouth=True, ears=0.6, tilt=-6 * hop),
                                       DG.SIT_W, DG.HAPPY_H, DG.HAPPY_VB), DG.SIT_W, DG.HAPPY_H)
    asyncio.run(R.main())

    # ---- post: mirror, rim light, pad, trick frames -> OUT
    import preview_compositor as F
    def save(img, name, rim=True, strength=230):
        (F.rim(img, strength=strength) if rim else img).save(OUT + name + '.png')
    L = lambda n: Image.open(RAW + n + '.png').convert('RGBA')
    names = ['g_front', 'g_lean', 'g_tired', 'g_cheer_00', 'g_cheer_01'] + [f'g_walk_{i:02d}' for i in range(N_WALK)] \
        + [f'g_sip_{k:02d}' for k in range(N_SIP)] + [f'g_coin_{k:02d}' for k in range(N_COIN)] + [f'g_pat_{k:02d}' for k in range(N_PAT)]
    for n in names: save(L(n), n)
    for k in range(N_PAT): save(ImageOps.mirror(L(f'g_patm_src_{k:02d}')), f'g_patm_{k:02d}')
    f = Image.open(OUT + 'g_front.png')
    for name, x in (('g_front_l130', 30), ('g_front_r130', 0)):
        im = Image.new('RGBA', (130, 161), (0, 0, 0, 0)); im.alpha_composite(f, (x, 0)); im.save(OUT + name + '.png')
    for n in [f'dog_walk_{i:02d}' for i in range(12)] + [f'dog_alert_{i:02d}' for i in range(8)] + [f'dog_happy_{i:02d}' for i in range(8)]:
        save(L(n), n, strength=170)
    sit = F.rim(L('dog_sit'), strength=170)                      # 60x64, ground at 62.4
    tall = Image.new('RGBA', (60, 86), (0, 0, 0, 0)); tall.alpha_composite(sit, (0, 22)); tall.save(OUT + 'dog_sit_tall.png')
    heart = Image.open('build/art/heart_2.png').convert('RGBA')
    for fr in range(24):
        sx, sy, dy = 1.0, 1.0, 0.0
        if fr < 3: sy = 1 - 0.05 * (fr + 1)
        elif fr < 15:
            u = (fr - 3) / 12; dy = -22 * math.sin(math.pi * u); sx = math.cos(2 * math.pi * u)
        elif fr < 18: sy = 0.9 + 0.03 * (fr - 15)
        w = max(2, int(round(60 * abs(sx)))); h = int(round(64 * sy))
        d = sit.resize((w, h), Image.LANCZOS)
        if sx < 0: d = ImageOps.mirror(d)
        im = Image.new('RGBA', (60, 86), (0, 0, 0, 0))
        im.alpha_composite(d, (int((60 - w) / 2), int(86 - 1.6 - h + dy)))
        if 14 <= fr <= 23:
            u = (fr - 14) / 9
            hh = heart.copy(); hh.putalpha(hh.getchannel('A').point(lambda v: int(v * (1 - u * u))))
            im.alpha_composite(hh, (24, int(14 - 16 * u)))
        im.save(OUT + f'dog_trick_{fr:02d}.png')
    print('frames done')
