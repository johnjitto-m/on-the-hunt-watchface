"""v2.4 hero: the coffee guy (denim jacket, beanie, coffee, boots) - full sprite set, realistic style.
Standard box 100x161 (rig viewBox 240 x 386.667, translate 40 26.667, ground y=297, 0.41667 px/unit)."""
import asyncio, json, math, os, sys
sys.path.insert(0, 'tools')
import render_v2 as R, real_guy as G

OUT = 'build/v24'
os.makedirs(OUT, exist_ok=True)
R.OUT = OUT
O = dict(G.DENIM)
W, H = 100, 161
K = W / 240


def rp(p, c, deg):
    a = math.radians(deg); x, y = p[0] - c[0], p[1] - c[1]
    return (c[0] + x * math.cos(a) - y * math.sin(a), c[1] + x * math.sin(a) + y * math.cos(a))


def lerp(a, b, u): return a + (b - a) * u
def ease(u): u = max(0.0, min(1.0, u)); return u * u * (3 - 2 * u)


def hand_pos(ua, fa, lean=0, dx=0, bob=0, pt=(72.5, 172)):
    p = rp(rp(pt, G.ELB, fa), G.SHO, ua)
    p = rp(p, G.HIP, lean)
    return (p[0] + dx, p[1] + bob)


