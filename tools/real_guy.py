"""Semi-realistic 'everyday guy' (side view, facing right): real proportions (~7.5 heads), gradient shading,
cloth folds, cool rim light from behind, warm key light from the front. Rig units match the face sprites
(viewBox 240 x 386.667, translate 40 26.667, ground at y=297)."""
import asyncio, math, os, sys
sys.path.insert(0, 'tools')
import render_v2 as R

OUT = 'build/art/real'
os.makedirs(OUT, exist_ok=True)
R.OUT = OUT

HIP, KNEE, ANK = (71, 157), (72, 226), (70, 286)
SHO, ELB, WRI = (70, 68), (71, 118), (72, 158)
NECKP = (70, 52)


def rot(a, c, inner):
    return f'<g transform="rotate({a:.2f} {c[0]} {c[1]})">{inner}</g>'


def lg(id_, stops, x1=0, y1=0, x2=1, y2=0):
    s = ''.join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in stops)
    return f'<linearGradient id="{id_}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}">{s}</linearGradient>'


def defs(o):
    J, JL, JD = o['jacket'], o['jacketl'], o['jacketd']
    D, DL, DD = o['denim'], o['denim_l'], o['denim_d']
    S, SL, SD = o['skin'], o['skin_l'], o['skin_d']
    return ('<defs>'
            + lg('jk', [(0, JD), (0.55, J), (0.9, JL), (1, J)])
            + lg('jkv', [(0, JL), (0.5, J), (1, JD)], 0, 0, 0, 1)
            + lg('dn', [(0, DD), (0.5, D), (0.85, DL), (1, D)])
            + lg('sk', [(0, SD), (0.6, S), (1, SL)])
            + lg('skv', [(0, SL), (1, SD)], 0, 0, 0, 1)
            + lg('hr', [(0, '#0d0b0a'), (0.6, o['hair']), (1, '#3a2c22')], 0, 1, 1, 0)
            + lg('sh', [(0, '#c9c6bf'), (0.6, '#f1efea'), (1, '#ffffff')])
            + lg('hp', [(0, '#0e0e10'), (0.6, '#2a2b30'), (1, '#55565c')])
            + lg('bt', [(0, '#3a2414'), (0.6, '#6b4527'), (1, '#8a5d36')])
            + lg('cp', [(0, '#cfc9bd'), (0.6, '#f3efe7'), (1, '#ffffff')])
            + lg('cc', [(0, '#d6d7da'), (1, '#8d9096')])
            + lg('bp', [(0, '#5a3a1c'), (0.6, '#8a5d30'), (1, '#a8743f')])
            + lg('hat', [(0, o.get('hatd', '#000')), (0.6, o.get('hat', '#000')), (1, o.get('hatl', '#000'))])
            + '<filter id="soft" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="2.2"/></filter>'
            + '<filter id="soft1" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="0.9"/></filter>'
            + '</defs>')


RIM = 'stroke="#9fb3cc" stroke-opacity="0.55" stroke-width="1.6" fill="none"'
FOLD = 'stroke="#000" stroke-opacity="0.28" stroke-width="1.6" fill="none" stroke-linecap="round"'
HL = 'stroke="#fff" stroke-opacity="0.13" stroke-width="2" fill="none" stroke-linecap="round"'


# ---------------- segments (rest pose: hanging straight down)
def thigh(o):
    return ('<path d="M58 146 C53 163 56 192 63 229 L81 230 C84 205 87 175 86 146 Z" fill="url(#dn)"/>'
            '<path d="M58 150 C54 165 57 192 63 228" ' + RIM + '/>'
            '<path d="M72 214 Q76 216 81 213 M71 219 Q75 221 80 219" stroke="#000" stroke-opacity="0.16" stroke-width="1.2" fill="none"/>'
            '<path d="M64 200 Q60 214 64 226" stroke="#000" stroke-opacity="0.14" stroke-width="2.4" fill="none"/>'
            '<path d="M83 160 C84 180 82 205 80 226" ' + HL + '/>'
            + ('<path d="M84 150 C86 180 83 205 81 228" stroke="#e8e4da" stroke-width="2.2" fill="none"/>' if o['kind'] == 'track' else ''))


