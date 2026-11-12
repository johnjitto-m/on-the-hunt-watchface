"""Two illustration styles of the original Specter character (front view, viewBox 0 0 140 300)."""

HAIR = 'M56.6 23 Q55 6 70 4.5 Q85 6 83.4 23 Q83 14 80 11.5 Q72 8.5 64 10.5 Q58 13 57.6 23 Z'
TAIL = 'M56 30 Q51 38 52 48 Q50 62 46 76 Q44 90 47 104 Q50 96 52 84 Q55 70 56 56 Q58 44 59 36 Z'
FACE = 'M57.5 19 Q57.5 9 70 9 Q82.5 9 82.5 19 L82.5 30 Q81.5 40 74 44.5 L66 44.5 Q58.5 40 57.5 30 Z'
NECK = 'M64 41 L76 41 L77 55 L63 55 Z'
JACKET = 'M37 66 Q49 57 60 54 L70 58 L80 54 Q91 57 103 66 L105 120 L103 176 L70 182 L37 176 L35 120 Z'
ARM_L = 'M36 68 C28 100 29 140 32 166 L43 166 C43 130 46 106 50 88 Z'
ARM_R = 'M104 68 C112 100 111 140 108 166 L97 166 C97 130 94 106 90 88 Z'
COLLAR = 'M58 50 L70 56 L82 50 L83 60 L70 64 L57 60 Z'
LEG_L = 'M54 178 C53 226 53 262 53 290 L66 290 C66.5 262 68 232 70 200 Z'
LEG_R = 'M86 178 C87 226 87 262 87 290 L74 290 C73.5 262 72 232 70 200 Z'
BOOT_L = 'M48 284 L67 284 L67 297 L45 297 Q45 290 48 284 Z'
BOOT_R = 'M92 284 L73 284 L73 297 L95 297 Q95 290 92 284 Z'
GUN = 'M98 168 L110 168 L110 178 L107 178 L108 208 L100 208 L100 178 L98 178 Z'
ALL = [HAIR, TAIL, FACE, NECK, JACKET, ARM_L, ARM_R, COLLAR, LEG_L, LEG_R, BOOT_L, BOOT_R, GUN]


def p(d, **a):
    attrs = ' '.join(f'{k.replace("_", "-")}="{v}"' for k, v in a.items())
    return f'<path d="{d}" {attrs}></path>'


def flat():
    """Bold flat vector, faceless, with a sticker-style light outline."""
    out = ''.join(p(d, fill='#f4f1ea', stroke='#f4f1ea', stroke_width=7, stroke_linejoin='round') for d in ALL)
    out += '<ellipse cx="37" cy="171" rx="7" ry="9" fill="#f4f1ea"></ellipse><ellipse cx="103" cy="171" rx="7" ry="9" fill="#f4f1ea"></ellipse>'
    out += p('M52 174 L88 174 L72 212 L68 212 Z', fill='#0b0b0d')
    out += p(LEG_L, fill='#0b0b0d') + p(LEG_R, fill='#0b0b0d') + p(BOOT_L, fill='#000') + p(BOOT_R, fill='#000')
    out += p(ARM_L, fill='#000') + p(ARM_R, fill='#000') + p(JACKET, fill='#000')
    out += p('M70 64 L70 182', stroke='#f4f1ea', stroke_width=1.6) + p('M44 96 L62 96 M78 96 L96 96', stroke='#f4f1ea', stroke_width=1.4)
    out += p('M37 170 L103 170', stroke='#f4f1ea', stroke_width=1.4)
    out += p(COLLAR, fill='#000', stroke='#f4f1ea', stroke_width=1.4, stroke_linejoin='round')
    out += p(NECK, fill='#d9b9a3') + p(FACE, fill='#f2d6c4')
    out += p('M57.5 30 Q60 40 66 44.5 L70 44.5 L70 30 Z', fill='#e2c2ad')
    out += p(HAIR, fill='#000') + p(TAIL, fill='#000')
    out += '<ellipse cx="37" cy="171" rx="5.5" ry="7.5" fill="#000"></ellipse><ellipse cx="103" cy="171" rx="5.5" ry="7.5" fill="#000"></ellipse>'
    out += p(GUN, fill='#000')
    return out


def ink():
    """Inverse ink line art: pale strokes with cross-hatched shadows on black."""
    L = '#e9e4d8'
    out = p('M52 174 L88 174 L72 212 L68 212 Z', fill='#050506')
    out += ''.join(p(d, fill='#050506', stroke=L, stroke_width=1.5, stroke_linejoin='round') for d in
                  [LEG_L, LEG_R, BOOT_L, BOOT_R, ARM_L, ARM_R, JACKET, COLLAR, NECK, FACE])
    hatch = []
    for i in range(0, 60, 4):   # shadow side of jacket
        hatch.append(f'M{88 + i * 0.25} {68 + i * 1.8} L{103 - i * 0.05} {60 + i * 1.8}')
    for i in range(0, 40, 4):   # right leg shadow
        hatch.append(f'M{76 + i * 0.1} {206 + i * 2} L{86} {200 + i * 2}')
    for i in range(0, 30, 3):   # face shadow
        hatch.append(f'M{74 + i * 0.1} {14 + i} L{82} {12 + i}')
    out += ''.join(p(h, stroke=L, stroke_width=0.6, opacity=0.7) for h in hatch)
    out += p('M70 64 L70 182', stroke=L, stroke_width=1) + p('M44 96 L62 96 L62 112 L44 112 Z M78 96 L96 96 L96 112 L78 112 Z', fill='none', stroke=L, stroke_width=0.8)
    out += p('M37 170 L103 170', stroke=L, stroke_width=1.2)
    out += p('M61 24 L67 25.4 M73 25.4 L79 24', stroke=L, stroke_width=1.3, stroke_linecap='round')
    out += p('M70 28 L68.6 35 L71 35.4', stroke=L, stroke_width=0.8, fill='none') + p('M66.5 39.4 L73.5 39.4', stroke=L, stroke_width=0.9)
    out += p(HAIR, fill='#050506', stroke=L, stroke_width=1.3) + p(TAIL, fill='#050506', stroke=L, stroke_width=1.2)
    out += p('M60.5 11.5 Q70 6.5 80 10.5 M62.5 8.8 Q70 5.6 77.5 7.8 M53 44 Q51 62 48 84 M55 46 Q54 64 50 92', stroke=L, stroke_width=0.6, fill='none')
    out += f'<ellipse cx="37" cy="171" rx="5.5" ry="7.5" fill="#050506" stroke="{L}" stroke-width="1.2"></ellipse><ellipse cx="103" cy="171" rx="5.5" ry="7.5" fill="#050506" stroke="{L}" stroke-width="1.2"></ellipse>'
    out += p(GUN, fill='#050506', stroke=L, stroke_width=1.2)
    return out
