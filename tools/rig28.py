"""v2.8 rig: the coffee guy (front view) with a real skeleton.
Arms are one continuous bending sleeve (shoulder -> elbow -> wrist) solved with IK, hands have fingers,
legs crouch with bending knees, the spine leans, shoulders rise with the arm, the head turns and blinks.
Rig units = the v2.7 front-view units (ground y = 297, centre x = 75)."""
import math, sys
sys.path.insert(0, 'tools')
import v27 as A
from dog2 import limb

O = A.O
RIM = A.RIM
JD, JC, JL = O['jacketd'], O['jacket'], O['jacketl']
SKIN, SKIN_D, SKIN_L = O['skin'], O['skin_d'], O['skin_l']


def lerp(a, b, u): return a + (b - a) * u
def lp(p, q, u): return (lerp(p[0], q[0], u), lerp(p[1], q[1], u))
def add(p, q): return (p[0] + q[0], p[1] + q[1])
def sub(p, q): return (p[0] - q[0], p[1] - q[1])
def mul(p, k): return (p[0] * k, p[1] * k)
def norm(v):
    d = math.hypot(*v) or 1.0
    return (v[0] / d, v[1] / d)
def perp(v): return (-v[1], v[0])
def ang(p, q): return math.degrees(math.atan2(q[1] - p[1], q[0] - p[0]))
def rot(p, c, deg):
    a = math.radians(deg); x, y = p[0] - c[0], p[1] - c[1]
    return (c[0] + x * math.cos(a) - y * math.sin(a), c[1] + x * math.sin(a) + y * math.cos(a))


def ik(a, c, l1, l2, bend):
    dx, dy = c[0] - a[0], c[1] - a[1]
    d = max(1e-6, min(l1 + l2 - 1e-3, math.hypot(dx, dy)))
    t = (l1 * l1 - l2 * l2 + d * d) / (2 * d)
    h = math.sqrt(max(0.0, l1 * l1 - t * t))
    ux, uy = dx / d, dy / d
    return (a[0] + ux * t - uy * h * bend, a[1] + uy * t + ux * h * bend)


def ik3(a, c, l1, l2, pole):
    """3D two-bone IK: joint between a and c (x, y, z; z toward the viewer), bending toward `pole`."""
    d = [c[i] - a[i] for i in range(3)]
    L = math.sqrt(sum(v * v for v in d)) or 1e-6
    if L > l1 + l2 - 1e-3:
        k = (l1 + l2 - 1e-3) / L; c = tuple(a[i] + d[i] * k for i in range(3)); d = [c[i] - a[i] for i in range(3)]; L = l1 + l2 - 1e-3
    u = [v / L for v in d]
    pd = sum(pole[i] * u[i] for i in range(3))
    v = [pole[i] - pd * u[i] for i in range(3)]
    vn = math.sqrt(sum(x * x for x in v)) or 1e-6
    v = [x / vn for x in v]
    t = (l1 * l1 - l2 * l2 + L * L) / (2 * L)
    h = math.sqrt(max(0.0, l1 * l1 - t * t))
    return tuple(a[i] + u[i] * t + v[i] * h for i in range(3)), c


def pts(*ps): return ' '.join(f'{p[0]:.2f} {p[1]:.2f}' for p in ps)


# ============================================================ hands
FINGERS = [(-3.5, 9.6, 4.4, 3.6, 0.92), (-1.15, 10.3, 4.9, 3.9, 1.0), (1.2, 10.1, 4.7, 3.8, 0.97), (3.4, 9.3, 3.9, 3.2, 0.85)]


