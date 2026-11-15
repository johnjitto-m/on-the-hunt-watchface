"""Golden retriever v2.7: hand-built sitting pose + a new head (drop ears, broad skull, feathered coat)
shared with the rig (dog3) so standing / trotting frames match.  Dog units: ground y=112, facing right."""
import math, sys
sys.path.insert(0, 'tools')
import dog2 as D2
from dog2 import limb

D2.set_palette('golden')
C0, CL, CD = '#c98d4a', '#efc27e', '#7e5226'          # coat mid / light / dark
CR, CRL = '#e9cc98', '#f8e6c4'                        # cream feathering
RIMC = '#ffe6b8'
RIM = f'stroke="{RIMC}" stroke-opacity="0.6" stroke-width="1.3" fill="none" stroke-linecap="round"'


def defs():
    return ('<defs>'
            f'<linearGradient id="rc" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{CL}"/><stop offset="0.35" stop-color="{C0}"/><stop offset="1" stop-color="{CD}"/></linearGradient>'
            f'<linearGradient id="rch" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{CD}"/><stop offset="0.55" stop-color="{C0}"/><stop offset="1" stop-color="{CL}"/></linearGradient>'
            f'<linearGradient id="rcr" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{CRL}"/><stop offset="1" stop-color="{CR}"/></linearGradient>'
            f'<linearGradient id="rear" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9a6430"/><stop offset="0.7" stop-color="#b87a3e"/><stop offset="1" stop-color="#d9a466"/></linearGradient>'
            '<radialGradient id="rsheen" cx="0.45" cy="0.25" r="0.6"><stop offset="0" stop-color="#fff0cc" stop-opacity="0.55"/><stop offset="1" stop-color="#fff0cc" stop-opacity="0"/></radialGradient>'
            '<linearGradient id="rnose" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3a3434"/><stop offset="1" stop-color="#0b0a0a"/></linearGradient>'
            '<filter id="rs" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="1.4"/></filter>'
            '<filter id="rpuff" x="-80%" y="-80%" width="260%" height="260%"><feGaussianBlur stdDeviation="3"/></filter>'
            '</defs>')


def strands(pts, color=CRL, op=0.6, w=0.8):
    return ''.join(f'<path d="M{x:.1f} {y:.1f} q{dx * 0.4:.1f} {dy * 0.6:.1f} {dx:.1f} {dy:.1f}" stroke="{color}" stroke-opacity="{op}" stroke-width="{w}" fill="none" stroke-linecap="round"/>'
                   for x, y, dx, dy in pts)