def shin(o, ank=0):
    return ('<path d="M63 222 C57 240 59 262 62 284 L60 289 L80 289 L78 284 C79 264 81 244 82 222 Z" fill="url(#dn)"/>'
            '<path d="M62 228 C58 244 60 264 62 284" ' + RIM + '/>'
            '<path d="M64 274 Q71 278 78 273 M63 281 Q71 285 79 280" ' + FOLD + '/>'
            '<path d="M80 232 C80 250 79 266 78 280" ' + HL + '/>'
            + ('<path d="M81 224 C81 246 79 266 78 278" stroke="#e8e4da" stroke-width="2.2" fill="none"/>'
               '<path d="M62 278 L79 278 L79.5 287 L61.5 287 Z" fill="#000" fill-opacity="0.35"/>' if o['kind'] == 'track' else '')
            + rot(ank, ANK, shoe(o)))


def shoe(o):
    if o.get('shoe') == 'boot':
        return ('<path d="M60 280 Q60 274 66 273 L79 273 Q81 279 86 282 Q96 285 98 291 L98 297.5 L59.5 297.5 Z" fill="url(#bt)"/>'
                '<path d="M59.5 294 L98.5 294 L98.5 297.5 L59.5 297.5 Z" fill="#1a120c"/>'
                '<path d="M78 276 L82 279 M80 274.5 L84 277.5 M82 277 L86 281" stroke="#e2c9a0" stroke-width="0.9"/>'
                '<path d="M86 284 Q93 285 96 289" stroke="#ffffff" stroke-opacity="0.22" stroke-width="1" fill="none"/>')
    if o.get('shoe') == 'high':
        return ('<path d="M59 284 Q58 272 64 271 L78 271 Q80 279 87 283 Q97 286 99 291 L98.5 297.5 L58.5 297.5 Z" fill="url(#sh)"/>'
                '<path d="M58.5 293 L99.5 293 L98.5 297.5 L58.5 297.5 Z" fill="#8f8a82"/>'
                '<circle cx="64" cy="279" r="2.6" fill="#222" fill-opacity="0.7"/>'
                '<path d="M78 275 L82 278 M80 273 L84 276 M83 279 L87 282" stroke="#9a968e" stroke-width="1"/>'
                f'<path d="M64 287 Q74 286 88 289" stroke="{o["accent"]}" stroke-width="2" fill="none"/>')
    return sneaker(o)


def sneaker(o):
    return ('<path d="M59 285 Q59 279 66 279 L79 280 Q88 282 95 288 Q100 291 99 295 L98 297.5 L58.5 297.5 Z" fill="url(#sh)"/>'
            '<path d="M58.5 293 L99.5 293 L98.5 297.5 L58.5 297.5 Z" fill="#8f8a82"/>'
            '<path d="M80 283 L84 286 M83 282 L87 285 M86 283 L90 287" stroke="#9a968e" stroke-width="1.1"/>'
            '<path d="M60 287 Q70 286 78 289" stroke="#00000030" stroke-width="1.4" fill="none"/>'
            f'<path d="M66 283 Q72 288 86 289" stroke="{o["accent"]}" stroke-width="2" fill="none" stroke-linecap="round"/>')


def upper_arm(o):
    return ('<path d="M60 62 C57 84 61 104 63 121 L80 121 C81 101 82 82 81 62 Q70 56 60 62 Z" fill="url(#jk)"/>'
            '<path d="M60 64 C58 84 61 104 63 120" ' + RIM + '/>'
            '<path d="M66 104 Q71 110 77 106 M65 112 Q71 117 78 113" ' + FOLD + '/>'
            '<path d="M78 70 C79 88 79 104 78 118" ' + HL + '/>'
            + ('<path d="M69 64 C69 86 70 104 71 120 M73 64 C73 86 74 104 75 120" stroke="#e8e4da" stroke-width="1.8" fill="none"/>' if o['kind'] == 'track' else '')
            + ('<path d="M66 82 L76 82 L76 92 L66 92 Z" fill="#000" fill-opacity="0.22"/><path d="M68 84 L74 84" stroke="url(#cc)" stroke-width="0.8"/>' if o['kind'] == 'bomber' else ''))