def hand(wrist, deg, pose='relax', curl=None, spread=0.0, thumb=None, s=1.0, mirror=False, back=True):
    """Posable hand. Local frame: wrist at (0,0), fingers toward +y; rotated so +y follows `deg` (0 = +x).
    pose: relax | open | fist | pinch | flick | grip.  curl overrides the finger curl (0 straight .. 1 closed)."""
    c = {'relax': 0.38, 'open': 0.06, 'fist': 1.0, 'pinch': 0.55, 'flick': 0.9, 'grip': 0.75}.get(pose, 0.38) if curl is None else curl
    th = thumb if thumb is not None else {'relax': 0.2, 'open': 0.0, 'fist': 0.9, 'pinch': 0.75, 'flick': -0.6, 'grip': 0.6}.get(pose, 0.2)
    sk = 'url(#skf)'
    out = ''
    # palm (slightly wider at the knuckles)
    palm = f'M-4.6 0 Q-5.6 5 -5.0 9.6 Q0 11.4 4.8 9.4 Q5.6 5 4.6 0 Z'
    # fingers: two segments each, curling toward -x... (toward the palm side = +z, drawn as shortening + bend)
    fing = ''
    for i, (x0, y0, l1, l2, k) in enumerate(FINGERS):
        cc = min(1.0, c * (0.9 + 0.12 * i)) if pose != 'pinch' else (0.35 if i == 0 else 0.85)
        a0 = math.radians(90 + (i - 1.5) * 6 * spread)
        b1 = cc * 70; b2 = cc * 95
        p0 = (x0, y0)
        d1 = (math.cos(a0 - math.radians(b1) * 0.0), math.sin(a0))
        # bending toward the viewer is shown as foreshortening plus a slight sideways roll
        L1 = l1 * k * (1 - 0.55 * cc); L2 = l2 * k * (1 - 0.75 * cc)
        roll = math.radians(-12 * cc)
        p1 = (p0[0] + L1 * math.cos(a0 + roll), p0[1] + L1 * math.sin(a0 + roll))
        p2 = (p1[0] + L2 * math.cos(a0 + 2 * roll), p1[1] + L2 * math.sin(a0 + 2 * roll))
        w = 2.5 if i < 3 else 2.2
        fing += limb([p0, p1, p2], [w, w * 0.95, w * 0.82], sk)
        fing += f'<circle cx="{p2[0]:.2f}" cy="{p2[1]:.2f}" r="{w * 0.41:.2f}" fill="{SKIN}"/>'
        if cc < 0.7:
            fing += f'<path d="M{p1[0] - w * 0.4:.2f} {p1[1]:.2f} L{p1[0] + w * 0.4:.2f} {p1[1]:.2f}" stroke="#000" stroke-opacity="0.22" stroke-width="0.35"/>'
        else:   # curled: show the knuckle row
            fing += f'<circle cx="{p1[0]:.2f}" cy="{p1[1]:.2f}" r="{w * 0.5:.2f}" fill="{SKIN_L}" fill-opacity="0.5"/>'
    # thumb from the side of the palm
    ta = math.radians(120 - 70 * th) if th >= 0 else math.radians(120 - 70 * th)
    t0 = (-4.4, 3.2)
    t1 = (t0[0] + 4.6 * math.cos(ta), t0[1] + 4.6 * math.sin(ta))
    tb = ta - math.radians(25 * max(0, th))
    t2 = (t1[0] + 3.8 * math.cos(tb), t1[1] + 3.8 * math.sin(tb))
    thumb_s = limb([t0, t1, t2], [3.4, 2.9, 2.5], sk) + f'<circle cx="{t2[0]:.2f}" cy="{t2[1]:.2f}" r="1.1" fill="{SKIN}"/>'
    out = (thumb_s if back else '') + f'<path d="{palm}" fill="{sk}"/>' + fing + ('' if back else thumb_s)
    out += ('<path d="M-3.8 8.4 Q0 9.8 3.8 8" stroke="#000" stroke-opacity="0.18" stroke-width="0.5" fill="none"/>'
            '<path d="M-1.6 2 Q-1 5 -1.4 8 M1.4 2 Q1.8 5 1.2 8" stroke="#000" stroke-opacity="0.08" stroke-width="0.5" fill="none"/>'
            '<path d="M4.4 1 Q5.3 5 4.6 9" stroke="#fff" stroke-opacity="0.22" stroke-width="0.6" fill="none"/>')
    m = ' scale(-1 1)' if mirror else ''
    return f'<g transform="translate({wrist[0]:.2f} {wrist[1]:.2f}) rotate({deg - 90:.2f}){m} scale({s})">{out}</g>'


# ============================================================ arms
L_UP, L_FORE = 48.0, 42.0


def sleeve_arm(sh, el, wr, hand_xml='', outfit='jacket', light=-1, cuff=True, watch=False):
    """One continuous bending sleeve through shoulder, elbow, wrist with folds at the bend."""
    m1, m2 = lp(sh, el, 0.5), lp(el, wr, 0.5)
    bend = abs(((ang(sh, el) - ang(el, wr) + 180) % 360) - 180)          # 0 straight .. 180 folded
    u = min(1.0, bend / 120)
    out = ''
    if outfit == 'jacket':
        widths = [17.0, 15.6, 13.8 + 1.6 * u, 12.4, 11.0]
        out += limb([sh, m1, el, m2, wr], widths, 'url(#jf)') + limb([sh, m1, el, m2, wr], widths, 'url(#twill)')
        # shading on the side away from the light, rim on the lit side
        n1 = perp(norm(sub(el, sh))); n2 = perp(norm(sub(wr, el)))
        side = 1 if light < 0 else -1
        def off(p, n, k): return add(p, mul(n, k))
        out += (f'<path d="M{pts(off(sh, n1, side * 5.4))} Q{pts(off(el, n1, side * 4.6))} {pts(off(m2, n2, side * 3.8))} L{pts(off(wr, n2, side * 3.4))}" '
                f'stroke="#0a1a30" stroke-opacity="0.35" stroke-width="3" fill="none" stroke-linecap="round"/>')
        out += (f'<path d="M{pts(off(sh, n1, -side * 7))} Q{pts(off(el, n1, -side * 6.4))} {pts(off(m2, n2, -side * 5.4))}" ' + RIM + '/>')
        # folds: inner elbow creases (more when bent) + sleeve bunching near the cuff + armpit fold
        e_dir = norm(add(norm(sub(sh, el)), norm(sub(wr, el))))     # points into the bend
        if u > 0.12:
            for k in range(3):
                a0 = add(el, add(mul(e_dir, 3.2 + 1.7 * k), mul(perp(e_dir), -3.5 + 3.2 * k)))
                a1 = add(a0, mul(e_dir, 3.6 + 2.2 * u))
                out += f'<path d="M{pts(a0)} Q{pts(add(lp(a0, a1, 0.5), mul(perp(e_dir), 1.4)))} {pts(a1)}" stroke="#061224" stroke-opacity="{0.25 + 0.3 * u:.2f}" stroke-width="1.1" fill="none" stroke-linecap="round"/>'
        for k, uu in enumerate((0.62, 0.72)):
            c = lp(el, wr, uu); n = perp(norm(sub(wr, el)))
            out += f'<path d="M{pts(add(c, mul(n, -5)))} Q{pts(add(add(c, mul(n, 0)), mul(norm(sub(wr, el)), 1.6)))} {pts(add(c, mul(n, 5)))}" stroke="#061224" stroke-opacity="0.22" stroke-width="0.9" fill="none"/>'
        c = lp(sh, el, 0.28); n = perp(norm(sub(el, sh)))
        out += f'<path d="M{pts(add(c, mul(n, 5.5)))} Q{pts(add(c, mul(norm(sub(el, sh)), 3)))} {pts(add(c, mul(n, -1)))}" stroke="#061224" stroke-opacity="0.2" stroke-width="1" fill="none"/>'
        if cuff:
            cs = lp(el, wr, 0.86)
            out += limb([cs, wr], [11.6, 11.4], JD) + limb([cs, wr], [11.6, 11.4], 'url(#wale)')
    else:   # tee: short sleeve, bare arm with skin shading
        sl = lp(sh, el, 0.46)
        out += limb([lp(sh, el, 0.25), m1, el, m2, wr], [12.8, 12.2, 10.8 + 1.2 * u, 9.8, 8.6], 'url(#skf)')
        out += limb([sh, sl], [17.4, 16], 'url(#tee)')
        n = perp(norm(sub(el, sh)))
        out += f'<path d="M{pts(add(sl, mul(n, -7.6)))} L{pts(add(sl, mul(n, 7.6)))}" stroke="#a9a397" stroke-width="1"/>'
        if u > 0.12:
            e_dir = norm(add(norm(sub(sh, el)), norm(sub(wr, el))))
            a0 = add(el, mul(e_dir, 2.5)); a1 = add(a0, mul(e_dir, 3))
            out += f'<path d="M{pts(a0)} L{pts(a1)}" stroke="#7a5a44" stroke-opacity="0.4" stroke-width="0.8" fill="none"/>'
    if watch:
        w = lp(el, wr, 0.8)
        out += (f'<g transform="translate({w[0]:.2f} {w[1]:.2f}) rotate({ang(el, wr) + 90:.1f})">'
                '<rect x="-6.2" y="-2.2" width="12.4" height="4.4" rx="1.4" fill="#111"/>'
                '<circle r="4.4" fill="#16171b" stroke="#6b6e78" stroke-width="0.9"/><circle r="3.3" fill="#7fd0ff"/>'
                '<circle r="10" fill="url(#glowscr)" opacity="0.7"/></g>')
    return out + hand_xml


