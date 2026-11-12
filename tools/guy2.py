"""Detail upgrade for the coffee guy (side view) - patches real_guy in place.
Import this module before rendering: realistic profile, knit beanie, denim twill + seams,
fingers around the cup, detailed boots, chino folds, and a more natural walk."""
import math, sys
sys.path.insert(0, 'tools')
import real_guy as G

_defs0 = G.defs


def defs(o):
    d = _defs0(o)
    extra = (
        '<pattern id="twill" width="3" height="3" patternUnits="userSpaceOnUse" patternTransform="rotate(35)">'
        '<rect width="3" height="3" fill="none"/><path d="M0 0.6 L3 0.6" stroke="#ffffff" stroke-opacity="0.07" stroke-width="0.8"/>'
        '<path d="M0 2.1 L3 2.1" stroke="#000000" stroke-opacity="0.08" stroke-width="0.8"/></pattern>'
        '<pattern id="knit" width="3.2" height="4" patternUnits="userSpaceOnUse">'
        '<path d="M0.4 0 Q1.6 2 0.4 4 M2 0 Q3.2 2 2 4" stroke="#000" stroke-opacity="0.16" stroke-width="0.7" fill="none"/></pattern>'
        '<pattern id="chino" width="2.4" height="2.4" patternUnits="userSpaceOnUse" patternTransform="rotate(-30)">'
        '<path d="M0 1.2 L2.4 1.2" stroke="#ffffff" stroke-opacity="0.05" stroke-width="0.7"/></pattern>'
        '<radialGradient id="cheek" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#d98a7a" stop-opacity="0.35"/><stop offset="1" stop-color="#d98a7a" stop-opacity="0"/></radialGradient>'
        '<linearGradient id="bt2" x1="0" y1="0" x2="1" y2="0.3"><stop offset="0" stop-color="#3a2212"/><stop offset="0.55" stop-color="#6e4526"/><stop offset="0.85" stop-color="#9a6638"/><stop offset="1" stop-color="#7a4e2a"/></linearGradient>'
    )
    return d.replace('</defs>', extra + '</defs>')


RIM = G.RIM
FOLD = G.FOLD


