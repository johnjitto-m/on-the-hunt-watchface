"""SVG backdrops (480x96 band, ground at y=96) for the v2 demo."""
import random


def close(s):
    import re
    return re.sub(r'<(path|circle|ellipse|polyline|line|rect|polygon|text)([^>]*?)/>', r'<\1\2></\1>', s)


def hotel():
    random.seed(21)
    far, near = [], []
    # neighbouring dim buildings
    for x, w, h in [(-40, 60, 58), (22, 46, 70), (70, 38, 50), (372, 40, 54), (414, 50, 72), (466, 60, 48)]:
        far.append(f'<rect x="{x}" y="{96 - h}" width="{w}" height="{h}" fill="#0d0e11" stroke="#17181c" stroke-width="1"/>')
    # wings
    for x in (112, 330):
        near.append(f'<rect x="{x}" y="30" width="38" height="66" fill="#14130f" stroke="#2c2719" stroke-width="1"/>')
        for wy in range(38, 88, 11):
            for wx in range(x + 6, x + 34, 10):
                near.append(f'<rect x="{wx}" y="{wy}" width="5" height="7" rx="2.5" fill="{{{{winColor}}}}" opacity="{random.choice([0.35, 0.6, 1])}"/>')
    # main block
    near.append('<rect x="150" y="10" width="180" height="86" fill="#17150f" stroke="#3a321c" stroke-width="1"/>')
    near.append('<rect x="146" y="8" width="188" height="4" fill="#3a321c"/>')
    near.append('<polygon points="200,8 240,-6 280,8" fill="#17150f" stroke="#3a321c" stroke-width="1"/>')
    near.append('<circle cx="240" cy="2" r="3" fill="none" stroke="#d4af37" stroke-width="1"/>')
    for fx in (196, 284):
        near.append(f'<line x1="{fx}" y1="8" x2="{fx}" y2="-10" stroke="#3a321c" stroke-width="1"/><rect x="{fx}" y="-10" width="9" height="5" fill="#5a1016"/>')
    for row, wy in enumerate(range(18, 64, 10)):
        for wx in range(160, 322, 13):
            if 222 <= wx <= 252 and wy > 50: continue
            near.append(f'<rect x="{wx}" y="{wy}" width="6" height="8" rx="3" fill="{{{{winColor}}}}" opacity="{random.choice([0.3, 0.5, 0.8, 1])}"/>')
    for cx in (160, 320):
        near.append(f'<rect x="{cx - 2}" y="12" width="4" height="84" fill="#211d12"/>')
    # entrance
    near.append('<path d="M226 96 L226 78 Q240 64 254 78 L254 96 Z" fill="#ffcf7a" opacity="0.85"/>')
    near.append('<rect x="212" y="68" width="56" height="5" fill="#d4af37"/>')
    near.append('<text x="240" y="64" text-anchor="middle" font-family="Bodoni Moda, serif" font-size="8" letter-spacing="2" fill="#d4af37">HOTEL</text>')
    for lx in (206, 274):
        near.append(f'<circle cx="{lx}" cy="80" r="2.5" fill="#ffcf7a"/><circle cx="{lx}" cy="80" r="7" fill="#ffcf7a" opacity="0.25"/>')
    return close(''.join(far)), close(''.join(near))