# ============================================================ legs
TH_L, SH_L = 66.0, 64.0


def legs_xml(drop=0.0, spread=0.0):
    """drop 0 = standing, 1 = deep crouch. Solved in 3D (knees come toward the viewer) and projected."""
    hy = 158 + 56 * drop
    hz = -26 * drop
    out = ''
    sides = []
    for sgn, hx, ax in ((-1, 64.0, 63.0 - 3 * spread), (1, 86.0, 87.0 + 3 * spread)):
        hip3 = (hx, hy, hz)
        ank3 = (ax, 286.0, 0.0)
        knee3, _ = ik3(hip3, ank3, TH_L, SH_L, (sgn * 0.04, 0.0, 1.0))
        sides.append((sgn, (hip3[0], hip3[1]), (knee3[0], knee3[1]), (ank3[0], ank3[1]), knee3[2]))
    for sgn, hip, knee, ank, kz in sides:
        d = max(0.0, min(1.0, (kz - 13) / 40))
        w_th = 20.5 + 3 * d
        chain = [hip, lp(hip, knee, 0.5), knee, lp(knee, ank, 0.5), ank]
        wid = [w_th, w_th - 0.8, 17.2 + 2 * d, 15.8, 14.6]
        out += limb(chain, wid, 'url(#pf)') + limb(chain, wid, 'url(#chino)')
        if d > 0.15:     # knee toward the viewer: rounded front, light on top, folds above and behind
            out += f'<ellipse cx="{knee[0]:.2f}" cy="{knee[1] - 1:.2f}" rx="{9.6 + 1.4 * d:.2f}" ry="{8.2 + 1.4 * d:.2f}" fill="url(#pf)"/>'
            out += f'<ellipse cx="{knee[0] + 0.6:.2f}" cy="{knee[1] - 3.4:.2f}" rx="{6.4:.2f}" ry="{3.8:.2f}" fill="{O["denim_l"]}" fill-opacity="{0.55 * d:.2f}"/>'
            out += f'<ellipse cx="{knee[0]:.2f}" cy="{knee[1] - 1:.2f}" rx="{9.6 + 1.4 * d:.2f}" ry="{8.2 + 1.4 * d:.2f}" fill="url(#chino)"/>'
            for k in range(3):
                y0 = knee[1] + 7 + 2.4 * k
                out += f'<path d="M{knee[0] - 6.5:.2f} {y0:.2f} Q{knee[0]:.2f} {y0 + 2.2:.2f} {knee[0] + 6.5:.2f} {y0:.2f}" stroke="#000" stroke-opacity="{0.12 + 0.15 * d:.2f}" stroke-width="0.9" fill="none"/>'
            out += (f'<path d="M{knee[0] - 8:.2f} {knee[1] - 6:.2f} Q{knee[0]:.2f} {knee[1] - 11:.2f} {knee[0] + 8:.2f} {knee[1] - 6:.2f}" '
                    f'stroke="#000" stroke-opacity="{0.2 * d:.2f}" stroke-width="1" fill="none"/>')
        else:
            out += f'<path d="M{knee[0] - 5:.2f} {knee[1]:.2f} Q{knee[0]:.2f} {knee[1] + 2.4:.2f} {knee[0] + 5:.2f} {knee[1]:.2f}" stroke="#000" stroke-opacity="0.18" stroke-width="1" fill="none"/>'
        out += (f'<path d="M{ank[0] - 7.3:.2f} 270 Q{ank[0]:.2f} 274 {ank[0] + 7.3:.2f} 270 M{ank[0] - 7.3:.2f} 276 Q{ank[0]:.2f} 279 {ank[0] + 7.3:.2f} 276" '
                'stroke="#000" stroke-opacity="0.22" stroke-width="1" fill="none"/>')
        if sgn < 0:
            out += f'<path d="M{hip[0] - 9:.2f} {hip[1] + 4:.2f} Q{knee[0] - 9:.2f} {lerp(hip[1], knee[1], 0.5):.2f} {knee[0] - 8:.2f} {knee[1]:.2f}" ' + RIM + '/>'
    # crotch shadow
    out += f'<path d="M73.5 {hy:.2f} L75 {hy + 30 - 14 * drop:.2f} L76.5 {hy:.2f} Z" fill="#000" fill-opacity="0.45"/>'
    boots = ''.join(
        f'<path d="M{x0} 279 L{x0 + 17} 279 L{x0 + 18.5} 290 Q{x0 + 19} 297.5 {x0 + 13} 297.5 L{x0 + 3} 297.5 Q{x0 - 2} 297.5 {x0 - 1} 290 Z" fill="url(#bt2)"/>'
        f'<path d="M{x0 - 1.4} 294 L{x0 + 19} 294 L{x0 + 18.5} 297.5 L{x0 - 1} 297.5 Z" fill="#1a120c"/>'
        f'<path d="M{x0 - 1} 293.4 L{x0 + 18.6} 293.4" stroke="#d9b98a" stroke-opacity="0.5" stroke-width="0.5" stroke-dasharray="1 0.8"/>'
        f'<path d="M{x0 + 4} 280 L{x0 + 13} 280 L{x0 + 12} 291 L{x0 + 5} 291 Z" fill="#2a180c" fill-opacity="0.8"/>'
        + ''.join(f'<path d="M{x0 + 5} {281.5 + 2.4 * i} L{x0 + 12} {282.6 + 2.4 * i}" stroke="#e2c9a0" stroke-width="0.7"/>' for i in range(4))
        + f'<path d="M{x0 + 13} 289 Q{x0 + 16} 292 {x0 + 15} 295" stroke="#fff" stroke-opacity="0.25" stroke-width="1" fill="none"/>'
        + (f'<path d="M{x0 + 1} 280 Q{x0 + 8.5} {283 + 2 * spread} {x0 + 16} 280" stroke="#000" stroke-opacity="0.3" stroke-width="1.2" fill="none"/>')
        for x0 in (54 - 3 * spread, 78 + 3 * spread))
    return boots + out, hy


