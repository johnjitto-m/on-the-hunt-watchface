"""v2.7 art: bigger, more detailed coffee guy + golden dog, with reactions to weather, time of day,
notifications and activity.  Scenes are composed in one SVG in 'duo px' (the v2.6 1x duo box units:
man box at x 50, dog box at (0, 69.8), ground at y ~134.7) and rendered at scale S (supersampled)."""
import math, sys
sys.path.insert(0, 'tools')
import render_v2 as R
import guy2, real_guy as G, coffee_guy as C, dog2 as D2, dog3 as D
from dog2 import limb

O = dict(C.O)
K = 100 / 240                      # man rig units -> duo px
DOGY = 69.8
GROUND = 134.75
VB = (-24, -10, 184, 150)        # scene box in duo px (x, y, w, h)


def lerp(a, b, u): return a + (b - a) * u
def lp(p, q, u): return (lerp(p[0], q[0], u), lerp(p[1], q[1], u))
def ang(p, q): return math.degrees(math.atan2(q[1] - p[1], q[0] - p[0]))


# ============================================================ man: shared defs
def mdefs(o=O):
    d = G.defs(o)
    extra = (
        f'<linearGradient id="jf" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{o["jacketd"]}"/><stop offset="0.55" stop-color="{o["jacket"]}"/><stop offset="1" stop-color="{o["jacketl"]}"/></linearGradient>'
        '<linearGradient id="tee" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#bdb8ad"/><stop offset="0.6" stop-color="#ecebe6"/><stop offset="1" stop-color="#f7f6f2"/></linearGradient>'
        f'<linearGradient id="pf" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{o["denim_d"]}"/><stop offset="0.6" stop-color="{o["denim"]}"/><stop offset="1" stop-color="{o["denim_l"]}"/></linearGradient>'
        f'<linearGradient id="skf" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{o["skin_d"]}"/><stop offset="0.55" stop-color="{o["skin"]}"/><stop offset="1" stop-color="{o["skin_l"]}"/></linearGradient>'
        f'<linearGradient id="hatf" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{o["hatd"]}"/><stop offset="0.55" stop-color="{o["hat"]}"/><stop offset="1" stop-color="{o["hatl"]}"/></linearGradient>'
        '<linearGradient id="cord" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#3e2716"/><stop offset="0.6" stop-color="#6a4426"/><stop offset="1" stop-color="#8a5c34"/></linearGradient>'
        '<pattern id="wale" width="1.6" height="4" patternUnits="userSpaceOnUse"><path d="M0.4 0 L0.4 4" stroke="#000" stroke-opacity="0.3" stroke-width="0.6"/></pattern>'
        '<linearGradient id="lens" x1="0" y1="0" x2="0.3" y2="1"><stop offset="0" stop-color="#4a5466"/><stop offset="0.45" stop-color="#14171d"/><stop offset="1" stop-color="#050608"/></linearGradient>'
        '<linearGradient id="scarf" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#5e0f17"/><stop offset="0.55" stop-color="#9a1f2a"/><stop offset="1" stop-color="#c23a46"/></linearGradient>'
        '<linearGradient id="umb" x1="0" y1="0" x2="1" y2="0.4"><stop offset="0" stop-color="#4a0a12"/><stop offset="0.5" stop-color="#8e1624"/><stop offset="0.8" stop-color="#c8323f"/><stop offset="1" stop-color="#8e1624"/></linearGradient>'
        '<linearGradient id="latte" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#8a5a33"/><stop offset="0.6" stop-color="#b98a5a"/><stop offset="1" stop-color="#d9b48a"/></linearGradient>'
        '<radialGradient id="glowscr" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#bfe6ff" stop-opacity="0.9"/><stop offset="1" stop-color="#bfe6ff" stop-opacity="0"/></radialGradient>'
        '<filter id="puff" x="-80%" y="-80%" width="260%" height="260%"><feGaussianBlur stdDeviation="2.6"/></filter>')
    return d.replace('</defs>', extra + '</defs>')


RIM = G.RIM
JD, JC, JL = O['jacketd'], O['jacket'], O['jacketl']


def hand_svg(at, deg, kind='relax', s=1.0):
    """hand at the wrist point, pointing along deg (0 = +x).  Drawn pointing down then rotated."""
    if kind == 'fist':
        h = ('<path d="M-5.2 0 Q-6.4 7 -4.6 11.6 Q-0.6 14.6 4 12 Q6.2 7 5.2 0 Z" fill="url(#skf)"/>'
             '<path d="M-3.8 8.6 Q0 10.6 4 8.4" stroke="#000" stroke-opacity="0.25" stroke-width="0.7" fill="none"/>')
    else:
        h = ('<path d="M-5.2 0 Q-6.6 9 -4.6 15 Q-1 19 3.4 16 Q6.4 9.6 5.2 0 Z" fill="url(#skf)"/>'
             '<path d="M5 3 Q8.6 7.4 6.4 11.6" stroke="url(#skf)" stroke-width="3.4" fill="none" stroke-linecap="round"/>'
             '<path d="M-3.6 10.4 Q0 12.6 3.6 10.2 M-3.8 14 Q-0.6 15.8 2.6 13.8" stroke="#000" stroke-opacity="0.22" stroke-width="0.7" fill="none"/>')
    return f'<g transform="translate({at[0]:.2f} {at[1]:.2f}) rotate({deg - 90:.2f}) scale({s})">{h}</g>'


def arm(sh, el, wr, outfit='jacket', hand='relax', hand_s=1.0, rim=True, cuff=True, watch=False):
    """front-view arm through shoulder, elbow, wrist (rig units)."""
    out = ''
    if outfit == 'jacket':
        out += limb([sh, lp(sh, el, 0.5), el], [16, 14.4, 12.8], 'url(#jf)') + limb([sh, lp(sh, el, 0.5), el], [16, 14.4, 12.8], 'url(#twill)')
        out += f'<ellipse cx="{el[0]:.2f}" cy="{el[1]:.2f}" rx="6.3" ry="6.3" fill="{JC}"/>'
        out += limb([el, lp(el, wr, 0.5), wr], [12.8, 11.8, 10.8], 'url(#jf)') + limb([el, wr], [12.8, 10.8], 'url(#twill)')
        mid = lp(sh, el, 0.62)
        out += f'<path d="M{mid[0] - 4:.1f} {mid[1]:.1f} Q{mid[0]:.1f} {mid[1] + 2.4:.1f} {mid[0] + 4:.1f} {mid[1]:.1f}" stroke="#000" stroke-opacity="0.22" stroke-width="1" fill="none"/>'
        if cuff:
            out += limb([lp(el, wr, 0.84), wr], [11.4, 11.2], JD)
            out += limb([lp(el, wr, 0.84), wr], [11.4, 11.2], 'url(#wale)')
    else:   # tee: short sleeve, bare arm
        sl = lp(sh, el, 0.46)
        out += limb([lp(sh, el, 0.3), el], [12.6, 10.6], 'url(#skf)')
        out += f'<ellipse cx="{el[0]:.2f}" cy="{el[1]:.2f}" rx="5.2" ry="5.2" fill="url(#skf)"/>'
        out += limb([el, lp(el, wr, 0.5), wr], [10.6, 9.6, 8.4], 'url(#skf)')
        out += limb([sh, sl], [17, 15.6], 'url(#tee)')
        out += f'<path d="M{sl[0] - 7.4:.1f} {sl[1]:.1f} L{sl[0] + 7.4:.1f} {sl[1]:.1f}" stroke="#a9a397" stroke-width="1" stroke-opacity="0.8"/>'
        m2 = lp(el, wr, 0.4)
        out += f'<path d="M{m2[0] - 2:.1f} {m2[1] - 3:.1f} Q{m2[0] - 2.6:.1f} {m2[1]:.1f} {m2[0] - 2:.1f} {m2[1] + 3:.1f}" stroke="#7a5a44" stroke-opacity="0.35" stroke-width="0.6" fill="none"/>'
    if watch:
        w = lp(el, wr, 0.8)
        out += (f'<g transform="translate({w[0]:.2f} {w[1]:.2f}) rotate({ang(el, wr) + 90:.1f})">'
                '<rect x="-6.2" y="-2.2" width="12.4" height="4.4" rx="1.4" fill="#111"/>'
                '<circle r="4.4" fill="#16171b" stroke="#6b6e78" stroke-width="0.9"/><circle r="3.3" fill="#7fd0ff"/>'
                '<circle r="10" fill="url(#glowscr)" opacity="0.7"/></g>')
    d = ang(el, wr)
    out += hand_svg((wr[0] + math.cos(math.radians(d)) * 0.8, wr[1] + math.sin(math.radians(d)) * 0.8), d, hand, hand_s)
    if rim:
        out += f'<path d="M{sh[0] - 7:.1f} {sh[1] + 4:.1f} Q{el[0] - 7.4:.1f} {lerp(sh[1], el[1], 0.5):.1f} {el[0] - 6.4:.1f} {el[1]:.1f}" {RIM}/>'
    return out


