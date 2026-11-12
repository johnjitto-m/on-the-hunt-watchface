"""Detailed realistic dog v2: black-and-tan short-coat mutt, red leather collar.
Side view facing right. Units: viewBox x 0..145, ground y=112. Legs are jointed tapered limbs; 4-beat walk."""
import asyncio, math, os, sys
sys.path.insert(0, 'tools')
import render_v2 as R

COAT, COATL, COATD = '#1f1e23', '#56545f', '#0e0d10'
TAN, TANL, TAND = '#9a5e33', '#c07a46', '#5e3519'
RIMC = '#b3c4da'
GROUND = 112


def rp(p, c, deg):
    a = math.radians(deg); x, y = p[0] - c[0], p[1] - c[1]
    return (c[0] + x * math.cos(a) - y * math.sin(a), c[1] + x * math.sin(a) + y * math.cos(a))


def limb(pts, widths, fill):
    """Smooth tapered limb through joint points."""
    L, Rr = [], []
    n = len(pts)
    for i, (p, w) in enumerate(zip(pts, widths)):
        if i == 0: d = (pts[1][0] - p[0], pts[1][1] - p[1])
        elif i == n - 1: d = (p[0] - pts[i - 1][0], p[1] - pts[i - 1][1])
        else: d = (pts[i + 1][0] - pts[i - 1][0], pts[i + 1][1] - pts[i - 1][1])
        ln = math.hypot(*d) or 1
        nx, ny = -d[1] / ln, d[0] / ln
        L.append((p[0] + nx * w / 2, p[1] + ny * w / 2)); Rr.append((p[0] - nx * w / 2, p[1] - ny * w / 2))
    def curve(ptsl):
        s = f'{ptsl[0][0]:.2f} {ptsl[0][1]:.2f}'
        for i in range(1, len(ptsl) - 1):
            mx, my = (ptsl[i][0] + ptsl[i + 1][0]) / 2, (ptsl[i][1] + ptsl[i + 1][1]) / 2
            s += f' Q{ptsl[i][0]:.2f} {ptsl[i][1]:.2f} {mx:.2f} {my:.2f}'
        s += f' L{ptsl[-1][0]:.2f} {ptsl[-1][1]:.2f}'
        return s
    rr = Rr[::-1]
    return f'<path d="M{curve(L)} L{curve(rr)} Z" fill="{fill}"/>'


def paw(p, ang=0, tan=True, scale=1.0):
    x, y = p
    s = scale
    body = (f'<path d="M{x - 4.2 * s:.2f} {y - 3.6 * s:.2f} Q{x - 4.6 * s:.2f} {y:.2f} {x - 3 * s:.2f} {y + 0.2:.2f} L{x + 5.5 * s:.2f} {y + 0.2:.2f} '
            f'Q{x + 7.6 * s:.2f} {y - 0.4 * s:.2f} {x + 6.4 * s:.2f} {y - 2.8 * s:.2f} Q{x + 4 * s:.2f} {y - 5 * s:.2f} {x - 1 * s:.2f} {y - 5.2 * s:.2f} Z" '
            f'fill="{"url(#gt)" if tan else "url(#gc)"}"/>'
            f'<path d="M{x + 1.8 * s:.2f} {y - 0.2:.2f} L{x + 2.2 * s:.2f} {y - 2.6 * s:.2f} M{x + 4.4 * s:.2f} {y - 0.2:.2f} L{x + 4.6 * s:.2f} {y - 2.4 * s:.2f}" stroke="#2a160a" stroke-width="0.7"/>')
    return f'<g transform="rotate({ang:.1f} {x} {y})">{body}</g>'


