"""Generate res/raw/watchface.xml for 'On the Hunt' v2.9 (Watch Face Format v2).
v2.9.2: no everyday bounty label over the steps. v2.9.1: date (cyan) + pulse (red) in a lit-window dot font floating over the city, no boxes; time in the dot font, white, a bit smaller.
Bigger, more detailed duo that reacts to time of day, weather, notifications and activity;
festivals (Diwali, Christmas, New Year); always-on screen; a complication slot under the time."""
import json, os
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ART = json.load(open(os.path.join(HERE, 'art28.json')))
GEO = json.load(open(os.path.join(HERE, 'towers29.json')))
DRW = os.path.join(HERE, '..', 'watchface/src/main/res/drawable/')
OUT_XML = os.path.join(HERE, '..', 'watchface/src/main/res/raw/watchface.xml')

OSW, OSWM, BOD = 'oswald_regular', 'oswald_medium', 'bebas_neue'
P = '([STEP_PERCENT] &gt; 100 ? 100 : [STEP_PERCENT])'
SECF = '(([SECOND] % 60) + [MILLISECOND] / 1000)'
GOLD, GOLDL, RED, CREAM, PINK = '#d4af37', '#ecd27a', '#e0213b', '#e8d9a8', '#ff7a8a'

E_DONE = '[STEP_COUNT] >= [STEP_GOAL] && [STEP_GOAL] > 0'
E_NIGHT = '([WEATHER.IS_AVAILABLE] == 1 && [WEATHER.IS_DAY] == 0) || ([WEATHER.IS_AVAILABLE] != 1 && ([HOUR_0_23] >= 18 || [HOUR_0_23] < 6))'
E_CHG = '[BATTERY_CHARGING_STATUS] == 1'
E_LOW = '[BATTERY_PERCENT] < 20'
E_BEHIND = '[HOUR_0_23] >= 10 && [HOUR_0_23] < 22 && [STEP_PERCENT] < (([HOUR_0_23] + [MINUTE] / 60 - 8) / 13 * 100 - 30)'
E_NOTIF = '[UNREAD_NOTIFICATION_COUNT] > 0'
E_WORK = '[HEART_RATE] >= 110'
TC = '([WEATHER.TEMPERATURE_UNIT] == 2 ? ([WEATHER.TEMPERATURE] - 32) / 1.8 : [WEATHER.TEMPERATURE])'
E_HOT = f'[WEATHER.IS_AVAILABLE] == 1 && {TC} >= 32 && [HOUR_0_23] >= 9 && [HOUR_0_23] < 19'
E_COLD = f'[WEATHER.IS_AVAILABLE] == 1 && {TC} <= 6'
E_LATE = '[HOUR_0_23] >= 22 || [HOUR_0_23] < 5'
E_MORNING = '[HOUR_0_23] >= 5 && [HOUR_0_23] < 9'
E_AM = '[HOUR_0_23] >= 5 && [HOUR_0_23] < 8'
E_PM = '[HOUR_0_23] >= 16 && [HOUR_0_23] < 19'


def wx(*codes):
    return '[WEATHER.IS_AVAILABLE] == 1 && (' + ' || '.join(f'[WEATHER.CONDITION] == {c}' for c in codes) + ')'


E_STORM, E_RAIN, E_SNOW, E_FOG, E_CLOUD = wx(9), wx(4, 6, 10, 12), wx(5, 7, 11), wx(3, 13), wx(2, 14)
# festivals: Diwali = the 5-day window around Lakshmi Puja (2026-2030)
DIWALI = ((2026, 11, 8), (2027, 10, 29), (2028, 10, 17), (2029, 11, 5), (2030, 10, 26))
E_DIWALI = ' || '.join(f'([YEAR] == {y} && [MONTH] == {m} && [DAY] >= {d - 2} && [DAY] <= {d + 2})' for y, m, d in DIWALI)
E_DIWALI_NIGHT = f'({E_DIWALI}) && [HOUR_0_23] >= 18'
E_XMAS = '[MONTH] == 12 && [DAY] >= 24 && [DAY] <= 26'
E_NYE = '([MONTH] == 12 && [DAY] == 31 && [HOUR_0_23] >= 22) || ([MONTH] == 1 && [DAY] == 1 && [HOUR_0_23] < 1)'
E_NEWYEAR = '[MONTH] == 1 && [DAY] == 1'
E_FIREWORKS = f'({E_DIWALI_NIGHT}) || ({E_NYE})'


