"""Lit-window dot fonts for On the Hunt v2.9.

dots.ttf        digits 5x7, letters 3x5 (sitting in rows 2-6), colon, hyphen, dots. Heart is blank (same advance).
dots_heart.ttf  every glyph blank except the heart, so it can pulse on its own over dots.ttf.

1 cell = 100 units, em = 1000, ascent 700 / descent 0 -> at font size S a cell is S/10 px and a line is 0.7*S px tall,
so a PartText whose height is 0.7*S lands the 7 rows exactly in the box whether the renderer centres or top-aligns.
Every advance is an even number of cells, so centred text always lands on the window grid.
"""
import sys
from fontTools.fontBuilder import FontBuilder
from fontTools.pens.ttGlyphPen import TTGlyphPen

D7 = {
    '0': ['01110', '10001', '10001', '10001', '10001', '10001', '01110'],
    '1': ['010', '110', '010', '010', '010', '010', '111'],
    '2': ['01110', '10001', '00001', '00010', '00100', '01000', '11111'],
    '3': ['11111', '00010', '00100', '00010', '00001', '10001', '01110'],
    '4': ['00010', '00110', '01010', '10010', '11111', '00010', '00010'],
    '5': ['11111', '10000', '11110', '00001', '00001', '10001', '01110'],
    '6': ['00110', '01000', '10000', '11110', '10001', '10001', '01110'],
    '7': ['11111', '00001', '00010', '00100', '01000', '01000', '01000'],
    '8': ['01110', '10001', '10001', '01110', '10001', '10001', '01110'],
    '9': ['01110', '10001', '10001', '01111', '00001', '00010', '01100'],
    ':': ['0', '0', '1', '0', '1', '0', '0'],
    '.': ['0', '0', '0', '0', '0', '0', '1'],
    '-': ['000', '000', '000', '000', '111', '000', '000'],
    '·': ['0', '0', '0', '0', '1', '0', '0'],
    '/': ['001', '001', '001', '010', '100', '100', '100'],
}
L5 = {
    'A': ['010', '101', '111', '101', '101'], 'B': ['110', '101', '110', '101', '110'], 'C': ['011', '100', '100', '100', '011'],
    'D': ['110', '101', '101', '101', '110'], 'E': ['111', '100', '110', '100', '111'], 'F': ['111', '100', '110', '100', '100'],
    'G': ['011', '100', '101', '101', '011'], 'H': ['101', '101', '111', '101', '101'], 'I': ['111', '010', '010', '010', '111'],
    'J': ['001', '001', '001', '101', '010'], 'K': ['101', '101', '110', '101', '101'], 'L': ['100', '100', '100', '100', '111'],
    'M': ['10001', '11011', '10101', '10001', '10001'], 'N': ['10001', '11001', '10101', '10011', '10001'],
    'O': ['111', '101', '101', '101', '111'], 'P': ['110', '101', '110', '100', '100'], 'Q': ['010', '101', '101', '110', '011'],
    'R': ['110', '101', '110', '101', '101'], 'S': ['011', '100', '010', '001', '110'], 'T': ['111', '010', '010', '010', '010'],
    'U': ['101', '101', '101', '101', '111'], 'V': ['101', '101', '101', '010', '010'],
    'W': ['10001', '10001', '10101', '11011', '10001'], 'X': ['101', '101', '010', '101', '101'], 'Y': ['101', '101', '010', '010', '010'],
    'Z': ['111', '001', '010', '100', '111'],
}
HEART = ['0', '01010', '11111', '11111', '01110', '00100', '0']

CELL, IN = 100, 12          # cell size and window inset (square is 76 units)
NAMES = {':': 'colon', '.': 'period', '-': 'hyphen', '·': 'periodcentered', '/': 'slash', ' ': 'space', '♥': 'heart'}


def glyph_rows():
    """char -> 7-row pattern (rows top to bottom; ragged rows are padded)"""
    g = {}
    for ch, rows in D7.items(): g[ch] = rows
    for ch, rows in L5.items(): g[ch] = ['0' * len(rows[0])] * 2 + rows
    g['♥'] = [r.ljust(5, '0') for r in HEART]
    return g


def build(path, family, keep, inset=IN):
    G = glyph_rows()
    order = ['.notdef', 'space'] + [NAMES.get(c, c if c.isalpha() else f'uni{ord(c):04X}') for c in G]
    fb = FontBuilder(1000, isTTF=True)
    fb.setupGlyphOrder(order)
    cmap = {32: 'space'}
    glyphs, metrics = {}, {}
    empty = TTGlyphPen(None).glyph()
    glyphs['.notdef'] = empty; metrics['.notdef'] = (400, 0)
    glyphs['space'] = empty; metrics['space'] = (2 * CELL, 0)
    for ch, rows in G.items():
        name = NAMES.get(ch, ch if ch.isalpha() else f'uni{ord(ch):04X}')
        w = max(len(r) for r in rows)
        pen = TTGlyphPen(None)
        drawn = False
        if keep(ch):
            for r, row in enumerate(rows):
                for c, v in enumerate(row):
                    if v != '1': continue
                    x0, x1 = c * CELL + inset, (c + 1) * CELL - inset
                    y1, y0 = 700 - r * CELL - inset, 700 - (r + 1) * CELL + inset
                    pen.moveTo((x0, y0)); pen.lineTo((x0, y1)); pen.lineTo((x1, y1)); pen.lineTo((x1, y0)); pen.closePath()
                    drawn = True
        glyphs[name] = pen.glyph() if drawn else empty
        adv = (w + 1) * CELL
        assert (w + 1) % 2 == 0, (ch, w)                       # even advances keep centred text on the grid
        metrics[name] = (adv, inset if drawn else 0)
        cmap[ord(ch)] = name
        if ch.isalpha(): cmap[ord(ch.lower())] = name
    fb.setupCharacterMap(cmap)
    fb.setupGlyf(glyphs)
    fb.setupHorizontalMetrics(metrics)
    fb.setupHorizontalHeader(ascent=700, descent=0, lineGap=0)
    fb.setupNameTable({'familyName': family, 'styleName': 'Regular'})
    fb.setupOS2(sTypoAscender=700, sTypoDescender=0, sTypoLineGap=0, usWinAscent=700, usWinDescent=0,
                fsSelection=0x40 | 0x80, achVendID='HUNT', version=4)
    fb.setupPost()
    fb.save(path)


if __name__ == '__main__':
    out = sys.argv[1] if len(sys.argv) > 1 else 'watchface/src/main/res/font/'
    build(out + 'dots.ttf', 'Hunt Dots', lambda c: c != '♥')
    build(out + 'dots_heart.ttf', 'Hunt Dots Heart', lambda c: c == '♥')
    build(out + 'dots_time.ttf', 'Hunt Dots Time', lambda c: c != '\u2665', inset=7)   # chunkier squares for the big clock
    print('fonts ok')