def forearm(o):
    return ('<path d="M63 116 C63 134 65 148 65 156 L80 156 C80 146 81 132 80 116 Z" fill="url(#jk)"/>'
            '<path d="M64.5 150 L80.5 150 L80.5 160 L65 160 Z" fill="' + o['jacketd'] + '"/>'
            '<path d="M65 152 L80 152 M65 155 L80 155 M65 158 L80 158" stroke="#000" stroke-opacity="0.25" stroke-width="0.8"/>'
            '<path d="M64 120 C64 134 65 146 65 156" ' + RIM + '/>'
            '<path d="M70 128 Q74 132 78 129" ' + FOLD + '/>'
            + ('<path d="M70 116 C70 132 71 146 71.5 150 M74 116 C74 132 75 146 75.5 150" stroke="#e8e4da" stroke-width="1.8" fill="none"/>' if o['kind'] == 'track' else '')
            + hand() + (cup(o) if o.get('coffee') and o.get('_front') else ''))


def cup(o):
    a = o['_cupang']
    return rot(a, (73, 170), '<path d="M66 154 L80 154 L78.5 176 L67.5 176 Z" fill="url(#cp)"/>'
               '<path d="M66.8 162 L79.2 162 L78.6 169 L67.4 169 Z" fill="#8a5a33"/>'
               '<path d="M65 151 L81 151 L81 155 L65 155 Z" fill="#2c2c30"/>'
               '<path d="M77 156 L76 174" stroke="#ffffff" stroke-opacity="0.5" stroke-width="1" fill="none"/>'
               '<path d="M71 147 Q69 142 72 138 Q75 134 73 130" stroke="#ffffff" stroke-opacity="0.25" stroke-width="1.2" fill="none"/>')


def hand():
    return ('<path d="M65.5 159 Q63 168 66 176 Q69 182 75 180 Q80 177 80 169 L79.5 159 Z" fill="url(#sk)"/>'
            '<path d="M78 162 Q83 167 80 172" stroke="url(#sk)" stroke-width="3.6" fill="none" stroke-linecap="round"/>'
            '<path d="M68 172 Q72 175 77 172 M67.5 176 Q71 178.5 75.5 177" stroke="#00000035" stroke-width="0.9" fill="none"/>')