def text(x, y, w, h, body, family=OSWM, size=12, color='#ffffff', align='CENTER', spacing=None, extra='', shadow=None):
    ls = f' letterSpacing="{spacing}"' if spacing is not None else ''
    if shadow: body = f'<Shadow color="#d8000000" offsetX="0" offsetY="1.5" radius="{shadow}">{body}</Shadow>'
    return (f'<PartText x="{x}" y="{y}" width="{w}" height="{h}">{extra}<Text align="{align}">'
            f'<Font family="{family}" size="{size}" color="{color}"{ls}>{body}</Font></Text></PartText>')


CYAN, NEON_RED = '#46ebff', '#ff3c5a'


def dots(x, y, w, body, color, glow=None, size=40, family='dots', extra='', glow_r=3, shade=None, shade_r=9, shade_dy=2):
    """lit-window text: line box is exactly 0.7*size tall so the 7 rows land on the window grid"""
    if glow: body = f'<OutGlow color="{glow}" radius="{glow_r}">{body}</OutGlow>'
    if shade: body = f'<Shadow color="{shade}" offsetX="0" offsetY="{shade_dy}" radius="{shade_r}">{body}</Shadow>'
    return (f'<PartText x="{x}" y="{y}" width="{w}" height="{round(size * 0.7)}">{extra}<Text align="CENTER">'
            f'<Font family="{family}" size="{size}" color="{color}">{body}</Font></Text></PartText>')


def tmpl(fmt, *exprs):
    return f'<Template><![CDATA[{fmt}]]>' + ''.join(f'<Parameter expression="{e}"/>' for e in exprs) + '</Template>'


def lit(s): return f'<![CDATA[{s}]]>'
def img(x, y, w, h, res, extra=''): return f'<PartImage x="{x}" y="{y}" width="{w}" height="{h}">{extra}<Image resource="{res}"/></PartImage>'


def rect(x, y, w, h, color, extra=''):
    return f'<PartDraw x="{x}" y="{y}" width="{w}" height="{h}">{extra}<Rectangle x="0" y="0" width="{w}" height="{h}"><Fill color="{color}"/></Rectangle></PartDraw>'


_n = [0]
def cond(pairs, default=''):
    ex, cmp_ = '', ''
    for n, e, body in pairs:
        _n[0] += 1; nm = f'{n}{_n[0]}'
        ex += f'<Expression name="{nm}"><![CDATA[{e}]]></Expression>'
        cmp_ += f'<Compare expression="{nm}">{body}</Compare>'
    d = f'<Default>{default}</Default>' if default else ''
    return f'<Condition><Expressions>{ex}</Expressions>{cmp_}{d}</Condition>'


def anim(x, y, w, h, frames, rate, loops, play='ON_VISIBLE TAP', thumb=None, before='THUMBNAIL', after='THUMBNAIL', repeat=False,
         extra='', delay_repeat=None, mode=None):
    t = f'<Thumbnail resource="{thumb}"/>' if thumb else ''
    rep = ' repeat="TRUE"' if repeat else ''
    dr = f' delayRepeat="{delay_repeat}"' if delay_repeat is not None else ''
    rm = f' renderMode="{mode}"' if mode else ''
    imgs = ''.join(f'<Image resource="{f}"/>' for f in frames)
    return (f'<PartAnimatedImage x="{x}" y="{y}" width="{w}" height="{h}"{rm}>{extra}{t}'
            f'<AnimationController play="{play}" beforePlaying="{before}" afterPlaying="{after}"{rep}{dr}/>'
            f'<SequenceImages loopCount="{loops}" frameRate="{rate}">{imgs}</SequenceImages></PartAnimatedImage>')


def mask(w, h, name, frames, rate, play='ON_VISIBLE'):
    """Hides its group while `frames` play (e.g. during the walk-on-wake), then shows it."""
    return anim(0, 0, w, h, [f'{name}_clear'] * frames, rate, 1, play=play, thumb=f'{name}_solid', before='FIRST_FRAME', after='THUMBNAIL', mode='MASK')


def fr(prefix, n): return [f'{prefix}_{i:02d}' for i in range(n)]


# ---------------- lighting: pick the graded sprite for the time of day
LIGHT = [('lgn', E_NIGHT, 'night'), ('lam', E_AM, 'am'), ('lpm', E_PM, 'pm')]


def graded(make, grades):
    """make(g) -> xml for grade g; chooses night / golden morning / golden evening / day among the available grades."""
    pairs = [(n, e, make(g)) for n, e, g in LIGHT if g in grades]
    default_g = 'day' if 'day' in grades else grades[0]
    return cond(pairs, make(default_g)) if pairs else make(default_g)