def make_defs():
    return ('<defs>'
        f'<linearGradient id="gc" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{COATL}"/><stop offset="0.28" stop-color="{COAT}"/><stop offset="1" stop-color="{COATD}"/></linearGradient>'
        f'<linearGradient id="gch" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{COATD}"/><stop offset="0.6" stop-color="{COAT}"/><stop offset="1" stop-color="#33313a"/></linearGradient>'
        f'<linearGradient id="gt" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{TANL}"/><stop offset="0.5" stop-color="{TAN}"/><stop offset="1" stop-color="{TAND}"/></linearGradient>'
        '<radialGradient id="gsheen" cx="0.5" cy="0.2" r="0.6"><stop offset="0" stop-color="#8a8a9a" stop-opacity="0.55"/><stop offset="1" stop-color="#8a8a9a" stop-opacity="0"/></radialGradient>'
        '<filter id="gs" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="1.4"/></filter>'
        '<filter id="gs2" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="0.6"/></filter>'
        '</defs>')


DEFS = make_defs()
PATCHES = False
PALETTES = {
    'black': dict(COAT='#1f1e23', COATL='#56545f', COATD='#0e0d10', TAN='#9a5e33', TANL='#c07a46', TAND='#5e3519', RIMC='#b3c4da'),
    'white': dict(COAT='#e4e0d8', COATL='#ffffff', COATD='#9f9a90', TAN='#d9cbb6', TANL='#efe4d2', TAND='#b3a38a', RIMC='#ffffff'),
    'patched': dict(COAT='#e4e0d8', COATL='#ffffff', COATD='#9f9a90', TAN='#d9cbb6', TANL='#efe4d2', TAND='#b3a38a', RIMC='#ffffff'),
    'golden': dict(COAT='#c58a48', COATL='#efc27e', COATD='#7e5226', TAN='#ecd3a8', TANL='#f8e8c8', TAND='#c4a272', RIMC='#ffe6b8'),
}


def set_palette(name):
    global DEFS, PATCHES, RIM
    g = globals()
    for k, v in PALETTES[name].items(): g[k] = v
    PATCHES = name == 'patched'
    RIM = f'stroke="{g["RIMC"]}" stroke-opacity="0.55" stroke-width="1.4" fill="none" stroke-linecap="round"'
    global SH
    SH = f'stroke="#000" stroke-opacity="{0.35 if name == "black" else 0.13}" fill="none" stroke-linecap="round"'
    DEFS = make_defs()
RIM = f'stroke="{RIMC}" stroke-opacity="0.55" stroke-width="1.4" fill="none" stroke-linecap="round"'
SH = 'stroke="#000" stroke-opacity="0.35" fill="none" stroke-linecap="round"'


# ---------------- leg kinematics
def front_leg(sw, flex, shoulder=(99, 58)):
    """sw: swing angle (deg, + = forward), flex: 0..1 carpus flex during swing."""
    s = shoulder
    elbow = rp((s[0] - 3, s[1] + 19), s, -sw)
    carpus = rp((elbow[0] + 1.5, elbow[1] + 25), elbow, -sw * 0.2 + flex * 40)
    pawp = rp((carpus[0] + 2, carpus[1] + 9.5), carpus, -sw * 0.2 + flex * 95)
    return [s, elbow, carpus, pawp]


def hind_leg(sw, flex, hip=(44, 54)):
    h = hip
    stifle = rp((h[0] + 9, h[1] + 25), h, -sw)
    hock = rp((stifle[0] - 15, stifle[1] + 17), stifle, -sw * 0.3 - flex * 30)
    pawp = rp((hock[0] + 3, hock[1] + 17), hock, -sw * 0.3 + flex * 60)
    return [h, stifle, hock, pawp]


def draw_front(pts, back=False, cap=True):
    s, e, c, p = pts
    g = ((f'<ellipse cx="{s[0]:.1f}" cy="{s[1] + 1:.1f}" rx="9.5" ry="10" fill="url(#gc)"/>' if cap else '') + limb([s, e], [17 if cap else 9, 10], 'url(#gc)')
         + limb([e, c, (c[0] + (p[0] - c[0]) * 0.6, c[1] + (p[1] - c[1]) * 0.6)], [10, 6.2, 5.6], 'url(#gc)')
         + limb([(e[0] + (c[0] - e[0]) * 0.55, e[1] + (c[1] - e[1]) * 0.55), c, p], [6.6, 6, 5.6], 'url(#gt)')
         + paw(p, 0)
         + f'<path d="M{s[0] - 6:.1f} {s[1] + 2:.1f} Q{e[0] - 6:.1f} {e[1] - 4:.1f} {e[0] - 4:.1f} {e[1] + 4:.1f}" {RIM}/>')
    return f'<g style="filter: brightness(0.55)" transform="translate(-6 0)">{g}</g>' if back else g