def torso(o):
    t = ('<path d="M58 58 Q70 52 83 57 Q91 63 91 82 Q92 101 89 121 Q87 141 88 158 L88.5 169 Q72 173 55.5 169 L55.5 150 Q53.5 130 54.5 110 Q52.5 84 58 58 Z" fill="url(#jk)"/>'
         '<path d="M55.5 158 L88.5 158 L88.5 169 Q72 173 55.5 169 Z" fill="' + o['jacketd'] + '"/>'
         '<path d="M56 160.5 L88 160.5 M56 163.5 L88 163.5 M56 166.5 L88 166.5" stroke="#000" stroke-opacity="0.22" stroke-width="0.8"/>'
         '<path d="M57 62 Q52.5 86 54.5 110 Q53.5 130 55.5 150" ' + RIM + '/>'
         '<path d="M72 128 Q81 126 89 129 L88 154 L71 154 Z" fill="#000" fill-opacity="0.16"/>'
         '<path d="M72 128 Q81 126 89 129" stroke="#000" stroke-opacity="0.35" stroke-width="1.2" fill="none"/>'
         '<path d="M62 136 Q70 140 76 137 M60 146 Q67 150 72 147 M84 96 Q88 102 89 110" ' + FOLD + '/>'
         '<path d="M86 70 C89 86 89 104 87 122" ' + HL + '/>')
    if o['kind'] == 'hoodie':
        t += ('<path d="M60 58 Q46 58 48 74 Q50 86 60 84 Q64 76 66 66 Z" fill="url(#jkv)"/>'
              '<path d="M49 64 Q47 74 52 82" ' + RIM + '/>'
              '<path d="M54 66 Q57 74 62 78" ' + FOLD + '/>'
              '<path d="M79 60 L80.5 84 M83 60 L85 82" stroke="#d9d4c8" stroke-width="1.3" stroke-linecap="round"/>'
              '<circle cx="80.5" cy="85" r="1.2" fill="#d9d4c8"/><circle cx="85" cy="83" r="1.2" fill="#d9d4c8"/>')
    if o['kind'] == 'bomber':
        t += ('<path d="M60 56 Q71 50 84 56 L85 63 Q72 58 60 63 Z" fill="' + o['jacketd'] + '"/>'
              '<path d="M61 58 L84 58 M61 60.5 L84.5 60.5" stroke="#000" stroke-opacity="0.3" stroke-width="0.7"/>'
              '<path d="M87 62 C90 86 89 120 88 158" stroke="url(#cc)" stroke-width="0.9" fill="none"/>')
    if o['kind'] == 'denim':
        t += ('<path d="M74 54 L84 56 L87 66 L76 64 Z" fill="#ecebe6"/>'
              '<path d="M62 54 Q70 50 76 54 L72 66 Z M84 55 L90 60 L86 70 L80 62 Z" fill="' + o['jacketd'] + '"/>'
              '<path d="M86 66 C89 90 89 120 87.5 158" stroke="#c9a46a" stroke-opacity="0.8" stroke-width="0.8" stroke-dasharray="1.6 1.2" fill="none"/>'
              '<path d="M74 82 L86 82 L86 92 L74 92 Z" fill="#000" fill-opacity="0.15" stroke="#c9a46a" stroke-opacity="0.7" stroke-width="0.7" stroke-dasharray="1.4 1"/>'
              '<path d="M56 112 L89 112" stroke="#c9a46a" stroke-opacity="0.6" stroke-width="0.7" stroke-dasharray="1.4 1"/>'
              '<circle cx="87.6" cy="96" r="0.9" fill="#d9c08a"/><circle cx="87.4" cy="122" r="0.9" fill="#d9c08a"/><circle cx="87.6" cy="146" r="0.9" fill="#d9c08a"/>')
    if o['kind'] == 'track':
        t += ('<path d="M61 50 Q72 46 84 51 L85 64 Q72 60 61 64 Z" fill="' + o['jacketd'] + '"/>'
              '<path d="M84 52 L85 64" stroke="url(#cc)" stroke-width="1"/>'
              '<path d="M86 64 C89 90 89 120 88 158" stroke="url(#cc)" stroke-width="0.9" fill="none"/>'
              '<path d="M56 100 Q55 130 56 160" stroke="#e8e4da" stroke-width="2" fill="none"/>')
    return t