# ============================================================ the man
def man(p):
    """p: dict of pose parameters (see DEFAULT)."""
    q = dict(DEFAULT); q.update(p)
    drop, lean = q['drop'], q['lean']
    legs, hy = legs_xml(drop, q['spread'])
    pelvis = (75.0, hy)
    dy = hy - 158
    br = q['breathe']

    def body(pt):   # body frame (standing coords) -> world
        x, y = pt[0], pt[1] + dy
        return rot((x, y), pelvis, lean)

    # shoulders: rise when the arm lifts
    def shoulder(base, target):
        s = body(base)
        el = max(0.0, (s[1] - target[1]) / 60.0) if target else 0.0
        return (s[0], s[1] - 3.6 * min(1.0, el) - 0.5 * br)

    # ---- torso (in body frame, then transformed)
    torso_g = (f'<g transform="rotate({lean:.2f} 75 {hy:.2f}) translate(0 {dy:.2f})">'
               f'<g transform="translate(0 {158 - 158 * (1 + 0.012 * br):.2f}) scale(1 {1 + 0.012 * br:.4f})">'
               + TORSO[q['outfit']] + (SCARF if q['scarf'] else '') + (WET if q.get('wet') else '') + (SNOW_BODY if q.get('snow') else '') + '</g></g>')
    # ---- head (neck pivot), turn shifts the features
    neck_w = body((74, 58))
    tilt = q['tilt'] + lean * 0.6
    head = head_xml(q) + (SHADES if q.get('shades') else '') + (SNOW_HEAD if q.get('snow') else '') + (HEAD_WET if q.get('wet') else '')
    head_g = (f'<g transform="translate({neck_w[0] - 74:.2f} {neck_w[1] - 58:.2f}) rotate({tilt:.2f} 74 52)">' + head + '</g>')
    neck_g = f'<g transform="translate({neck_w[0] - 74:.2f} {neck_w[1] - 58:.2f}) rotate({tilt * 0.4:.2f} 74 58)">' + NECK + '</g>'

    # ---- arms (world space IK)
    arms_back, arms_front = '', ''
    for side in ('L', 'R'):
        spec = q[side]
        base = (44.0, 66.0) if side == 'L' else (106.0, 66.0)
        kind = spec.get('kind', 'hang')
        if kind == 'hang':
            sh = shoulder(base, None)
            sw = spec.get('swing', 0.0)
            el = rot(add(sh, (-2 if side == 'L' else 2, 47)), sh, sw + (3 if side == 'L' else -3))
            wr = rot(add(el, (1 if side == 'L' else -1, 40)), el, sw * 1.4 + spec.get('fore', 0.0))
            hx = hand(wr, ang(el, wr) + spec.get('wbend', 0), spec.get('hand', 'relax'), spec.get('curl'), mirror=(side == 'R'))
            xml = sleeve_arm(sh, el, wr, hx, q['outfit'])
            if spec.get('front', True): arms_front += xml
            else: arms_back += xml
            continue
        tgt = spec['wrist']
        tz = spec.get('z', 0.0)
        sh = shoulder(base, tgt)
        sx = -1 if side == 'L' else 1
        pole = spec.get('pole', (sx * 0.55, 0.45, -0.7))
        el3, wr3 = ik3((sh[0], sh[1], 0.0), (tgt[0], tgt[1], tz), L_UP, L_FORE, pole)
        el, wr = (el3[0], el3[1]), (wr3[0], wr3[1])
        if kind == 'cup':
            hx = A.cup_group(spec.get('cup', 'cup'), spec.get('steam', 0.8), wr, spec.get('cup_rot', 0.0))
            xml = sleeve_arm(sh, el, wr, '', q['outfit'], cuff=True)
            xml += hx
        else:
            fs = max(0.6, min(1.0, math.hypot(wr[0] - el[0], wr[1] - el[1]) / L_FORE + 0.25))
            if spec.get('hand') == 'hidden':
                hx = f'<path d="M{wr[0] - 6:.1f} {wr[1] + 1:.1f} Q{wr[0]:.1f} {wr[1] - 3:.1f} {wr[0] + 6:.1f} {wr[1] + 1:.1f}" stroke="#000" stroke-opacity="0.45" stroke-width="1.2" fill="none"/>'
            else:
                hx = hand(wr, ang(el, wr) + spec.get('wbend', 0), spec.get('hand', 'relax'), spec.get('curl'), spec.get('spread', 0.0),
                          spec.get('thumb'), s=fs, mirror=(side == 'R'), back=spec.get('back', True))
            xml = sleeve_arm(sh, el, wr, hx, q['outfit'], watch=spec.get('watch', False))
        if spec.get('front', True):
            arms_front += xml
        else:
            arms_back += xml
    props = q.get('props', '')
    tied = f'<g transform="translate(0 {dy:.2f})">{TIED}</g>' if q['outfit'] == 'tee' else ''
    return (A.mdefs() + f'<ellipse cx="75" cy="298" rx="{34 + 8 * drop:.1f}" ry="3.4" fill="#000" fill-opacity="0.5" filter="url(#soft1)"/>'
            + tied + legs + (SNOW_FEET if q.get('snow') else '') + arms_back + torso_g + neck_g + head_g + q.get('props_back', '') + arms_front + props)