def draw_hind(pts, back=False):
    h, st, hk, p = pts
    thigh = (f'<path d="M{h[0] - 13:.1f} {h[1] - 4:.1f} Q{h[0] - 2:.1f} {h[1] - 13:.1f} {h[0] + 11:.1f} {h[1] - 5:.1f} '
             f'Q{h[0] + 16:.1f} {h[1] + 8:.1f} {st[0] + 6:.1f} {st[1] + 1:.1f} L{st[0] - 6:.1f} {st[1] + 4:.1f} '
             f'Q{h[0] - 18:.1f} {h[1] + 12:.1f} {h[0] - 13:.1f} {h[1] - 4:.1f} Z" fill="url(#gc)"/>')
    g = (thigh
         + limb([st, hk, (hk[0] + (p[0] - hk[0]) * 0.5, hk[1] + (p[1] - hk[1]) * 0.5)], [11, 6.4, 5.6], 'url(#gc)')
         + limb([(st[0] + (hk[0] - st[0]) * 0.6, st[1] + (hk[1] - st[1]) * 0.6), hk, p], [5, 6, 5.4], 'url(#gt)')
         + paw(p, 0)
         + f'<path d="M{h[0] - 15:.1f} {h[1] - 6:.1f} Q{h[0] - 17:.1f} {h[1] + 12:.1f} {st[0] - 6:.1f} {st[1] + 2:.1f}" {RIM}/>'
         + f'<path d="M{h[0] + 4:.1f} {h[1] + 2:.1f} Q{h[0] + 6:.1f} {h[1] + 14:.1f} {st[0] + 1:.1f} {st[1] - 2:.1f}" {SH} stroke-width="1.3"/>')
    return f'<g style="filter: brightness(0.55)" transform="translate(-6 0)">{g}</g>' if back else g


def torso():
    return ('<path d="M33 47 Q33 38 46 37 Q66 37.5 86 36 Q97 34.5 104 41 Q112 49 112.5 60 Q112 71 104 76.5 Q97 79 90 77 '
            'Q80 73.5 70 71.5 Q60 70.5 54 67 Q45 66.5 38 62 Q32 56 33 47 Z" fill="url(#gc)"/>'
            '<ellipse cx="74" cy="44" rx="34" ry="8" fill="url(#gsheen)"/>'
            '<path d="M104 62 Q110 66 110.5 68 Q106 77 97 77.5 L95 70 Q99 64 104 62 Z" fill="url(#gt)" fill-opacity="0.45"/>'   # tan chest
            '<path d="M36 41 Q48 36.5 86 35.5 Q98 34.5 104 40" ' + RIM + '/>'
            '<path d="M88 44 Q93 53 91 64 M80 56 Q84 62 83 70 M72 58 Q75 64 74 70" ' + SH + ' stroke-width="1.1"/>'          # shoulder blade + ribs
            '<path d="M58 66 Q66 63.5 76 66" ' + SH + ' stroke-width="1.3"/>'
            + ('<path d="M50 39 Q57 34.6 67 36.2 Q77 35 80.6 40.6 Q79 48.4 70.4 51.2 Q63.6 53.6 57 50.4 Q50.4 46.8 50 39 Z" fill="#b8763c" fill-opacity="0.9" filter="url(#gs2)"/>'
               '<path d="M54 39 Q66 36 77 38.5" stroke="#e8b680" stroke-opacity="0.6" stroke-width="1" fill="none"/>' if PATCHES else ''))