def head(o):
    h = ('<path d="M65 40 L77 40 L78.5 62 L64 62 Z" fill="url(#skv)"/>'
         '<path d="M65 46 Q71 52 78 49 L78.5 62 L64 62 Z" fill="#000" fill-opacity="0.22"/>'
         # skull + face profile
         '<path d="M60 13 Q72 4 83 11 Q88 17 87 25 L88.5 29.5 Q92.5 33.5 89 35 L88 36.5 Q89.5 38.5 87.8 39.6 Q88.8 42.5 86 45 '
         'Q81 50.5 74 50.5 Q67 50 63.5 45 Q57.5 40 57 30 Q56.5 19 60 13 Z" fill="url(#sk)"/>'
         '<path d="M74 50.5 Q81 50.5 86 45 Q82 47 76 47 Z" fill="#000" fill-opacity="0.18"/>'           # jaw shadow
         '<path d="M63.5 45 Q60 41 58 34" stroke="#000" stroke-opacity="0.2" stroke-width="3" fill="none" filter="url(#soft1)"/>'
         # ear
         '<ellipse cx="66.5" cy="30.5" rx="3.6" ry="5.4" fill="url(#sk)" stroke="#00000040" stroke-width="0.8"/>'
         '<path d="M67.5 27.5 Q65.5 30.5 67.5 33.5" stroke="#00000050" stroke-width="1" fill="none"/>'
         # eye, brow, nose shade, lips
         '<path d="M81 25.6 Q83 24.4 85 25.6 Q83 27 81 25.6 Z" fill="#1a1412"/>'
         '<path d="M84 25.8 L85.2 25.8" stroke="#ffffff" stroke-opacity="0.5" stroke-width="0.5"/>'
         '<path d="M79.5 22.3 Q83 20.8 86.5 22.4" stroke="#2a1e18" stroke-width="1.5" fill="none" stroke-linecap="round"/>'
         '<path d="M86 28 Q87.5 32 86.8 34.5" stroke="#00000030" stroke-width="1.2" fill="none"/>'
         '<path d="M85.6 39.4 L88 39.6" stroke="#6e3d34" stroke-width="1.1" stroke-linecap="round"/>'
         '<path d="M79 41 Q83 47 86 44.5" stroke="#00000022" stroke-width="2.2" fill="none"/>'               # stubble
         '<path d="M60 18 Q57.5 30 60 40" ' + RIM + '/>')
    if o['hairstyle'] == 'short':
        h += ('<path d="M57.5 28 Q54 13 64 7 Q75 2.5 84 9 Q88.5 13 87 19.5 Q83 15.5 77 15.5 Q72 15.5 69.5 18 '
              'Q66 20 65 24 Q63 27 62.5 31 L60 32 Z" fill="url(#hr)"/>'
              '<path d="M63 9 Q72 6 82 10 M61 13 Q68 10 76 11" stroke="#ffffff" stroke-opacity="0.12" stroke-width="1" fill="none"/>'
              '<path d="M57.5 28 Q55 18 60 11" ' + RIM + '/>'
              '<path d="M69.5 24 Q70 30 69 34" stroke="url(#hr)" stroke-width="2" fill="none"/>')
    if o['hairstyle'] == 'cap':
        h += ('<path d="M57.5 29 Q55 12 66 7 Q77 3 85 10 Q88.5 15 87.5 21 L58.5 27 Z" fill="url(#hat)"/>'
              '<path d="M84 17.5 L101 19.5 Q103.5 21.5 101 23 L86 23 Z" fill="url(#hat)"/>'
              '<path d="M84.5 22.6 L101 22.6" stroke="#000" stroke-opacity="0.5" stroke-width="1"/>'
              '<path d="M60 22 Q72 16 86 19" stroke="#000" stroke-opacity="0.25" stroke-width="1.4" fill="none"/>'
              '<circle cx="72" cy="6" r="1.4" fill="url(#hat)"/>'
              '<path d="M58 30 Q57 34 60 38" stroke="#1a120c" stroke-width="2.4" fill="none"/>'
              '<path d="M57.8 28 Q55.5 18 61 10" ' + RIM + '/>')
    if o['hairstyle'] == 'beanie':
        h += ('<path d="M57.5 31 Q54 4 72 2 Q90 3 88 24 L58 31 Z" fill="url(#hat)"/>'
              '<path d="M57 24 L88.5 18.5 L89 26 L58 32 Z" fill="url(#hat)"/>'
              '<path d="M57 24 L88.5 18.5" stroke="#000" stroke-opacity="0.3" stroke-width="1"/>'
              + ''.join(f'<path d="M{62 + i * 5} {5 + i * 0.2} L{62.5 + i * 5} {29 - i * 1.0}" stroke="#000" stroke-opacity="0.18" stroke-width="0.9"/>' for i in range(6))
              + '<path d="M58 31 Q57 35 60 39" stroke="#6b4a2a" stroke-width="2.2" fill="none"/>'
              '<path d="M57.5 28 Q55 14 62 7" ' + RIM + '/>')
    if o['hairstyle'] == 'curly':
        blobs = [(60, 14, 6), (66, 8, 6.5), (73, 6, 6.5), (80, 8, 6), (85, 13, 5), (58, 22, 5.5), (62, 28, 4.6), (69, 14, 5), (77, 13, 5)]
        h += ''.join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="url(#hr)"/>' for x, y, r in blobs)
        h += ''.join(f'<path d="M{x - r * 0.6} {y - r * 0.2} Q{x} {y - r * 0.8} {x + r * 0.5} {y - r * 0.3}" stroke="#ffffff" stroke-opacity="0.14" stroke-width="0.9" fill="none"/>' for x, y, r in blobs)
        h += '<path d="M54.5 22 Q55 12 62 7" ' + RIM + '/>'
    if o.get('phones'):
        h += ('<path d="M61 60 Q70 70 84 60" stroke="#0e0e10" stroke-width="3.2" fill="none"/>'
              '<ellipse cx="62" cy="58.5" rx="4.6" ry="5.8" fill="url(#hp)"/>'
              '<ellipse cx="83.5" cy="58.5" rx="4.6" ry="5.8" fill="url(#hp)"/>'
              '<path d="M85 55 Q87 58 85 62" stroke="#ffffff" stroke-opacity="0.35" stroke-width="0.9" fill="none"/>')
    return h