def head(o):
    sk = 'url(#sk)'
    h = (# neck with sternocleidomastoid shading and nape
         '<path d="M64.5 42 L79 47 Q80.2 55 81.6 64 L63.4 64 Q63.6 53 64.5 42 Z" fill="url(#skv)"/>'
         '<path d="M70 48 Q76 56 79.6 63" stroke="#000" stroke-opacity="0.18" stroke-width="1.6" fill="none"/>'
         '<path d="M64.6 46 Q71 53 79.4 50.4 L80.4 57 Q72 60 64 56 Z" fill="#000" fill-opacity="0.22"/>'
         '<path d="M78.6 52.5 Q80.4 54 79.8 56" stroke="#000" stroke-opacity="0.25" stroke-width="0.8" fill="none"/>'   # adam's apple
         # head profile: forehead, brow, nose, lips, chin, jaw
         '<path d="M60 14 Q70 5 82 9 Q86.5 13 86.8 19 Q87.8 22.5 87.3 25.2 Q89.4 28.6 91.5 32.4 Q92 34.4 89.1 35.1 '
         'Q89.8 36.6 89.3 37.6 Q88.5 38.6 89 39.4 Q89.6 40.6 88.6 41.7 Q87.4 42.8 87.9 44.2 Q88.4 46.8 86.2 48.7 '
         'Q82 51.2 76.4 50.6 Q70.4 50.4 66.4 46.8 Q61 43 58.6 36 Q56.6 26 60 14 Z" fill="' + sk + '"/>'
         '<path d="M76.4 50.6 Q82 51.2 86.2 48.7 Q88 46.6 87.6 44.4 Q84 47.8 77.6 48 Q70.6 47.6 66.4 46.8 Q70.4 50.4 76.4 50.6 Z" fill="#000" fill-opacity="0.2"/>'
         '<path d="M66 44.4 Q62 40 59.6 34" stroke="#000" stroke-opacity="0.2" stroke-width="3.2" fill="none" filter="url(#soft1)"/>'
         # stubble on jaw + upper lip
         '<path d="M74 45.6 Q81 47.4 86.6 44.4 Q87.4 46.6 85.4 48.6 Q80 50.6 74 49.6 Q70 48.4 68 46.4 Z" fill="#5a3d28" fill-opacity="0.16"/>'
         '<path d="M86.4 35.4 Q88.6 35.6 89 36.4" stroke="#5a3d28" stroke-opacity="0.35" stroke-width="1.2" fill="none"/>'
         '<ellipse cx="80.4" cy="33.6" rx="4.2" ry="3" fill="url(#cheek)"/>'
         # ear
         '<path d="M65.6 26 Q69.6 24.6 70.4 29 Q70.8 33.2 68.4 35.6 Q66.6 37 65.2 35.6 Q63.6 31 65.6 26 Z" fill="' + sk + '" stroke="#000" stroke-opacity="0.25" stroke-width="0.6"/>'
         '<path d="M66.6 28 Q68.8 28 68.8 31 Q68.4 33.4 66.8 34" stroke="#000" stroke-opacity="0.32" stroke-width="0.8" fill="none"/>'
         # eye: lid, iris, lash line, highlight, under-eye
         '<path d="M81 24.9 Q83.2 23.3 85.6 24.6 Q84.6 26.2 83 26.4 Q81.8 26.2 81 24.9 Z" fill="#f2ece4"/>'
         '<path d="M82.6 24.2 Q84.4 24.1 85.1 25.2 Q84.4 26.2 83.1 26.3 Q82.3 25.4 82.6 24.2 Z" fill="#3a2a1e"/>'
         '<circle cx="84.2" cy="24.9" r="0.42" fill="#fff" fill-opacity="0.85"/>'
         '<path d="M80.7 24.8 Q83.2 22.9 85.9 24.4" stroke="#1a110c" stroke-width="0.9" fill="none" stroke-linecap="round"/>'
         '<path d="M81.6 27.1 Q83.4 27.9 85.2 27.1" stroke="#000" stroke-opacity="0.18" stroke-width="0.7" fill="none"/>'
         '<path d="M79.6 21.6 Q83 19.9 87 21.4" stroke="#3a2618" stroke-width="1.6" fill="none" stroke-linecap="round"/>'
         # nose shading, nostril, lips
         '<path d="M86.6 25.6 Q88.4 29.6 88.6 33" stroke="#000" stroke-opacity="0.16" stroke-width="1.1" fill="none"/>'
         '<path d="M87.4 33.6 Q88.4 34.4 89.4 34.2" stroke="#3a2016" stroke-opacity="0.6" stroke-width="0.8" fill="none"/>'
         '<path d="M86.4 37.9 Q88 37.4 89.2 37.8 Q88.4 38.6 86.6 38.7 Z" fill="#8a4a40"/>'
         '<path d="M86.6 39 Q88 39.4 88.9 40 Q88.2 41 86.8 40.6 Z" fill="#a85a4c"/>'
         '<path d="M85.4 38.7 L89 38.9" stroke="#4a2420" stroke-width="0.7"/>'
         '<path d="M86 42.6 Q87.2 42.4 87.6 43.2" stroke="#000" stroke-opacity="0.2" stroke-width="0.8" fill="none"/>'
         '<path d="M60 18 Q57.6 30 60.2 40" ' + RIM + '/>'
         '<path d="M86.8 19 Q87.8 22.5 87.3 25.2 Q89.4 28.6 91.5 32.4" stroke="#fff" stroke-opacity="0.18" stroke-width="0.9" fill="none"/>')
    # hair under the beanie (sideburn + nape)
    h += ('<path d="M61 26 Q63 30 64.6 34 L66 30 Q65 27 64.6 24 Z" fill="#5a3a22"/>'
          '<path d="M58 32 Q58.6 40 62.6 44 Q60 37 60.6 31 Z" fill="#5a3a22"/>')
    # knit beanie: crown, rib cuff, slouch, highlights
    h += ('<path d="M57.2 30 Q52.8 2 71.6 -0.2 Q90.6 -0.4 88.4 19.6 Z" fill="url(#hat)"/>'
          '<path d="M57.2 30 Q52.8 2 71.6 -0.2 Q90.6 -0.4 88.4 19.6 Z" fill="url(#knit)"/>'
          '<path d="M56.6 22.2 L88.4 13.4 L88.9 20.6 L57.4 30.4 Z" fill="url(#hat)"/>'
          + ''.join(f'<path d="M{58 + i * 2.6:.1f} {22 - i * 0.72:.2f} L{58.6 + i * 2.6:.1f} {30 - i * 0.8:.2f}" stroke="#000" stroke-opacity="0.2" stroke-width="0.9"/>' for i in range(12))
          + '<path d="M56.6 22.2 L88.4 13.4" stroke="#000" stroke-opacity="0.35" stroke-width="1"/>'
          '<path d="M57.4 30.4 L88.9 20.6" stroke="#000" stroke-opacity="0.3" stroke-width="0.8"/>'
          '<path d="M62 8 Q72 3 84 7" stroke="#fff" stroke-opacity="0.22" stroke-width="1.6" fill="none"/>'
          '<path d="M57.4 28 Q55 14 62 6.6" ' + RIM + '/>')
    return h