def head(open_mouth=False, ears=0.0, tilt=0.0):
    h = ('<path d="M100 44 Q97 30 103 20 Q107 14 114 11 L121 22 Q117 34 111 46 Z" fill="url(#gc)"/>'                  # neck
         '<path d="M101 36 Q99 28 104 21" ' + RIM + '/>'
         '<path d="M106 14 Q108 3 119 1.6 Q128 1.4 131.5 8 Q133 11 133.5 12.5 L140.5 16.6 Q144 19.4 142.4 23.2 Q140.5 25.6 136 26 '
         'L130 27.6 Q123.5 30 117.5 27.6 Q109.5 24 106 14 Z" fill="url(#gc)"/>'
         '<path d="M127 14.5 L140.5 16.8 Q144 19.6 142.4 23.2 Q140.5 25.6 136 26 L130 27.6 Q124 29.2 120 26.8 Q125 22 127 14.5 Z" fill="url(#gt)"/>'
         '<ellipse cx="121" cy="21.5" rx="4" ry="3" fill="url(#gt)" opacity="0.9"/>'                                     # cheek
         '<ellipse cx="124.6" cy="7.6" rx="2.4" ry="1.3" fill="url(#gt)"/>'                                               # brow dot
         '<path d="M121.6 11.6 Q124.4 9.9 127 11.9 Q124.3 13.5 121.6 11.6 Z" fill="#0b0706"/>'
         '<path d="M121.4 11.4 Q124.4 9.4 127.3 11.6" stroke="#000" stroke-width="0.7" fill="none"/>'
         '<circle cx="125.3" cy="11.2" r="0.55" fill="#fff" fill-opacity="0.85"/>'
         '<path d="M138.4 14.6 Q143.4 15.2 143.4 18.6 Q142 20.2 138.6 19.6 Q137 17.2 138.4 14.6 Z" fill="#0a0a0b"/>'       # nose
         '<path d="M141 15.6 Q142.4 16 142.6 17.2" stroke="#fff" stroke-opacity="0.45" stroke-width="0.6" fill="none"/>'
         '<circle cx="139.6" cy="18" r="0.5" fill="#000"/>'
         '<path d="M131 18.5 l0.3 0 M133 19.5 l0.3 0 M131.5 21 l0.3 0 M134 21.6 l0.3 0" stroke="#2a160a" stroke-width="0.8" stroke-linecap="round"/>'
         '<path d="M107 6 Q114 -0.5 125 0.6" ' + RIM + '/>'
         '<path d="M118 16 Q119.5 20.5 118 25" ' + SH + ' stroke-width="1"/>')
    if open_mouth:
        h += ('<path d="M141.6 23.6 Q134 29.6 125.5 26.6 L127.6 25 Z" fill="#2a0c0b"/>'
              '<path d="M132.5 27.2 Q135 33.2 131 33.8 Q128.4 32.4 129.6 27.4 Z" fill="#d8606a"/>'
              '<path d="M131 28 L131.2 32" stroke="#b04450" stroke-width="0.6"/>')
    else:
        h += '<path d="M141.8 23.4 Q135 26 128 25.4" stroke="#140c09" stroke-width="0.9" fill="none"/>'
    ear = ('<path d="M110.5 7.5 Q107.5 -5 112.5 -11 Q119.5 -7.5 121 2.5 Q120 5 116 6 Z" fill="url(#gch)"/>'
           '<path d="M112.6 3.5 Q111 -4 113.5 -7.4 Q117.6 -3.8 117.6 2.4 Z" fill="#c98a7a" fill-opacity="0.5"/>'
           '<path d="M110.6 6 Q108 -4 112.5 -10.6" ' + RIM + '/>')
    if PATCHES:
        h = h.replace('<path d="M121.6 11.6', '<ellipse cx="121.5" cy="10.5" rx="6.5" ry="5.2" fill="#b8763c" fill-opacity="0.92"/><path d="M121.6 11.6', 1)
        ear = ear.replace('fill="url(#gch)"', 'fill="#a8662e"', 1)
    h += f'<g transform="rotate({-14 * ears:.1f} 115 5)">{ear}</g>'
    return f'<g transform="rotate({tilt:.1f} 104 40)">{h}</g>'