DEFAULT = dict(outfit='jacket', drop=0.0, spread=0.0, lean=0.0, breathe=0.0, tilt=0.0, turn=0.0, look=(0.0, 0.0), blink=0.0,
               smile=0.4, brows=0.0, mouth=0.0, scarf=False, hat='beanie',
               L=dict(kind='hang'), R=dict(kind='cup', wrist=(98.0, 118.0), z=34.0))

# --------------------------------------------------------------- torso / neck / head art (from v2.7, body frame)
_src = A.front2()
TORSO = {
    'jacket': ('<path d="M61 58 Q75 66 89 58 L91 160 L59 160 Z" fill="url(#tee)"/>'
               '<path d="M64 58 Q75 64 86 58" stroke="#b8b2a6" stroke-width="1.4" fill="none"/>'
               '<path d="M66 120 Q75 124 84 120 M68 96 Q75 99 82 96" stroke="#000" stroke-opacity="0.1" stroke-width="1.4" fill="none"/>'
               '<path d="M44 66 Q50 58 62 57 L66 64 L65 104 L64 168 L48 168 Q45 120 44 66 Z" fill="url(#jf)"/>'
               '<path d="M106 66 Q100 58 88 57 L84 64 L85 104 L86 168 L102 168 Q105 120 106 66 Z" fill="url(#jf)"/>'
               '<path d="M44 66 Q50 58 62 57 L66 64 L65 104 L64 168 L48 168 Q45 120 44 66 Z M106 66 Q100 58 88 57 L84 64 L85 104 L86 168 L102 168 Q105 120 106 66 Z" fill="url(#twill)"/>'
               '<path d="M47 160 L64 160 L64 168 L48 168 Z M86 160 L102.5 160 L102 168 L86 168 Z" fill="' + JD + '"/>'
               '<path d="M48 162 L64 162 M48 165 L64 165 M86 162 L102 162 M86 165 L102 165" stroke="#000" stroke-opacity="0.25" stroke-width="0.6"/>'
               '<circle cx="60" cy="164" r="1" fill="#d9c08a"/><circle cx="90" cy="164" r="1" fill="#d9c08a"/>'
               '<path d="M62 57 L54 60 L59 82 L66 65 Z" fill="url(#cord)"/><path d="M62 57 L54 60 L59 82 L66 65 Z" fill="url(#wale)"/>'
               '<path d="M88 57 L96 60 L91 82 L84 65 Z" fill="url(#cord)"/><path d="M88 57 L96 60 L91 82 L84 65 Z" fill="url(#wale)"/>'
               '<path d="M54 60 L59 82 M96 60 L91 82" stroke="#d8b080" stroke-opacity="0.35" stroke-width="0.6"/>'
               '<path d="M45 76 Q54 73 64.6 75 M105 76 Q96 73 85.4 75" stroke="#c9a46a" stroke-opacity="0.6" stroke-width="0.7" stroke-dasharray="1.4 1" fill="none"/>'
               '<path d="M50 84 L61 84 L61 97 L50 97 Z M89 84 L100 84 L100 97 L89 97 Z" fill="#000" fill-opacity="0.14" stroke="#c9a46a" stroke-opacity="0.75" stroke-width="0.7" stroke-dasharray="1.4 1"/>'
               '<path d="M50 84 L61 84 L60 89 L55.5 91 L51 89 Z M89 84 L100 84 L99 89 L94.5 91 L90 89 Z" fill="' + JD + '" fill-opacity="0.85"/>'
               '<circle cx="55.5" cy="88.6" r="0.95" fill="#d9c08a"/><circle cx="94.5" cy="88.6" r="0.95" fill="#d9c08a"/>'
               '<path d="M49 108 L49.6 150 M101 108 L100.4 150" stroke="#c9a46a" stroke-opacity="0.45" stroke-width="0.7" stroke-dasharray="1.4 1"/>'
               '<path d="M64.5 66 L63.5 166 M85.5 66 L86.5 166" stroke="#c9a46a" stroke-opacity="0.7" stroke-width="0.7" stroke-dasharray="1.4 1" fill="none"/>'
               '<circle cx="64.6" cy="110" r="0.9" fill="#d9c08a"/><circle cx="64.4" cy="134" r="0.9" fill="#d9c08a"/>'
               '<path d="M52 128 Q56 132 61 129 M90 132 Q94 136 99 133 M54 112 Q57 116 61 114 M90 116 Q93 119 97 117" stroke="#000" stroke-opacity="0.2" stroke-width="1.2" fill="none"/>'
               '<path d="M45 70 Q44 120 48 166" ' + RIM + '/>'
               '<path d="M102 72 Q104 120 101 160" stroke="#fff" stroke-opacity="0.15" stroke-width="2" fill="none"/>'),
}
TORSO['tee'] = ('<path d="M46 66 Q50 58 62 57 Q75 65 88 57 Q100 58 104 66 L102 160 L48 160 Z" fill="url(#tee)"/>'
                '<path d="M62 57 Q75 66 88 57" stroke="#b8b2a6" stroke-width="1.6" fill="none"/>'
                '<path d="M56 90 Q60 100 58 112 M92 92 Q90 102 93 112 M64 132 Q75 136 86 132" stroke="#000" stroke-opacity="0.13" stroke-width="1.4" fill="none"/>'
                '<path d="M49 70 Q47 120 49 158" ' + RIM + '/>'
                '<path d="M46 150 Q75 160 104 150 L104 162 Q75 170 46 162 Z" fill="url(#jf)"/><path d="M46 150 Q75 160 104 150 L104 162 Q75 170 46 162 Z" fill="url(#twill)"/>'
                '<path d="M46 150 Q75 160 104 150" stroke="#000" stroke-opacity="0.25" stroke-width="1" fill="none"/>'
                '<path d="M68 156 Q75 152 82 156 Q84 164 77 168 Q70 167 68 156 Z" fill="' + JC + '"/>'
                '<path d="M70 164 Q66 182 69 200 L76 199 Q75 182 77 166 Z" fill="url(#jf)"/>'
                '<path d="M78 164 Q84 180 82 194 L88 193 Q89 178 82 163 Z" fill="url(#jf)"/>'
                '<path d="M69 196 L76 195.4 L76 200 L69 200.6 Z M82 190.6 L88 190 L88 194 L82 194.6 Z" fill="' + JD + '"/>'
                '<path d="M71 160 Q75 158 80 160" stroke="#000" stroke-opacity="0.3" stroke-width="0.9" fill="none"/>')