def still(prefix, grades):
    def make(g):
        n = f'h_{prefix}_{g}'
        x, y, w, h = ART['stills'][n]
        return img(x, y, w, h, n)
    return graded(make, grades)


def seq(name, grades, play='ON_VISIBLE', thumb='first', before='THUMBNAIL', after='THUMBNAIL', repeat=False, delay=None, loops=1, order=None, rate=None):
    def make(g):
        g2 = g if f'{name}_{g}' in ART['seqs'] else ('night' if g == 'night' and f'{name}_night' in ART['seqs'] else
                                                       next(k.split('_')[-1] for k in ART['seqs'] if k.rsplit('_', 1)[0] == name))
        s = ART['seqs'][f'{name}_{g2}']
        x, y, w, h = s['box']
        frames = [s['frames'][i] for i in order] if order else s['frames']
        th = None
        if thumb == 'first': th = frames[0]
        elif thumb == 'last': th = frames[-1]
        elif thumb: th = thumb(g, s)
        return anim(x, y, w, h, frames, rate or s['fps'], loops, play=play, thumb=th, before=before, after=after, repeat=repeat, delay_repeat=delay)
    return graded(make, grades)


def tap_thumb(seq_name):
    """the graded base still re-cropped into a tap sequence's box (so the right lighting shows between taps)."""
    def th(g, s):
        name = f'h_thumb_{seq_name}_{g}'
        if not os.path.exists(DRW + name + '.png'):
            bx, by, bw, bh = s['box']
            base = f'h_base_{g}'
            x, y, w, h = ART['stills'][base]
            canvas = Image.new('RGBA', (248, 260), (0, 0, 0, 0))
            canvas.alpha_composite(Image.open(DRW + base + '.png').convert('RGBA'), (x, y))
            canvas.crop((bx, by, bx + bw, by + bh)).save(DRW + name + '.png')
        return name
    return th


live = []
# ---------------- sky (time of day / weather) + city
sky = cond([('sst', E_STORM, img(0, 0, 480, 380, 'sky_storm')), ('snt', E_NIGHT, img(0, 0, 480, 380, 'sky_night')),
            ('srn', E_RAIN, img(0, 0, 480, 380, 'sky_rain')), ('ssn', E_SNOW, img(0, 0, 480, 380, 'sky_snow')),
            ('scl', f'({E_CLOUD}) || ({E_FOG})', img(0, 0, 480, 380, 'sky_cloudy')),
            ('sdw', '[HOUR_0_23] >= 5 && [HOUR_0_23] < 7', img(0, 0, 480, 380, 'sky_dawn')),
            ('sdk', '[HOUR_0_23] >= 17 && [HOUR_0_23] < 19', img(0, 0, 480, 380, 'sky_dusk'))],
           img(0, 0, 480, 380, 'sky_day'))
live.append(sky)

PI = '3.14159'
SUN_T = '(([HOUR_0_23] + [MINUTE] / 60 - 6) / 12)'
MOON_T = '((([HOUR_0_23] + [MINUTE] / 60) + 6) % 24 / 12)'
LOW = f'(1 - clamp(sin({PI} * {SUN_T}) * 2.2, 0, 1))'
E_PRECIP = f'({E_RAIN}) || ({E_STORM}) || ({E_SNOW})'
E_DIM = f'({E_CLOUD}) || ({E_FOG})'
E_SUN = '[HOUR_0_23] >= 6 && [HOUR_0_23] < 18 && !([WEATHER.IS_AVAILABLE] == 1 && [WEATHER.IS_DAY] == 0)'
E_MOON = '[HOUR_0_23] >= 18 || [HOUR_0_23] < 6'


def body(name, size, t, inner, alpha=255):
    pos = (f'<Transform target="x" value="240 - 205 * cos({PI} * {t}) - {size // 2}"/>'
           f'<Transform target="y" value="318 - 262 * sin({PI} * {t}) - {size // 2}"/>')
    return f'<Group name="{name}" x="0" y="0" width="{size}" height="{size}" alpha="{alpha}">{pos}{inner}</Group>'


def sun(part, alpha):
    inner = (img(0, 0, 200, 200, f'sun_{part}_high', f'<Transform target="alpha" value="255 * (1 - {LOW})"/>')
             + img(0, 0, 200, 200, f'sun_{part}_low', f'<Transform target="alpha" value="255 * {LOW}"/>'))
    return body(f'sun_{part}', 200, SUN_T, inner, alpha)