# ---------------------------------------------------------------- front view
def front(arm=0.0, tilt=0.0, look=0.0, smile=0.0):
    o = O
    d = G.defs(o).replace('</defs>',
        f'<linearGradient id="jf" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{o["jacketd"]}"/><stop offset="0.55" stop-color="{o["jacket"]}"/><stop offset="1" stop-color="{o["jacketl"]}"/></linearGradient>'
        '<linearGradient id="tee" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#bdb8ad"/><stop offset="0.6" stop-color="#ecebe6"/><stop offset="1" stop-color="#f7f6f2"/></linearGradient>'
        f'<linearGradient id="pf" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{o["denim_d"]}"/><stop offset="0.6" stop-color="{o["denim"]}"/><stop offset="1" stop-color="{o["denim_l"]}"/></linearGradient>'
        f'<linearGradient id="skf" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{o["skin_d"]}"/><stop offset="0.55" stop-color="{o["skin"]}"/><stop offset="1" stop-color="{o["skin_l"]}"/></linearGradient>'
        f'<linearGradient id="hatf" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{o["hatd"]}"/><stop offset="0.55" stop-color="{o["hat"]}"/><stop offset="1" stop-color="{o["hatl"]}"/></linearGradient>'
        '</defs>')
    RIM = G.RIM
    st = '<ellipse cx="75" cy="298" rx="30" ry="3.2" fill="#000" fill-opacity="0.45" filter="url(#soft1)"/>'
    legs = ('<path d="M53 156 L73.5 156 L72 230 L71 285 L56 285 L54.5 230 Z" fill="url(#pf)"/>'
            '<path d="M76.5 156 L97 156 L95.5 230 L94 285 L79 285 L78 230 Z" fill="url(#pf)"/>'
            '<path d="M73.5 158 L75 196 L76.5 158 Z" fill="#000" fill-opacity="0.45"/>'
            '<path d="M54 160 L55.5 284" ' + RIM + '/>'
            '<path d="M58 226 Q63 229 69 226 M81 226 Q86 229 92 226" stroke="#000" stroke-opacity="0.25" stroke-width="1.2" fill="none"/>'
            '<path d="M93 170 L92 280" stroke="#fff" stroke-opacity="0.1" stroke-width="2"/>')
    boots = ''.join(
        f'<path d="M{x0} 279 L{x0 + 17} 279 L{x0 + 18.5} 290 Q{x0 + 19} 297.5 {x0 + 13} 297.5 L{x0 + 3} 297.5 Q{x0 - 2} 297.5 {x0 - 1} 290 Z" fill="url(#bt)"/>'
        f'<path d="M{x0 - 1.4} 294 L{x0 + 19} 294 L{x0 + 18.5} 297.5 L{x0 - 1} 297.5 Z" fill="#1a120c"/>'
        f'<path d="M{x0 + 5} 282 L{x0 + 12} 282 M{x0 + 5} 285 L{x0 + 12} 285 M{x0 + 5} 288 L{x0 + 12} 288" stroke="#e2c9a0" stroke-width="0.8"/>'
        f'<path d="M{x0 + 13} 289 Q{x0 + 16} 292 {x0 + 15} 295" stroke="#fff" stroke-opacity="0.25" stroke-width="1" fill="none"/>'
        for x0 in (54, 78))
    tee = ('<path d="M61 58 Q75 66 89 58 L91 160 L59 160 Z" fill="url(#tee)"/>'
           '<path d="M64 58 Q75 64 86 58" stroke="#b8b2a6" stroke-width="1.4" fill="none"/>'
           '<path d="M66 120 Q75 124 84 120" stroke="#000" stroke-opacity="0.12" stroke-width="1.4" fill="none"/>')
    jacket = ('<path d="M44 66 Q50 58 62 57 L66 64 L65 104 L64 168 L48 168 Q45 120 44 66 Z" fill="url(#jf)"/>'
              '<path d="M106 66 Q100 58 88 57 L84 64 L85 104 L86 168 L102 168 Q105 120 106 66 Z" fill="url(#jf)"/>'
              '<path d="M47 160 L64 160 L64 168 L48 168 Z M86 160 L102.5 160 L102 168 L86 168 Z" fill="' + O['jacketd'] + '"/>'
              '<path d="M62 57 L55 60 L59 80 L66 65 Z" fill="' + O['jacketd'] + '" stroke="#d9d4c8" stroke-opacity="0.5" stroke-width="0.6"/>'
              '<path d="M88 57 L95 60 L91 80 L84 65 Z" fill="' + O['jacket'] + '" stroke="#d9d4c8" stroke-opacity="0.5" stroke-width="0.6"/>'
              '<path d="M50 84 L61 84 L61 97 L50 97 Z M89 84 L100 84 L100 97 L89 97 Z" fill="#000" fill-opacity="0.14" stroke="#c9a46a" stroke-opacity="0.75" stroke-width="0.7" stroke-dasharray="1.4 1"/>'
              '<path d="M50 84 L61 84 L60 89 L51 89 Z M89 84 L100 84 L99 89 L90 89 Z" fill="#000" fill-opacity="0.15"/>'
              '<circle cx="55.5" cy="87.5" r="0.9" fill="#d9c08a"/><circle cx="94.5" cy="87.5" r="0.9" fill="#d9c08a"/>'
              '<path d="M64.5 66 L63.5 166 M85.5 66 L86.5 166" stroke="#c9a46a" stroke-opacity="0.7" stroke-width="0.7" stroke-dasharray="1.4 1" fill="none"/>'
              '<path d="M45 70 Q44 120 48 166" ' + RIM + '/>'
              '<path d="M102 72 Q104 120 101 160" stroke="#fff" stroke-opacity="0.15" stroke-width="2" fill="none"/>')
    larm = ('<path d="M37 68 Q43 61 51 67 L51 119 L38.5 119 Q36 92 37 68 Z" fill="url(#jf)"/>'
            '<path d="M38.5 117 L51 117 L50 152 L40 152 Z" fill="url(#jf)"/>'
            '<path d="M39.5 150 L50.2 150 L50 158 L40 158 Z" fill="' + O['jacketd'] + '"/>'
            '<path d="M40 157 Q38 168 41 176 Q45 180 49 176 Q51 168 50 157 Z" fill="url(#skf)"/>'
            '<path d="M37.5 72 Q36.5 100 39 150" ' + RIM + '/>'
            '<path d="M41 104 Q45 108 50 105" stroke="#000" stroke-opacity="0.25" stroke-width="1.2" fill="none"/>')
    rarm = ('<path d="M99 68 Q107 61 113 68 L113.5 116 L101 116 Q99 92 99 68 Z" fill="url(#jf)"/>'
            '<path d="M101 108 L113.5 110 Q114 122 106 127 L93 130 L90 119 Z" fill="url(#jf)"/>'
            '<path d="M93 118 L91 130 L96 130.5 L98 118 Z" fill="' + O['jacketd'] + '"/>'
            '<path d="M111 74 Q113 96 112 114" stroke="#fff" stroke-opacity="0.18" stroke-width="2" fill="none"/>')
    cupf = ('<path d="M79 98 L94 98 L92.5 124 L80.5 124 Z" fill="url(#cp)"/>'
            '<path d="M79.6 106 L93.4 106 L92.8 115 L80.2 115 Z" fill="#8a5a33"/>'
            '<path d="M78 95 L95 95 L95 99 L78 99 Z" fill="#2c2c30"/>'
            '<path d="M91 100 L90 122" stroke="#fff" stroke-opacity="0.55" stroke-width="1"/>'
            '<path d="M84 91 Q82 86 85 82 Q88 78 86 73" stroke="#fff" stroke-opacity="0.25" stroke-width="1.2" fill="none"/>'
            '<path d="M88 108 Q96 106 97 112 Q97 120 90 121 Q86 119 88 108 Z" fill="url(#skf)"/>'
            '<path d="M86 112 Q89 111 92 112 M86 116 Q89 115 92 116" stroke="#000" stroke-opacity="0.25" stroke-width="0.8" fill="none"/>')
    neck = ('<path d="M67 42 L81 42 L81.5 60 L66.5 60 Z" fill="url(#skf)"/>'
            '<path d="M67 46 Q74 52 81 46 L81.5 52 Q74 56 67 52 Z" fill="#000" fill-opacity="0.22"/>')
    hd = ('<ellipse cx="60" cy="30" rx="2.6" ry="5" fill="url(#skf)"/><ellipse cx="88.4" cy="30" rx="2.6" ry="5" fill="url(#skf)"/>'
          '<path d="M60.5 22 Q60.5 9 74 9 Q87.5 9 87.5 22 L87.5 33 Q86.5 43.5 80 47.5 Q74 50.5 68 47.5 Q61.5 43.5 60.5 33 Z" fill="url(#skf)"/>'
          '<path d="M61 34 Q63 44 68 47.5 Q74 50.5 80 47.5 Q76 48 74 47 Q66 44 61 34 Z" fill="#000" fill-opacity="0.18"/>'
          '<path d="M63 38 Q66 47 74 48.5 Q82 47 85 38 Q83 45 74 46 Q65 45 63 38 Z" fill="#6b4a2a" fill-opacity="0.25"/>'
          '<path d="M65.5 28 Q68 26.6 70.5 28 Q68 29.4 65.5 28 Z M77.5 28 Q80 26.6 82.5 28 Q80 29.4 77.5 28 Z" fill="#1a1412"/>'
          '<circle cx="68.6" cy="27.7" r="0.45" fill="#fff" fill-opacity="0.7"/><circle cx="80.6" cy="27.7" r="0.45" fill="#fff" fill-opacity="0.7"/>'
          '<path d="M64.5 24.6 Q68 23 71.5 24.4 M76.5 24.4 Q80 23 83.5 24.6" stroke="#5a3d22" stroke-width="1.3" fill="none" stroke-linecap="round"/>'
          '<path d="M74.5 29 L75.6 36" stroke="#000" stroke-opacity="0.2" stroke-width="1.2"/>'
          '<path d="M72 37.4 Q74 38.8 76.5 37.4" stroke="#000" stroke-opacity="0.35" stroke-width="0.9" fill="none"/>'
          '<path d="M70.6 41.6 Q74 42.6 77.6 41.6" stroke="#7a4a3c" stroke-width="1.1" fill="none" stroke-linecap="round"/>'
          '<path d="M61 22 Q60.5 30 62 38" ' + RIM + '/>'
          # beanie
          '<path d="M59 24 Q58 1 74 0.5 Q90 1 89.5 24 Z" fill="url(#hatf)"/>'
          '<path d="M58.4 17.5 Q74 15 90 17.5 L90 25.5 Q74 23.5 58.4 25.5 Z" fill="url(#hatf)"/>'
          '<path d="M58.4 17.5 Q74 15 90 17.5" stroke="#000" stroke-opacity="0.3" stroke-width="1" fill="none"/>'
          + ''.join(f'<path d="M{x} 18 L{x} 25" stroke="#000" stroke-opacity="0.18" stroke-width="0.8"/>' for x in range(61, 89, 3))
          + ''.join(f'<path d="M{x} 3 Q{x + 0.3} 10 {x} 16" stroke="#000" stroke-opacity="0.14" stroke-width="0.8" fill="none"/>' for x in range(63, 87, 4))
          + '<path d="M60 26 Q60 29 61.5 31 M87.8 26 Q88 29 86.6 31" stroke="#6b4a2a" stroke-width="2" fill="none"/>'
          '<path d="M59.6 22 Q58.6 10 64 4" ' + RIM + '/>')
    eyes = ('<path d="M65.5 28 Q68 26.6 70.5 28 Q68 29.4 65.5 28 Z M77.5 28 Q80 26.6 82.5 28 Q80 29.4 77.5 28 Z" fill="#1a1412"/>'
            '<circle cx="68.6" cy="27.7" r="0.45" fill="#fff" fill-opacity="0.7"/><circle cx="80.6" cy="27.7" r="0.45" fill="#fff" fill-opacity="0.7"/>')
    if look:
        # eyelids lower a little and the eyes turn toward the dog (viewer's left, down)
        new_eyes = (f'<g transform="translate({-1.3 * look:.2f} {0.7 * look:.2f})">' + eyes + '</g>'
                    f'<path d="M65 27.2 Q68 25.4 71 27.2 L71 {26.4 + 1.2 * look:.2f} L65 {26.4 + 1.2 * look:.2f} Z M77 27.2 Q80 25.4 83 27.2 L83 {26.4 + 1.2 * look:.2f} L77 {26.4 + 1.2 * look:.2f} Z" fill="url(#skf)"/>')
        hd = hd.replace(eyes, new_eyes)
    if smile:
        hd = hd.replace('<path d="M70.6 41.6 Q74 42.6 77.6 41.6"', f'<path d="M70.4 {41.4 - 0.4 * smile:.2f} Q74 {42.8 + 1.2 * smile:.2f} 77.8 {41.4 - 0.4 * smile:.2f}"')
    larm = f'<g transform="rotate({arm:.2f} 44 66)">' + larm + '</g>'
    hd = f'<g transform="rotate({tilt:.2f} 74 50)">' + hd + '</g>'
    neckg = f'<g transform="rotate({tilt * 0.4:.2f} 74 58)">' + neck + '</g>'
    return d + st + legs + boots + tee + jacket + larm + neckg + hd + rarm + cupf


