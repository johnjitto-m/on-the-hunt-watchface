"""Three original, more realistic assassin characters (front view, viewBox 0 0 140 300)."""
import re

RIM = '#d9d4c8'


def close(s):
    return re.sub(r'<(path|circle|ellipse|polyline|line|rect|polygon|stop)([^>]*?)/>', r'<\1\2></\1>', s)


def defs(uid):
    return (f'<defs>'
            f'<linearGradient id="skin{uid}" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#d8c7b4"/><stop offset="0.55" stop-color="#b9a38c"/><stop offset="1" stop-color="#7d6a5a"/></linearGradient>'
            f'<linearGradient id="cloth{uid}" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#34363d"/><stop offset="0.45" stop-color="#1e2025"/><stop offset="1" stop-color="#0e0f12"/></linearGradient>'
            f'<linearGradient id="grey{uid}" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#5a5c63"/><stop offset="0.5" stop-color="#3b3d43"/><stop offset="1" stop-color="#202226"/></linearGradient>'
            f'<linearGradient id="dark{uid}" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#26282d"/><stop offset="1" stop-color="#0b0c0e"/></linearGradient>'
            f'</defs>')


def face(uid, stubble=False):
    s = (f'<path d="M64 41 L76 41 L77 55 L63 55 Z" fill="#8c7766"/>'
         f'<ellipse cx="56.5" cy="27" rx="2.6" ry="4.2" fill="#a8927d"/><ellipse cx="83.5" cy="27" rx="2.6" ry="4.2" fill="#6f5d4f"/>'
         f'<path d="M57.5 19 Q57.5 9 70 9 Q82.5 9 82.5 19 L82.5 30 Q81.5 40 74 44.5 L66 44.5 Q58.5 40 57.5 30 Z" fill="url(#skin{uid})"/>'
         '<path d="M60.8 22.8 L67.2 24.8" stroke="#201a16" stroke-width="1.6" stroke-linecap="round"/><path d="M72.8 24.8 L79.2 22.8" stroke="#201a16" stroke-width="1.6" stroke-linecap="round"/>'
         '<path d="M61.6 27.4 L66.6 27.6" stroke="#120e0c" stroke-width="1.5" stroke-linecap="round"/><path d="M73.4 27.6 L78.4 27.4" stroke="#120e0c" stroke-width="1.5" stroke-linecap="round"/><path d="M61 25.6 L67 26.4 L67 28.6 L61 28.2 Z M73 26.4 L79 25.6 L79 28.2 L73 28.6 Z" fill="#000" opacity="0.18"/>'
         '<path d="M70 27 L68.6 34.5 L71.2 35" stroke="#6b5748" stroke-width="0.9" fill="none"/>'
         '<path d="M66.5 39.2 L73.5 39.2" stroke="#4a382e" stroke-width="1" fill="none"/>')
    if stubble:
        s += '<path d="M58.5 31 Q60 41 66 44.5 L74 44.5 Q80 41 81.5 31 Q78 37 74 38.5 L66 38.5 Q62 37 58.5 31 Z" fill="#3a3330" opacity="0.45"/>'
    return s


def legs(fill, shoe='#060607'):
    return (f'<path d="M54 200 C53 236 53 262 53 290 L66 290 C66.5 262 68 232 70 212 Z" fill="{fill}" stroke="{RIM}" stroke-width="1.2"/>'
            f'<path d="M86 200 C87 236 87 262 87 290 L74 290 C73.5 262 72 232 70 212 Z" fill="{fill}" stroke="{RIM}" stroke-width="1.2"/>'
            f'<path d="M48 290 L67 290 L67 297 L45 297 Q45 292 48 290 Z" fill="{shoe}" stroke="{RIM}" stroke-width="1"/>'
            f'<path d="M92 290 L73 290 L73 297 L95 297 Q95 292 92 290 Z" fill="{shoe}" stroke="{RIM}" stroke-width="1"/>'
            '<path d="M49 292 L56 291" stroke="#9a968c" stroke-width="0.7"/><path d="M84 291 L91 292" stroke="#9a968c" stroke-width="0.5"/>')


def hands_gun(glove=True):
    c = '#0b0b0d' if glove else '#b9a38c'
    return (f'<ellipse cx="37" cy="171" rx="5.5" ry="7.5" fill="{c}" stroke="{RIM}" stroke-width="0.8"/>'
            f'<ellipse cx="103" cy="171" rx="5.5" ry="7.5" fill="{c}" stroke="{RIM}" stroke-width="0.8"/>'
            '<path d="M98 168 L110 168 L110 178 L107 178 L108 208 L100 208 L100 178 L98 178 Z" fill="#050506" stroke="#8c887f" stroke-width="1"/>'
            '<path d="M104 182 L104 206" stroke="#3a3b40" stroke-width="0.8"/>')