def moon(part, alpha):
    if part == 'disc':
        inner = cond([(f'mp{k}', f'[MOON_PHASE_TYPE] == {k}', img(0, 0, 80, 80, f'moon_{k}')) for k in range(8)])
    else:
        inner = img(0, 0, 80, 80, 'moon_glow', f'<Transform target="alpha" value="(1 - cos([MOON_PHASE_TYPE] * 0.7854)) * 127"/>')
    return body(f'moon_{part}', 80, MOON_T, inner, alpha)


def sky_bodies(part):
    return (cond([('sp', f'({E_SUN}) && !({E_PRECIP})', cond([('sd', E_DIM, sun(part, 90))], sun(part, 255)))])
            + cond([('mn', f'({E_MOON}) && !({E_PRECIP})', cond([('md', E_DIM, moon(part, 90))], moon(part, 255)))]))


live.append(sky_bodies('disc'))
# fireworks over the city on Diwali nights and at New Year
FW = ''.join(anim(x, y, 120, 120, fr(f'fw_{c}', 14), 14, 1, play='ON_VISIBLE', before='HIDE', after='HIDE', repeat=True, delay_repeat=d)
             for (x, y, c, d) in ((24, 24, 'gold', 1.4), (300, 6, 'rose', 2.2), (170, 92, 'teal', 3.0), (370, 96, 'gold', 2.6)))
live.append(cond([('fw', E_FIREWORKS, f'<Group name="fireworks" x="0" y="0" width="480" height="240">{FW}</Group>')]))
live.append(cond([('twn', E_NIGHT, img(0, 0, 480, 380, 'towers_night'))], img(0, 0, 480, 380, 'towers_day')))
live.append(sky_bodies('glow'))
live.append(cond([('cn', E_NIGHT, img(0, 176, 480, 204, 'city_night'))], img(0, 176, 480, 204, 'city_day')))



def string_lights(k):
    return (img(0, 176, 480, 204, f'lights_{k}_a', f'<Transform target="alpha" value="150 + 105 * sin({SECF} * 3.1416)"/>')
            + img(0, 176, 480, 204, f'lights_{k}_b', f'<Transform target="alpha" value="150 - 105 * sin({SECF} * 3.1416)"/>'))


live.append(cond([('ldw', E_DIWALI, string_lights('dw')), ('lxm', E_XMAS, string_lights('xm'))]))

# ---------------- weather above the walking line
rain_layer = img(0, -360, 480, 720, 'wx_rain', f'<Transform target="y" value="(({SECF}) % 3) * 120 - 360"/>')
snow_layer = img(0, -360, 480, 720, 'wx_snow', f'<Transform target="y" value="(({SECF}) % 12) * 30 - 360"/>')
def drift(res): return img(-40, 0, 560, 374, res, f'<Transform target="x" value="-40 + 40 * sin({SECF} * 0.10472)"/>')
flash = img(0, 0, 480, 374, 'wx_storm', '<Transform target="alpha" value="([SECOND] % 5 == 0 &amp;&amp; ([MILLISECOND] &lt; 140 || ([MILLISECOND] &gt; 260 &amp;&amp; [MILLISECOND] &lt; 380))) ? 255 : 0"/>')
weather = cond([('st', E_STORM, rain_layer + flash), ('ra', E_RAIN, rain_layer), ('sn', E_SNOW, snow_layer),
                ('fo', E_FOG, drift('wx_fog')), ('cl', E_CLOUD, drift('wx_cloudy'))])
live.append(f'<Group name="weather" x="0" y="0" width="480" height="480">{weather}</Group>')
live.append(rect(0, 380, 480, 100, '#000000'))

# ---------------- time: lit-window dot font, cyan (12/24 h follows the watch)
TIME_S, TIME_Y = 90, 73
WHITE = '#f4f4f2'
DATE = '%s · %s %s'
def clock(color, family='dots_time', size=TIME_S, glow=None, shade=None, glow_r=7):
    h24 = dots(0, 0, 480, tmpl('%s:%s', '[HOUR_0_23_Z]', '[MINUTE_Z]'), color, glow, size, family, glow_r=glow_r, shade=shade)
    h12 = dots(0, 0, 480, tmpl('%s:%s', '[HOUR_1_12_Z]', '[MINUTE_Z]'), color, glow, size, family, glow_r=glow_r, shade=shade)
    return cond([('h24', '[IS_24_HOUR_MODE] == 1', h24)], h12)