TIED = ('<path d="M45 150 Q75 146 105 150 L108 212 Q96 216 92 206 L58 206 Q54 216 42 212 Z" fill="url(#jf)"/>'
        '<path d="M45 150 Q75 146 105 150 L108 212 Q96 216 92 206 L58 206 Q54 216 42 212 Z" fill="url(#twill)"/>'
        '<path d="M44 196 Q48 206 42 212 M106 196 Q102 206 108 212" stroke="#c9a46a" stroke-opacity="0.5" stroke-width="0.7" stroke-dasharray="1.4 1" fill="none"/>')
SCARF = ('<path d="M60 50 Q74 44 89 50 Q92 56 89 62 Q74 68 60 62 Q57 56 60 50 Z" fill="url(#scarf)"/>'
         '<path d="M60 50 Q74 44 89 50 Q92 56 89 62 Q74 68 60 62 Q57 56 60 50 Z" fill="url(#knit)"/>'
         '<path d="M61 55 Q74 51 88 55" stroke="#000" stroke-opacity="0.25" stroke-width="1" fill="none"/>'
         '<path d="M64 60 Q61 84 63 108 L73 108 Q72 84 73 62 Z" fill="url(#scarf)"/><path d="M64 60 Q61 84 63 108 L73 108 Q72 84 73 62 Z" fill="url(#knit)"/>'
         '<path d="M70 62 Q75 80 78 96 L86 93 Q82 78 78 61 Z" fill="#7a1620"/><path d="M70 62 Q75 80 78 96 L86 93 Q82 78 78 61 Z" fill="url(#knit)"/>'
         + ''.join(f'<path d="M{x} 108 L{x - 0.3} 112.4" stroke="#9a1f2a" stroke-width="1.2" stroke-linecap="round"/>' for x in (64, 66.2, 68.4, 70.6, 72.8))
         + ''.join(f'<path d="M{x} {y} L{x + 0.6} {y + 4.2}" stroke="#7a1620" stroke-width="1.1" stroke-linecap="round"/>' for x, y in ((78.4, 95.8), (80.6, 95), (82.8, 94.2), (85, 93.4)))
         + '<path d="M64 64 L72 64 M63.6 76 L72.4 76 M63.4 88 L72.4 88 M63.2 100 L72.6 100" stroke="#e8c070" stroke-opacity="0.5" stroke-width="1.2"/>'
         '<path d="M59.6 52 Q58.4 57 60 61" ' + RIM + '/>')
WET = ('<path d="M44 66 Q50 58 62 57 L66 64 L65 104 L64 168 L48 168 Q45 120 44 66 Z M106 66 Q100 58 88 57 L84 64 L85 104 L86 168 L102 168 Q105 120 106 66 Z" fill="#0a1424" fill-opacity="0.22"/>'
       + ''.join(f'<path d="M{x} {y} l0 {l}" stroke="#dfe8ff" stroke-opacity="0.55" stroke-width="0.9" stroke-linecap="round"/>' for x, y, l in
                 ((99, 70, 3), (104, 84, 2.6), (102, 100, 3), (93, 76, 2), (88, 112, 2.4), (100, 128, 2.2))))
