"""Full-height skyline (480 x 380, ground at y=380): tall hazy towers that rise behind the time and date.
Two depths: distant towers (very hazy, tinted by the sky) and mid towers (darker). Day and night variants."""
import asyncio, random, sys
sys.path.insert(0, 'tools')
import render_v2 as R


def tower(x, w, top, fill, edge, win, win_op, seed, spire=False, setback=True, beacon=False):
    rnd = random.Random(seed)
    s = [f'<rect x="{x}" y="{top}" width="{w}" height="{380 - top}" fill="{fill}"/>']
    s.append(f'<rect x="{x}" y="{top}" width="1.2" height="{380 - top}" fill="{edge}" opacity="0.6"/>')
    if setback and w > 26:
        sw = w * rnd.uniform(0.5, 0.7); sh = rnd.randint(14, 30)
        sx = x + (w - sw) / 2
        s.append(f'<rect x="{sx:.1f}" y="{top - sh}" width="{sw:.1f}" height="{sh}" fill="{fill}"/>')
        top2 = top - sh
        if rnd.random() < 0.6:
            s.append(f'<rect x="{sx + sw * 0.3:.1f}" y="{top2 - 12}" width="{sw * 0.4:.1f}" height="12" fill="{fill}"/>'); top2 -= 12
    else:
        top2 = top
    if spire:
        cx = x + w / 2
        s.append(f'<line x1="{cx:.1f}" y1="{top2}" x2="{cx:.1f}" y2="{top2 - 34}" stroke="{fill}" stroke-width="2"/>')
        if beacon:
            s.append(f'<circle cx="{cx:.1f}" cy="{top2 - 34}" r="1.8" fill="#ff3b3b"/><circle cx="{cx:.1f}" cy="{top2 - 34}" r="5" fill="#ff3b3b" opacity="0.35"/>')
    # windows: faint vertical bands by day, scattered lights at night
    for wy in range(int(top) + 8, 372, 9):
        for wx in range(int(x) + 4, int(x + w) - 3, 6):
            if rnd.random() < win_op[0]:
                s.append(f'<rect x="{wx}" y="{wy}" width="2.4" height="3.6" fill="{win}" opacity="{rnd.choice(win_op[1]):.2f}"/>')
    return ''.join(s)


def skyline(night):
    rnd = random.Random(42)
    far, mid = [], []
    # distant towers: tallest in the middle (behind the time), shorter to the edges
    x = -10
    i = 0
    while x < 490:
        w = rnd.randint(22, 40)
        cx = x + w / 2
        centre = 1 - min(1, abs(cx - 240) / 260)
        h = int(150 + 210 * centre * rnd.uniform(0.75, 1.0))
        far.append(tower(x, w, 380 - h, '#202833' if not night else '#10131b', '#56657a' if not night else '#232a38',
                         '#c8b27a' if night else '#7a8696', (0.14, [0.3, 0.45, 0.7]) if night else (0.16, [0.18, 0.3, 0.4]), 100 + i,
                         spire=(i % 4 == 1), beacon=night and (i % 4 == 1)))
        x += w + rnd.randint(4, 14); i += 1
    x = -20; i = 0
    while x < 500:
        w = rnd.randint(30, 52)
        cx = x + w / 2
        centre = 1 - min(1, abs(cx - 240) / 280)
        h = int(110 + 120 * centre * rnd.uniform(0.6, 1.0))
        mid.append(tower(x, w, 380 - h, '#151b23' if not night else '#090b10', '#3f4a5a' if not night else '#181d28',
                         '#e3c463' if night else '#6a7482', (0.2, [0.35, 0.6, 0.9]) if night else (0.12, [0.15, 0.25, 0.35]), 300 + i,
                         spire=(i % 5 == 2), beacon=night and (i % 5 == 2)))
        x += w + rnd.randint(2, 10); i += 1
    haze_far = 0.8 if not night else 0.9
    haze_mid = 0.92 if not night else 0.95
    return (f'<svg width="480" height="380" viewBox="0 0 480 380" xmlns="http://www.w3.org/2000/svg">'
            '<defs><linearGradient id="fade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity="0.55"/>'
            '<stop offset="0.35" stop-color="#fff" stop-opacity="0.85"/><stop offset="1" stop-color="#fff" stop-opacity="1"/></linearGradient>'
            '<mask id="m"><rect x="0" y="0" width="480" height="380" fill="url(#fade)"/></mask></defs>'
            f'<g mask="url(#m)"><g opacity="{haze_far}">{"".join(far)}</g><g opacity="{haze_mid}">{"".join(mid)}</g></g></svg>')


if __name__ == '__main__':
    R.OUT = sys.argv[1] if len(sys.argv) > 1 else 'build/frames'
    R.JOBS.clear()
    R.job('towers_day', R.fix(skyline(False)), 480, 380)
    R.job('towers_night', R.fix(skyline(True)), 480, 380)
    asyncio.run(R.main())
    print('ok')