# ------------------------------------------------------------------ head (local: pivot (0,0) at the occiput/neck joint)
def head_local(mouth='closed', ears=0.0, eyes_closed=False, look=0.0):
    """mouth: closed | open (bark) | pant | yawn.  ears: + alert/forward, - relaxed back."""
    h = ''
    # far ear peeks behind the skull
    h += '<path d="M8 -14 Q14 -15 15 -10 Q15 -6 12 -6 Z" fill="#8a5a2a"/>'
    jaw_open = {'closed': 0, 'open': 16, 'pant': 9, 'yawn': 26}[mouth]
    if jaw_open:
        # mouth interior + lower jaw (rotates down around the jaw hinge)
        h += (f'<path d="M14 6 Q24 6 35 2.6 L33 8 Q24 14 14 10 Z" fill="#3a0e10"/>')
        jaw = ('<path d="M6 8 Q14 12 22 11 Q30 10 34 7 Q34 10.6 30.4 12.4 Q22 15.6 12 14.6 Q6 13.4 4 10 Z" fill="url(#rc)"/>'
               '<path d="M14 11.4 Q22 12 33 7.6" stroke="#2a0a0a" stroke-width="1" fill="none"/>'
               '<path d="M16 14 Q24 14.6 30 12" stroke="' + CRL + '" stroke-opacity="0.5" stroke-width="0.7" fill="none"/>')
        tongue = ''
        if mouth in ('pant', 'yawn', 'open'):
            L = 11 if mouth == 'pant' else 7
            tongue = (f'<path d="M18 9 Q27 8 31 9.6 Q32 {11 + L * 0.5:.1f} 29.4 {11 + L:.1f} Q26.6 {14 + L:.1f} 24 {11.4 + L:.1f} Q22.6 {10 + L * 0.5:.1f} 18 9 Z" fill="#e07580"/>'
                      f'<path d="M26.4 10.4 L26.8 {10 + L:.1f}" stroke="#b44a56" stroke-width="0.6"/>'
                      f'<path d="M23.4 11 Q24 {12 + L * 0.4:.1f} 24.6 {11 + L * 0.8:.1f}" stroke="#ffc0c8" stroke-opacity="0.6" stroke-width="0.6" fill="none"/>')
        h += f'<g transform="rotate({jaw_open:.1f} 6 8)">{tongue}{jaw}</g>'
    # skull + muzzle
    skull = ('M-3 -2 Q-3.4 -12 5 -15.4 Q13 -18 20 -12.6 Q22.6 -10.2 25 -9 L33 -6.8 Q37.2 -5.6 37.8 -2.2 Q37.8 1.2 35 2.8 '
             'Q32.6 6.4 27.6 7.4 Q21.6 9.2 15.4 10.2 Q7.6 11.8 2.4 9.8 Q-3 6.4 -3 -2 Z')
    h += (f'<path d="{skull}" fill="url(#rc)"/>'
          '<path d="M22 -9.4 L33 -6.8 Q37.2 -5.6 37.8 -2.2 Q37.8 1.2 35 2.8 Q32.6 6.4 27.6 7.4 Q22 8.8 17.6 8.6 Q22 3 22 -9.4 Z" fill="url(#rcr)" fill-opacity="0.75"/>'
          f'<ellipse cx="10" cy="-9" rx="9" ry="5" fill="url(#rsheen)"/>'
          '<path d="M19 -12 Q21.6 -8.6 22.4 -5" stroke="#6a4218" stroke-opacity="0.35" stroke-width="1" fill="none"/>'      # stop
          '<path d="M24 -8 Q30 -6.6 35.6 -5.6" stroke="#fff4dc" stroke-opacity="0.45" stroke-width="0.9" fill="none"/>'     # muzzle highlight
          '<path d="M4 4 Q8 8.6 15 9.4" stroke="#6a4218" stroke-opacity="0.3" stroke-width="1.2" fill="none"/>'              # cheek
          '<path d="M-2.6 -6 Q-2 -13 5 -15" ' + RIM + '/>')
    # eye + brow
    if eyes_closed:
        h += ('<path d="M13.6 -6.2 Q16.6 -4.6 19.4 -6.4" stroke="#2a1608" stroke-width="1.1" fill="none" stroke-linecap="round"/>'
              '<path d="M14 -5.4 Q16.6 -3.8 19 -5.6" stroke="#fff0cc" stroke-opacity="0.3" stroke-width="0.6" fill="none"/>')
    else:
        lx = 0.5 * look
        h += ('<path d="M13.4 -6.4 Q16.4 -9.4 19.8 -6.8 Q17 -4.2 13.4 -6.4 Z" fill="#1c0e06"/>'
              f'<ellipse cx="{16.8 + lx:.2f}" cy="-6.7" rx="1.9" ry="1.7" fill="#4a2810"/>'
              f'<circle cx="{17.5 + lx:.2f}" cy="-7.4" r="0.65" fill="#fff" fill-opacity="0.9"/>'
              '<path d="M13.2 -6.6 Q16.4 -9.8 20 -6.9" stroke="#120804" stroke-width="0.8" fill="none"/>'
              '<path d="M14 -4.9 Q16.6 -3.8 19.4 -5.4" stroke="#6a4218" stroke-opacity="0.45" stroke-width="0.6" fill="none"/>')
    h += '<path d="M12.6 -10.4 Q16 -12.6 20.2 -10.6" stroke="#8a5a2a" stroke-opacity="0.6" stroke-width="1.1" fill="none" stroke-linecap="round"/>'
    # nose, nostril, lip line, whisker pores
    h += ('<path d="M33.2 -7 Q37.6 -7.6 38.8 -4.2 Q39.2 -1.2 36.6 -0.4 Q33.4 -0.4 32.6 -3.6 Q32.4 -5.8 33.2 -7 Z" fill="url(#rnose)"/>'
          '<path d="M34.4 -6.2 Q36.8 -6.4 37.6 -4.8" stroke="#fff" stroke-opacity="0.5" stroke-width="0.6" fill="none"/>'
          '<path d="M37.6 -2.4 Q37 -1.4 35.8 -1.6" stroke="#000" stroke-width="0.6" fill="none"/>'
          '<path d="M36.4 -0.4 L36 2.2" stroke="#3a2010" stroke-width="0.6"/>')
    if not jaw_open:
        h += ('<path d="M36 2.4 Q30 6 21.6 7" stroke="#2a1608" stroke-width="0.9" fill="none" stroke-linecap="round"/>'
              '<path d="M21.6 7 Q20.6 6.2 20.8 5.2" stroke="#2a1608" stroke-width="0.7" fill="none"/>')
    h += ''.join(f'<circle cx="{x}" cy="{y}" r="0.45" fill="#5a3410"/>' for x, y in ((27, 0.6), (29.2, 1.6), (26.2, 2.8), (28.6, 3.4), (31, 2.4)))
    # drop ear (near), feathered edge
    ear = ('<path d="M1.4 -12.6 Q9.6 -15.6 12.6 -9 Q15 0 12 10.4 Q9.6 15.8 4 14.6 Q-1.8 12 -1.6 1.6 Q-1.6 -8 1.4 -12.6 Z" fill="url(#rear)"/>'
           '<path d="M12 10.4 Q11 14 8.6 15.4 M9.6 12 Q8 15.6 5.4 16 M6.8 13.4 Q5 16.2 2.6 15.2" stroke="#d9a466" stroke-opacity="0.8" stroke-width="0.8" fill="none" stroke-linecap="round"/>'
           '<path d="M3 -9 Q1 0 3 10 M7 -10 Q7.6 0 6.6 11" stroke="#6a3c14" stroke-opacity="0.3" stroke-width="0.7" fill="none"/>'
           '<path d="M-1.2 0 Q-1 -8 1.6 -12" ' + RIM + '/>')
    h += f'<g transform="rotate({-18 * ears:.1f} 6 -11)">{ear}</g>'
    # fur on top of the head and cheek fluff
    h += strands([(2, -13, 3, -1.6), (6, -15, 3.4, -0.6), (-1.6, -4, -1.4, 2.6), (0, 6, -1.4, 3), (3, 9, -0.4, 3.4)], CL, 0.55, 0.7)
    return h