SNOW_BODY = ''.join(f'<ellipse cx="{x}" cy="{y}" rx="{r * 1.4:.1f}" ry="{r:.1f}" fill="#f4f8ff" fill-opacity="0.9"/>' for x, y, r in ((48, 64, 1.6), (54, 60, 1.2), (98, 62, 1.5), (104, 66, 1.2)))
SNOW_FEET = ''.join(f'<ellipse cx="{x}" cy="{y}" rx="{r * 1.4:.1f}" ry="{r:.1f}" fill="#f4f8ff" fill-opacity="0.9"/>' for x, y, r in ((57, 296, 2), (66, 297, 1.5), (82, 296.4, 2), (92, 297, 1.4)))
SNOW_HEAD = ''.join(f'<ellipse cx="{x}" cy="{y}" rx="{r * 1.5:.1f}" ry="{r:.1f}" fill="#f4f8ff"/>' for x, y, r in ((66, 3, 1.6), (73, 1, 2), (81, 2.4, 1.6), (77, 0.4, 1.2), (61, 9, 1.2), (87, 9, 1.1)))
SHADES = ('<path d="M63.4 25.4 L72 25.4 L71.4 30.4 Q67.6 32.4 64.2 30.4 Z M76 25.4 L84.6 25.4 L83.8 30.4 Q80.4 32.4 76.6 30.4 Z" fill="url(#lens)" stroke="#0a0a0c" stroke-width="0.8"/>'
          '<path d="M72 26.4 Q74 25.4 76 26.4" stroke="#0a0a0c" stroke-width="1" fill="none"/>'
          '<path d="M63.4 25.8 L60.6 27 M84.6 25.8 L87.6 27" stroke="#0a0a0c" stroke-width="0.9"/>'
          '<path d="M65 26.4 L67.8 26.4 M77.6 26.4 L80.4 26.4" stroke="#ffffff" stroke-opacity="0.45" stroke-width="0.8"/>')
HEAD_WET = ''.join(f'<path d="M{x} {y} l0 {l}" stroke="#dfe8ff" stroke-opacity="0.55" stroke-width="0.9" stroke-linecap="round"/>' for x, y, l in ((60, 2, 2), (82, 4, 2.2), (70, 6, 1.6)))


NECK = ('<path d="M67 42 L81 42 L81.5 60 L66.5 60 Z" fill="url(#skf)"/>'
        '<path d="M67 46 Q74 52 81 46 L81.5 52 Q74 56 67 52 Z" fill="#000" fill-opacity="0.22"/>'
        '<path d="M71 52 Q74 55 77 52" stroke="#000" stroke-opacity="0.15" stroke-width="0.8" fill="none"/>')
A_SCARF = ''


