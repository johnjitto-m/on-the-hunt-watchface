"""Full-colour poses of the original Specter (tactical jacket, tied-back long hair) on the shared rig."""
import re
import characters as C

RIM = '#d9d4c8'; RIMB = '#6f6b65'
JACKET = '#202227'; JACKETB = '#121317'; PANTS = '#16171b'; PANTSB = '#0e0f12'
SKIN = '#cdb8a4'; SKIND = '#8c7766'; HAIR = '#141418'; BLK = '#060607'; GLOVE = '#0b0b0d'
HIP = (71, 196); KNEE = (71, 244); SH = (70, 72)


def g(fill, inner, rim=RIM, sw=3.0):
    return f'<g fill="{fill}" stroke="{rim}" stroke-width="{sw}" stroke-linejoin="round" stroke-linecap="round">{inner}</g>'


def rot(a, cx, cy, inner):
    return f'<g transform="rotate({a:.2f} {cx} {cy})">{inner}</g>'


def nest(x, y, anim, inner):
    return (f'<g transform="translate({x} {y})"><g style="animation: {anim}">'
            f'<g transform="translate({-x} {-y})">{inner}</g></g></g>')


def thigh(back=False):
    return g(PANTSB if back else PANTS, '<path d="M61 188 C63 208 65 228 65 248 L78 248 C78 228 80 208 81 188 Z"></path>', rim=RIMB if back else RIM)


def shin(back=False):
    r = RIMB if back else RIM
    return (g(PANTSB if back else PANTS, '<path d="M65 242 L78 242 C78 262 77 276 77 284 L65 284 Z"></path>', rim=r)
            + g(BLK, '<path d="M63 282 L79 282 L93 288 Q96 292 94 297 L62 297 Z"></path>', rim=r, sw=2.4))


HIPS = f'<path d="M56 176 L90 176 L84 202 L60 202 Z" fill="{PANTS}"></path>'
TORSO = (g(JACKET, '<path d="M57 66 C69 61 82 62 87 70 C91 98 90 128 88 150 L90 182 L55 182 C55 160 56 150 55 140 C53 110 53 90 57 66 Z"></path>')
         + '<path d="M60 70 C57 100 57 140 58 178" stroke="#3a3c43" stroke-width="5" fill="none" opacity="0.7"></path>'
         + g('#1a1c20', '<path d="M62 58 L80 60 L82 71 L61 69 Z"></path>', sw=2)
         + '<path d="M86 76 L88.5 180" stroke="#8c887f" stroke-width="1.4"></path>'
         + '<path d="M55 172 L90 172" stroke="#2c2e33" stroke-width="6"></path>'
         + '<path d="M70 96 L84 96 L84 110 L70 110 Z" fill="none" stroke="#3a3c42" stroke-width="1.4"></path>')
NECK = f'<path d="M66 55 L77 55 L78 68 L66 68 Z" fill="{SKIND}"></path>'
HEAD = (f'<path d="M60 30 Q60 14 72 13 Q84 13 85 26 L84.5 34 Q86.5 40 87.5 45 L84.5 47 Q84 55 79 59 Q73 61 68 58 Q62 54 61 46 Z" fill="{SKIN}" stroke="{RIM}" stroke-width="1.6"></path>'
        '<path d="M61 46 Q62 54 68 58 L70 40 L62 36 Z" fill="#a8927d"></path>'
        '<path d="M76.5 28 L83.5 27" stroke="#1d1714" stroke-width="2" stroke-linecap="round"></path>'
        '<path d="M78 31.5 L82.5 31.6" stroke="#120e0c" stroke-width="1.8" stroke-linecap="round"></path>'
        '<path d="M75 52 L80.5 52.5" stroke="#4a382e" stroke-width="1.4"></path>'
        f'<ellipse cx="66" cy="37" rx="2.4" ry="4" fill="#a8927d"></ellipse>'
        + g(HAIR, '<path d="M58.5 33 Q56.5 13 71 10.5 Q85 10 86.5 24 Q80 16.5 71 16.5 Q63.5 17.5 62 31 Z"></path>', rim='#55555c', sw=1.4)
        + '<path d="M64 13.5 Q72 11 82 15.5 M62 18 Q68 14.5 76 14" stroke="#5c5c64" stroke-width="1" fill="none"></path>')
TAIL = g(HAIR, '<path d="M60 28 Q52 34 53 46 Q52 58 49.5 72 Q55 64 57 53 Q59 41 62.5 34 Z"></path>', rim='#55555c', sw=1.4)
BACKARM = g(JACKETB, '<path d="M66 72 L77 71 L86 104 L104 98 L106 107 L81 115 Z"></path>', rim=RIMB)
FRONTARM = (g(JACKET, '<path d="M61 74 L75 72 L86 106 L107 101 L109 111 L81 120 Z"></path>')
            + '<path d="M66 82 L78 112" stroke="#3a3c43" stroke-width="3" opacity="0.7"></path>'
            + g(GLOVE, '<ellipse cx="108" cy="104" rx="6.5" ry="6"></ellipse>', sw=1.8))
PISTOL = g('#0d0d10', '<path d="M104 96 L140 97 L140 105 L104 105 Z"></path><path d="M106 102 L115 103 L112 120 L103 119 Z"></path><path d="M114 105 Q117 110 112 111"></path>', rim='#e6e1d6', sw=2.2)
UPPER = TORSO + NECK + TAIL + HEAD