live.append(f'<Group name="time" x="0" y="{TIME_Y}" width="480" height="{round(TIME_S * 0.7)}"><Launch target="ALARM"/>'
            + clock(WHITE, shade='#e6000000') + clock(WHITE, glow='#73ffffff', glow_r=5) + '</Group>')

# ---------------- battery: a colour-coded arc hugging the left edge (green > yellow > red), no number
ARC_A0, ARC_A1, NSEG = 242.0, 300.0, 10          # degrees, 0 = 12 o'clock, clockwise; fills from the bottom up
SEG = (ARC_A1 - ARC_A0) / NSEG
GREEN, YELLOW, REDB, TRACK = '#3ddc84', '#f5c542', '#ff4b4b', '#34343a'


def seg(i, color, extra='', thick=7):
    a0 = ARC_A0 + i * SEG + 0.8; a1 = ARC_A0 + (i + 1) * SEG - 0.8
    return (f'<PartDraw x="0" y="0" width="480" height="480">{extra}'
            f'<Arc centerX="240" centerY="240" width="452" height="452" startAngle="{a0:.2f}" endAngle="{a1:.2f}">'
            f'<Stroke color="{color}" thickness="{thick}" cap="BUTT"/></Arc></PartDraw>')


def arc_fill(color, blink=False):
    b = ' * ([SECOND] % 2 == 0 ? 1 : 0.35)' if blink else ''
    return ''.join(seg(i, color, f'<Transform target="alpha" value="([BATTERY_PERCENT] &gt; {i * 10} ? 255 : 0){b}"/>') for i in range(NSEG))


live.append(''.join(seg(i, TRACK) for i in range(NSEG)))
live.append(cond([('bl', E_LOW, arc_fill(REDB, blink=True)), ('bm', '[BATTERY_PERCENT] < 50', arc_fill(YELLOW))], arc_fill(GREEN)))
# charging: the next segment breathes
live.append(cond([('cp', E_CHG, ''.join(seg(i, '#c8ffe0', f'<Transform target="alpha" value="([BATTERY_PERCENT] &gt; {i * 10} &amp;&amp; [BATTERY_PERCENT] &lt;= {(i + 1) * 10}) ? (140 + 115 * sin({SECF} * 6.2832)) : 0"/>') for i in range(NSEG)))]))


# ---------------- the towers: date (left, tap -> calendar) and pulse (right, tap -> heart rate)
PI_, GY0 = GEO['pitch'], GEO['gy0']
WR, WC0, WST = GEO['week']


def row_y(r0, gy): return GY0 + r0 * PI_ - gy


def tower_group(name, side, target, inner):
    x0 = GEO['x0'][side]; gx, gy = x0 - 4 * PI_, 158          # text boxes are 36 cells wide, centred on the 27-column tower
    return f'<Group name="{name}" x="{gx}" y="{gy}" width="{36 * PI_}" height="120"><Launch target="{target}"/>{inner(x0, gx, gy)}</Group>'


def lit2(y, body, color, glow, family='dots', extra=''):
    """dark halo layer for contrast over the skyline + the glowing layer on top"""
    return (dots(0, y, 36 * PI_, body, color, family=family, extra=extra, shade='#cc000000', shade_r=5, shade_dy=0)
            + dots(0, y, 36 * PI_, body, color, glow, family=family, extra=extra))


def date_tower(x0, gx, gy):
    g = '#9946ebff'
    out = lit2(row_y(1, gy), f'<Upper>{tmpl("%s %s", "[DAY]", "[MONTH_S]")}</Upper>', CYAN, g)
    out += lit2(row_y(8, gy), f'<Upper>{tmpl("%s", "[DAY_OF_WEEK_S]")}</Upper>', CYAN, g)
    wx = x0 - gx + WC0 * PI_; wy = row_y(WR, gy)          # today's window in the Sun..Sat row
    out += (f'<PartDraw x="{wx}" y="{wy}" width="{6 * WST * PI_ + 4}" height="4">'
            + ''.join(f'<Rectangle x="{k * WST * PI_ + 0.5}" y="0.5" width="3" height="3"><Fill color="#6e46ebff"/></Rectangle>' for k in range(7))
            + '</PartDraw>')
    out += (f'<PartDraw x="{wx - 2}" y="{wy - 2}" width="8" height="8">'
            f'<Transform target="x" value="{wx - 2} + ([DAY_OF_WEEK] - 1) * {WST * PI_}"/>'
            f'<Rectangle x="0.5" y="0.5" width="7" height="7"><Fill color="#5546ebff"/></Rectangle>'
            f'<Rectangle x="2.5" y="2.5" width="3" height="3"><Fill color="{CYAN}"/></Rectangle></PartDraw>')
    return out


