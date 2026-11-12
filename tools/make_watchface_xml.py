import json, os
LISTS = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "duo_lists.json")))
OUT_XML = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "watchface/src/main/res/raw/watchface.xml")
"""Generate res/raw/watchface.xml for 'On the Hunt' v2.6 (Watch Face Format v2).
Hero: the coffee guy (original character). Steps = today's bounty, battery = health."""
OSW, OSWM, BOD = 'oswald_regular', 'oswald_medium', 'bebas_neue'
P = '([STEP_PERCENT] &gt; 100 ? 100 : [STEP_PERCENT])'
FIGX = f'(24 + 2.3 * {P})'
DOGX = f'({FIGX} &gt;= 60 ? {FIGX} - 30 : {FIGX} + 72)'
SECF = '(([SECOND] % 60) + [MILLISECOND] / 1000)'
GOLD, GOLDL, RED, CREAM, PINK = '#d4af37', '#ecd27a', '#e0213b', '#e8d9a8', '#ff7a8a'

E_DONE = '[STEP_COUNT] >= [STEP_GOAL] && [STEP_GOAL] > 0'
E_NIGHT = '([WEATHER.IS_AVAILABLE] == 1 && [WEATHER.IS_DAY] == 0) || ([WEATHER.IS_AVAILABLE] != 1 && ([HOUR_0_23] >= 18 || [HOUR_0_23] < 6))'
E_CHG = '[BATTERY_CHARGING_STATUS] == 1'
E_LOW = '[BATTERY_PERCENT] < 20'
E_BEHIND = ('[HOUR_0_23] >= 10 && [HOUR_0_23] < 22 && [STEP_PERCENT] < (([HOUR_0_23] + [MINUTE] / 60 - 8) / 13 * 100 - 30)')
E_DOGLEFT = '(24 + 2.3 * ([STEP_PERCENT] > 100 ? 100 : [STEP_PERCENT])) >= 60'


def wx(*codes):
    return '[WEATHER.IS_AVAILABLE] == 1 && (' + ' || '.join(f'[WEATHER.CONDITION] == {c}' for c in codes) + ')'


E_STORM, E_RAIN, E_SNOW, E_FOG, E_CLOUD = wx(9), wx(4, 6, 10, 12), wx(5, 7, 11), wx(3, 13), wx(2, 14)


def text(x, y, w, h, body, family=OSWM, size=12, color='#ffffff', align='CENTER', spacing=None, extra='', shadow=None):
    ls = f' letterSpacing="{spacing}"' if spacing is not None else ''
    sh = f'<Shadow color="#d8000000" offsetX="0" offsetY="1.5" radius="{shadow}"/>' if shadow else ''
    return (f'<PartText x="{x}" y="{y}" width="{w}" height="{h}">{extra}<Text align="{align}">'
            f'<Font family="{family}" size="{size}" color="{color}"{ls}>{sh}{body}</Font></Text></PartText>')


def tmpl(fmt, *exprs):
    return f'<Template><![CDATA[{fmt}]]>' + ''.join(f'<Parameter expression="{e}"/>' for e in exprs) + '</Template>'


def lit(s): return f'<![CDATA[{s}]]>'
def img(x, y, w, h, res, extra=''): return f'<PartImage x="{x}" y="{y}" width="{w}" height="{h}">{extra}<Image resource="{res}"/></PartImage>'


def rect(x, y, w, h, color, extra=''):
    return f'<PartDraw x="{x}" y="{y}" width="{w}" height="{h}">{extra}<Rectangle x="0" y="0" width="{w}" height="{h}"><Fill color="{color}"/></Rectangle></PartDraw>'


def cond(pairs, default=''):
    ex = ''.join(f'<Expression name="{n}"><![CDATA[{e}]]></Expression>' for n, e, _ in pairs)
    cmp_ = ''.join(f'<Compare expression="{n}">{body}</Compare>' for n, _, body in pairs)
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


live = []

