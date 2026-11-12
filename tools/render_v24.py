"""v2.4 bitmaps: bigger hero + dog, lean pose, transparent-sky city, stronger weather. Output: build/art"""
import asyncio, os, random, re, sys
sys.path.insert(0, 'tools')
import render_v2 as R, color_poses as P, backdrops as B, real_car

R.OUT = OUT = 'build/art'
os.makedirs(OUT, exist_ok=True)
R.JOBS.clear()
job, fig, fix, subs = R.job, R.fig, R.fix, R.subs
SC = 1.3
FW, FH = round(72 * SC), round(116 * SC)          # 94 x 151
g, rot = P.g, P.rot


def fig(inner, w=FW, h=FH):
    return (f'<svg width="{w}" height="{h}" viewBox="0 0 240 386.667" style="display:block; overflow: hidden">'
            f'<g transform="translate(40 26.667)">{fix(inner)}</g></svg>')


def lean():
    """Idle: leaning back on a lamp post, arms folded, ankles crossed."""
    post = ('<path d="M34 -10 L42 -10 L42 300 L34 300 Z" fill="#141519" stroke="#5a5a62" stroke-width="2"></path>'
            '<path d="M28 296 L48 296 L50 302 L26 302 Z" fill="#141519" stroke="#5a5a62" stroke-width="2"></path>')
    back_leg = rot(-14, *P.HIP, P.thigh(True) + rot(8, *P.KNEE, P.shin(True)))
    front_leg = rot(10, *P.HIP, P.thigh() + rot(-16, *P.KNEE, P.shin()))
    arms = (g(P.JACKETB, '<path d="M62 76 L74 74 L84 110 L74 112 Z"></path>', rim=P.RIMB)
            + g(P.JACKET, '<path d="M58 104 Q70 96 90 100 L90 114 Q72 112 58 116 Z"></path>')
            + g(P.JACKET, '<path d="M60 76 L73 74 L80 104 L68 108 Z"></path>')
            + g(P.GLOVE, '<ellipse cx="88" cy="107" rx="5.5" ry="5"></ellipse>', sw=1.4))
    return post + rot(-7, *P.HIP, back_leg + P.HIPS + P.UPPER + arms) + front_leg


job('fig_front', fig(P.front(), FW, FH), FW, FH)
job('fig_aim', fig(P.aim_static(42), FW, FH), FW, FH)
job('fig_kneel', fig(P.kneel(), FW, FH), FW, FH)
job('fig_lean', fig(lean(), FW, FH), FW, FH)
job('walk', fig(P.walk(), FW, FH), FW, FH, [i * 1.8 / 12 for i in range(12)])
job('reload', fig(P.reload(), FW, FH), FW, FH, [i * 1.6 / 8 for i in range(8)])


def dogbox(svg, w, h, pad):
    W_, H_ = round(w * SC), round(h * SC)
    return (f'<div style="width:{W_}px;height:{H_}px;padding-top:{round(pad * SC)}px;box-sizing:border-box">'
            f'<div style="transform:scale({SC});transform-origin:0 0">{svg}</div></div>'), W_, H_


for name, svg, w, h, pad, times in (('dog_sit', B.DOG, 34, 30, 4, None), ('dog_walk', B.DOGWALK, 34, 30, 4, [i * 0.45 / 6 for i in range(6)]),
                                    ('dog_alert', B.DOGALERT, 34, 44, 18, [i * 1.2 / 8 for i in range(8)]),
                                    ('dog_happy', B.DOGHAPPY, 34, 34, 8, [i * 0.8 / 8 for i in range(8)])):
    body, W_, H_ = dogbox(svg, w, h, pad)
    job(name, body, W_, H_, times)


def city(night):
    vals = dict(winColor='#e3c463' if night else '#3a3424', neonColor='#e0213b', neonGlow=0.8 if night else 0.4, lampGlow=0.35 if night else 0.15, lampGlow2=0.9 if night else 0.35)
    far, near = B.noir()
    a = near.index('<g transform="translate(14 132)">'); b = near.index('</g>', a) + 4
    near = near[:a] + '<g transform="translate(14 132)">' + R.fix(real_car.car('n' if night else 'd')) + '</g>' + near[b:]
    html = (f'<div style="position:relative;width:480px;height:204px;overflow:hidden"><div style="position:absolute;left:0;top:36px;width:480px;height:168px">'
            f'<svg width="480" height="168" viewBox="0 0 480 168" style="position:absolute;left:0;top:0;overflow:visible;opacity:.5">{far}</svg>'
            f'<svg width="480" height="168" viewBox="0 0 480 168" style="position:absolute;left:0;top:0;overflow:visible">{near}</svg>'
            f'<svg width="480" height="168" viewBox="0 0 480 168" style="position:absolute;left:0;top:0;overflow:visible">{B.noir_signs()}</svg></div>'
            '<div style="position:absolute;left:0;top:192px;width:480px;height:12px;background:linear-gradient(180deg,rgba(0,0,0,0) 0%,#000 95%)"></div></div>')
    return subs(fix(html), vals)


job('city_day', city(False), 480, 204)
job('city_night', city(True), 480, 204)

random.seed(8)
drops = [(random.randint(-10, 500), random.randint(0, 360), random.choice([1.3, 1.6]), random.choice([0.35, 0.45, 0.55])) for _ in range(110)]
rain = ''.join(f'<line x1="{x}" y1="{y + k * 360}" x2="{x - 3}" y2="{y + k * 360 + 16}" stroke="#c4cfe0" stroke-width="{w}" stroke-linecap="round" opacity="{o}"></line>'
               for k in (0, 1) for x, y, w, o in drops)
job('wx_rain', f'<svg width="480" height="720" viewBox="0 0 480 720">{rain}</svg>', 480, 720)
random.seed(4)
fl = [(random.randint(-10, 490), random.randint(0, 360), random.choice([1.6, 2.2, 2.8]), random.choice([0.6, 0.8, 0.95])) for _ in range(110)]
snow = ''.join(f'<circle cx="{x}" cy="{y + k * 360}" r="{r}" fill="#f2f5fa" opacity="{o}"></circle>' for k in (0, 1) for x, y, r, o in fl)
job('wx_snow', f'<svg width="480" height="720" viewBox="0 0 480 720">{snow}</svg>', 480, 720)
job('wx_cloudy', R.clouds([(-40, 60, 240, 54, .75), (200, 30, 280, 60, .7), (380, 100, 220, 50, .65), (40, 170, 260, 46, .5), (280, 200, 240, 44, .5)], '#6a707c'), 560, 374)

if __name__ == '__main__':
    asyncio.run(R.main())
    print('rendered', len(R.JOBS))