def pose(o, th_f, sh_f, th_b, sh_b, ua_f, fa_f, ua_b, fa_b, lean=0, bob=0, tilt=0, dx=0):
    dim = 'style="filter: brightness(0.62)"'
    ank_b = -(th_b + sh_b) + 0.4 * th_b + o.get('_ankb', 0)
    ank_f = -(th_f + sh_f) + 0.4 * th_f + o.get('_ankf', 0)
    back_leg = f'<g {dim}>' + rot(th_b, HIP, thigh(o) + rot(sh_b, KNEE, shin(o, ank_b))) + '</g>'
    front_leg = rot(th_f, HIP, thigh(o) + rot(sh_f, KNEE, shin(o, ank_f)))
    if o.get('_arm'):
        ua_f, fa_f = o['_arm']
    elif o.get('coffee') and not o.get('_free'):
        ua_f, fa_f = -6 + ua_f * 0.15, -92
    ob = dict(o, _front=bool(o.get('_cupback')), _cupang=-(ua_b + fa_b + lean))
    back_arm = f'<g {dim}>' + rot(ua_b, SHO, upper_arm(o) + rot(fa_b, ELB, forearm(ob))) + '</g>'
    of = dict(o, _front=not o.get('_free'), _cupang=-(ua_f + fa_f + lean) + o.get('_cuptilt', 0))
    front_arm = rot(ua_f, SHO, upper_arm(o) + rot(fa_f, ELB, forearm(of)))
    pack = ''
    if o.get('backpack'):
        pack = ('<path d="M38 70 Q38 64 45 63 L58 63 L58 140 L45 140 Q38 140 38 133 Z" fill="url(#bp)"/>'
                '<path d="M40 96 L57 96 L57 128 L40 128 Z" fill="#000" fill-opacity="0.2"/><path d="M40 96 L57 96" stroke="#3a2410" stroke-width="1.2"/>'
                '<path d="M39 72 Q38.5 100 39.5 132" stroke="#a9bad0" stroke-opacity="0.45" stroke-width="1.4" fill="none"/>')
    arm_shadow = (f'<g opacity="0.45" filter="url(#soft)">' + rot(ua_f, SHO, '<path d="M62 64 L80 64 L81 156 L65 156 Z" fill="#000"/>') + '</g>') if abs(ua_f) < 25 else ''
    body_back = rot(lean, HIP, back_arm)
    strap = ('<path d="M62 60 Q76 64 80 78 Q82 96 76 122" stroke="#3a2410" stroke-width="3.6" fill="none"/>'
             '<path d="M62 60 Q76 64 80 78" stroke="#ffffff" stroke-opacity="0.15" stroke-width="1" fill="none"/>') if o.get('backpack') else ''
    body = rot(lean, HIP, pack + torso(o) + strap + rot(tilt, NECKP, head(o)) + arm_shadow + front_arm)
    ground = f'<ellipse cx="{76 + dx}" cy="298" rx="{o.get("_shadow", 30)}" ry="3.2" fill="#000" fill-opacity="0.45" filter="url(#soft1)"/>'
    return (defs(o) + o.get('_under', '') + ground + f'<g transform="translate({dx} {bob:.2f})">' + back_leg + body_back + front_leg + body + '</g>'
            + o.get('_extra', ''))