def collar():
    return ('<path d="M103.6 27 Q110 35.5 120.6 31.6" stroke="#8e0d20" stroke-width="4" fill="none" stroke-linecap="round"/>'
            '<path d="M104 26 Q110 33.8 120 30.4" stroke="#ff6a7c" stroke-opacity="0.45" stroke-width="0.9" fill="none"/>'
            '<path d="M104.4 28.6 Q110.4 36.6 120.6 33" stroke="#4a0610" stroke-width="0.7" fill="none"/>'
            '<circle cx="111.6" cy="35.8" r="1.9" fill="#d9b25a"/><circle cx="111.2" cy="35.3" r="0.6" fill="#fff4c8"/>')


def tail(a):
    return (f'<g transform="rotate({a:.1f} 34 45)">'
            '<path d="M35.5 43 Q26 39.5 19.5 30 Q15 22.5 12.5 18 Q11.6 16.3 13.2 16.4 Q18 21.5 22 27.6 Q28 35.5 37 39.6 Z" fill="url(#gc)"/>'
            '<path d="M33 41 Q24 36.4 16.6 22.6" stroke="' + RIMC + '" stroke-opacity="0.4" stroke-width="1" fill="none"/>'
            '</g>')


def shadow(cx=72, rx=42):
    return f'<ellipse cx="{cx}" cy="{GROUND + 0.8}" rx="{rx}" ry="2.8" fill="#000" fill-opacity="0.55" filter="url(#gs)"/>'


def standing(ph=None, swings=None, tail_a=0, bob=0.0, mouth=False, ears=0.0, tilt=0.0):
    """ph: walk phase 0..1 (4-beat), or swings dict for a fixed pose."""
    if swings is None:
        def leg(off):
            u = (ph + off) % 1.0
            if u < 0.62:                      # stance: sweep back
                k = u / 0.62; return 18 - 36 * k, 0.0
            k = (u - 0.62) / 0.38              # swing: lift and bring forward
            return -18 + 36 * (0.5 - 0.5 * math.cos(math.pi * k)), math.sin(math.pi * k)
        lh, lf, rh, rf = leg(0), leg(0.25), leg(0.5), leg(0.75)
    else:
        lh, lf, rh, rf = swings
    near_f, near_h, far_f, far_h = front_leg(*lf), hind_leg(*lh), front_leg(*rf), hind_leg(*rh)
    body = torso() + collar() + head(mouth, ears, tilt)
    return (DEFS + shadow() + f'<g transform="translate(0 {bob:.2f})">' + tail(tail_a) + draw_hind(far_h, True) + draw_front(far_f, True)
            + body + draw_hind(near_h) + draw_front(near_f) + '</g>')


def sitting(tail_a=0, ears=0.0, look_up=0.0, mouth=False):
    sit_torso = ('<path d="M44 110 Q30 106 30 92 Q31 74 46 58 Q62 42 78 30 Q84 22 88 17 Q94 14 99 19 Q104 28 106 40 '
                 'Q108 54 104 68 Q100 80 92 92 Q82 106 64 110 Z" fill="url(#gc)"/>'
                 '<path d="M100 54 Q106 60 104 70 Q99 82 92 87 L89 77 Q95 66 100 54 Z" fill="url(#gt)" fill-opacity="0.85"/>'
                 '<path d="M32 90 Q34 72 48 58 Q62 44 77 32" ' + RIM + '/>'
                 '<path d="M90 36 Q96 48 94 62" ' + SH + ' stroke-width="1.1"/>'
                 '<path d="M66 64 Q72 76 70 88" ' + SH + ' stroke-width="1"/>')
    haunch = ('<path d="M30 98 Q28 76 48 70 Q66 68 70 88 Q72 104 62 110.5 L36 111 Q28 107 30 98 Z" fill="url(#gc)"/>'
              '<path d="M31 98 Q30 80 46 72" ' + RIM + '/>'
              '<path d="M52 80 Q60 90 58 104" ' + SH + ' stroke-width="1.4"/>'
              + limb([(58, 104), (70, 108.5), (78, 109.5)], [7, 6, 5.6], 'url(#gt)') + paw((79, 111.5), 0))
    fl = front_leg(0, 0, shoulder=(95, 62))
    fl = [fl[0], (96, 80), (97, 101), (99, 111)]
    near_front = draw_front(fl, cap=False)
    far_front = draw_front([(p[0] - 1, p[1]) for p in fl], True, cap=False)
    # head group sits on the neck top; reuse the standing head translated up/back
    hd = f'<g transform="translate(-14 -26)">' + collar() + head(mouth, ears, -8 * look_up) + '</g>'
    tl = (f'<g transform="rotate({tail_a:.1f} 34 108)">'
          '<path d="M38 108 Q22 111.5 8 106.5 Q6 104 8.6 103.6 Q22 107.6 38 104 Z" fill="url(#gc)"/></g>')
    return DEFS + shadow(62, 34) + tl + far_front + sit_torso + hd + haunch + near_front