# ---------------------------------------------------------------- side poses
STEAM = ('<path d="M{x} {y} Q{x2} {y1} {x} {y2} Q{x3} {y3} {x} {y4}" stroke="#ffffff" stroke-opacity="{a}" stroke-width="1.3" fill="none"/>')


def side(**k):
    o = dict(O)
    for key in ('_arm', '_free', '_cupback', '_cuptilt', '_extra', '_under', '_ankb', '_ankf', '_shadow'):
        if key in k: o[key] = k.pop(key)
    defaults = dict(th_f=-3, sh_f=2, th_b=5, sh_b=0, ua_f=-2, fa_f=-6, ua_b=6, fa_b=-4)
    defaults.update(k)
    return G.pose(o, **defaults)


def sip_frame(i):
    # 0-2 raise, 3-12 at mouth, 13-16 lower, 17-23 at chest with steam
    if i <= 2: u = ease((i + 1) / 3)
    elif i <= 12: u = 1.0
    elif i <= 16: u = 1 - ease((i - 12) / 4)
    else: u = 0.0
    ua = lerp(-6, -58, u); fa = lerp(-92, -146, u)
    tilt = -9 * u
    cuptilt = -28 * u
    extra = ''
    if i >= 17:
        hp = hand_pos(ua, fa)
        a = 0.35 * math.sin((i - 17) / 6 * math.pi)
        extra = STEAM.format(x=hp[0] + 1, y=hp[1] - 24, x2=hp[0] - 3, y1=hp[1] - 30, y2=hp[1] - 36, x3=hp[0] + 4, y3=hp[1] - 42, y4=hp[1] - 48 - (i - 17) * 2, a=f'{a:.2f}')
    return side(_arm=(ua, fa), _cuptilt=cuptilt, tilt=tilt, _extra=extra)