def stand(o):
    return pose(o, -3, 2, 5, 0, -2, -6, 6, -4)


def walk(o, ph):
    s = math.sin(2 * math.pi * ph)
    c = math.cos(2 * math.pi * ph)
    th_f, th_b = -24 * s, 24 * s
    sh_f = 34 * max(0, math.sin(2 * math.pi * ph + 1.25)) + 3
    sh_b = 34 * max(0, math.sin(2 * math.pi * ph + 1.25 + math.pi)) + 3
    ua_f, ua_b = 20 * s, -20 * s
    fa_f, fa_b = -14 - 10 * max(0, s), -14 - 10 * max(0, -s)
    bob = -2.6 * abs(c)
    return pose(o, th_f, sh_f, th_b, sh_b, ua_f, fa_f, ua_b, fa_b, lean=3, bob=bob)


def svg(inner, w, h, mirror=False):
    m = '<g transform="translate(240 0) scale(-1 1)">' if mirror else '<g>'
    return (f'<svg width="{w}" height="{h}" viewBox="0 0 240 386.667" style="display:block; overflow: hidden">'
            f'{m}<g transform="translate(40 26.667)">{inner}</g></g></svg>')


BOMBER = dict(kind='bomber', jacket='#45523c', jacketl='#66765a', jacketd='#26301f', denim='#232428', denim_l='#3a3c42', denim_d='#121316',
              skin='#8d5f43', skin_l='#a8765a', skin_d='#5f3c28', hair='#120d0a', hairstyle='cap', hat='#9a1f2a', hatl='#c23a46', hatd='#5a0f16',
              shoe='high', accent='#2a2b30', backpack=True)
DENIM = dict(kind='denim', jacket='#4c6e94', jacketl='#6f92b8', jacketd='#2e4a6a', denim='#2a2b2f', denim_l='#41434a', denim_d='#16171a',
             skin='#d7b99c', skin_l='#ecd2b6', skin_d='#a3836a', hair='#6b4a2a', hairstyle='beanie', hat='#b5762e', hatl='#d69a4a', hatd='#7a4c1a',
             shoe='boot', accent='#000', coffee=True)
TRACK = dict(kind='track', jacket='#26305a', jacketl='#3c4a80', jacketd='#151b36', denim='#26272c', denim_l='#3b3d44', denim_d='#121317',
             skin='#b58466', skin_l='#cf9c7c', skin_d='#7f5641', hair='#1a1411', hairstyle='curly', accent='#2a6bd4')
HOODIE = dict(kind='hoodie', jacket='#4b525d', jacketl='#6c7480', jacketd='#2c3038', denim='#34507a', denim_l='#4d6c96', denim_d='#1e3150',
              skin='#c49a7a', skin_l='#dcb595', skin_d='#8f6a52', hair='#2a2019', hairstyle='short', phones=True, accent='#c8102e')

OUTFITS = dict(A=HOODIE, B=BOMBER, C=DENIM, D=TRACK)

if __name__ == '__main__':
    R.JOBS.clear()
    for k, o in OUTFITS.items():
        R.job(f'{k}_big_stand', svg(stand(o), 376, 604), 376, 604)
        R.job(f'{k}_big_walk', svg(walk(o, 3 / 12), 376, 604), 376, 604)
        R.job(f'{k}_stand', svg(stand(o), 100, 161), 100, 161)
        for i in range(12):
            R.job(f'{k}_walk_{i:02d}', svg(walk(o, i / 12), 100, 161), 100, 161)
    asyncio.run(R.main())
    print('ok')