def svg(inner, w, h, vb):
    return f'<svg width="{w}" height="{h}" viewBox="{vb}" style="display:block;overflow:hidden">{R.fix(inner)}</svg>'


WALK_VB, WALK_W, WALK_H = '0 -12 150 127', 60, 51          # ground at (112+12)*0.4 = 49.6
SIT_VB, SIT_W, SIT_H = '0 -44 150 159', 60, 64             # ground at (112+44)*0.4 = 62.4
ALERT_VB, ALERT_H = '0 -66 150 181', 72                    # ground at 71.2
HAPPY_VB, HAPPY_H = '0 -28 150 143', 57                    # ground at 56
BADGE = ('<circle cx="112" cy="-40" r="7.5" fill="#ffb347"/><circle cx="112" cy="-40" r="{r}" fill="#ffb347" fill-opacity="0.3"/>'
         '<rect x="110.8" y="-44.8" width="2.4" height="6" rx="1" fill="#2a1a08"/><circle cx="112" cy="-36" r="1.3" fill="#2a1a08"/>')

if __name__ == '__main__':
    OUT = sys.argv[1] if len(sys.argv) > 1 else 'build/frames'
    R.OUT = OUT
    R.JOBS.clear()
    big = '--big' in sys.argv
    R.job('d2_sit', svg(sitting(), SIT_W, SIT_H, SIT_VB), SIT_W, SIT_H)
    for i in range(12):
        R.job(f'd2_walk_{i:02d}', svg(standing(ph=i / 12, tail_a=5 * math.sin(i / 12 * 4 * math.pi), bob=-0.8 * abs(math.cos(i / 12 * 4 * math.pi))), WALK_W, WALK_H, WALK_VB), WALK_W, WALK_H)
    for i, a in enumerate([0, -12, 5, -9]):
        R.job(f'd2_wag_{i:02d}', svg(sitting(tail_a=a, mouth=True), SIT_W, SIT_H, SIT_VB), SIT_W, SIT_H)
    for i in range(8):
        pulse = 0.5 + 0.5 * math.sin(i / 8 * 2 * math.pi)
        R.job(f'd2_alert_{i:02d}', svg(sitting(ears=1, look_up=1, tail_a=-5 * pulse) + BADGE.format(r=f'{9 + 3 * pulse:.1f}'), SIT_W, ALERT_H, ALERT_VB), SIT_W, ALERT_H)
    for i in range(8):
        u = i / 8; hop = abs(math.sin(math.pi * 2 * u))
        sw = ((10 * hop, 0.2 * hop), (-30 * hop, 0.6 * hop), (6 * hop, 0.1), (-24 * hop, 0.5 * hop))
        R.job(f'd2_happy_{i:02d}', svg(standing(swings=sw, tail_a=-28 + 22 * math.sin(4 * math.pi * u), bob=-7 * hop, mouth=True, ears=0.6, tilt=-6 * hop),
                                        SIT_W, HAPPY_H, HAPPY_VB), SIT_W, HAPPY_H)
    if big:
        R.job('big_d2_sit', svg(sitting(), 300, 318, SIT_VB), 300, 318)
        R.job('big_d2_walk', svg(standing(ph=0.1), 300, 254, WALK_VB), 300, 254)
        R.job('big_d2_walk2', svg(standing(ph=0.6), 300, 254, WALK_VB), 300, 254)
    asyncio.run(R.main())
    print('dog2 ok')