def state(word, blink=False):
    ex = f'<Transform target="alpha" value="([SECOND] % 2 == 0) ? 255 : 120"/>' if blink else ''
    return lit2(0, lit(word), NEON_RED, '#99ff3c5a', extra=ex)


def pulse_tower(x0, gx, gy):
    g = '#99ff3c5a'
    hr = tmpl('\u2665%s', '[HEART_RATE]')
    out = cond([('hr0', '[HEART_RATE] <= 0', lit2(row_y(1, gy), lit('\u2665--'), NEON_RED, g))],
               lit2(row_y(1, gy), hr, NEON_RED, g))
    beat = f'<Transform target="alpha" value="150 + 105 * sin({SECF} * 6.2832 * ([HEART_RATE] &gt; 0 ? [HEART_RATE] : 60) / 60)"/>'
    out += cond([('hb0', '[HEART_RATE] <= 0', dots(0, row_y(1, gy), 36 * PI_, lit('\u2665--'), NEON_RED, g, family='dots_heart', extra=beat))],
                dots(0, row_y(1, gy), 36 * PI_, hr, NEON_RED, g, family='dots_heart', extra=beat))
    out += (f'<Group name="hr_state" x="0" y="{row_y(8, gy)}" width="{36 * PI_}" height="28">'
            + cond([('rush', '[HEART_RATE] >= 140', state('RUSH', blink=True)), ('edge', '[HEART_RATE] >= 100', state('ALERT'))], state('CALM'))
            + '</Group>')
    return out


live.append(tower_group('date_tower', 'l', 'CALENDAR', date_tower))
live.append(tower_group('pulse_tower', 'r', 'HEALTH_HEART_RATE', pulse_tower))

# ---------------- bounty trail with 25/50/75 milestones
TX0, TW = 70, 282
live.append(img(TX0, 374, TW, 3, 'track_dash'))


def trail(color):
    bar = (f'<PartDraw x="{TX0}" y="373" width="{TW}" height="5"><Rectangle x="0" y="0" width="0" height="5"><Fill color="{color}"/>'
           f'<Transform target="width" value="{P} * {TW / 100}"><Animation duration="2.5" interpolation="EASE_IN_OUT"/></Transform></Rectangle></PartDraw>')
    ticks = ''.join(rect(int(TX0 + TW * mk / 100) - 1, 368, 2, 14, color, f'<Transform target="alpha" value="{P} &gt;= {mk} ? 255 : 0"/>') for mk in (25, 50, 75))
    return bar + ticks


for mk in (25, 50, 75):
    live.append(rect(int(TX0 + TW * mk / 100) - 1, 368, 2, 14, '#55555c'))
live.append(cond([('tn', E_NIGHT, trail('#c8102e'))], trail(GOLD)))
live.append(cond([('cd', E_DONE, img(352, 360, 30, 30, 'coin_done')), ('cnn', E_NIGHT, img(352, 360, 30, 30, 'coin_red'))], img(352, 360, 30, 30, 'coin_gold')))

# ---------------- diyas along the path during Diwali
DIYA = ''.join(anim(x, 356, 24, 22, ['diya_0', 'diya_1', 'diya_2', 'diya_1'], 6 + (i % 3), 1, play='ON_VISIBLE', thumb='diya_0', repeat=True)
               for i, x in enumerate((44, 96, 208, 268, 330, 412)))
live.append(cond([('dy', E_DIWALI, f'<Group name="diyas" x="0" y="0" width="480" height="400">{DIYA}</Group>')]))

# ---------------- the hero and his dog: positions
DUOX = f'(63 + 0.97 * {P})'
GX = f'{DUOX} - 32'
GY = 180
MOVE = f'<Transform target="x" value="{GX}"><Animation duration="2.5" interpolation="EASE_IN_OUT"/></Transform>'

pool = (f'<Group name="pool" x="0" y="205" width="240" height="200"><Transform target="x" value="{DUOX} - 19">'
        f'<Animation duration="2.5" interpolation="EASE_IN_OUT"/></Transform>' + img(0, 0, 240, 200, 'pool') + '</Group>')
live.append(pool)
glow = (f'<Group name="glow" x="0" y="250" width="120" height="120"><Transform target="x" value="{DUOX} + 64"/>'
        + img(0, 0, 120, 120, 'glow', f'<Transform target="alpha" value="150 + 100 * sin({SECF} * 6.2832 * [HEART_RATE] / 60)"/>') + '</Group>')
