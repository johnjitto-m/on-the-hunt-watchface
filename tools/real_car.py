"""Semi-realistic original classic coupe for the city backdrop (parked, facing right).
Local units = watch px. ~112 x 34, wheels touch y=34. Placed with translate(14 132) in the 480x168 band."""


def car(uid='c'):
    d = (f'<defs>'
         f'<linearGradient id="{uid}b" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5d6573"/><stop offset="0.22" stop-color="#262a31"/>'
         f'<stop offset="0.5" stop-color="#121317"/><stop offset="0.78" stop-color="#1c1e23"/><stop offset="1" stop-color="#08080a"/></linearGradient>'
         f'<linearGradient id="{uid}g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#3b4a5e"/><stop offset="0.45" stop-color="#18202b"/>'
         f'<stop offset="0.55" stop-color="#4f5f74"/><stop offset="0.62" stop-color="#1a222d"/><stop offset="1" stop-color="#0e1218"/></linearGradient>'
         f'<linearGradient id="{uid}c" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f2f2f0"/><stop offset="0.5" stop-color="#8d9096"/><stop offset="1" stop-color="#d6d7da"/></linearGradient>'
         f'<radialGradient id="{uid}w" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#d8dadf"/><stop offset="0.55" stop-color="#7c8088"/><stop offset="1" stop-color="#2b2d32"/></radialGradient>'
         f'<radialGradient id="{uid}h" cx="0" cy="0.5" r="1"><stop offset="0" stop-color="#ffe2a0" stop-opacity="0.9"/><stop offset="1" stop-color="#ffe2a0" stop-opacity="0"/></radialGradient>'
         f'<filter id="{uid}s" x="-20%" y="-50%" width="140%" height="200%"><feGaussianBlur stdDeviation="1.4"/></filter>'
         f'</defs>')
    body = ('<ellipse cx="57" cy="34" rx="58" ry="3" fill="#000" fill-opacity="0.65" filter="url(#{u}s)"/>'
            # main body: long hood, notch-back roof
            '<path d="M1.5 27.5 L1.5 19.5 Q2 15.5 8 15 L33 13.6 Q38 13 42 8.5 L48.5 3.2 Q51.5 1.6 58 1.5 L69 1.5 Q74.5 1.8 78.5 5.6 L85.5 12.6 '
            'L104 13.6 Q110.5 14.2 112 18 L112.5 27.5 Q112.5 29.5 110 29.5 L99.5 29.5 A9.5 9.5 0 0 0 80.5 29.5 L33.5 29.5 A9.5 9.5 0 0 0 14.5 29.5 L3.5 29.5 Q1.5 29.5 1.5 27.5 Z" fill="url(#{u}b)"/>'
            # side glass
            '<path d="M44.5 12.4 L50.5 5.2 Q52.5 3.6 57 3.5 L57.5 12.4 Z" fill="url(#{u}g)"/>'
            '<path d="M60 3.5 L68.5 3.5 Q73 3.8 76 6.8 L81.5 12.5 L60 12.5 Z" fill="url(#{u}g)"/>'
            '<path d="M57.5 3.4 L60 3.4 L60 12.6 L57.5 12.6 Z" fill="#0a0b0d"/>'
            '<path d="M44 12.6 L50.3 5 Q52.5 3.3 57 3.2 L69 3.2 Q73.5 3.5 76.5 6.6 L82.3 12.8" stroke="url(#{u}c)" stroke-width="0.8" fill="none"/>'
            # body lines, door, handle, mirror
            '<path d="M3 18.2 Q40 16.6 111 17.6" stroke="#aeb6c4" stroke-opacity="0.75" stroke-width="0.7" fill="none"/>'
            '<path d="M3 21.5 L111.5 21.5" stroke="url(#{u}c)" stroke-width="0.9"/>'
            '<path d="M58.5 13 L58.5 28 M81 13.2 Q82 20 81.5 28" stroke="#000" stroke-opacity="0.55" stroke-width="0.7" fill="none"/>'
            '<rect x="73.5" y="15.2" width="4" height="1" rx="0.5" fill="url(#{u}c)"/>'
            '<path d="M82.5 10.5 L86 10 L86.5 12.4 L83 12.6 Z" fill="#16181c" stroke="#7d828a" stroke-width="0.4"/>'
            # bumpers + lights
            '<path d="M106 22.2 L113.5 22.2 Q114.5 22.5 114.3 24.5 L106 24.8 Z" fill="url(#{u}c)"/>'
            '<path d="M0 22.2 L8 22.2 L8 24.8 L0.2 24.6 Q-0.6 23.5 0 22.2 Z" fill="url(#{u}c)"/>'
            '<rect x="108.6" y="16.2" width="3.6" height="3.4" rx="1.2" fill="#fff1c8"/>'
            '<ellipse cx="128" cy="19" rx="20" ry="6" fill="url(#{u}h)" opacity="{{lampGlow2}}"/>'
            '<rect x="1.6" y="16.4" width="3" height="3.4" rx="0.8" fill="#c8102e"/>'
            '<ellipse cx="2" cy="18" rx="5" ry="3.5" fill="#ff2a3c" opacity="0.18"/>'
            # roof + hood reflections
            '<path d="M50 2.6 Q60 1.4 72 2.2" stroke="#ffffff" stroke-opacity="0.35" stroke-width="0.8" fill="none"/>'
            '<path d="M86 13.4 Q96 13.2 106 14.2" stroke="#ffffff" stroke-opacity="0.25" stroke-width="0.8" fill="none"/>'
            '<path d="M8 15.5 Q20 14.6 34 14" stroke="#ffffff" stroke-opacity="0.2" stroke-width="0.8" fill="none"/>')
    wheels = ''
    for cx in (24, 90):
        spokes = ''.join(f'<path d="M{cx} 29.5 L{cx + 4.2 * __import__("math").cos(a * 1.2566):.2f} {29.5 + 4.2 * __import__("math").sin(a * 1.2566):.2f}" stroke="#3a3c42" stroke-width="1.1"/>' for a in range(5))
        wheels += (f'<circle cx="{cx}" cy="29.5" r="8.6" fill="#08080a"/>'
                   f'<circle cx="{cx}" cy="29.5" r="8.6" fill="none" stroke="#2a2b30" stroke-width="1.2"/>'
                   f'<circle cx="{cx}" cy="29.5" r="5.2" fill="url(#{{u}}w)"/>' + spokes
                   + f'<circle cx="{cx}" cy="29.5" r="1.4" fill="#e6e7ea"/>'
                   f'<path d="M{cx - 9.6} 29.5 A9.6 9.6 0 0 1 {cx + 9.6} 29.5" stroke="#000" stroke-opacity="0.7" stroke-width="1.4" fill="none"/>')
    return (d + body + wheels).replace('{u}', uid)