def neck_rig():
    """neck for the rig head group (rig N0 pivot at (104, 40))."""
    return ('<path d="M98.6 46 Q95.4 30 101.6 19 Q106 11.6 113.6 9.6 L123 21 Q119.6 36 112.6 48 Z" fill="url(#rc)"/>'
            '<path d="M100 38 Q98.6 28 103 20" ' + RIM + '/>'
            + strands([(114, 30, 2.4, 4), (116, 36, 2, 4.6), (112, 42, 2.6, 4.4), (118, 26, 2, 3.4)], CRL, 0.55, 0.8))


def collar(cx=111, cy=30, a=0):
    return (f'<g transform="rotate({a} {cx} {cy})">'
            f'<path d="M{cx - 11} {cy - 4} Q{cx - 1} {cy + 5} {cx + 11} {cy - 1}" stroke="#8e0d20" stroke-width="3.6" fill="none" stroke-linecap="round"/>'
            f'<path d="M{cx - 11} {cy - 5} Q{cx - 1} {cy + 3.6} {cx + 11} {cy - 2.2}" stroke="#ff6a7c" stroke-opacity="0.4" stroke-width="0.8" fill="none"/>'
            f'<circle cx="{cx + 1}" cy="{cy + 4.6}" r="2" fill="#d9b25a"/><circle cx="{cx + 0.4}" cy="{cy + 4}" r="0.6" fill="#fff4c8"/></g>')