COIN_N = 30


def coin_frame(i):
    # cup moves to the back hand; free hand flicks a coin
    seq_ua = {0: -4, 1: -8, 2: -10, 3: -12, 4: -16}
    ua = seq_ua.get(i, -12 if i < 23 else (-12 + (i - 22) * 6 if i < 26 else 6))
    fa = -70 if i < 24 else (-70 + (i - 23) * 25 if i < 26 else -6)
    if i == 4: fa = -84
    hp = hand_pos(ua, fa, pt=(76, 168))
    extra = ''
    h0 = hand_pos(-16, -84, pt=(76, 168)); h1 = hand_pos(-12, -70, pt=(76, 168))
    if 4 <= i <= 22:
        u = (i - 4) / 18
        cx = lerp(h0[0], h1[0], u); cy = lerp(h0[1], h1[1], u) - 112 * 4 * u * (1 - u)
    elif i < 4 or i <= 24:
        cx, cy = hp
    else:
        cx = None
    if cx is not None:
        rx = 1.4 + 6.2 * abs(math.cos(i * 1.15))
        glow = f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="13" fill="#f0c85a" fill-opacity="0.25" filter="url(#soft)"/>' if 4 <= i <= 22 else ''
        extra = (glow + f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{rx:.1f}" ry="7.4" fill="#d9b04a" stroke="#7a5a18" stroke-width="1.2"/>'
                 + (f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{rx * 0.5:.1f}" ry="3.8" fill="none" stroke="#fff1b0" stroke-width="1"/>' if rx > 3 else ''))
    tilt = 0
    if 6 <= i <= 20: tilt = -10 * math.sin((i - 6) / 14 * math.pi)
    return side(_free=True, _cupback=True, _arm=(ua, fa), ua_b=8, fa_b=-60, tilt=tilt, _extra=extra)


# pat: kneel facing right, reaching to a dog head at rig (205, 194); box 130 px (312 rig) starting at rig x=-40
PAT_TARGET = (205, 194)
PAT_N = 30
KNEEL = dict(th_f=-86, sh_f=86, th_b=31, sh_b=59, lean=28, bob=74, dx=20, _ankb=47, _ankf=34, _shadow=40)


def solve_reach(target, lean, dx, bob):
    best = None
    for ua in range(-120, 0, 2):
        for fa in range(-80, 40, 2):
            p = hand_pos(ua, fa, lean, dx, bob, pt=(72.5, 176))
            dd = math.hypot(p[0] - target[0], p[1] - target[1])
            if best is None or dd < best[0]: best = (dd, ua, fa)
    return best


def pat_frame(i, base):
    _, ua0, fa0 = base
    if i < 3:
        u = (i + 1) / 3
        k = {key: (v * u if isinstance(v, (int, float)) else v) for key, v in KNEEL.items()}
        ua, fa = lerp(-2, ua0, u), lerp(-6, fa0 - 20, u)
    elif i >= PAT_N - 3:
        u = (PAT_N - i) / 3
        k = {key: (v * u if isinstance(v, (int, float)) else v) for key, v in KNEEL.items()}
        ua, fa = lerp(-2, ua0, u), lerp(-6, fa0 - 20, u)
    else:
        k = dict(KNEEL)
        w = math.sin((i - 3) * 1.5)
        ua, fa = ua0 + 3 * w, fa0 - 4 + 6 * w
    k['_shadow'] = 30 + 10 * (k['_shadow'] - 30) / 10 if i in (0, 1, 2, PAT_N - 3, PAT_N - 2, PAT_N - 1) else 40
    extra = ''
    if 10 <= i <= 24:
        u = (i - 10) / 14
        a = 1 if u < 0.6 else max(0, 1 - (u - 0.6) / 0.4)
        hx, hy = PAT_TARGET[0] - 4, PAT_TARGET[1] - 26 - 30 * u
        extra = (f'<path transform="translate({hx:.1f} {hy:.1f}) scale(0.9)" d="M0 6 C-10 -2 -8 -10 -2 -9 C1 -8.5 0 -6 0 -5 C0 -6 -1 -8.5 2 -9 C8 -10 10 -2 0 6 Z" '
                 f'fill="#e8384f" fill-opacity="{a:.2f}"/>')
    return side(_free=True, _cupback=True, _arm=(ua, fa), ua_b=10, fa_b=-50, _extra=extra, **{kk: vv for kk, vv in k.items() if not kk.startswith('_')},
                **{kk: vv for kk, vv in k.items() if kk.startswith('_')})


def lean_pose():
    post = ('<path d="M41 -6 L47 -6 L47.8 297 L40.2 297 Z" fill="url(#lp)"/>'
            '<path d="M35 292 L53 292 L54 298 L34 298 Z" fill="#1c1d22"/>'
            '<path d="M30 -16 L58 -16 L54 -8 L34 -8 Z" fill="#26272c" stroke="#55565c" stroke-width="0.8"/>'
            '<ellipse cx="44" cy="-6" rx="7" ry="2.4" fill="#ffd88a"/>'
            '<ellipse cx="44" cy="0" rx="22" ry="12" fill="#ffd88a" fill-opacity="0.18" filter="url(#soft)"/>'
            '<path d="M46.6 0 L47.4 296" stroke="#9fb3cc" stroke-opacity="0.35" stroke-width="1"/>')
    under = ('<defs><linearGradient id="lp" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#121317"/><stop offset="0.6" stop-color="#2a2c32"/>'
             '<stop offset="1" stop-color="#3c3f46"/></linearGradient></defs>' + post)
    return side(_under=under, th_f=-16, sh_f=2, th_b=-9, sh_b=0, lean=-11, ua_b=14, fa_b=-10, dx=14, _ankf=6, _ankb=4)


def tired_pose():
    return side(_arm=(10, -14), _cuptilt=-10, th_f=-8, sh_f=14, th_b=6, sh_b=12, lean=12, tilt=20, bob=4, ua_b=8, fa_b=-4)


def cheer_pose(k=0):
    return side(_free=True, _cupback=True, _arm=(-128 - 6 * k, -52 + 4 * k), ua_b=14, fa_b=-30, th_f=-10, sh_f=8, th_b=8, sh_b=6, lean=-4, tilt=-8 - 3 * k, bob=-2 * k)


def svgbox(inner, w=W, h=H, vbx=0, vbw=240, mirror=False):
    m = f'<g transform="translate({vbw + 2 * vbx} 0) scale(-1 1)">' if mirror else '<g>'
    return (f'<svg width="{w}" height="{h}" viewBox="{vbx} 0 {vbw} 386.667" style="display:block; overflow: hidden">'
            f'{m}<g transform="translate(40 26.667)">{inner}</g></g></svg>')


if __name__ == '__main__':
    R.JOBS.clear()
    only = sys.argv[1:]
    def J(name, body, w=W, h=H, **kw):
        if only and not any(name.startswith(x) for x in only): return
        R.job(name, svgbox(body, w, h, **kw), w, h)
    J('g_front', front())
    J('big_g_front', front(), 400, 644)
    for i in range(12):
        J(f'g_walk_{i:02d}', G.walk(O, i / 12))
    for i in range(24):
        J(f'g_sip_{i:02d}', sip_frame(i))
    for i in range(COIN_N):
        J(f'g_coin_{i:02d}', coin_frame(i))
    base = solve_reach(PAT_TARGET, KNEEL['lean'], KNEEL['dx'], KNEEL['bob'])
    print('pat reach', base)
    for i in range(PAT_N):
        J(f'g_pat_{i:02d}', pat_frame(i, base), 130, H, vbx=0, vbw=312)
    J('g_lean', lean_pose())
    J('g_tired', tired_pose())
    J('g_cheer_00', cheer_pose(0)); J('g_cheer_01', cheer_pose(1))
    J('big_g_cheer', cheer_pose(1), 400, 644)
    J('big_g_lean', lean_pose(), 400, 644)
    J('big_g_tired', tired_pose(), 400, 644)
    J('big_g_pat', pat_frame(12, base), 520, 644, vbx=0, vbw=312)
    J('big_g_sip', sip_frame(8), 400, 644)
    J('big_g_coin', coin_frame(13), 400, 644)
    asyncio.run(R.main())
    print('done', len(R.JOBS))