def club():
    far = ['<rect x="-40" y="0" width="560" height="96" fill="#0b0a10"/>']
    for x in range(-40, 520, 24):
        far.append(f'<line x1="{x}" y1="0" x2="{x}" y2="96" stroke="#121019" stroke-width="1"/>')
    near = []
    glow = 'style="filter: blur(3px)"'
    shapes = [('#ff2bd6', 'M60 30 L120 30 L120 70 L60 70 Z'), ('#29e6ff', 'M150 50 L170 30 L190 50 L210 30 L230 50'),
              ('#ff2bd6', 'M262 26 L262 72'), ('#29e6ff', 'M290 40 Q320 10 350 40 Q380 70 410 40'), ('#ff2bd6', 'M430 30 L470 30')]
    for col, d in shapes:
        near.append(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="6" opacity="0.45" {glow}/>')
        near.append(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="1.6" style="animation: hneon 5s linear infinite"/>')
    near.append('<rect x="-40" y="92" width="560" height="4" fill="#ff2bd6" opacity="0.18"/>')
    beams = ''.join(f'<polygon points="{x},0 {x - 26},96 {x + 26},96" fill="url(#beam)" style="transform-origin: {x}px 0px; animation: hbeam {4 + i}s ease-in-out infinite alternate"/>'
                    for i, x in enumerate((140, 250, 360)))
    defs = '<defs><linearGradient id="beam" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffffff" stop-opacity="0.22"/><stop offset="1" stop-color="#ffffff" stop-opacity="0"/></linearGradient></defs>'
    return close(''.join(far)), close(defs + beams + ''.join(near))


def rain():
    random.seed(9)
    far = []
    x = -40
    while x < 520:
        w = random.randint(20, 36); h = random.randint(40, 90)
        far.append(f'<rect x="{x}" y="{96 - h}" width="{w}" height="{h}" fill="#0c0d10" stroke="#15161a" stroke-width="1"/>')
        for wy in range(96 - h + 6, 90, 8):
            for wx in range(x + 4, x + w - 3, 6):
                if random.random() < 0.08:
                    far.append(f'<rect x="{wx}" y="{wy}" width="2" height="3" fill="{{{{winColor}}}}" opacity="0.6"/>')
        x += w + 2
    near = ['<defs><linearGradient id="cone" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffcf7a" stop-opacity="0.35"/><stop offset="1" stop-color="#ffcf7a" stop-opacity="0"/></linearGradient></defs>']
    for lx in (90, 250, 410):
        near.append(f'<polygon points="{lx},18 {lx - 34},96 {lx + 34},96" fill="url(#cone)"/>')
        near.append(f'<rect x="{lx - 1}" y="14" width="2" height="82" fill="#26272c"/><path d="M{lx - 8} 16 L{lx + 8} 16 L{lx + 4} 20 L{lx - 4} 20 Z" fill="#26272c"/><circle cx="{lx}" cy="20" r="2" fill="#ffcf7a"/>')
        near.append(f'<ellipse cx="{lx}" cy="95" rx="30" ry="2.5" fill="#ffcf7a" opacity="0.25"/>')
    drops = ''.join(f'<line x1="{random.randint(-40, 520)}" y1="{random.randint(-30, 90)}" x2="0" y2="0" stroke="#9aa3b5" stroke-width="0.8" opacity="0.45"/>' for _ in range(0))
    lines = []
    for _ in range(70):
        x0 = random.randint(-40, 520); y0 = random.randint(-40, 96)
        lines.append(f'<line x1="{x0}" y1="{y0}" x2="{x0 - 3}" y2="{y0 + 10}" stroke="#9aa3b5" stroke-width="0.8" opacity="0.45"/>')
    rainy = f'<g style="animation: hrain 0.45s linear infinite">{"".join(lines)}</g>'
    return close(''.join(far)), close(''.join(near))


def subway():
    far = ['<rect x="-40" y="0" width="560" height="96" fill="#0f1012"/>']
    for y in range(4, 96, 8):
        far.append(f'<line x1="-40" y1="{y}" x2="520" y2="{y}" stroke="#16171a" stroke-width="1"/>')
    for x in range(-40, 520, 12):
        far.append(f'<line x1="{x}" y1="0" x2="{x}" y2="96" stroke="#141518" stroke-width="1"/>')
    far.append('<rect x="-40" y="44" width="560" height="6" fill="#4a0e14"/>')
    far.append('<rect x="190" y="22" width="100" height="16" fill="#0a0a0b" stroke="#3a3a40" stroke-width="1"/>')
    far.append('<text x="240" y="33.5" text-anchor="middle" font-family="Oswald, sans-serif" font-size="9" letter-spacing="2" fill="#d6d6da">UPTOWN ⟶</text>')
    near = []
    for x in range(10, 480, 92):
        near.append(f'<rect x="{x}" y="0" width="14" height="96" fill="#18191c" stroke="#2a2b30" stroke-width="1"/>')
    for x in range(56, 480, 92):
        near.append(f'<circle cx="{x}" cy="4" r="2.5" fill="#f2efe6"/><circle cx="{x}" cy="4" r="9" fill="#f2efe6" opacity="0.12"/>')
    near.append('<rect x="-40" y="90" width="560" height="6" fill="#d4af37" opacity="0.35"/>')
    near.append('<g style="animation: htrain 7s linear infinite"><rect x="-220" y="56" width="200" height="26" rx="3" fill="#ffffff" opacity="0.10" style="filter: blur(4px)"/><rect x="-220" y="66" width="200" height="4" fill="#fff3c4" opacity="0.35" style="filter: blur(2px)"/></g>')
    return close(''.join(far)), close(''.join(near))


def noir():
    """Taller noir city: 480 x 168 band, ground at y=168."""
    random.seed(31)
    far = []
    x = -40
    while x < 520:
        w = random.randint(26, 46); h = random.randint(80, 150)
        far.append(f'<rect x="{x}" y="{168 - h}" width="{w}" height="{h}" fill="#0b0c0f" stroke="#15161b" stroke-width="1"/>')
        if random.random() < 0.5:
            sw = w - 12; sh = random.randint(14, 26)
            far.append(f'<rect x="{x + 6}" y="{168 - h - sh}" width="{sw}" height="{sh}" fill="#0b0c0f" stroke="#15161b" stroke-width="1"/>')
            if random.random() < 0.6:
                far.append(f'<line x1="{x + w / 2}" y1="{168 - h - sh}" x2="{x + w / 2}" y2="{168 - h - sh - 16}" stroke="#1c1d23" stroke-width="1"/>')
        for wy in range(168 - h + 6, 160, 9):
            for wx in range(x + 5, x + w - 4, 7):
                if random.random() < 0.05:
                    far.append(f'<rect x="{wx}" y="{wy}" width="2" height="3" fill="{{{{winColor}}}}" opacity="0.45"/>')
        x += w + random.randint(2, 8)
    # distant suspension bridge (right side)
    far.append('<g stroke="#1e2027" stroke-width="1" fill="none">')
    for tx in (318, 430):
        far.append(f'<rect x="{tx}" y="70" width="8" height="70" fill="#101116"/>')
        far.append(f'<line x1="{tx}" y1="84" x2="{tx + 8}" y2="84"/><line x1="{tx}" y1="100" x2="{tx + 8}" y2="100"/>')
    far.append('<path d="M240 136 Q280 96 322 72 Q376 128 434 72 Q470 96 520 116"/>')
    for cx in range(250, 520, 10):
        far.append(f'<line x1="{cx}" y1="{136}" x2="{cx}" y2="{130}"/>')
    far.append('<line x1="230" y1="136" x2="520" y2="136" stroke="#23252c" stroke-width="2"/></g>')
    for cx in range(240, 520, 14):
        far.append(f'<circle cx="{cx}" cy="134" r="0.9" fill="{{{{winColor}}}}" opacity="0.7"/>')

    near = []
    x = -40
    idx = 0
    while x < 520:
        w = random.randint(34, 52); h = random.randint(38, 74)
        top = 168 - h
        near.append(f'<rect x="{x}" y="{top}" width="{w}" height="{h}" fill="#121216" stroke="#23242a" stroke-width="1"/>')
        near.append(f'<rect x="{x - 2}" y="{top}" width="{w + 4}" height="3" fill="#1d1e24"/>')
        for wy in range(top + 8, 156, 11):
            for wx in range(x + 6, x + w - 6, 9):
                near.append(f'<rect x="{wx}" y="{wy}" width="4" height="6" fill="{{{{winColor}}}}" opacity="{random.choice([0.0, 0.0, 0.25, 0.5, 0.9])}"/>')
        if idx % 2 == 0:  # fire escape
            fx = x + w - 16
            pts = []
            for i, fy in enumerate(range(top + 12, 150, 12)):
                near.append(f'<line x1="{fx - 2}" y1="{fy}" x2="{fx + 14}" y2="{fy}" stroke="#2c2d34" stroke-width="1"/>')
                a, b = (fx, fx + 12) if i % 2 == 0 else (fx + 12, fx)
                near.append(f'<line x1="{a}" y1="{fy}" x2="{b}" y2="{fy + 12}" stroke="#2c2d34" stroke-width="0.8"/>')
        if idx % 3 == 1:  # rooftop water tower
            wx = x + 8
            near.append(f'<rect x="{wx}" y="{top - 16}" width="12" height="11" rx="2" fill="#16171b" stroke="#2a2b31" stroke-width="1"/>'
                        f'<path d="M{wx - 1} {top - 16} L{wx + 6} {top - 21} L{wx + 13} {top - 16} Z" fill="#16171b" stroke="#2a2b31" stroke-width="1"/>'
                        f'<line x1="{wx + 2}" y1="{top - 5}" x2="{wx}" y2="{top}" stroke="#2a2b31"/><line x1="{wx + 10}" y1="{top - 5}" x2="{wx + 12}" y2="{top}" stroke="#2a2b31"/>')
        x += w + random.randint(0, 3)
        idx += 1
    # street lamps
    for lx in (150, 330):
        near.append(f'<rect x="{lx - 1}" y="120" width="2" height="48" fill="#26272c"/><path d="M{lx - 6} 120 L{lx + 6} 120 L{lx + 3} 124 L{lx - 3} 124 Z" fill="#26272c"/>'
                    f'<circle cx="{lx}" cy="124" r="1.8" fill="#ffcf7a"/><circle cx="{lx}" cy="126" r="9" fill="#ffcf7a" opacity="{{{{lampGlow}}}}"/>')
    # classic black muscle car (original design), parked left, facing right
    near.append('<g transform="translate(14 132)">'
                '<path d="M2 26 L3 18 Q4 14 12 13 L30 12 L42 3 Q46 1 54 1 L66 1 Q72 2 76 6 L84 12 L104 13 Q110 14 111 19 L111 26 Z" fill="#0d0d10" stroke="#9a968c" stroke-width="1"/>'
                '<path d="M45 5 L54 3 L54 12 L36 12 Z M57 3 L66 3 Q70 4 73 7 L78 12 L57 12 Z" fill="#1d2129" stroke="#3a3d45" stroke-width="0.6"/>'
                '<line x1="6" y1="19" x2="108" y2="19" stroke="#c9c5bb" stroke-width="0.8" opacity="0.7"/>'
                '<rect x="104" y="15" width="6" height="3" rx="1" fill="#ffd98a"/><ellipse cx="118" cy="17" rx="12" ry="4" fill="#ffd98a" opacity="{{lampGlow}}"/>'
                '<rect x="2" y="15" width="4" height="3" fill="#c8102e"/>'
                '<circle cx="24" cy="27" r="7" fill="#050506" stroke="#6f6b65" stroke-width="1"/><circle cx="24" cy="27" r="3" fill="#2a2b30" stroke="#b5b1a8" stroke-width="0.8"/>'
                '<circle cx="90" cy="27" r="7" fill="#050506" stroke="#6f6b65" stroke-width="1"/><circle cx="90" cy="27" r="3" fill="#2a2b30" stroke="#b5b1a8" stroke-width="0.8"/>'
                '</g>')
    return close(''.join(far)), close(''.join(near))


DOG = close('<svg aria-hidden="true" width="30" height="26" viewBox="-3 -4 30 26" style="overflow: visible">'
            '<g fill="#26221f" stroke="#cfcac0" stroke-width="1.1" stroke-linejoin="round">'
            '<path d="M1 19 Q-3 16 0 11" fill="none"/>'
            '<ellipse cx="7" cy="15.5" rx="7" ry="5.5"/>'
            '<path d="M5 10 Q9 3 16 5 L18.5 13 L19 21 L11 21 Z"/>'
            '<rect x="14.5" y="12" width="2.4" height="9.5" rx="1"/><rect x="17.4" y="12" width="2.4" height="9.5" rx="1"/>'
            '<path d="M13 1 L14.5 -3.5 L16.5 1 Z"/>'
            '<ellipse cx="17" cy="4" rx="4.6" ry="3.8"/>'
            '<path d="M20 3 L25.5 4.5 L25 7.5 L20 7.5 Z"/>'
            '</g><circle cx="18.2" cy="3" r="0.8" fill="#cfcac0"/><circle cx="25.3" cy="5" r="0.9" fill="#0b0b0c"/>'
            '<path d="M15 9.5 L20 9.5" stroke="#c8102e" stroke-width="1.4"/></svg>')


DOGWALK = close('<svg aria-hidden="true" width="34" height="26" viewBox="-4 -4 34 26" style="overflow: visible">'
    '<g style="animation: hbob 0.45s ease-in-out infinite">'
    '<g fill="#26221f" stroke="#cfcac0" stroke-width="1.1" stroke-linejoin="round">'
    '<g transform="translate(5 13)"><g style="animation: hdogA 0.45s ease-in-out infinite"><rect x="-1.2" y="0" width="2.4" height="8.5" rx="1"/></g></g>'
    '<g transform="translate(19 13)"><g style="animation: hdogB 0.45s ease-in-out infinite"><rect x="-1.2" y="0" width="2.4" height="8.5" rx="1"/></g></g>'
    '<path d="M0 9 Q-4 6 -3 2" fill="none"/>'
    '<path d="M0 8 Q2 5 8 5 L18 5 Q22 5 22 9 L21 14 L1 14 Z"/>'
    '<g transform="translate(8 13)"><g style="animation: hdogB 0.45s ease-in-out infinite"><rect x="-1.2" y="0" width="2.4" height="8.5" rx="1"/></g></g>'
    '<g transform="translate(22 13)"><g style="animation: hdogA 0.45s ease-in-out infinite"><rect x="-1.2" y="0" width="2.4" height="8.5" rx="1"/></g></g>'
    '<path d="M19 1 L20.5 -3.5 L22.5 1 Z"/>'
    '<ellipse cx="23" cy="3.5" rx="4.6" ry="3.8"/>'
    '<path d="M26 2.5 L31.5 4 L31 7 L26 7 Z"/>'
    '</g><circle cx="24.2" cy="2.6" r="0.8" fill="#cfcac0"/><circle cx="31.3" cy="4.6" r="0.9" fill="#0b0b0c"/>'
    '<path d="M20 7 L21.5 10" stroke="#c8102e" stroke-width="1.4"/></g></svg>')


DOGALERT = close('<svg aria-hidden="true" width="30" height="26" viewBox="-3 -4 30 26" style="overflow: visible">'
    '<g fill="#26221f" stroke="#cfcac0" stroke-width="1.1" stroke-linejoin="round">'
    '<path d="M1 19 Q-4 13 -1 8" fill="none" style="transform-origin: 1px 19px; animation: hwag 0.35s ease-in-out infinite"/>'
    '<ellipse cx="7" cy="15.5" rx="7" ry="5.5"/>'
    '<path d="M5 10 Q9 2 16 3 L18.5 13 L19 21 L11 21 Z"/>'
    '<rect x="14.5" y="12" width="2.4" height="9.5" rx="1"/><rect x="17.4" y="12" width="2.4" height="9.5" rx="1"/>'
    '<g style="transform-origin: 17px 3px; animation: hperk 1.6s ease-in-out infinite">'
    '<path d="M13.2 -0.5 L13.8 -7 L16.6 -0.8 Z"/><path d="M17.4 -0.8 L19.6 -7 L20.6 -0.4 Z"/>'
    '<ellipse cx="17" cy="2.2" rx="4.8" ry="4"/>'
    '<path d="M19.8 1.2 L24.5 2.4 L24 5.4 L19.8 5.6 Z"/></g>'
    '</g><circle cx="17.6" cy="1.2" r="0.9" fill="#ffffff"/><circle cx="24.3" cy="3" r="0.9" fill="#0b0b0c"/>'
    '<path d="M15 9.5 L20 9.5" stroke="#c8102e" stroke-width="1.4"/>'
    '<g style="animation: halert 1.2s ease-in-out infinite"><circle cx="21" cy="-12" r="5.5" fill="#ffc83a" stroke="#000000" stroke-width="0.8"/>'
    '<rect x="20.2" y="-15.4" width="1.6" height="4" rx="0.8" fill="#111111"/><circle cx="21" cy="-9.4" r="0.95" fill="#111111"/></g>'
    '</svg>')


def noir_signs():
    near = []
    # neon signs high on the edges, clear of the walking path and the text
    near.append('<rect x="22" y="22" width="15" height="46" rx="2" fill="#0a0a0c" stroke="{{neonColor}}" stroke-width="1"/>')
    near.append('<rect x="17" y="17" width="25" height="56" fill="{{neonColor}}" opacity="{{neonGlow}}" style="filter: blur(6px)"/>')
    for i, ch in enumerate('BAR'):
        near.append(f'<text x="29.5" y="{38 + i * 13}" text-anchor="middle" font-family="Oswald, sans-serif" font-size="11" font-weight="500" fill="{{{{neonColor}}}}" style="animation: hneon 4s linear infinite">{ch}</text>')
    near.append('<rect x="440" y="26" width="15" height="62" rx="2" fill="#0a0a0c" stroke="#e3c463" stroke-width="1"/>')
    near.append('<rect x="435" y="21" width="25" height="72" fill="#e3c463" opacity="{{neonGlow}}" style="filter: blur(6px)"/>')
    for i, ch in enumerate('HOTEL'):
        near.append(f'<text x="447.5" y="{39 + i * 11.5}" text-anchor="middle" font-family="Bodoni Moda, serif" font-size="10" font-weight="600" fill="#e3c463">{ch}</text>')
    return close(''.join(near))


DOGHAPPY = (DOGWALK.replace('animation: hbob 0.45s ease-in-out infinite', 'animation: hhop 0.8s ease-in-out infinite')
            .replace('animation: hdogA 0.45s ease-in-out infinite', 'animation: none').replace('animation: hdogB 0.45s ease-in-out infinite', 'animation: none')
            .replace('<path d="M0 9 Q-4 6 -3 2" fill="none"></path>', '<path d="M0 9 Q-4 6 -3 2" fill="none" style="transform-origin: 0px 9px; animation: hwag 0.3s ease-in-out infinite"></path>'))