def rig_head(mouth=False, ears=0.0, eyes_closed=False):
    """drop-in for dog3.head (inside the rig's head group)."""
    m = mouth if isinstance(mouth, str) else ('open' if mouth else 'closed')
    return neck_rig() + collar(112, 30, 8) + f'<g transform="translate(110 14) scale(1.15)">{head_local(m, ears, eyes_closed)}</g>'


# ------------------------------------------------------------------ sitting body
HEAD_K = 1.22


def tail_chain(sweep=0.0, lift=0.0, n=8, seg=4.6):
    """feathered tail lying on the ground; `sweep` (-1..1) swings it across the floor (seen as foreshortening + a lift)."""
    base = (42.0, 104.6)
    P = [base]
    for i in range(1, n + 1):
        f = i / n
        sw = sweep * f ** 1.3
        dx = -seg * math.cos(sw * 1.1)
        dy = seg * (0.12 - 0.5 * lift * (1 - f) - 0.35 * abs(sw) * f)
        P.append((P[-1][0] + dx, min(110.6, P[-1][1] + dy)))
    W = [8.2 - 5.6 * (i / n) for i in range(n + 1)]
    out = limb(P, W, 'url(#rc)')
    under = [(p[0], p[1] + w * 0.42) for p, w in zip(P, W)]
    out += limb(under[1:], [w * 0.55 for w in W[1:]], CR)
    out += ''.join(f'<path d="M{p[0]:.1f} {p[1] + w * 0.4:.1f} q{-1.2:.1f} {1.4:.1f} {-2.4:.1f} {2.2:.1f}" stroke="{CRL}" stroke-opacity="0.7" stroke-width="0.8" fill="none" stroke-linecap="round"/>'
                   for p, w in zip(P[1:], W[1:]))
    tip = P[-1]
    out += f'<path d="M{tip[0]:.1f} {tip[1]:.1f} q-2.6 -0.6 -4.4 0.8" stroke="{CRL}" stroke-opacity="0.7" stroke-width="0.9" fill="none" stroke-linecap="round"/>'
    return out