# ---------------- A: The Ghost (long overcoat, undercut, clean-shaven)
def ghost(uid='a'):
    return close(defs(uid) + legs('#121316')
        + f'<path d="M36 68 C27 100 27 140 31 168 L43 168 C43 132 46 106 50 88 Z" fill="url(#cloth{uid})" stroke="{RIM}" stroke-width="1.2"/>'
        + f'<path d="M104 68 C113 100 113 140 109 168 L97 168 C97 132 94 106 90 88 Z" fill="url(#cloth{uid})" stroke="{RIM}" stroke-width="1.2"/>'
        + f'<path d="M37 66 Q49 56 60 55 L70 63 L80 55 Q91 56 103 66 L106 120 L109 236 L86 240 L70 232 L54 240 L31 236 L34 120 Z" fill="url(#cloth{uid})" stroke="{RIM}" stroke-width="1.3"/>'
        + '<path d="M60 55 L70 63 L80 55 L79 62 Q70 66 61 62 Z" fill="#0a0a0c"/>'
        + '<path d="M62 61 L70 104 L78 61 Q70 66 62 61 Z" fill="#0b0b0e"/>'
        + f'<path d="M60 55 L53 64 L63 104 L70 106 L62 62 Z" fill="#17181c" stroke="{RIM}" stroke-width="0.8"/>'
        + f'<path d="M80 55 L87 64 L77 104 L70 106 L78 62 Z" fill="#101114" stroke="{RIM}" stroke-width="0.8"/>'
        + '<path d="M70 106 L70 232" stroke="#060607" stroke-width="1.2"/>'
        + '<circle cx="74" cy="122" r="1.6" fill="#55575e"/><circle cx="74" cy="146" r="1.6" fill="#55575e"/><circle cx="74" cy="170" r="1.6" fill="#55575e"/>'
        + '<path d="M36 128 L104 128" stroke="#0a0a0c" stroke-width="3" opacity="0.6"/>'
        + '<path d="M40 70 C34 100 34 140 37 166" stroke="#5f6168" stroke-width="1" fill="none" opacity="0.8"/>'
        + hands_gun(True) + face(uid)
        + '<path d="M57 22 Q56 8 70 6 Q84 7 83.5 20 Q82 13 74 12.5 Q64 12 59 18 Z" fill="#121216" stroke="#3a3a40" stroke-width="0.6"/>'
        + '<path d="M57.3 22 L57.6 28" stroke="#3a3530" stroke-width="1.6"/><path d="M82.7 22 L82.4 28" stroke="#2a2522" stroke-width="1.6"/>'
        + '<path d="M62 9 Q70 6 79 9" stroke="#4a4a52" stroke-width="0.8" fill="none"/>')


# ---------------- B: The Ronin (grey suit, open collar, buzz cut, stubble)
def ronin(uid='b'):
    return close(defs(uid) + legs(f'url(#grey{uid})')
        + f'<path d="M37 68 C29 100 29 140 32 168 L43 168 C43 132 46 106 50 88 Z" fill="url(#grey{uid})" stroke="{RIM}" stroke-width="1.2"/>'
        + f'<path d="M103 68 C111 100 111 140 108 168 L97 168 C97 132 94 106 90 88 Z" fill="url(#grey{uid})" stroke="{RIM}" stroke-width="1.2"/>'
        + f'<path d="M38 66 Q50 56 60 55 L70 63 L80 55 Q90 56 102 66 L104 120 L101 158 Q100 186 97 204 L70 210 L43 204 Q40 186 39 158 L36 120 Z" fill="url(#grey{uid})" stroke="{RIM}" stroke-width="1.3"/>'
        + ''.join(f'<path d="M{x} 66 L{x + (2 if x < 70 else -2)} 204" stroke="#6a6c73" stroke-width="0.5" opacity="0.6"/>' for x in (46, 54, 86, 94))
        + '<path d="M61 57 L70 92 L79 57 Q70 61 61 57 Z" fill="#ece8e0"/><path d="M64 57 L70 70 L76 57" stroke="#b9b5ad" stroke-width="0.8" fill="none"/>'
        + f'<path d="M60 55 L54 64 L66 108 L70 110 L62 60 Z" fill="#2d2f34" stroke="{RIM}" stroke-width="0.8"/>'
        + f'<path d="M80 55 L86 64 L74 108 L70 110 L78 60 Z" fill="#26282c" stroke="{RIM}" stroke-width="0.8"/>'
        + '<circle cx="70" cy="128" r="1.6" fill="#121316"/><circle cx="70" cy="146" r="1.6" fill="#121316"/>'
        + '<path d="M79 82 L89 80 L89 83 L79 85 Z" fill="#ece8e0" opacity="0.8"/>'
        + hands_gun(False) + face(uid, stubble=True)
        + '<path d="M57.5 21 Q57 8 70 7.5 Q83 8 82.5 21 Q81 13 70 12 Q59 13 57.5 21 Z" fill="#2c2b2e" opacity="0.85"/>')