live.append(cond([('adr', f'[HEART_RATE] >= 120 && !({E_DONE})', glow)]))


def duo_group(name, body, fixed_x=None):
    if fixed_x is not None:
        return f'<Group name="{name}" x="{fixed_x}" y="{GY}" width="248" height="232">{body}</Group>'
    return f'<Group name="{name}" x="0" y="{GY}" width="248" height="232">{MOVE}{body}</Group>'


DN = ('day', 'night')
REFL_Y = 195


def refl(kind):
    return cond([('rn', E_NIGHT, img(0, REFL_Y, 248, 26, f'h_refl_{kind}_night'))], img(0, REFL_Y, 248, 26, f'h_refl_{kind}_day'))


# default: walk in on wake, then together; tap for one of three moves
def tap(seq_name):
    return seq(seq_name, ('day', 'am', 'pm', 'night'), play='TAP', thumb=tap_thumb(seq_name))


together = duo_group('duo',
    seq('wake_dog', DN, before='HIDE', after='HIDE', thumb=None)
    + seq('wake_man', DN, before='HIDE', after='HIDE', thumb=None)
    + '<Group name="duo_tap" x="0" y="0" width="248" height="232">'
    + cond([('t1', '[SECOND] < 20', tap('pat')), ('t2', '[SECOND] < 40', tap('coin'))], tap('sip'))
    + mask(248, 232, 'mask_duo', 16, 6) + '</Group>')

morning = duo_group('duo_morning', still('morning_man', ('am',)) + seq('steam', ('none',), repeat=True, thumb='first', play='ON_VISIBLE')
                    + seq('yawn', ('am',), thumb='last'))
hot = duo_group('duo_hot', still('hot_man', ('day', 'pm')) + seq('pant', ('day', 'pm'), repeat=True, rate=6))
rain = duo_group('duo_rain', refl('rain') + seq('shake', DN, thumb='last') + still('rain_man', DN))
storm = duo_group('duo_storm', refl('storm') + still('storm', DN))
snow = duo_group('duo_snow', still('snow', DN) + seq('breath', ('none',), repeat=True, thumb=None, before='HIDE'))
cold = duo_group('duo_cold', still('cold', DN) + seq('breath', ('none',), repeat=True, thumb=None, before='HIDE'))
late = duo_group('duo_late', seq('sleep', ('night',), repeat=True) + still('night_man', ('night',)))
notif = duo_group('duo_notif', still('notif_man', ('day', 'am', 'pm', 'night')) + seq('bark', DN, play='ON_VISIBLE TAP', repeat=True, delay=3))
charging = duo_group('duo_chg', seq('sip', ('day', 'am', 'pm', 'night'), play='ON_VISIBLE TAP', thumb=tap_thumb('sip'), repeat=True, delay=3))
low = duo_group('duo_low', still('low', DN))
behind = duo_group('duo_lean', still('behind', DN))
workout = duo_group('duo_jog', seq('jog', DN, repeat=True))
done = (duo_group('duo_done', seq('cheer', DN, repeat=True, loops=2, delay=2), fixed_x=104)
        + anim(292, 300, 150, 150, fr('burst', 20), 15, 1, before='HIDE', after='HIDE'))
diwali = duo_group('duo_diwali', still('diwali_dog', ('night',)) + still('diwali_man', ('night',)) + seq('sparks', ('none',), repeat=True))
xmas = duo_group('duo_xmas', still('xmas', DN))
nye = duo_group('duo_nye', still('nye', ('night',)))

live.append(cond([('hd', E_DONE, done), ('hn', E_NOTIF, notif), ('hc', E_CHG, charging), ('hl', E_LOW, low), ('hw', E_WORK, workout),
                  ('hs', E_STORM, storm), ('hny', E_NYE, nye), ('hdw', E_DIWALI_NIGHT, diwali), ('hx', E_XMAS, xmas),
                  ('hr', E_RAIN, rain), ('hsn', E_SNOW, snow), ('hco', E_COLD, cold), ('hb', E_BEHIND, behind), ('hh', E_HOT, hot),
                  ('hlt', E_LATE, late), ('hm', E_MORNING, morning)],
                 together))

