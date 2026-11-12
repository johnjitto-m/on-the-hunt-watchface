"""Rigged realistic dog (golden short coat, red collar). One skeleton for standing, trotting and sitting,
so poses blend smoothly. Body pitches around the hip; head has its own world angle (look up / down).
Units: dog space x 0..150, ground y=112. Render box viewBox '0 -50 150 165' -> 60 x 66 px (ground at 64.8 px)."""
import math, sys
sys.path.insert(0, 'tools')
import dog2 as D2
import render_v2 as R

D2.set_palette('golden')
VB, BW, BH, GROUND_PX = '0 -50 150 165', 60, 66, 64.8
H0, S0, N0, T0 = (44, 54), (99, 58), (104, 40), (34, 45)
G = 112


def lerp(a, b, u): return a + (b - a) * u
def lerpp(p, q, u): return (lerp(p[0], q[0], u), lerp(p[1], q[1], u))
def ease(u): u = max(0.0, min(1.0, u)); return u * u * (3 - 2 * u)
rp = D2.rp


def world(p, theta, hip):
    q = rp(p, H0, theta)
    return (q[0] + hip[0] - H0[0], q[1] + hip[1] - H0[1])


def ik2(a, c, l1, l2, bend=1):
    """two-bone IK: joint between a and c with segment lengths l1, l2; bend sign picks the side."""
    dx, dy = c[0] - a[0], c[1] - a[1]
    d = max(1e-6, min(l1 + l2 - 1e-3, math.hypot(dx, dy)))
    t = (l1 * l1 - l2 * l2 + d * d) / (2 * d)
    h = math.sqrt(max(0.0, l1 * l1 - t * t))
    ux, uy = dx / d, dy / d
    return (a[0] + ux * t - uy * h * bend, a[1] + uy * t + ux * h * bend)


FUR = ('<pattern id="fur" width="5" height="4" patternUnits="userSpaceOnUse" patternTransform="rotate(-12)">'
       '<path d="M0.5 3 Q1.6 1.6 3 1.2 M2.6 3.6 Q3.8 2.4 4.8 2.2" stroke="#fff3d6" stroke-opacity="0.14" stroke-width="0.5" fill="none"/>'
       '<path d="M1.4 3.8 Q2.4 2.8 3.6 2.6" stroke="#5a3814" stroke-opacity="0.12" stroke-width="0.5" fill="none"/></pattern>')


def defs():
    return D2.DEFS.replace('</defs>', FUR + '</defs>')


TORSO_PATH = ('M33 47 Q33 38 46 37 Q66 37.5 86 36 Q97 34.5 104 41 Q112 49 112.5 60 Q112 71 104 76.5 Q97 79 90 77 '
              'Q80 73.5 70 71.5 Q60 70.5 54 67 Q45 66.5 38 62 Q32 56 33 47 Z')


def torso():
    return D2.torso() + f'<path d="{TORSO_PATH}" fill="url(#fur)"/>'


def head(mouth=False, ears=0.0, eyes_closed=False):
    h = D2.head(mouth, ears, 0)
    # detail: whiskers, wet eye highlight, nose texture, fur on the neck
    extra = ('<path d="M100 44 Q97 30 103 20 Q107 14 114 11 L121 22 Q117 34 111 46 Z" fill="url(#fur)"/>'
             '<path d="M134 21.5 Q140 21 145 19.5 M134 22.6 Q140 23.4 145 23.8 M133 23.6 Q138 25.6 142.6 27.4" stroke="#fff6e0" stroke-opacity="0.55" stroke-width="0.35" fill="none"/>'
             '<circle cx="139.4" cy="16.4" r="0.35" fill="#fff" fill-opacity="0.6"/><circle cx="141.2" cy="17.4" r="0.3" fill="#fff" fill-opacity="0.5"/>')
    if eyes_closed:
        extra += ('<path d="M121.4 11.4 Q124.4 9.4 127.3 11.6 Q124.3 13.6 121.4 11.4 Z" fill="url(#gc)"/>'
                  '<path d="M121.6 11.8 Q124.4 13 127 11.8" stroke="#1a0f08" stroke-width="0.8" fill="none"/>')
    return h + extra


def paw_fix(p): return D2.paw(p, 0)