def shoe(o):
    return ('<path d="M60 281 Q59.6 273.6 66 272.6 L79.6 272.8 Q81.6 279 86.6 281.6 Q96.6 284.6 98.6 290.6 L98.8 296 L59.6 296 Z" fill="url(#bt2)"/>'
            '<path d="M59.4 294 L99 294 Q99.6 296.4 98.8 297.6 L59.4 297.6 Z" fill="#1a110a"/>'
            '<path d="M60 293.2 L98.8 293.2" stroke="#d9b98a" stroke-opacity="0.55" stroke-width="0.6" stroke-dasharray="1.2 1"/>'
            '<path d="M60 281 Q60 288 61 293 L66 293 Q65 286 66 280 Z" fill="#000" fill-opacity="0.25"/>'                 # heel counter
            '<path d="M86.6 281.6 Q93 283.6 96.6 287.4" stroke="#000" stroke-opacity="0.28" stroke-width="1" fill="none"/>'  # toe cap seam
            '<path d="M76 274.6 Q80 276.6 85 280.6" stroke="#2a180c" stroke-width="2.4" fill="none"/>'                        # tongue/laces
            + ''.join(f'<circle cx="{76.6 + i * 2.6:.1f}" cy="{275.2 + i * 1.8:.1f}" r="0.55" fill="#d9c08a"/>' for i in range(4))
            + '<path d="M77 276.4 L80.4 275.4 M79.4 278 L82.8 277 M81.8 279.6 L85 278.8" stroke="#e8d2a8" stroke-width="0.7"/>'
            '<path d="M88 284.4 Q94 285.6 96.4 289" stroke="#fff" stroke-opacity="0.28" stroke-width="1.1" fill="none"/>'
            '<path d="M62 276 Q66 274 72 274.4" stroke="#fff" stroke-opacity="0.15" stroke-width="0.9" fill="none"/>')


def hand():
    return ('<path d="M65.5 158.6 Q63 167 65.4 174.6 Q68.4 181.6 74.6 180.6 Q79.6 178.6 80.2 170.4 L79.8 158.6 Z" fill="url(#sk)"/>'
            '<path d="M78.2 161.6 Q83.4 166.2 81 172" stroke="url(#sk)" stroke-width="3.8" fill="none" stroke-linecap="round"/>'
            '<path d="M67.4 168.6 Q71.4 171.4 77.4 168.4 M67 173 Q71 175.6 76.6 172.8 M67.6 177 Q70.6 179 74.6 177.4" stroke="#000" stroke-opacity="0.25" stroke-width="0.8" fill="none"/>'
            '<path d="M79.4 161 Q81 168 79.6 175" stroke="#fff" stroke-opacity="0.2" stroke-width="0.8" fill="none"/>')


def cup(o):
    a = o['_cupang']
    return G.rot(a, (73, 170),
                 '<path d="M65.6 153.4 L80.4 153.4 L78.8 176.4 L67.2 176.4 Z" fill="url(#cp)"/>'
                 '<path d="M66.3 161 L79.7 161 L79.1 169.6 L66.9 169.6 Z" fill="#8a5a33"/>'
                 '<path d="M66.3 161 L79.7 161 L79.1 169.6 L66.9 169.6 Z" fill="url(#chino)"/>'
                 '<path d="M64.6 150.2 L81.4 150.2 Q82 152 81.4 154 L64.6 154 Q64 152 64.6 150.2 Z" fill="#2c2c30"/>'
                 '<path d="M73.6 149.4 L77.6 149.4 L77.6 150.4 L73.6 150.4 Z" fill="#111"/>'
                 '<path d="M78 155.6 L76.8 175" stroke="#fff" stroke-opacity="0.55" stroke-width="1.1"/>'
                 '<path d="M68 155.6 L69 175" stroke="#000" stroke-opacity="0.12" stroke-width="1.4"/>'
                 # fingers wrapped around the front of the cup
                 '<path d="M77.4 162.6 Q82.2 162.4 82.4 165.2 Q82.2 167.4 77.6 167.2 Z M77.4 167.8 Q81.8 167.8 81.8 170.4 Q81.6 172.4 77.4 172 Z" fill="url(#sk)" stroke="#000" stroke-opacity="0.25" stroke-width="0.5"/>'
                 '<path d="M71 145.6 Q69.4 141 72 137.4 Q74.6 133.8 72.6 130" stroke="#fff" stroke-opacity="0.22" stroke-width="1.2" fill="none"/>')