# ---------------- extra life: gallop, lying + chewing a bone
def gallop(ph):
    th = 2 * math.pi * ph
    cf, ch = math.cos(th), math.cos(th + math.pi)
    lf = (34 * cf, max(0, -math.sin(th)) * 0.9)
    rf = (34 * math.cos(th - 0.5), max(0, -math.sin(th - 0.5)) * 0.9)
    lh = (34 * ch, max(0, math.sin(th)) * 0.8)
    rh = (34 * math.cos(th + math.pi - 0.5), max(0, math.sin(th - 0.5)) * 0.8)
    return standing(swings=(lh, lf, rh, rf), tail_a=-18 + 6 * math.sin(th), bob=-4.5 * abs(math.sin(th)), ears=-0.9, tilt=4 * math.sin(th))


BONE = ('<g transform="translate(132 106)">'
        '<ellipse cx="0" cy="5.6" rx="11" ry="1.6" fill="#000" fill-opacity="0.35"/>'
        '<rect x="-8" y="-1.6" width="16" height="4" rx="2" fill="#efe6d2"/>'
        '<circle cx="-8.4" cy="-1.4" r="2.4" fill="#efe6d2"/><circle cx="-8.4" cy="2.4" r="2.4" fill="#efe6d2"/>'
        '<circle cx="8.4" cy="-1.4" r="2.4" fill="#efe6d2"/><circle cx="8.4" cy="2.4" r="2.4" fill="#efe6d2"/>'
        '<path d="M-7 -1 L7 -1" stroke="#fff" stroke-opacity="0.7" stroke-width="0.8"/>'
        '<path d="M-6 2.4 L6 2.4" stroke="#b8a888" stroke-width="0.8"/></g>')


def lying(chew=0.0, tail_a=0.0, mouth=False, bone=True, head_up=0.0):
    DY = 34
    hind = ('<path d="M26 104 Q22 86 40 80 Q56 78 60 92 Q62 106 52 111.5 L30 111.6 Q24 109 26 104 Z" fill="url(#gc)"/>'
            '<path d="M27 103 Q25 88 38 82" ' + RIM + '/>'
            + limb([(50, 106), (64, 109.4), (74, 110.2)], [7, 6, 5.6], 'url(#gt)') + paw((76, 111.6), 0))
    front = (limb([(94, 104), (110, 108.6), (122, 110)], [10, 6.4, 5.8], 'url(#gc)')
             + limb([(104, 107), (116, 109.6), (124, 110.4)], [6, 5.8, 5.6], 'url(#gt)') + paw((126, 111.6), 0))
    far_front = f'<g style="filter: brightness(0.6)" transform="translate(-6 0)">{front}</g>'
    body = f'<g transform="translate(0 {DY})">' + torso() + '</g>'
    hd = f'<g transform="translate(-8 {DY + 8}) rotate({48 + 5 * chew:.1f} 104 40)">' + collar() + head(mouth, 0.2, 0) + '</g>'
    tl = f'<g transform="translate(0 {DY})">' + tail(-50 + tail_a) + '</g>'
    if head_up:
        hd = f'<g transform="translate({-8 + 8 * head_up:.1f} {DY + 8 - 6 * head_up:.1f}) rotate({48 - 40 * head_up + 5 * chew:.1f} 104 40)">' + collar() + head(mouth, 0.2, 0) + '</g>'
    return DEFS + shadow(76, 50) + tl + far_front + body + hind + (BONE if bone else '') + hd + front