def pose(theta=0.0, hip=None, head_a=0.0, tail_a=0.0, fl=None, ff=None, hl=None, hf=None, mouth=False, ears=0.0,
         eyes_closed=False, x=0.0, sit=0.0, bob=0.0):
    """theta: body pitch (deg, - = front up); head_a: head world angle (- = nose up);
    fl/ff/hl/hf: (swing, flex) for near/far front and near/far hind legs (standing kinematics);
    sit: 0..1 blends legs toward the sitting placement."""
    hip = hip or H0
    hip = (hip[0], hip[1] + bob)
    fl, ff, hl, hf = fl or (0, 0), ff or (0, 0), hl or (0, 0), hf or (0, 0)
    sh = world(S0, theta, hip)

    def front_pts(sw, flex, far):
        stand = D2.front_leg(sw, flex, shoulder=sh)
        paw = (sh[0] + 3, G - 1.5)
        carpus = (paw[0] - 2, paw[1] - 9.5)
        elbow = ik2(sh, carpus, 19, 27, bend=-1)
        sitp = [sh, elbow, carpus, paw]
        return [lerpp(a, b, sit) for a, b in zip(stand, sitp)]

    def hind_pts(sw, flex, far):
        stand = D2.hind_leg(sw, flex, hip=hip)
        st = (hip[0] + 19, G - 9); hk = (hip[0] - 3, G - 3); pw = (hip[0] + 20, G - 1.5)
        sitp = [hip, st, hk, pw]
        return [lerpp(a, b, sit) for a, b in zip(stand, sitp)]

    T = f'translate({hip[0] - H0[0]:.2f} {hip[1] - H0[1]:.2f}) rotate({theta:.2f} {H0[0]} {H0[1]})'
    body = f'<g transform="{T}">' + torso() + '</g>'
    phi = head_a - theta
    hd = f'<g transform="{T}"><g transform="rotate({phi:.2f} {N0[0]} {N0[1]})">' + D2.collar() + head(mouth, ears, eyes_closed) + '</g></g>'
    tl = f'<g transform="{T}">' + D2.tail(tail_a) + '</g>'
    haunch = ''
    if sit > 0.4:
        a = min(1, (sit - 0.4) / 0.6)
        haunch = (f'<g opacity="{a:.2f}"><path d="M{hip[0] - 16:.1f} {G - 12:.1f} Q{hip[0] - 18:.1f} {hip[1] - 14:.1f} {hip[0] + 2:.1f} {hip[1] - 18:.1f} '
                  f'Q{hip[0] + 22:.1f} {hip[1] - 14:.1f} {hip[0] + 26:.1f} {G - 10:.1f} Q{hip[0] + 24:.1f} {G - 0.5:.1f} {hip[0] + 10:.1f} {G - 0.4:.1f} '
                  f'L{hip[0] - 10:.1f} {G - 0.4:.1f} Q{hip[0] - 18:.1f} {G - 3:.1f} {hip[0] - 16:.1f} {G - 12:.1f} Z" fill="url(#gc)"/>'
                  f'<path d="M{hip[0] - 16:.1f} {G - 12:.1f} Q{hip[0] - 18:.1f} {hip[1] - 14:.1f} {hip[0] + 2:.1f} {hip[1] - 18:.1f} '
                  f'Q{hip[0] + 22:.1f} {hip[1] - 14:.1f} {hip[0] + 26:.1f} {G - 10:.1f} Q{hip[0] + 24:.1f} {G - 0.5:.1f} {hip[0] + 10:.1f} {G - 0.4:.1f} '
                  f'L{hip[0] - 10:.1f} {G - 0.4:.1f} Z" fill="url(#fur)"/>'
                  f'<path d="M{hip[0] - 15:.1f} {G - 14:.1f} Q{hip[0] - 16:.1f} {hip[1] - 12:.1f} {hip[0] + 1:.1f} {hip[1] - 16:.1f}" {D2.RIM}/></g>')
    shadow = D2.shadow(70 + (hip[0] - 44) * 0.5, 40 - 6 * sit)
    out = (defs() + shadow + f'<g transform="translate({x:.2f} 0)">' + tl
           + D2.draw_hind(hind_pts(*hf, True), True) + D2.draw_front(front_pts(*ff, True), True, cap=sit < 0.5)
           + body + hd + D2.draw_hind(hind_pts(*hl, False)) + haunch + D2.draw_front(front_pts(*fl, False), cap=sit < 0.5) + '</g>')
    return out


SIT = dict(theta=-50, hip=(44, 92), sit=1.0)


def sit_pose(head_a=-6, tail_a=0, mouth=False, ears=0.0, eyes_closed=False, breathe=0.0):
    return pose(theta=-50 + breathe, hip=(44, 92), sit=1.0, head_a=head_a, tail_a=tail_a + 40, mouth=mouth, ears=ears, eyes_closed=eyes_closed)


def stand_pose(head_a=0, tail_a=0, mouth=False, ears=0.0, x=0.0):
    return pose(head_a=head_a, tail_a=tail_a, mouth=mouth, ears=ears, x=x)


def blend_sit(u, head_a=-6, tail_a=0):
    """u = 0 standing .. 1 sitting (rear lowers first)."""
    th = lerp(0, -50, ease(u))
    hip = (44, lerp(54, 92, ease(min(1, u * 1.15))))
    return pose(theta=th, hip=hip, sit=ease(u), head_a=lerp(0, head_a, ease(u)), tail_a=lerp(0, 40, ease(u)) + tail_a)


def trot(ph, head_a=0.0):
    """2-beat trot: diagonal pairs together; stance 0.6, swing 0.4."""
    def leg(off, hind):
        u = (ph + off) % 1.0
        if u < 0.6:
            k = u / 0.6; return (16 - 32 * k, 0.0)
        k = (u - 0.6) / 0.4
        return (-16 + 32 * (0.5 - 0.5 * math.cos(math.pi * k)), math.sin(math.pi * k) * (0.85 if hind else 0.95))
    lf, rh = leg(0.0, False), leg(0.0, True)
    rf, lh = leg(0.5, False), leg(0.5, True)
    bob = -1.2 * abs(math.sin(2 * math.pi * ph))
    return pose(fl=lf, ff=rf, hl=lh, hf=rh, head_a=head_a + 2 * math.sin(4 * math.pi * ph), tail_a=6 * math.sin(2 * math.pi * ph), bob=bob)


def svg(inner, w=BW, h=BH):
    return f'<svg width="{w}" height="{h}" viewBox="{VB}" style="display:block;overflow:hidden">{R.fix(inner)}</svg>'