# ---------------- C: The Specter (tactical jacket, slicked-back short hair)
def specter(uid='c'):
    return close(defs(uid) + legs('#141518', shoe='#0a0a0b')
        + '<path d="M52 284 L67 284 L67 292 L52 292 Z M73 284 L88 284 L88 292 L73 292 Z" fill="#0a0a0b"/>'
        + f'<path d="M36 68 C28 100 29 140 32 166 L43 166 C43 130 46 106 50 88 Z" fill="url(#dark{uid})" stroke="{RIM}" stroke-width="1.2"/>'
        + f'<path d="M104 68 C112 100 111 140 108 166 L97 166 C97 130 94 106 90 88 Z" fill="url(#dark{uid})" stroke="{RIM}" stroke-width="1.2"/>'
        + f'<path d="M37 66 Q49 57 60 54 L70 58 L80 54 Q91 57 103 66 L105 120 L103 176 L70 182 L37 176 L35 120 Z" fill="url(#dark{uid})" stroke="{RIM}" stroke-width="1.3"/>'
        + f'<path d="M58 50 L70 56 L82 50 L83 60 L70 64 L57 60 Z" fill="#1b1d21" stroke="{RIM}" stroke-width="0.8"/>'
        + '<path d="M70 64 L70 182" stroke="#8c887f" stroke-width="0.9"/>'
        + '<path d="M44 96 L62 96 L62 112 L44 112 Z M78 96 L96 96 L96 112 L78 112 Z" fill="none" stroke="#3a3c42" stroke-width="0.9"/>'
        + '<path d="M37 170 L103 170" stroke="#2c2e33" stroke-width="5"/>'
        + '<path d="M33 128 L42 128 M98 128 L107 128" stroke="#3a3c42" stroke-width="1"/>'
        + f'<path d="M54 182 L86 182 L86 204 L54 204 Z" fill="#141518"/>'
        + hands_gun(True) + face(uid)
        + '<path d="M57 21 Q56 6 70 5 Q84 6 83.5 19 Q80 11 70 11 Q62 11 58.5 17 Z" fill="#0f0f12" stroke="#55555c" stroke-width="0.6"/>'
        + '<path d="M60 12 Q70 7 80 11 M62 9.5 Q70 6 78 8.5" stroke="#5a5a62" stroke-width="0.7" fill="none"/>')


def specter_long(uid='d'):
    base = specter(uid)
    # remove the short slicked hair (last two hair paths) and add long tied-back hair
    i = base.index('<path d="M57 21 Q56 6 70 5')
    base = base[:i]
    hair = ('<path d="M56.6 23 Q55 6 70 4.5 Q85 6 83.4 23 Q83 14 80 11.5 Q72 8.5 64 10.5 Q58 13 57.6 23 Z" fill="#141418" stroke="#55555c" stroke-width="0.6"></path>'
            '<path d="M60.5 11.5 Q70 6.5 80 10.5 M62.5 8.8 Q70 5.6 77.5 7.8 M58.5 15 Q63 9.5 70 9" stroke="#5c5c64" stroke-width="0.7" fill="none"></path>'
            '<path d="M56.6 22 Q55.8 30 57.2 33" stroke="#141418" stroke-width="2.2" fill="none"></path>'
            '<path d="M83.4 22 Q84.2 30 82.8 33" stroke="#141418" stroke-width="2.2" fill="none"></path>'
            # ponytail falling forward over the left shoulder
            '<path d="M56 30 Q51 38 52 48 Q50 62 46 76 Q44 90 47 104 Q50 96 52 84 Q55 70 56 56 Q58 44 59 36 Z" fill="#141418" stroke="#55555c" stroke-width="0.7"></path>'
            '<path d="M53 44 Q51 62 48 84 M55 46 Q54 64 50 92" stroke="#3a3a42" stroke-width="0.6" fill="none"></path>'
            '<rect x="51.6" y="40" width="6" height="3" rx="1" fill="#2c2e33" transform="rotate(12 54.6 41.5)"></rect>')
    return base + hair