def umbrella(handle, top, r=86, drops=True):
    """J-handle at `handle`, shaft to the canopy apex `top`; canopy perpendicular to the shaft."""
    a = ang(handle, top) + 90            # canopy rotation (0 when the shaft is vertical)
    hx, hy = handle
    ux, uy = (top[0] - hx), (top[1] - hy)
    L = math.hypot(ux, uy)
    shaft = (f'<path d="M{hx:.1f} {hy:.1f} L{top[0]:.1f} {top[1]:.1f}" stroke="#2a2b30" stroke-width="2.4"/>'
             f'<path d="M{hx:.1f} {hy:.1f} L{top[0]:.1f} {top[1]:.1f}" stroke="#9aa0ad" stroke-opacity="0.5" stroke-width="0.7"/>'
             f'<g transform="translate({hx:.1f} {hy:.1f}) rotate({a:.1f})"><path d="M0 0 L0 12 Q0 22 -8 22 Q-15 22 -15 14" stroke="#4a2c16" stroke-width="4.2" fill="none" stroke-linecap="round"/>'
             '<path d="M0.8 2 L0.8 12 Q0.8 20 -7 20.6" stroke="#a87448" stroke-opacity="0.6" stroke-width="1" fill="none"/></g>')
    ribs = 8
    # canopy in its own frame: apex at (0,0), rim at y = 34, half width r
    pts = [(-r + 2 * r * i / ribs, 34 - 6 * math.sin(math.pi * i / ribs) * 0) for i in range(ribs + 1)]
    dome = f'M{-r} 34 Q{-r * 0.78} -2 0 -6 Q{r * 0.78} -2 {r} 34 '
    scallop = ''.join(f'Q{(pts[i][0] + pts[i + 1][0]) / 2:.1f} {27:.1f} {pts[i + 1][0]:.1f} 34 ' for i in range(ribs - 1, -1, -1)).replace(f'{pts[0][0]:.1f} 34 ', f'{pts[0][0]:.1f} 34 Z', 1)
    canopy = (f'<path d="{dome}{scallop}" fill="url(#umb)"/>'
              + ''.join(f'<path d="M0 -6 Q{p[0] * 0.55:.1f} {6 + abs(p[0]) * 0.05:.1f} {p[0]:.1f} 34" stroke="#000" stroke-opacity="0.45" stroke-width="0.9" fill="none"/>' for p in pts[1:-1])
              + f'<path d="M{-r * 0.6:.1f} 10 Q{-r * 0.2:.1f} -4 {r * 0.3:.1f} -2" stroke="#ffd0d4" stroke-opacity="0.4" stroke-width="2.2" fill="none" stroke-linecap="round"/>'
              + f'<path d="M{-r} 34 Q{-r * 0.78} -2 0 -6" stroke="#ffb0b8" stroke-opacity="0.5" stroke-width="1.6" fill="none"/>'
              + ''.join(f'<circle cx="{p[0]:.1f}" cy="34.6" r="1.2" fill="#c9ccd4"/>' for p in pts)
              + '<path d="M-1.4 -6 L0 -13 L1.4 -6 Z" fill="#c9ccd4"/>'
              + ''.join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="0.9" fill="#dfe8ff" fill-opacity="0.7"/>' for x, y in ((-40, 10), (-22, 2), (8, 4), (30, 9), (52, 16), (-58, 20), (66, 24), (-8, 14)))
              + (''.join(f'<path d="M{p[0]:.1f} 37 L{p[0] - 0.3:.1f} {41 + (i * 7) % 9:.1f}" stroke="#dfe8ff" stroke-opacity="0.75" stroke-width="1" stroke-linecap="round"/>'
                         f'<circle cx="{p[0] - 0.3:.1f}" cy="{44 + (i * 7) % 9 + (i * 13) % 11:.1f}" r="0.9" fill="#dfe8ff" fill-opacity="0.65"/>' for i, p in enumerate(pts)) if drops else ''))
    canopy = f'<g transform="translate({top[0]:.1f} {top[1]:.1f}) rotate({a:.1f})">{canopy}</g>'
    return shaft + canopy


def iced_cup():
    return ('<path d="M78.4 92 L94.6 92 L92.6 125 L80.4 125 Z" fill="#e8eef2" fill-opacity="0.28" stroke="#ffffff" stroke-opacity="0.55" stroke-width="0.7"/>'
            '<path d="M79.2 100 L93.8 100 L92.6 125 L80.4 125 Z" fill="url(#latte)" fill-opacity="0.92"/>'
            '<path d="M79.6 104 Q86 106 93.4 103" stroke="#f3e2c6" stroke-opacity="0.7" stroke-width="2" fill="none"/>'
            + ''.join(f'<rect x="{x}" y="{y}" width="5" height="4.6" rx="1.2" fill="#ffffff" fill-opacity="0.5" stroke="#ffffff" stroke-opacity="0.7" stroke-width="0.4" transform="rotate({r} {x + 2.5} {y + 2.3})"/>'
                      for x, y, r in ((80.6, 94, 12), (86.4, 95.4, -8), (88.4, 101.4, 20), (81.6, 102, -14)))
            + '<path d="M77 89.4 Q86.5 85 96 89.4 L96 92.6 L77 92.6 Z" fill="#f4f6f8" fill-opacity="0.55" stroke="#ffffff" stroke-opacity="0.7" stroke-width="0.6"/>'
            '<path d="M88 90 L92.6 68" stroke="#1d5c3a" stroke-width="2.6" stroke-linecap="round"/>'
            '<path d="M88.4 89 L92.6 69" stroke="#8fd6a8" stroke-opacity="0.5" stroke-width="0.7"/>'
            + ''.join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#ffffff" fill-opacity="0.7"/>' for x, y, r in ((82, 110, 0.6), (84.6, 116, 0.5), (90.4, 112, 0.7), (91.6, 119, 0.5), (81.4, 120, 0.5)))
            + '<path d="M93 95 L91.6 123" stroke="#ffffff" stroke-opacity="0.6" stroke-width="1"/>'
            '<path d="M88 108 Q96 106 97 112 Q97 120 90 121 Q86 119 88 108 Z" fill="url(#skf)"/>'
            '<path d="M86 112 Q89 111 92 112 M86 116 Q89 115 92 116" stroke="#000" stroke-opacity="0.25" stroke-width="0.8" fill="none"/>')