# ---------------- bounty / contract text
count = text(0, 408, 480, 44, tmpl('%s / %s', '[STEP_COUNT]', '[STEP_GOAL]'), size=34)
def label(s, color, sp=0.2): return text(0, 390, 480, 22, lit(s), size=15, color=color, spacing=sp)
bounty = cond([('tb', E_BEHIND, label('BEHIND PACE · TIME TO MOVE', '#ffb347', 0.16)),
               ('tny', E_NEWYEAR, label('HAPPY NEW YEAR', GOLDL)), ('tdw', E_DIWALI, label('HAPPY DIWALI', '#ffc14d')),
               ('txm', E_XMAS, label('MERRY CHRISTMAS', '#ff6b74'))]) + count     # no everyday label: just the step numbers
done_txt = ('<Group name="done_txt" x="0" y="384" width="480" height="80">'
            + text(0, 6, 480, 32, lit('CONTRACT FULFILLED'), size=22, color='#f4f4f2', spacing=0.17)
            + rect(152, 40, 176, 2, RED)
            + text(0, 44, 480, 26, tmpl('+%s OVERTIME', '[STEP_COUNT] - [STEP_GOAL]'), size=16, color=GOLDL, spacing=0.12)
            + mask(480, 80, 'mask_txt', 20, 15) + '</Group>')
live.append(cond([('dt', E_DONE, done_txt)], bounty))

# ---------------- always-on screen: calm and dim (well under the 10 MB ambient budget)
ax, ay, aw, ah = ART['stills']['aod_duo']
AS = 0.62
aod = ('<Group name="aod" x="0" y="0" width="480" height="480" alpha="0"><Variant mode="AMBIENT" target="alpha" value="255"/>'
       + text(0, 92, 480, 26, f'<Upper>{tmpl(DATE, "[DAY_OF_WEEK_S]", "[DAY_Z]", "[MONTH_S]")}</Upper>', size=18, color='#8c8c94', spacing=0.22)
       + '<Group name="aod_time" x="0" y="124" width="480" height="63">' + clock('#bdbdc2', family='dots', size=90) + '</Group>'
       + text(0, 236, 480, 30, tmpl('%s / %s', '[STEP_COUNT]', '[STEP_GOAL]'), size=22, color='#8a7a48', spacing=0.06)
       + img(round(240 - aw * AS / 2 + 10), round(388 - ah * AS), round(aw * AS), round(ah * AS), 'aod_duo')
       + rect(150, 388, 180, 2, '#3a3a40')
       + '</Group>')

# ---------------- complication slot under the time (next event by default; customisable)
COMP = ('<ComplicationSlot slotId="0" name="under_time" displayName="Under the time" x="140" y="148" width="200" height="26" '
        'supportedTypes="SHORT_TEXT LONG_TEXT EMPTY" isCustomizable="TRUE">'
        '<Variant mode="AMBIENT" target="alpha" value="0"/>'
        '<DefaultProviderPolicy defaultSystemProvider="NEXT_EVENT" defaultSystemProviderType="SHORT_TEXT"/>'
        '<BoundingBox x="0" y="0" width="200" height="26"/>'
        '<Complication type="SHORT_TEXT">'
        + text(0, 0, 200, 26, f'<Upper>{tmpl("%s  %s", "[COMPLICATION.TEXT]", "[COMPLICATION.TITLE]")}</Upper>', size=15, color=CREAM, spacing=0.1, shadow=5)
        + '</Complication>'
        '<Complication type="LONG_TEXT">'
        + text(0, 0, 200, 26, f'<Upper>{tmpl("%s", "[COMPLICATION.TEXT]")}</Upper>', size=15, color=CREAM, spacing=0.08, shadow=5)
        + '</Complication>'
        '<Complication type="EMPTY"></Complication>'
        '</ComplicationSlot>')

xml = f'''<?xml version="1.0" encoding="utf-8"?>
<!-- On the Hunt v2.9.2: steps = today's bounty, battery = health. Original characters (the coffee guy and his golden retriever). -->
<WatchFace width="480" height="480">
  <Metadata key="CLOCK_TYPE" value="DIGITAL"/>
  <Metadata key="PREVIEW_TIME" value="10:08:32"/>
  <Scene backgroundColor="#ff000000">
    <Group name="interactive" x="0" y="0" width="480" height="480" alpha="255">
      <Variant mode="AMBIENT" target="alpha" value="0"/>
      {"".join(live)}
    </Group>
    {aod}
    {COMP}
  </Scene>
</WatchFace>
'''
os.makedirs(os.path.dirname(OUT_XML), exist_ok=True)
open(OUT_XML, 'w').write(xml)
print('written', len(xml))