def head_xml(q):
    turn, (lx, ly), blink, smile, brows = q['turn'], q['look'], q['blink'], q['smile'], q['brows']
    fx = 2.6 * turn                  # features shift when the head turns
    lids = max(q.get('lids', 0.0), blink)
    eyes = ('<path d="M65.5 28 Q68 26.4 70.5 28 Q68 29.6 65.5 28 Z M77.5 28 Q80 26.4 82.5 28 Q80 29.6 77.5 28 Z" fill="#f1ebe3"/>'
            f'<g transform="translate({lx:.2f} {ly:.2f})">'
            '<circle cx="68.2" cy="28" r="1.25" fill="#4a3424"/><circle cx="80.2" cy="28" r="1.25" fill="#4a3424"/>'
            '<circle cx="68.2" cy="28" r="0.6" fill="#0d0907"/><circle cx="80.2" cy="28" r="0.6" fill="#0d0907"/>'
            '<circle cx="68.7" cy="27.5" r="0.4" fill="#fff" fill-opacity="0.85"/><circle cx="80.7" cy="27.5" r="0.4" fill="#fff" fill-opacity="0.85"/></g>')
    if lids > 0.02:
        ly2 = 26.2 + 3.4 * lids
        eyes += (f'<path d="M64.8 28.4 Q68 25.2 71.2 28.4 L71.2 {ly2 - 0.2:.2f} Q68 {ly2 - 2.6 + 3.4 * lids:.2f} 64.8 {ly2 - 0.2:.2f} Z '
                 f'M76.8 28.4 Q80 25.2 83.2 28.4 L83.2 {ly2 - 0.2:.2f} Q80 {ly2 - 2.6 + 3.4 * lids:.2f} 76.8 {ly2 - 0.2:.2f} Z" fill="url(#skf)"/>')
    lash_y = 27.9 + 1.6 * lids
    eyes += (f'<path d="M65.2 {lash_y:.2f} Q68 {26.0 + 3.4 * lids:.2f} 70.8 {lash_y:.2f} M77.2 {lash_y:.2f} Q80 {26.0 + 3.4 * lids:.2f} 82.8 {lash_y:.2f}" '
             'stroke="#1a110c" stroke-width="0.85" fill="none"/>')
    by = -brows
    mo = q['mouth']
    mouth = (f'<path d="M70.4 {41.4 - 0.4 * smile:.2f} Q74 {42.8 + 1.2 * smile:.2f} 77.8 {41.4 - 0.4 * smile:.2f}" stroke="#7a4a3c" stroke-width="1.1" fill="none" stroke-linecap="round"/>'
             if mo < 0.1 else
             f'<path d="M70.8 41.2 Q74 {41.2 + 4 * mo:.2f} 77.4 41.2 Q74 40.4 70.8 41.2 Z" fill="#4a1e1a"/>')
    feats = (eyes
             + f'<path d="M64.5 {24.6 + by:.2f} Q68 {23 + by:.2f} 71.5 {24.4 + by:.2f} M76.5 {24.4 + by:.2f} Q80 {23 + by:.2f} 83.5 {24.6 + by:.2f}" stroke="#5a3d22" stroke-width="1.4" fill="none" stroke-linecap="round"/>'
             '<path d="M74.5 29 L75.6 36" stroke="#000" stroke-opacity="0.2" stroke-width="1.2"/>'
             '<path d="M72 37.4 Q74 38.8 76.5 37.4" stroke="#000" stroke-opacity="0.35" stroke-width="0.9" fill="none"/>'
             '<path d="M76.2 30 Q77 34 76.4 36.4" stroke="#fff" stroke-opacity="0.2" stroke-width="0.7" fill="none"/>'
             + mouth +
             '<path d="M71.6 43.6 Q74 44.4 76.4 43.6" stroke="#000" stroke-opacity="0.12" stroke-width="0.8" fill="none"/>'
             '<ellipse cx="65" cy="35" rx="3.4" ry="2.4" fill="url(#cheek)"/><ellipse cx="83" cy="35" rx="3.4" ry="2.4" fill="url(#cheek)"/>')
    ear_l = f'<ellipse cx="{60 + 0.8 * max(0, turn):.2f}" cy="30" rx="{2.8 * (1 - 0.5 * max(0, turn)):.2f}" ry="5.2" fill="url(#skf)"/>'
    ear_r = f'<ellipse cx="{88.4 + 0.8 * min(0, turn):.2f}" cy="30" rx="{2.8 * (1 + 0.5 * min(0, turn)):.2f}" ry="5.2" fill="url(#skf)"/>'
    h = (ear_l + ear_r
         + '<path d="M60.5 22 Q60.5 9 74 9 Q87.5 9 87.5 22 L87.5 33 Q86.5 43.5 80 47.5 Q74 50.5 68 47.5 Q61.5 43.5 60.5 33 Z" fill="url(#skf)"/>'
         '<path d="M61 34 Q63 44 68 47.5 Q74 50.5 80 47.5 Q76 48 74 47 Q66 44 61 34 Z" fill="#000" fill-opacity="0.18"/>'
         '<path d="M63 38 Q66 47 74 48.5 Q82 47 85 38 Q83 45 74 46 Q65 45 63 38 Z" fill="#6b4a2a" fill-opacity="0.28"/>'
         f'<g transform="translate({fx:.2f} 0)">{feats}</g>'
         '<path d="M61 22 Q60.5 30 62 38" ' + RIM + '/>'
         '<path d="M60.6 24 Q61 29 62 32 L63.4 31 Q62.6 27 62.8 24 Z M87.4 24 Q87 29 86 32 L84.6 31 Q85.4 27 85.2 24 Z" fill="#5a3a22"/>')
    if q['hat'] == 'santa':
        h += A.SANTA
    else:
        h += ('<path d="M59 24 Q58 1 74 0.5 Q90 1 89.5 24 Z" fill="url(#hatf)"/><path d="M59 24 Q58 1 74 0.5 Q90 1 89.5 24 Z" fill="url(#knit)"/>'
              '<path d="M58.4 17.5 Q74 15 90 17.5 L90 25.5 Q74 23.5 58.4 25.5 Z" fill="url(#hatf)"/>'
              '<path d="M58.4 17.5 Q74 15 90 17.5" stroke="#000" stroke-opacity="0.3" stroke-width="1" fill="none"/>'
              '<path d="M58.4 25.5 Q74 23.5 90 25.5" stroke="#000" stroke-opacity="0.25" stroke-width="0.8" fill="none"/>'
              + ''.join(f'<path d="M{x} 18 L{x} 25" stroke="#000" stroke-opacity="0.2" stroke-width="0.8"/>' for x in [round(59.6 + i * 1.9, 1) for i in range(16)])
              + '<path d="M62 8 Q72 3 84 7" stroke="#fff" stroke-opacity="0.2" stroke-width="1.6" fill="none"/>'
              '<path d="M59.6 22 Q58.6 10 64 4" ' + RIM + '/>')
    return h


# ============================================================ keyframe animation
def ease(kind, u):
    u = max(0.0, min(1.0, u))
    if kind == 'lin': return u
    if kind == 'in': return u * u * u
    if kind == 'out': return 1 - (1 - u) ** 3
    if kind == 'back':           # ease out with a small overshoot (follow-through)
        c = 1.6; return 1 + (c + 1) * (u - 1) ** 3 + c * (u - 1) ** 2
    if kind == 'step': return 0.0 if u < 1 else 1.0
    return u * u * (3 - 2 * u) if kind == 'io2' else (4 * u ** 3 if u < 0.5 else 1 - (-2 * u + 2) ** 3 / 2)


class Track:
    def __init__(self, keys):
        self.k = sorted(keys, key=lambda x: x[0])

    def __call__(self, t):
        k = self.k
        if t <= k[0][0]: return k[0][1]
        for (t0, v0, *_), (t1, v1, *e) in zip(k, k[1:]):
            if t <= t1:
                u = ease(e[0] if e else 'io', (t - t0) / (t1 - t0))
                if isinstance(v0, tuple):
                    return tuple(a + (b - a) * u for a, b in zip(v0, v1))
                return v0 + (v1 - v0) * u
        return k[-1][1]


def spring(signal, t, dt=1 / 24, k=0.55, lag=2):
    """follow-through: the value of a signal a little in the past, overshooting a bit."""
    a = signal(t - lag * dt); b = signal(t - 2 * lag * dt)
    return a + (a - b) * k