def hot_cup(steam=1.0):
    st = ''
    if steam:
        for k, (x, y, s) in enumerate(((85, 90, 1.0), (89, 86, 0.8), (82, 84, 0.7))):
            st += (f'<path d="M{x} {y} Q{x - 3} {y - 6} {x} {y - 11} Q{x + 3} {y - 16} {x} {y - 22}" stroke="#ffffff" stroke-opacity="{0.32 * steam * s:.2f}" '
                   f'stroke-width="{1.6 * s:.1f}" fill="none" stroke-linecap="round"/>')
        st += f'<ellipse cx="86" cy="76" rx="7" ry="10" fill="#ffffff" fill-opacity="{0.07 * steam:.2f}" filter="url(#puff)"/>'
    return ('<path d="M79 98 L94 98 L92.5 124 L80.5 124 Z" fill="url(#cp)"/>'
            '<path d="M79.6 106 L93.4 106 L92.8 115 L80.2 115 Z" fill="#8a5a33"/><path d="M79.6 106 L93.4 106 L92.8 115 L80.2 115 Z" fill="url(#chino)"/>'
            '<path d="M78 95 L95 95 Q95.6 97 95 99 L78 99 Q77.4 97 78 95 Z" fill="#2c2c30"/>'
            '<path d="M86 94.2 L90 94.2 L90 95.2 L86 95.2 Z" fill="#111"/>'
            '<path d="M91 100 L90 122" stroke="#fff" stroke-opacity="0.55" stroke-width="1"/>'
            '<path d="M81 100 L82 122" stroke="#000" stroke-opacity="0.1" stroke-width="1.4"/>'
            + st +
            '<path d="M88 108 Q96 106 97 112 Q97 120 90 121 Q86 119 88 108 Z" fill="url(#skf)"/>'
            '<path d="M86 112 Q89 111 92 112 M86 116 Q89 115 92 116" stroke="#000" stroke-opacity="0.25" stroke-width="0.8" fill="none"/>')