def sit(head_a=-6, mouth='closed', ears=0.0, eyes_closed=False, tail_a=0.0, look=0.0, extra_body='', extra_head='', breathe=0.0,
        sweep=None, lean=0.0):
    out = defs()
    out += '<ellipse cx="74" cy="112.8" rx="44" ry="2.8" fill="#000" fill-opacity="0.55" filter="url(#rs)"/>'
    out += f'<g transform="rotate({lean:.2f} 104 112)">'
    if sweep is None:
        sweep = max(-1.0, min(1.0, tail_a / 14.0))
    out += tail_chain(sweep, 0.15)
    # far front leg (darker)
    out += ('<g style="filter: brightness(0.58)">' + limb([(100, 66), (100, 90), (101, 106)], [13, 10, 9], 'url(#rch)')
            + D2.paw((103, 111.6), 0) + '</g>')
    # torso: upright, deep chest, back sloping to the rump
    torso = ('M86 26 Q103 21 114 31 Q125 43 123 60 Q121 76 112 86 L106 98 Q92 108 70 108.6 L46 110.6 '
             'Q33 107 33 94 Q33 80 45 69 Q58 56 68 42 Q76 30 86 26 Z')
    out += (f'<g transform="translate(0 {breathe:.2f})"><path d="{torso}" fill="url(#rc)"/>'
            '<path d="M44 68 Q58 54 67 42 Q76 30 86 27" ' + RIM + '/>'
            '<path d="M50 64 Q62 52 70 40" stroke="#fff0cc" stroke-opacity="0.22" stroke-width="3" fill="none" stroke-linecap="round"/>'
            '<path d="M102 70 Q98 82 102 96" stroke="#5a3410" stroke-opacity="0.35" stroke-width="2.2" fill="none"/>'        # elbow / chest separation
            # chest feathering (cream ruff)
            '<path d="M110 30 Q124 42 123 60 Q121 76 112 86 Q107 80 108 66 Q106 48 110 30 Z" fill="url(#rcr)" fill-opacity="0.9"/>'
            + strands([(117, 44, 2.6, 3.6), (120, 52, 2.2, 4), (121, 60, 1.6, 4.4), (119, 68, 1, 4.6), (116, 76, 0.4, 4.6), (112, 82, -0.4, 4.4),
                       (113, 48, 1.6, 4), (115, 58, 1.4, 4.4), (114, 66, 0.8, 4.4)], CRL, 0.75, 0.8)
            + strands([(58, 54, -2, 2.4), (50, 62, -2.4, 2.6), (64, 46, -2, 2), (72, 36, -1.6, 1.8), (80, 30, -1.4, 1.6)], CL, 0.45, 0.7)
            + extra_body + '</g>')
    # thigh (long oval, tucked) + hind foot flat on the ground
    out += ('<g transform="rotate(-24 58 92)"><ellipse cx="58" cy="92" rx="25" ry="15.6" fill="url(#rc)"/>'
            '<ellipse cx="54" cy="86" rx="15" ry="7" fill="url(#rsheen)"/></g>'
            '<path d="M36 100 Q32 86 44 76" ' + RIM + '/>'
            '<path d="M74 80 Q82 92 76 104" stroke="#5a3410" stroke-opacity="0.3" stroke-width="1.4" fill="none"/>'
            + strands([(36, 102, -2.4, 3.2), (39, 106, -2, 3), (43, 108.6, -1.4, 2.6)], CR, 0.75, 0.8)
            + '<path d="M54 111.6 L55 105.6 Q66 102.6 80 103.2 Q90.6 104.4 91.6 108.6 Q91.8 112 87.6 112 Z" fill="url(#rcr)"/>'
            '<path d="M80 111.8 L80.4 108.4 M84.2 111.8 L84.6 108.2 M87.8 111.6 L88 108.6" stroke="#6a4218" stroke-width="0.6"/>'
            '<path d="M56 105.4 Q68 103 80 103.6" stroke="#fff8e8" stroke-opacity="0.45" stroke-width="0.8" fill="none"/>')
    # near front leg: defined back edge, feathering, cream pastern
    out += (limb([(106, 64), (106.4, 88), (107, 106)], [15, 11, 9.6], 'url(#rch)')
            + limb([(106.6, 94), (107, 107)], [9.4, 9.4], 'url(#rcr)')
            + D2.paw((109, 111.6), 0)
            + '<path d="M99.4 70 Q99 86 101.6 100" stroke="#4a2a0c" stroke-opacity="0.35" stroke-width="1.2" fill="none"/>'
            + '<path d="M112.4 70 Q113 86 111.6 104" stroke="#fff4dc" stroke-opacity="0.4" stroke-width="1" fill="none"/>'
            + strands([(100, 74, -2.6, 2.4), (99.6, 80, -2.6, 2.6), (100, 86, -2.2, 2.6), (100.6, 92, -1.8, 2.2)], CR, 0.8, 0.8))
    # neck + collar + head
    out += ('<path d="M84 38 Q82 20 94 9 Q102 3 112 4 L122 14 Q126 30 120 44 Q102 50 84 38 Z" fill="url(#rc)"/>'
            '<path d="M85 34 Q84 20 94 10" ' + RIM + '/>'
            '<path d="M112 14 Q123 22 122 42 Q114 38 111 28 Z" fill="url(#rcr)" fill-opacity="0.85"/>'
            + strands([(118, 22, 2.4, 3.6), (120, 28, 2.2, 4), (120, 34, 1.6, 4.2), (116, 18, 2, 3)], CRL, 0.7, 0.8)
            + collar(103, 25, 16))
    out += (f'<g transform="translate(106 6) rotate({head_a:.2f}) scale({HEAD_K})">'
            f'{head_local(mouth, ears, eyes_closed, look)}{extra_head}</g>')
    return out + '</g>'


def svg(inner, w=60, h=66):
    return f'<svg width="{w}" height="{h}" viewBox="0 -50 150 165" style="display:block;overflow:hidden">{inner}</svg>'