_torso0 = G.torso


def torso(o):
    t = _torso0(o)
    if o['kind'] != 'denim':
        return t
    body = 'M58 58 Q70 52 83 57 Q91 63 91 82 Q92 101 89 121 Q87 141 88 158 L88.5 169 Q72 173 55.5 169 L55.5 150 Q53.5 130 54.5 110 Q52.5 84 58 58 Z'
    t += (f'<path d="{body}" fill="url(#twill)"/>'
          '<path d="M56.6 76 Q70 72 89.6 76" stroke="#c9a46a" stroke-opacity="0.65" stroke-width="0.7" stroke-dasharray="1.4 1" fill="none"/>'   # yoke seam
          '<path d="M56.6 78 Q70 74 89.6 78" stroke="#c9a46a" stroke-opacity="0.5" stroke-width="0.7" stroke-dasharray="1.4 1" fill="none"/>'
          '<path d="M60 128 Q62 140 60 152 M80 124 Q82 132 81 140" ' + FOLD + '/>'
          '<path d="M57 158 L88.4 158" stroke="#c9a46a" stroke-opacity="0.55" stroke-width="0.7" stroke-dasharray="1.4 1"/>'
          '<rect x="84.6" y="160.6" width="2" height="2" rx="0.6" fill="#d9c08a"/>')
    return t


_upper0, _fore0 = G.upper_arm, G.forearm


def upper_arm(o):
    u = _upper0(o)
    if o['kind'] != 'denim':
        return u
    return u + ('<path d="M60 62 C57 84 61 104 63 121 L80 121 C81 101 82 82 81 62 Q70 56 60 62 Z" fill="url(#twill)"/>'
                '<path d="M80.4 66 C81 86 80.6 104 79.8 120" stroke="#c9a46a" stroke-opacity="0.5" stroke-width="0.7" stroke-dasharray="1.4 1" fill="none"/>'
                '<path d="M62 64 Q70 60 80 64" stroke="#000" stroke-opacity="0.2" stroke-width="1" fill="none"/>')


def forearm(o):
    f = _fore0(o)
    if o['kind'] != 'denim':
        return f
    i = f.index('<path d="M65.5 15')            # put twill under the hand
    return (f[:i] + '<path d="M63 116 C63 134 65 148 65 156 L80 156 C80 146 81 132 80 116 Z" fill="url(#twill)"/>'
            '<circle cx="78.6" cy="154.6" r="0.9" fill="#d9c08a"/>' + f[i:])


_thigh0, _shin0 = G.thigh, G.shin


def thigh(o):
    t = _thigh0(o)
    return t + ('<path d="M58 146 C53 163 56 192 63 229 L81 230 C84 205 87 175 86 146 Z" fill="url(#chino)"/>'
                '<path d="M84 156 Q85 164 83.6 170" stroke="#000" stroke-opacity="0.25" stroke-width="0.8" fill="none"/>')


def shin(o, ank=0):
    s = _shin0(o, ank)
    i = s.index('<g transform="rotate(')
    return s[:i] + '<path d="M63 222 C57 240 59 262 62 284 L60 289 L80 289 L78 284 C79 264 81 244 82 222 Z" fill="url(#chino)"/>' + s[i:]


def walk(o, ph):
    """Natural walk: contact / down / passing / up, knee flex in swing, heel strike + toe-off foot roll."""
    s = math.sin(2 * math.pi * ph)
    c = math.cos(2 * math.pi * ph)
    th_f, th_b = -25 * s, 25 * s

    sh_f = 55 * max(0, c) ** 1.6 + 5
    sh_b = 55 * max(0, -c) ** 1.6 + 5
    ua_f, ua_b = 22 * s, -22 * s
    fa_f, fa_b = -12 - 16 * max(0, s), -12 - 16 * max(0, -s)
    bob = -3.2 * abs(c) + 1.0
    oo = dict(o, _ankf=-12 * max(0, s) ** 2 + 16 * max(0, -s) ** 2, _ankb=-12 * max(0, -s) ** 2 + 16 * max(0, s) ** 2)
    return G.pose(oo, th_f, sh_f, th_b, sh_b, ua_f, fa_f, ua_b, fa_b, lean=3, bob=bob, tilt=1.5 * c)


# patch the module
G.defs, G.head, G.shoe, G.hand, G.cup, G.torso = defs, head, shoe, hand, cup, torso
G.upper_arm, G.forearm, G.thigh, G.shin, G.walk = upper_arm, forearm, thigh, shin, walk