def front2(outfit='jacket', left=('hang', 0), right='cup', tilt=0.0, look=(0.0, 0.0), lids=0.0, smile=0.0, shades=False,
           scarf=False, breath=0.0, snow=False, wet=False, steam=1.0, brows=0.0, lean=0.0, kneel=False, hat='beanie', coin=None, closed=False):
    o = O
    st = '<ellipse cx="75" cy="298" rx="34" ry="3.4" fill="#000" fill-opacity="0.5" filter="url(#soft1)"/>'
    legs = ('<path d="M53 156 L73.5 156 L72 230 L71 285 L56 285 L54.5 230 Z" fill="url(#pf)"/>'
            '<path d="M76.5 156 L97 156 L95.5 230 L94 285 L79 285 L78 230 Z" fill="url(#pf)"/>'
            '<path d="M53 156 L73.5 156 L72 230 L71 285 L56 285 L54.5 230 Z M76.5 156 L97 156 L95.5 230 L94 285 L79 285 L78 230 Z" fill="url(#chino)"/>'
            '<path d="M73.5 158 L75 196 L76.5 158 Z" fill="#000" fill-opacity="0.45"/>'
            '<path d="M54 160 L55.5 284" ' + RIM + '/>'
            '<path d="M58 226 Q63 229 69 226 M81 226 Q86 229 92 226" stroke="#000" stroke-opacity="0.25" stroke-width="1.2" fill="none"/>'
            '<path d="M57 270 Q63 274 70 270 M80 270 Q86 274 93 270 M57 276 Q63 279 70 276 M80 276 Q86 279 93 276" stroke="#000" stroke-opacity="0.22" stroke-width="1" fill="none"/>'
            '<path d="M93 170 L92 280" stroke="#fff" stroke-opacity="0.1" stroke-width="2"/>'
            '<path d="M60 162 Q62 190 61 224 M86 164 Q88 192 87 224" stroke="#000" stroke-opacity="0.12" stroke-width="1.6" fill="none"/>')
    boots = ''.join(
        f'<path d="M{x0} 279 L{x0 + 17} 279 L{x0 + 18.5} 290 Q{x0 + 19} 297.5 {x0 + 13} 297.5 L{x0 + 3} 297.5 Q{x0 - 2} 297.5 {x0 - 1} 290 Z" fill="url(#bt2)"/>'
        f'<path d="M{x0 - 1.4} 294 L{x0 + 19} 294 L{x0 + 18.5} 297.5 L{x0 - 1} 297.5 Z" fill="#1a120c"/>'
        f'<path d="M{x0 - 1} 293.4 L{x0 + 18.6} 293.4" stroke="#d9b98a" stroke-opacity="0.5" stroke-width="0.5" stroke-dasharray="1 0.8"/>'
        f'<path d="M{x0 + 4} 280 L{x0 + 13} 280 L{x0 + 12} 291 L{x0 + 5} 291 Z" fill="#2a180c" fill-opacity="0.8"/>'
        + ''.join(f'<path d="M{x0 + 5} {281.5 + 2.4 * i} L{x0 + 12} {282.6 + 2.4 * i}" stroke="#e2c9a0" stroke-width="0.7"/>' for i in range(4))
        + f'<path d="M{x0 + 13} 289 Q{x0 + 16} 292 {x0 + 15} 295" stroke="#fff" stroke-opacity="0.25" stroke-width="1" fill="none"/>'
        for x0 in (54, 78))
    snow_l = ''
    if snow:
        snow_l = ''.join(f'<ellipse cx="{x}" cy="{y}" rx="{r * 1.4:.1f}" ry="{r:.1f}" fill="#f4f8ff" fill-opacity="0.9"/>' for x, y, r in
                         ((48, 64, 1.6), (54, 60, 1.2), (98, 62, 1.5), (104, 66, 1.2), (57, 296, 2), (66, 297, 1.5), (82, 296.4, 2), (92, 297, 1.4)))
    torso, tied = '', ''
    if outfit == 'jacket':
        torso = ('<path d="M61 58 Q75 66 89 58 L91 160 L59 160 Z" fill="url(#tee)"/>'
                 '<path d="M64 58 Q75 64 86 58" stroke="#b8b2a6" stroke-width="1.4" fill="none"/>'
                 '<path d="M66 120 Q75 124 84 120 M68 96 Q75 99 82 96" stroke="#000" stroke-opacity="0.1" stroke-width="1.4" fill="none"/>'
                 '<path d="M44 66 Q50 58 62 57 L66 64 L65 104 L64 168 L48 168 Q45 120 44 66 Z" fill="url(#jf)"/>'
                 '<path d="M106 66 Q100 58 88 57 L84 64 L85 104 L86 168 L102 168 Q105 120 106 66 Z" fill="url(#jf)"/>'
                 '<path d="M44 66 Q50 58 62 57 L66 64 L65 104 L64 168 L48 168 Q45 120 44 66 Z M106 66 Q100 58 88 57 L84 64 L85 104 L86 168 L102 168 Q105 120 106 66 Z" fill="url(#twill)"/>'
                 '<path d="M47 160 L64 160 L64 168 L48 168 Z M86 160 L102.5 160 L102 168 L86 168 Z" fill="' + JD + '"/>'
                 '<path d="M48 162 L64 162 M48 165 L64 165 M86 162 L102 162 M86 165 L102 165" stroke="#000" stroke-opacity="0.25" stroke-width="0.6"/>'
                 '<circle cx="60" cy="164" r="1" fill="#d9c08a"/><circle cx="90" cy="164" r="1" fill="#d9c08a"/>'
                 # corduroy collar
                 '<path d="M62 57 L54 60 L59 82 L66 65 Z" fill="url(#cord)"/><path d="M62 57 L54 60 L59 82 L66 65 Z" fill="url(#wale)"/>'
                 '<path d="M88 57 L96 60 L91 82 L84 65 Z" fill="url(#cord)"/><path d="M88 57 L96 60 L91 82 L84 65 Z" fill="url(#wale)"/>'
                 '<path d="M54 60 L59 82 M96 60 L91 82" stroke="#d8b080" stroke-opacity="0.35" stroke-width="0.6"/>'
                 # yoke seams + chest pockets with flaps and buttons
                 '<path d="M45 76 Q54 73 64.6 75 M105 76 Q96 73 85.4 75" stroke="#c9a46a" stroke-opacity="0.6" stroke-width="0.7" stroke-dasharray="1.4 1" fill="none"/>'
                 '<path d="M50 84 L61 84 L61 97 L50 97 Z M89 84 L100 84 L100 97 L89 97 Z" fill="#000" fill-opacity="0.14" stroke="#c9a46a" stroke-opacity="0.75" stroke-width="0.7" stroke-dasharray="1.4 1"/>'
                 '<path d="M50 84 L61 84 L60 89 L55.5 91 L51 89 Z M89 84 L100 84 L99 89 L94.5 91 L90 89 Z" fill="' + JD + '" fill-opacity="0.85"/>'
                 '<circle cx="55.5" cy="88.6" r="0.95" fill="#d9c08a"/><circle cx="94.5" cy="88.6" r="0.95" fill="#d9c08a"/>'
                 '<path d="M49 108 L49.6 150 M101 108 L100.4 150" stroke="#c9a46a" stroke-opacity="0.45" stroke-width="0.7" stroke-dasharray="1.4 1"/>'
                 '<path d="M64.5 66 L63.5 166 M85.5 66 L86.5 166" stroke="#c9a46a" stroke-opacity="0.7" stroke-width="0.7" stroke-dasharray="1.4 1" fill="none"/>'
                 '<circle cx="64.6" cy="110" r="0.9" fill="#d9c08a"/><circle cx="64.4" cy="134" r="0.9" fill="#d9c08a"/>'
                 '<path d="M52 128 Q56 132 61 129 M90 132 Q94 136 99 133" stroke="#000" stroke-opacity="0.2" stroke-width="1.2" fill="none"/>'
                 '<path d="M45 70 Q44 120 48 166" ' + RIM + '/>'
                 '<path d="M102 72 Q104 120 101 160" stroke="#fff" stroke-opacity="0.15" stroke-width="2" fill="none"/>')
    else:
        torso = ('<path d="M46 66 Q50 58 62 57 Q75 65 88 57 Q100 58 104 66 L102 160 L48 160 Z" fill="url(#tee)"/>'
                 '<path d="M62 57 Q75 66 88 57" stroke="#b8b2a6" stroke-width="1.6" fill="none"/>'
                 '<path d="M56 90 Q60 100 58 112 M92 92 Q90 102 93 112 M64 132 Q75 136 86 132" stroke="#000" stroke-opacity="0.13" stroke-width="1.4" fill="none"/>'
                 '<path d="M49 70 Q47 120 49 158" ' + RIM + '/>')
        # denim jacket tied around the waist: back panel behind the legs, sleeves knotted in front
        tied = ('<path d="M45 150 Q75 146 105 150 L108 212 Q96 216 92 206 L58 206 Q54 216 42 212 Z" fill="url(#jf)"/>'
                '<path d="M45 150 Q75 146 105 150 L108 212 Q96 216 92 206 L58 206 Q54 216 42 212 Z" fill="url(#twill)"/>'
                '<path d="M44 196 Q48 206 42 212 M106 196 Q102 206 108 212" stroke="#c9a46a" stroke-opacity="0.5" stroke-width="0.7" stroke-dasharray="1.4 1" fill="none"/>')
        torso += ('<path d="M46 150 Q75 160 104 150 L104 162 Q75 170 46 162 Z" fill="url(#jf)"/><path d="M46 150 Q75 160 104 150 L104 162 Q75 170 46 162 Z" fill="url(#twill)"/>'
                  '<path d="M46 150 Q75 160 104 150" stroke="#000" stroke-opacity="0.25" stroke-width="1" fill="none"/>'
                  '<path d="M68 156 Q75 152 82 156 Q84 164 77 168 Q70 167 68 156 Z" fill="' + JC + '"/>'
                  '<path d="M70 164 Q66 182 69 200 L76 199 Q75 182 77 166 Z" fill="url(#jf)"/>'
                  '<path d="M78 164 Q84 180 82 194 L88 193 Q89 178 82 163 Z" fill="url(#jf)"/>'
                  '<path d="M69 196 L76 195.4 L76 200 L69 200.6 Z M82 190.6 L88 190 L88 194 L82 194.6 Z" fill="' + JD + '"/>'
                  '<path d="M71 160 Q75 158 80 160" stroke="#000" stroke-opacity="0.3" stroke-width="0.9" fill="none"/>')
    neck = ('<path d="M67 42 L81 42 L81.5 60 L66.5 60 Z" fill="url(#skf)"/>'
            '<path d="M67 46 Q74 52 81 46 L81.5 52 Q74 56 67 52 Z" fill="#000" fill-opacity="0.22"/>'
            '<path d="M71 52 Q74 55 77 52" stroke="#000" stroke-opacity="0.15" stroke-width="0.8" fill="none"/>')
    scarf_s = ''
    if scarf:
        scarf_s = ('<path d="M60 50 Q74 44 89 50 Q92 56 89 62 Q74 68 60 62 Q57 56 60 50 Z" fill="url(#scarf)"/>'
                   '<path d="M60 50 Q74 44 89 50 Q92 56 89 62 Q74 68 60 62 Q57 56 60 50 Z" fill="url(#knit)"/>'
                   '<path d="M61 55 Q74 51 88 55" stroke="#000" stroke-opacity="0.25" stroke-width="1" fill="none"/>'
                   '<path d="M64 60 Q61 84 63 108 L73 108 Q72 84 73 62 Z" fill="url(#scarf)"/><path d="M64 60 Q61 84 63 108 L73 108 Q72 84 73 62 Z" fill="url(#knit)"/>'
                   '<path d="M70 62 Q75 80 78 96 L86 93 Q82 78 78 61 Z" fill="#7a1620"/><path d="M70 62 Q75 80 78 96 L86 93 Q82 78 78 61 Z" fill="url(#knit)"/>'
                   + ''.join(f'<path d="M{x} 108 L{x - 0.3} 112.4" stroke="#9a1f2a" stroke-width="1.2" stroke-linecap="round"/>' for x in (64, 66.2, 68.4, 70.6, 72.8))
                   + ''.join(f'<path d="M{x} {y} L{x + 0.6} {y + 4.2}" stroke="#7a1620" stroke-width="1.1" stroke-linecap="round"/>' for x, y in ((78.4, 95.8), (80.6, 95), (82.8, 94.2), (85, 93.4)))
                   + '<path d="M64 64 L72 64 M63.6 76 L72.4 76 M63.4 88 L72.4 88 M63.2 100 L72.6 100" stroke="#e8c070" stroke-opacity="0.5" stroke-width="1.2"/>'
                   '<path d="M59.6 52 Q58.4 57 60 61" ' + RIM + '/>')
    # ---------------- head
    eyes = ('<path d="M65.5 28 Q68 26.4 70.5 28 Q68 29.6 65.5 28 Z M77.5 28 Q80 26.4 82.5 28 Q80 29.6 77.5 28 Z" fill="#f1ebe3"/>'
            '<circle cx="68.2" cy="28" r="1.25" fill="#4a3424"/><circle cx="80.2" cy="28" r="1.25" fill="#4a3424"/>'
            '<circle cx="68.2" cy="28" r="0.6" fill="#0d0907"/><circle cx="80.2" cy="28" r="0.6" fill="#0d0907"/>'
            '<circle cx="68.7" cy="27.5" r="0.4" fill="#fff" fill-opacity="0.85"/><circle cx="80.7" cy="27.5" r="0.4" fill="#fff" fill-opacity="0.85"/>')
    eyes = f'<g transform="translate({look[0]:.2f} {look[1]:.2f})">{eyes}</g>'
    lid_y = 26.6 + 1.6 * lids
    lidp = (f'<path d="M65 28 Q68 25.6 71 28 L71 {lid_y - 0.6:.2f} Q68 {lid_y - 2:.2f} 65 {lid_y - 0.6:.2f} Z M77 28 Q80 25.6 83 28 L83 {lid_y - 0.6:.2f} Q80 {lid_y - 2:.2f} 77 {lid_y - 0.6:.2f} Z" fill="url(#skf)"/>'
            if lids > 0.05 else '')
    lashes = (f'<path d="M65.2 {27.9 - 1.2 * (1 - lids) + 1.6 * lids:.2f} Q68 {26.2 + 1.8 * lids:.2f} 70.8 {27.9 - 1.2 * (1 - lids) + 1.6 * lids:.2f} '
              f'M77.2 {27.9 - 1.2 * (1 - lids) + 1.6 * lids:.2f} Q80 {26.2 + 1.8 * lids:.2f} 82.8 {27.9 - 1.2 * (1 - lids) + 1.6 * lids:.2f}" stroke="#1a110c" stroke-width="0.8" fill="none"/>')
    by = -brows
    hd = ('<ellipse cx="60" cy="30" rx="2.8" ry="5.2" fill="url(#skf)"/><ellipse cx="88.4" cy="30" rx="2.8" ry="5.2" fill="url(#skf)"/>'
          '<path d="M59.4 28 Q60.6 30 59.8 33 M89 28 Q87.8 30 88.6 33" stroke="#000" stroke-opacity="0.3" stroke-width="0.7" fill="none"/>'
          '<path d="M60.5 22 Q60.5 9 74 9 Q87.5 9 87.5 22 L87.5 33 Q86.5 43.5 80 47.5 Q74 50.5 68 47.5 Q61.5 43.5 60.5 33 Z" fill="url(#skf)"/>'
          '<path d="M61 34 Q63 44 68 47.5 Q74 50.5 80 47.5 Q76 48 74 47 Q66 44 61 34 Z" fill="#000" fill-opacity="0.18"/>'
          '<path d="M63 38 Q66 47 74 48.5 Q82 47 85 38 Q83 45 74 46 Q65 45 63 38 Z" fill="#6b4a2a" fill-opacity="0.28"/>'
          '<path d="M70.4 39.8 Q74 38.6 77.6 39.8 Q74 40.6 70.4 39.8 Z" fill="#6b4a2a" fill-opacity="0.3"/>'
          '<ellipse cx="65" cy="35" rx="3.4" ry="2.4" fill="url(#cheek)"/><ellipse cx="83" cy="35" rx="3.4" ry="2.4" fill="url(#cheek)"/>'
          + eyes + lidp + lashes +
          f'<path d="M64.5 {24.6 + by:.2f} Q68 {23 + by:.2f} 71.5 {24.4 + by:.2f} M76.5 {24.4 + by:.2f} Q80 {23 + by:.2f} 83.5 {24.6 + by:.2f}" stroke="#5a3d22" stroke-width="1.4" fill="none" stroke-linecap="round"/>'
          '<path d="M74.5 29 L75.6 36" stroke="#000" stroke-opacity="0.2" stroke-width="1.2"/>'
          '<path d="M72 37.4 Q74 38.8 76.5 37.4" stroke="#000" stroke-opacity="0.35" stroke-width="0.9" fill="none"/>'
          '<path d="M76.2 30 Q77 34 76.4 36.4" stroke="#fff" stroke-opacity="0.2" stroke-width="0.7" fill="none"/>'
          f'<path d="M70.4 {41.4 - 0.4 * smile:.2f} Q74 {42.8 + 1.2 * smile:.2f} 77.8 {41.4 - 0.4 * smile:.2f}" stroke="#7a4a3c" stroke-width="1.1" fill="none" stroke-linecap="round"/>'
          '<path d="M71.6 43.6 Q74 44.4 76.4 43.6" stroke="#000" stroke-opacity="0.12" stroke-width="0.8" fill="none"/>'
          '<path d="M61 22 Q60.5 30 62 38" ' + RIM + '/>'
          # hair at the temples under the beanie
          '<path d="M60.6 24 Q61 29 62 32 L63.4 31 Q62.6 27 62.8 24 Z M87.4 24 Q87 29 86 32 L84.6 31 Q85.4 27 85.2 24 Z" fill="#5a3a22"/>'
          # knit beanie (crown + ribbed cuff + texture)
          '<path d="M59 24 Q58 1 74 0.5 Q90 1 89.5 24 Z" fill="url(#hatf)"/><path d="M59 24 Q58 1 74 0.5 Q90 1 89.5 24 Z" fill="url(#knit)"/>'
          '<path d="M58.4 17.5 Q74 15 90 17.5 L90 25.5 Q74 23.5 58.4 25.5 Z" fill="url(#hatf)"/>'
          '<path d="M58.4 17.5 Q74 15 90 17.5" stroke="#000" stroke-opacity="0.3" stroke-width="1" fill="none"/>'
          '<path d="M58.4 25.5 Q74 23.5 90 25.5" stroke="#000" stroke-opacity="0.25" stroke-width="0.8" fill="none"/>'
          + ''.join(f'<path d="M{x} 18 L{x} 25" stroke="#000" stroke-opacity="0.2" stroke-width="0.8"/>' for x in [round(59.6 + i * 1.9, 1) for i in range(16)])
          + '<path d="M62 8 Q72 3 84 7" stroke="#fff" stroke-opacity="0.2" stroke-width="1.6" fill="none"/>'
          '<path d="M59.6 22 Q58.6 10 64 4" ' + RIM + '/>')
    if hat == 'santa':
        hd = hd[:hd.index('<path d="M59 24 Q58 1 74 0.5')] + SANTA
    if closed:
        hd += ('<path d="M65 26.6 Q68 25 71 26.6 L71 29.4 Q68 31 65 29.4 Z M77 26.6 Q80 25 83 26.6 L83 29.4 Q80 31 77 29.4 Z" fill="url(#skf)"/>'
               '<path d="M65.2 28.6 Q68 30 70.8 28.6 M77.2 28.6 Q80 30 82.8 28.6" stroke="#1a110c" stroke-width="0.8" fill="none"/>')
    if snow:
        hd += ''.join(f'<ellipse cx="{x}" cy="{y}" rx="{r * 1.5:.1f}" ry="{r:.1f}" fill="#f4f8ff"/>' for x, y, r in ((66, 3, 1.6), (73, 1, 2), (81, 2.4, 1.6), (77, 0.4, 1.2), (61, 9, 1.2), (87, 9, 1.1)))
    if shades:
        hd += ('<path d="M63.4 25.4 L72 25.4 L71.4 30.4 Q67.6 32.4 64.2 30.4 Z M76 25.4 L84.6 25.4 L83.8 30.4 Q80.4 32.4 76.6 30.4 Z" fill="url(#lens)" stroke="#0a0a0c" stroke-width="0.8"/>'
               '<path d="M72 26.4 Q74 25.4 76 26.4" stroke="#0a0a0c" stroke-width="1" fill="none"/>'
               '<path d="M63.4 25.8 L60.6 27 M84.6 25.8 L87.6 27" stroke="#0a0a0c" stroke-width="0.9"/>'
               '<path d="M65 26.4 L67.8 26.4 M77.6 26.4 L80.4 26.4" stroke="#ffffff" stroke-opacity="0.45" stroke-width="0.8"/>')
    if breath:
        hd += (f'<g opacity="{breath:.2f}"><ellipse cx="80" cy="44" rx="4" ry="3" fill="#ffffff" fill-opacity="0.35" filter="url(#puff)"/>'
               '<ellipse cx="87" cy="40" rx="6" ry="4.4" fill="#ffffff" fill-opacity="0.28" filter="url(#puff)"/>'
               '<ellipse cx="95" cy="35" rx="7" ry="5" fill="#ffffff" fill-opacity="0.18" filter="url(#puff)"/></g>')
    # ---------------- arms
    LSH, RSH = (44, 66), (106, 66)
    larm = ''
    lk = left[0]
    if lk == 'hang':
        lsleeve = 'url(#jf)' if outfit == 'jacket' else 'url(#skf)'
        if outfit == 'jacket':
            g = ('<path d="M37 68 Q43 61 51 67 L51 119 L38.5 119 Q36 92 37 68 Z" fill="url(#jf)"/><path d="M37 68 Q43 61 51 67 L51 119 L38.5 119 Q36 92 37 68 Z" fill="url(#twill)"/>'
                 '<path d="M38.5 117 L51 117 L50 152 L40 152 Z" fill="url(#jf)"/><path d="M38.5 117 L51 117 L50 152 L40 152 Z" fill="url(#twill)"/>'
                 '<path d="M39.5 150 L50.2 150 L50 158 L40 158 Z" fill="' + JD + '"/><path d="M39.5 150 L50.2 150 L50 158 L40 158 Z" fill="url(#wale)"/>'
                 '<path d="M37.5 72 Q36.5 100 39 150" ' + RIM + '/>'
                 '<path d="M41 104 Q45 108 50 105 M41 122 Q45 125 49.6 122" stroke="#000" stroke-opacity="0.25" stroke-width="1.2" fill="none"/>')
        else:
            g = ('<path d="M39.6 92 L50 92 L50.4 152 L41 152 Z" fill="url(#skf)"/>'
                 '<path d="M37 68 Q43 61 51 67 L51.6 94 L38.4 95 Q36 80 37 68 Z" fill="url(#tee)"/>'
                 '<path d="M38.4 94 L51.6 93.4" stroke="#a9a397" stroke-width="1"/>'
                 '<path d="M40.6 100 Q40 128 42 150" ' + RIM + '/>')
        g += ('<path d="M40 157 Q38 168 41 176 Q45 180 49 176 Q51 168 50 157 Z" fill="url(#skf)"/>'
              '<path d="M41.4 170 Q45 172.6 49 170 M41.6 174 Q45 176 48.6 174" stroke="#000" stroke-opacity="0.22" stroke-width="0.7" fill="none"/>')
        larm = f'<g transform="rotate({left[1]:.2f} 44 66)">{g}</g>'
    elif lk == 'wrist':
        larm = arm(LSH, (39, 113), (64, 98), outfit, 'relax', watch=True)
    elif lk == 'pocket':
        larm = arm(LSH, (39, 112), (51, 150), outfit, 'fist', hand_s=0.0)
        larm += '<path d="M47 150 Q52 147 57 151" stroke="#000" stroke-opacity="0.45" stroke-width="1.2" fill="none"/>'
    elif lk == 'umbrella':
        hand = left[1]
        el = left[2] if len(left) > 2 else (32, 108)
        larm = umbrella(hand, left[3] if len(left) > 3 else (hand[0] - 70, hand[1] - 110), r=left[4] if len(left) > 4 else 86) + arm(LSH, el, hand, outfit, 'fist')
    elif lk == 'wave':
        larm = arm(LSH, (30, 96), (24, 52), outfit, 'relax')
    elif lk == 'reach':                     # hand target in body frame (already un-rotated by the caller)
        tx, ty = left[1]
        d = math.hypot(tx - LSH[0], ty - LSH[1]); ux, uy = (tx - LSH[0]) / d, (ty - LSH[1]) / d
        wr = (tx - ux * 9, ty - uy * 9)
        el = D.ik2(LSH, wr, 48, 42, bend=1)
        larm = arm(LSH, el, wr, outfit, 'relax')
    elif lk == 'coin':                      # forearm up in front of the chest, thumb ready
        u = left[1]
        el = (lerp(41, 38, u), lerp(116, 112, u)); wr = (lerp(46, 60, u), lerp(150, 97, u))
        larm = arm(LSH, el, wr, outfit, 'fist')
    rarm = right_arm(right, outfit, steam)
    wet_s = ''
    if wet:
        wet_s = ('<path d="M44 66 Q50 58 62 57 L66 64 L65 104 L64 168 L48 168 Q45 120 44 66 Z M106 66 Q100 58 88 57 L84 64 L85 104 L86 168 L102 168 Q105 120 106 66 Z" fill="#0a1424" fill-opacity="0.22"/>'
                 + ''.join(f'<path d="M{x} {y} l0 {l}" stroke="#dfe8ff" stroke-opacity="0.55" stroke-width="0.9" stroke-linecap="round"/>' for x, y, l in
                           ((99, 70, 3), (104, 84, 2.6), (102, 100, 3), (93, 76, 2), (88, 112, 2.4), (100, 128, 2.2), (60, 2, 2), (82, 4, 2.2), (70, 6, 1.6))))
    hd = f'<g transform="rotate({tilt:.2f} 74 50)">' + hd + '</g>'
    neckg = f'<g transform="rotate({tilt * 0.4:.2f} 74 58)">' + neck + '</g>'
    order_l_front = lk in ('wrist', 'coin')
    coin_s = ''
    if coin is not None:
        cx, cy, rx = coin
        coin_s = (f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="12" fill="#f0c85a" fill-opacity="0.25" filter="url(#soft)"/>'
                  f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{rx:.1f}" ry="6.4" fill="#d9b04a" stroke="#7a5a18" stroke-width="1.1"/>'
                  + (f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{rx * 0.5:.1f}" ry="3.3" fill="none" stroke="#fff1b0" stroke-width="0.9"/>' if rx > 2.6 else ''))
    upper = (torso + (larm if not order_l_front else '') + neckg + scarf_s + hd + rarm + (larm if order_l_front else '') + wet_s + coin_s)
    if kneel:
        legs, boots, st = KNEEL_LEGS, '', '<ellipse cx="78" cy="298" rx="36" ry="3.4" fill="#000" fill-opacity="0.5" filter="url(#soft1)"/>'
    dy = KNEEL_DY if kneel else 0
    upper = f'<g transform="translate(0 {dy}) rotate({lean:.2f} 75 158)">{upper}</g>'
    return mdefs() + st + tied + legs + boots + upper + snow_l


SANTA = ('<path d="M59 24 Q57 4 74 1 Q86 -1 96 8 Q104 16 106 30 L100 29 Q96 18 89 16 L89.5 24 Z" fill="#b3121f"/>'
         '<path d="M59 24 Q57 4 74 1 Q86 -1 96 8" stroke="#ff6a74" stroke-opacity="0.4" stroke-width="1.6" fill="none"/>'
         '<path d="M74 4 Q84 2 92 10" stroke="#5a0610" stroke-opacity="0.4" stroke-width="1.4" fill="none"/>'
         '<path d="M57.4 18 Q74 14.6 91 18 L91 26.4 Q74 23.4 57.4 26.4 Z" fill="#f4f1ea"/>'
         '<path d="M57.4 18 Q74 14.6 91 18 L91 26.4 Q74 23.4 57.4 26.4 Z" fill="url(#knit)"/>'
         '<circle cx="104" cy="31" r="4.6" fill="#f4f1ea"/><circle cx="103" cy="29.8" r="1.6" fill="#ffffff"/>'
         '<path d="M59.6 22 Q58.6 10 64 4" ' + RIM + '/>')

W0 = (98.0, 118.0)          # wrist point of the cup-holding hand in the rest pose


def cup_group(kind, steam, wrist, rot=0.0):
    body = iced_cup() if kind == 'iced' else hot_cup(steam)
    return (f'<g transform="translate({wrist[0] - W0[0]:.2f} {wrist[1] - W0[1]:.2f}) rotate({rot:.2f} {W0[0]} {W0[1]})">{body}</g>')


def right_arm(right, outfit, steam):
    RSH = (106, 66)
    kind = right[0] if isinstance(right, tuple) else right
    if kind in ('cup', 'iced'):
        return arm(RSH, (111, 112), W0, outfit, 'fist', hand_s=0.0, rim=False) + cup_group(kind, steam, W0)
    if kind == 'sip':
        u = right[1]
        el = (lerp(111, 117, u), lerp(112, 98, u)); wr = (lerp(W0[0], 90, u), lerp(W0[1], 66, u))
        return arm(RSH, el, wr, outfit, 'fist', hand_s=0.0, rim=False) + cup_group('cup', steam * (1 - u), wr, -26 * u)
    if kind == 'cup_low':
        el, wr = (110, 113), (104, 152)
        return arm(RSH, el, wr, outfit, 'fist', hand_s=0.0, rim=False) + cup_group('cup', 0.2, wr, 8)
    if kind == 'pocket':
        return (arm(RSH, (111, 112), (99, 150), outfit, 'fist', hand_s=0.0, rim=False)
                + '<path d="M93 151 Q98 147 103 150" stroke="#000" stroke-opacity="0.45" stroke-width="1.2" fill="none"/>')
    if kind == 'sparkler':
        el, wr = (113, 108), (104, 92)
        stick = (f'<path d="M{wr[0] - 2:.1f} {wr[1] + 4:.1f} L{SPARK_TIP[0]:.1f} {SPARK_TIP[1]:.1f}" stroke="#4a4a50" stroke-width="1.6"/>'
                 f'<path d="M{wr[0] + 3:.1f} {wr[1] - 8:.1f} L{SPARK_TIP[0]:.1f} {SPARK_TIP[1]:.1f}" stroke="#9a9aa4" stroke-width="2.6" stroke-linecap="round"/>')
        return stick + arm(RSH, el, wr, outfit, 'fist', rim=False)
    return ''


SPARK_TIP = (122.0, 40.0)


def kneel_legs():
    # front view kneel: near knee (viewer-left) on the ground, far knee up, both feet tucked
    pf = 'url(#pf)'
    out = ('<path d="M53 206 L73 206 L72 236 L70 284 Q66 292 60 292 Q54 292 54 284 L54 236 Z" fill="' + pf + '"/>'
           '<path d="M53 206 L73 206 L72 236 L70 284 Q66 292 60 292 Q54 292 54 284 L54 236 Z" fill="url(#chino)"/>'
           '<ellipse cx="62" cy="290" rx="9" ry="5" fill="#26272b"/>'
           '<path d="M55 212 L55.6 284" ' + RIM + '/>'
           '<path d="M57 262 Q62 266 68 262 M57 270 Q62 273 68 270" stroke="#000" stroke-opacity="0.22" stroke-width="1" fill="none"/>'
           # far leg: thigh toward the viewer (foreshortened) -> knee cap -> shin down to a flat boot
           '<path d="M76 206 L97 206 L98 226 Q98 238 87 239 Q77 238 77 226 Z" fill="' + pf + '"/>'
           '<ellipse cx="87.6" cy="232" rx="11" ry="9" fill="' + pf + '"/><ellipse cx="88.6" cy="229" rx="6" ry="4" fill="#ffffff" fill-opacity="0.08"/>'
           '<path d="M79 236 L96.6 236 L95.6 284 L80 284 Z" fill="' + pf + '"/><path d="M79 236 L96.6 236 L95.6 284 L80 284 Z" fill="url(#chino)"/>'
           '<path d="M80 270 Q86 274 94 270 M80 276 Q86 279 94 276" stroke="#000" stroke-opacity="0.22" stroke-width="1" fill="none"/>'
           '<path d="M78 279 L95 279 L96.5 290 Q97 297.5 91 297.5 L81 297.5 Q76 297.5 77 290 Z" fill="url(#bt2)"/>'
           '<path d="M76.6 294 L97 294 L96.5 297.5 L77 297.5 Z" fill="#1a120c"/>'
           + ''.join(f'<path d="M83 {281.5 + 2.4 * i} L90 {282.6 + 2.4 * i}" stroke="#e2c9a0" stroke-width="0.7"/>' for i in range(4))
           + '<path d="M50 286 Q52 293 60 296 L46 297.6 Q43 292 50 286 Z" fill="url(#bt2)"/>')
    return out


KNEEL_DY = 50
KNEEL_LEGS = None


# ============================================================ man: side poses (jog)
def jog(ph):
    s = math.sin(2 * math.pi * ph); c = math.cos(2 * math.pi * ph)
    o = dict(O, coffee=False)
    th_f, th_b = -34 * s, 30 * s
    sh_f = 70 * max(0, c) ** 1.2 + 14
    sh_b = 70 * max(0, -c) ** 1.2 + 14
    ua_f, ua_b = 38 * s, -38 * s
    fa_f, fa_b = -92, -92
    o['_ankf'] = -14 * max(0, s) ** 2 + 20 * max(0, -s) ** 2
    o['_ankb'] = -14 * max(0, -s) ** 2 + 20 * max(0, s) ** 2
    return G.pose(o, th_f, sh_f, th_b, sh_b, ua_f, fa_f, ua_b, fa_b, lean=9, bob=-5 * abs(c) + 1, tilt=-4)


KNEEL_LEGS = kneel_legs()


# ============================================================ dog (golden retriever: hand-built sit + rig with the new head)
import retriever as RT
RT.head_local.__defaults__  # noqa
D.head = RT.rig_head
D2.collar = lambda: ''


def _rig_torso():
    return ('<g transform="translate(0 56) scale(1 1.16) translate(0 -56)">' + D2.torso() + '</g>'
            + RT.strands([(60, 70, -1, 3), (70, 72, -0.6, 3.2), (80, 74, -0.4, 3.2), (92, 76, 0.4, 3)], RT.CR, 0.6, 0.8)
            + RT.strands([(50, 37, -2, -1), (62, 35, -2, -0.8), (74, 35, -2, -0.6), (86, 34, -2, -0.4)], RT.CL, 0.4, 0.7))


D.torso = _rig_torso
_ddefs0 = D.defs
D.defs = lambda: _ddefs0() + RT.defs()

# extras in the sitting dog's frames (body = dog units, head = head-local units)
SNOW_BACK = ''.join(f'<ellipse cx="{x}" cy="{y}" rx="{r * 1.5:.1f}" ry="{r:.1f}" fill="#f4f8ff" fill-opacity="0.95"/>' for x, y, r in
                    ((46, 68, 1.6), (54, 59, 1.4), (61, 50, 1.8), (68, 41, 1.3), (76, 32, 1.5), (40, 80, 1.2)))
SNOW_HEAD = ''.join(f'<ellipse cx="{x}" cy="{y}" rx="{r * 1.5:.1f}" ry="{r:.1f}" fill="#f4f8ff"/>' for x, y, r in ((4, -15.4, 1.3), (10, -17, 1.2), (16, -15.6, 1)))
DOG_BREATH = ('<ellipse cx="44" cy="0" rx="4" ry="3" fill="#fff" fill-opacity="0.35" filter="url(#rpuff)"/>'
              '<ellipse cx="51" cy="-4" rx="6" ry="4.4" fill="#fff" fill-opacity="0.22" filter="url(#rpuff)"/>')
WET = ''.join(f'<path d="M{x} {y} l0 {l}" stroke="#eaf2ff" stroke-opacity="0.65" stroke-width="0.8" stroke-linecap="round"/>' for x, y, l in
              ((48, 66, 2.4), (57, 56, 2), (65, 46, 2.6), (73, 37, 2), (82, 30, 2.2), (116, 50, 2), (119, 64, 2.4)))


def sit(**k):
    return RT.sit(**k)


def dog_sleep(breathe=0.0, awake=False, head_up=0.0):
    """lying down, head resting on the front paws (eyes closed), or awake with the head raised."""
    o = RT.defs() + '<ellipse cx="80" cy="112.8" rx="56" ry="2.6" fill="#000" fill-opacity="0.55" filter="url(#rs)"/>'
    tail = ('<path d="M34 104 Q18 108 6 104 Q2 102.6 3 100.6 Q10 102 18 102 Q28 101.6 34 99 Z" fill="url(#rc)"/>'
            + RT.strands([(8, 105, -2.4, 1.4), (14, 106, -2, 1.6), (20, 106, -1.6, 1.6)], RT.CRL, 0.7, 0.8))
    o += tail
    o += ('<g style="filter: brightness(0.58)">' + limb([(104, 100), (124, 106), (138, 108.6)], [11, 8, 7.6], 'url(#rch)') + D2.paw((136, 110.6), 0) + '</g>')
    torso = f'M30 {93 - breathe:.1f} Q32 {75 - breathe:.1f} 54 {71 - breathe:.1f} Q80 {67 - breathe:.1f} 102 {73 - breathe:.1f} Q118 80 118 94 Q116 108 100 111.4 L44 111.6 Q30 108 30 {93 - breathe:.1f} Z'
    o += (f'<path d="{torso}" fill="url(#rc)"/>'
          f'<path d="M33 88 Q36 {76 - breathe:.1f} 54 {72 - breathe:.1f} Q78 {68 - breathe:.1f} 100 {73.6 - breathe:.1f}" ' + RT.RIM + '/>'
          + RT.strands([(60, 108, -1, 3), (72, 108.4, -0.6, 3), (84, 108.6, -0.4, 3)], RT.CR, 0.7, 0.8)
          + RT.strands([(52, 73, -2, -0.8), (66, 70, -2, -0.6), (80, 69, -2, -0.4), (92, 70, -2, -0.2)], RT.CL, 0.4, 0.7))
    o += ('<g transform="rotate(-8 48 96)"><ellipse cx="48" cy="96" rx="20" ry="13.4" fill="url(#rc)"/><ellipse cx="45" cy="91" rx="12" ry="5.6" fill="url(#rsheen)"/></g>'
          '<path d="M52 111.6 L53 106 Q64 103.6 76 104.6 Q84 106 84.6 109.4 Q84.6 112 81 112 Z" fill="url(#rcr)"/>')
    o += ('<path d="M96 78 Q112 74 122 84 Q126 94 118 100 Q106 100 98 92 Z" fill="url(#rc)"/>'
          '<path d="M112 80 Q124 86 122 98 Q116 94 112 88 Z" fill="url(#rcr)" fill-opacity="0.85"/>'
          + RT.collar(110, 86, 70))
    o += (limb([(108, 102), (128, 108), (144, 109.6)], [12, 8.6, 8], 'url(#rch)') + limb([(132, 108.6), (144, 109.8)], [8.4, 8], 'url(#rcr)')
          + D2.paw((146, 111.6), 0))
    if awake:
        o += f'<g transform="translate({117 - 3 * head_up:.1f} {90 - 10 * head_up:.1f}) rotate({10 - 22 * head_up:.1f}) scale(1.2)">{RT.head_local("closed", -0.3, False)}</g>'
    else:
        o += f'<g transform="translate(117 90) rotate(10) scale(1.2)">{RT.head_local("closed", -0.6, True)}</g>'
    return o


# ============================================================ scene composer
def scene(man, dog, dog_dx=0.0, dog_dy=0.0, dog_front=False, extra='', man_dx=0.0, dk=1.08):
    mg = f'<g transform="translate({50 + man_dx:.2f} 0) scale({K:.6f}) translate(40 26.667)">{man}</g>'
    dg = f'<g transform="translate({dog_dx:.2f} {GROUND + dog_dy:.2f}) scale({0.4 * dk:.4f}) translate(0 -112)">{dog}</g>' if dog else ''
    body = (mg + dg) if dog_front else (dg + mg)
    return body + extra


def svg(body, S=1.3, ss=2):
    x, y, w, h = VB
    W, H = round(w * S), round(h * S)
    return (f'<svg width="{W * ss}" height="{H * ss}" viewBox="{x} {y} {w} {h}" style="display:block;overflow:hidden">{R.fix(body)}</svg>', W, H)


def _unused_woof(x, y, s=1.0):
    return (f'<g transform="translate({x} {y}) scale({s})">'
            '<path d="M2 1 Q2 -1 4 -1 L40 -1 Q42 -1 42 1 L42 15 Q42 17 40 17 L14 17 L6 24 L8 17 L4 17 Q2 17 2 15 Z" fill="#faf6ec" stroke="#1e1a14" stroke-width="1.4"/>'
            '<text x="22" y="13.2" text-anchor="middle" font-family="Bebas Neue, Oswald, sans-serif" font-size="14" font-weight="700" fill="#b01c28" letter-spacing="0.6">WOOF</text></g>')