def walk():
    def leg(back, d):
        return nest(71, 196, f'hthigh 1.8s ease-in-out {d}s infinite',
                    thigh(back) + nest(71, 244, f'hshin 1.8s linear {d}s infinite', shin(back)))
    tail = nest(60, 30, 'hwag 1.8s ease-in-out infinite', TAIL)
    return ('<g style="animation: hbob 0.9s ease-in-out infinite">' + leg(True, -0.9) + HIPS
            + rot(9, *HIP, BACKARM + TORSO + NECK + tail + HEAD + FRONTARM + PISTOL)
            + leg(False, 0) + '</g>')


def kneel():
    return ('<g transform="translate(0 45)">'
            + rot(8, *HIP, thigh(True) + rot(95, *KNEE, shin(True))) + HIPS
            + rot(12, *HIP, BACKARM + UPPER)
            + rot(-82, *HIP, thigh() + rot(84, *KNEE, shin()))
            + rot(12, *HIP, rot(28, *SH, FRONTARM + PISTOL)) + '</g>')


def reload():
    return (rot(5, *HIP, thigh(True) + shin(True)) + HIPS
            + g(JACKETB, '<path d="M64 72 L76 70 L100 124 L92 130 Z"></path>', rim=RIMB)
            + UPPER + rot(-5, *HIP, thigh() + shin())
            + '<g style="animation: hmag 1.6s ease-in-out infinite">'
            + g(BLK, '<path d="M91 114 L99 115 L97 131 L89 130 Z"></path>', rim='#9a968c', sw=1.6)
            + g(GLOVE, '<ellipse cx="95" cy="128" rx="6" ry="5"></ellipse>', sw=1.4) + '</g>'
            + g(JACKET, '<path d="M62 75 L76 72 L101 95 L93 105 Z"></path>')
            + g(GLOVE, '<ellipse cx="98" cy="100" rx="6" ry="5.5"></ellipse>', sw=1.4)
            + g(BLK, '<path d="M93 97 L103 69 L111 71 L101 100 Z"></path><path d="M94 95 L102 98 L99 114 L91 112 Z"></path>', rim='#9a968c', sw=2))


def front():
    s = C.specter_long(uid='fw')
    # holster the pistol: drop the gun from the right hand, add a hip holster under a relaxed hand
    s = s.replace('<path d="M98 168 L110 168 L110 178 L107 178 L108 208 L100 208 L100 178 L98 178 Z" fill="#050506" stroke="#8c887f" stroke-width="1"></path>', '')
    s = s.replace('<path d="M104 182 L104 206" stroke="#3a3b40" stroke-width="0.8"></path>', '')
    holster = ('<path d="M98 176 L109 176 L110 200 L99 200 Z" fill="#0b0b0d" stroke="#8c887f" stroke-width="1"></path>'
               '<path d="M100 170 L107 170 L107.5 177 L100.5 177 Z" fill="#050506" stroke="#8c887f" stroke-width="1"></path>')
    i = s.index('<ellipse cx="37" cy="171"')
    s = s[:i] + holster + s[i:]
    # idle life: eyes/brows glance toward the bounty once, ponytail settles
    a = s.index('<path d="M60.8 22.8'); b = s.index('<path d="M70 27 L68.6')
    s = s[:a] + '<g style="animation: hglance 5s ease-in-out 0.6s 1 both">' + s[a:b] + '</g>' + s[b:]
    t = s.index('<path d="M56 30 Q51 38 52 48')
    t2 = s.index('</path>', t) + 7
    s = s[:t] + '<g style="transform-origin: 57px 32px; animation: hsettle 2.4s ease-out 0.3s 1 both">' + s[t:t2] + '</g>' + s[t2:]
    s = re.sub(r'stroke-width="1\.[23]"', 'stroke-width="3"', s)
    s = s.replace('stroke-width="0.8"', 'stroke-width="2"').replace('stroke-width="0.7"', 'stroke-width="1.6"').replace('stroke-width="1"', 'stroke-width="2.2"')
    return s


def aim():
    arm = (g(JACKET, '<path d="M63 69 L114 72 L114 83 L65 85 Z"></path>') + g(GLOVE, '<ellipse cx="116" cy="77" rx="7" ry="6"></ellipse>', sw=1.6)
           + g('#0d0d10', '<path d="M111 64 L145 64 L145 73 L111 73 Z"></path><path d="M113 70 L123 70 L121 89 L111 89 Z"></path>', rim='#e6e1d6', sw=2.2))
    return (rot(14, *HIP, thigh(True) + rot(6, *KNEE, shin(True))) + HIPS
            + UPPER + rot(-10, *HIP, thigh() + rot(4, *KNEE, shin()))
            + rot(26, *SH, '<g style="animation: hrecoil 4s linear 3">' + arm + '</g>'))


def aim_static(angle=42):
    arm = (g(JACKET, '<path d="M63 69 L114 72 L114 83 L65 85 Z"></path>') + g(GLOVE, '<ellipse cx="116" cy="77" rx="7" ry="6"></ellipse>', sw=1.6)
           + g('#0d0d10', '<path d="M111 64 L145 64 L145 73 L111 73 Z"></path><path d="M113 70 L123 70 L121 89 L111 89 Z"></path>', rim='#e6e1d6', sw=2.2))
    return (rot(14, *HIP, thigh(True) + rot(6, *KNEE, shin(True))) + HIPS
            + UPPER + rot(-10, *HIP, thigh() + rot(4, *KNEE, shin()))
            + rot(angle, *SH, arm))