# ---------------- sky (time of day / weather) + city
sky = cond([('sst', E_STORM, img(0, 0, 480, 380, 'sky_storm')),
            ('snt', E_NIGHT, img(0, 0, 480, 380, 'sky_night')),
            ('srn', E_RAIN, img(0, 0, 480, 380, 'sky_rain')),
            ('ssn', E_SNOW, img(0, 0, 480, 380, 'sky_snow')),
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
live.append(cond([('twn', E_NIGHT, img(0, 0, 480, 380, 'towers_night'))], img(0, 0, 480, 380, 'towers_day')))
live.append(sky_bodies('glow'))
live.append(cond([('cn', E_NIGHT, img(0, 176, 480, 204, 'city_night'))], img(0, 176, 480, 204, 'city_day')))

# ---------------- weather above the walking line
rain_layer = img(0, -360, 480, 720, 'wx_rain', f'<Transform target="y" value="(({SECF}) % 3) * 120 - 360"/>')
snow_layer = img(0, -360, 480, 720, 'wx_snow', f'<Transform target="y" value="(({SECF}) % 12) * 30 - 360"/>')
def drift(res): return img(-40, 0, 560, 374, res, f'<Transform target="x" value="-40 + 40 * sin({SECF} * 0.10472)"/>')
flash = img(0, 0, 480, 374, 'wx_storm', '<Transform target="alpha" value="([SECOND] % 5 == 0 &amp;&amp; ([MILLISECOND] &lt; 140 || ([MILLISECOND] &gt; 260 &amp;&amp; [MILLISECOND] &lt; 380))) ? 255 : 0"/>')
weather = cond([('st', E_STORM, rain_layer + flash), ('ra', E_RAIN, rain_layer), ('sn', E_SNOW, snow_layer),
                ('fo', E_FOG, drift('wx_fog')), ('cl', E_CLOUD, drift('wx_cloudy'))])
live.append(f'<Group name="weather" x="0" y="0" width="480" height="480">{weather}</Group>')
live.append(rect(0, 380, 480, 100, '#000000'))

# ---------------- date (+ temperature) and time
DATE = '%s · %s %s'
live.append(cond([('tmp', '[WEATHER.IS_AVAILABLE] == 1',
                   text(0, 26, 480, 26, f'<Upper>{tmpl(DATE + "  ·  %s°", "[DAY_OF_WEEK_S]", "[DAY_Z]", "[MONTH_S]", "[WEATHER.TEMPERATURE]")}</Upper>', size=19, color='#d6d6da', spacing=0.22, shadow=6))],
                 text(0, 26, 480, 26, f'<Upper>{tmpl(DATE, "[DAY_OF_WEEK_S]", "[DAY_Z]", "[MONTH_S]")}</Upper>', size=19, color='#d6d6da', spacing=0.22, shadow=6)))
live.append('<Group name="time" x="0" y="46" width="480" height="124"><Launch target="ALARM"/>'
            + ''.join('<DigitalClock x="0" y="0" width="480" height="124">'
                      f'<TimeText format="hh:mm" hourFormat="SYNC_TO_DEVICE" align="CENTER" x="{dx}" y="{dy}" width="480" height="124"><Font family="{BOD}" size="120" color="{c}"/></TimeText>'
                      '</DigitalClock>' for dx, dy, c in ((0, 4, '#50000000'), (0, 2, '#80000000')))
            + '<DigitalClock x="0" y="0" width="480" height="124">'
            f'<TimeText format="hh:mm" hourFormat="SYNC_TO_DEVICE" align="CENTER" x="0" y="0" width="480" height="124"><Font family="{BOD}" size="120" color="#f4f4f2"/></TimeText>'
            '</DigitalClock></Group>')

# ---------------- health (battery) column, left edge (centre x = 105)
BX = 37
live.append(cond([('chg', E_CHG, img(142, 184, 11, 15, 'ic_bolt'))]))
live.append(text(18, 176, 100, 40, tmpl('%s', '[BATTERY_PERCENT]'), size=32, align='END'))
live.append(text(119, 184, 40, 28, lit('%'), size=21, align='START'))
for i in range(10):
    live.append(rect(BX + i * 14, 218, 10, 10, '#2a2a2e'))


def blocks(color, blink=False):
    b = ' * ([SECOND] % 2 == 0 ? 1 : 0.35)' if blink else ''
    return ''.join(rect(BX + i * 14, 218, 10, 10, color, f'<Transform target="alpha" value="([BATTERY_PERCENT] &gt;= {i * 10 + 5} ? 255 : 0){b}"/>') for i in range(10))


live.append(cond([('bl', E_LOW, blocks('#ff6a3d', True)), ('bn', E_NIGHT, blocks(RED))], blocks(GOLD)))
live.append(cond([('cp', E_CHG, rect(BX, 218, 10, 10, '#ffe08a',
                                     f'<Transform target="x" value="{BX} + 14 * ([BATTERY_PERCENT] &gt;= 95 ? 9 : floor(([BATTERY_PERCENT] + 5) / 10))"/>'
                                     f'<Transform target="alpha" value="140 + 115 * sin({SECF} * 6.2832)"/>'))]))


def status(word, color): return text(18, 232, 175, 18, lit(word), size=13, color=color, spacing=0.12)


live.append(cond([('sc', E_CHG, status('RELOADING…', '#ffe08a')),
                  ('sl', E_LOW, status('CRITICAL', '#ff8a4a')),
                  ('swn', f'[BATTERY_PERCENT] < 50 && ({E_NIGHT})', status('WOUNDED', PINK)),
                  ('sw', '[BATTERY_PERCENT] < 50', status('WOUNDED', CREAM)),
                  ('srn', E_NIGHT, status('COMBAT READY', PINK))],
                 status('COMBAT READY', CREAM)))

# ---------------- heart-rate column, right edge (tap -> heart rate)
def hstatus(word, color): return text(0, 56, 175, 18, lit(word), size=13, color=color, spacing=0.12)


live.append('<Group name="heart" x="288" y="176" width="175" height="74"><Launch target="HEALTH_HEART_RATE"/>'
            + anim(19, 8, 24, 22, fr('heart', 6)[:0] + [f'heart_{i}' for i in range(6)], 8, 1, play='ON_VISIBLE', thumb='heart_0', repeat=True)
            + text(43, 0, 62, 40, tmpl('%s', '[HEART_RATE]'), size=32)
            + text(107, 13, 50, 20, lit('BPM'), size=14, color='#d6d6da', spacing=0.1, align='START')
            + img(32, 40, 110, 14, 'ecg')
            + cond([('rage', '[HEART_RATE] >= 140', hstatus('ADRENALINE', '#ff3b52')),
                    ('edge', '[HEART_RATE] >= 100', hstatus('ON EDGE', PINK)),
                    ('hn', E_NIGHT, hstatus('CALM', PINK))],
                   hstatus('CALM', CREAM))
            + '</Group>')

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

# ---------------- adrenaline glow behind him
glow = (f'<Group name="glow" x="0" y="250" width="120" height="120"><Transform target="x" value="{FIGX} - 10"/>'
        + img(0, 0, 120, 120, 'glow', f'<Transform target="alpha" value="150 + 100 * sin({SECF} * 6.2832 * [HEART_RATE] / 60)"/>') + '</Group>')
live.append(cond([('adr', f'[HEART_RATE] >= 120 && !({E_DONE})', glow)]))

# ---------------- the hero and his dog (always together)
FY = 241
DUOX = f'({FIGX} - 50 &gt;= 30 ? {FIGX} - 50 : 30)'
DMOVE = f'<Transform target="x" value="{DUOX}"><Animation duration="2.5" interpolation="EASE_IN_OUT"/></Transform>'
DOGY = 70

pool_move = (f'<Group name="pool" x="0" y="205" width="240" height="200"><Transform target="x" value="{DUOX} - 20">'
             f'<Animation duration="2.5" interpolation="EASE_IN_OUT"/></Transform>' + img(0, 0, 240, 200, 'pool') + '</Group>')
live.append(cond([('pd', E_DONE, img(184, 205, 240, 200, 'pool'))], pool_move))


def duo_group(name, body):
    return f'<Group name="{name}" x="0" y="{FY}" width="150" height="161">{DMOVE}{body}</Group>'


def tap(seq):
    return anim(0, 0, 150, 161, LISTS[seq], 20, 1, play='TAP', thumb='duo_base')


together = duo_group('duo',
    anim(0, DOGY, 60, 66, LISTS['dog_wake'], 20, 1, play='ON_VISIBLE', before='HIDE', after='HIDE')
    + anim(50, 0, 100, 161, LISTS['man_wake'], 16, 1, play='ON_VISIBLE', before='HIDE', after='HIDE')
    + '<Group name="duo_tap" x="0" y="0" width="150" height="161">'
    + cond([('t1', '[SECOND] < 15', tap('nuzzle')), ('t2', '[SECOND] < 30', tap('coin')), ('t3', '[SECOND] < 45', tap('pat'))], tap('sip'))
    + mask(150, 161, 'mask_duo', 24, 5) + '</Group>')
notif = duo_group('duo_notif', anim(0, 0, 150, 161, LISTS['notif'], 20, 1, play='ON_VISIBLE TAP', thumb='duo_base', repeat=True, delay_repeat=3))
charging = duo_group('duo_chg', img(0, DOGY, 60, 66, 'dog3_look')
                     + anim(50, 0, 100, 161, fr('g_sip', 32), 16, 1, play='ON_VISIBLE TAP', thumb='g_sip_28', repeat=True, delay_repeat=2.5))
low = duo_group('duo_low', img(0, 85, 60, 51, 'dog_lie') + img(50, 0, 100, 161, 'g_tired'))
behind = duo_group('duo_lean', img(0, 85, 60, 51, 'dog_lie_up') + img(50, 0, 100, 161, 'g_lean'))
done = (anim(204, FY + DOGY, 60, 66, fr('dog3_happy', 8), 10, 1, play='ON_VISIBLE', thumb='dog3_happy_00', repeat=True)
        + anim(254, FY, 100, 161, ['g_cheer_00', 'g_cheer_01'], 3, 4, thumb='g_cheer_00')
        + anim(292, 300, 150, 150, fr('burst', 20), 15, 1, before='HIDE', after='HIDE'))
live.append(cond([('hd', E_DONE, done),
                  ('hn', '[UNREAD_NOTIFICATION_COUNT] > 0', notif),
                  ('hc', E_CHG, charging),
                  ('hl', E_LOW, low),
                  ('hb', E_BEHIND, behind)],
                 together))

# ---------------- bounty / contract text
count = text(0, 408, 480, 44, tmpl('%s / %s', '[STEP_COUNT]', '[STEP_GOAL]'), size=34)
bounty = cond([('tb', E_BEHIND, text(0, 390, 480, 22, lit('BEHIND PACE · TIME TO MOVE'), size=15, color='#ffb347', spacing=0.16)),
               ('tn', E_NIGHT, text(0, 390, 480, 22, lit("TONIGHT'S BOUNTY"), size=15, color=PINK, spacing=0.2))],
              text(0, 390, 480, 22, lit("TODAY'S BOUNTY"), size=15, color=GOLDL, spacing=0.2)) + count
done_txt = ('<Group name="done_txt" x="0" y="384" width="480" height="80">'
            + text(0, 6, 480, 32, lit('CONTRACT FULFILLED'), size=22, color='#f4f4f2', spacing=0.17)
            + rect(152, 40, 176, 2, RED)
            + text(0, 44, 480, 26, tmpl('+%s OVERTIME', '[STEP_COUNT] - [STEP_GOAL]'), size=16, color=GOLDL, spacing=0.12)
            + mask(480, 80, 'mask_txt', 20, 15) + '</Group>')
live.append(cond([('dt', E_DONE, done_txt)], bounty))

xml = f'''<?xml version="1.0" encoding="utf-8"?>
<!-- On the Hunt v2.6: steps = today's bounty, battery = health. Original characters (the coffee guy and his golden dog). -->
<WatchFace width="480" height="480">
  <Metadata key="CLOCK_TYPE" value="DIGITAL"/>
  <Metadata key="PREVIEW_TIME" value="10:08:32"/>
  <Scene backgroundColor="#ff000000">
    <Group name="interactive" x="0" y="0" width="480" height="480" alpha="255">
      <Variant mode="AMBIENT" target="alpha" value="0"/>
      {"".join(live)}
    </Group>
  </Scene>
</WatchFace>
'''
open(OUT_XML, 'w').write(xml)
print('written', len(xml))
