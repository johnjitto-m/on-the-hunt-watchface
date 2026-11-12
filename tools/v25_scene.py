"""v2.5 scene bitmaps: calm skies (no baked moon), calm city with the car, towers, sun/moon, light pool + shared bits."""
import math, shutil, sys
sys.path.insert(0, 'tools')
from PIL import Image, ImageDraw, ImageEnhance
import preview_compositor as F

OUT = 'build/v25/'
B3 = 'build/art/'
B4 = 'build/v24/'
FR = 'build/frames/'
half = lambda im: im.resize((im.width // 2, im.height // 2), Image.LANCZOS)

for k in F.SKIES:
    sk = F.sky(k, False).convert('RGB')
    sk = ImageEnhance.Brightness(ImageEnhance.Color(sk).enhance(0.8)).enhance(0.86)
    sk.resize((480, 480), Image.LANCZOS).crop((0, 0, 480, 380)).save(OUT + f'sky_{k}.png')
for n, b in (('city_day', 0.62), ('city_night', 0.75)):
    F.calm(Image.open(B3 + n + '.png').convert('RGBA'), bright=b, blur=0.6).save(OUT + n + '.png')
for n in ('towers_day', 'towers_night'):
    shutil.copy(FR + n + '.png', OUT + n + '.png')
for low, tag in ((0.0, 'high'), (1.0, 'low')):
    half(F.sun_img(low, 'disc')).save(OUT + f'sun_disc_{tag}.png')
    half(F.sun_img(low, 'glow')).save(OUT + f'sun_glow_{tag}.png')
for k in range(8):
    ph = k / 8
    half(F.moon_img(ph if k else 0.02, 'disc')).save(OUT + f'moon_{k}.png')
half(F.moon_img(0.5, 'glow')).save(OUT + 'moon_glow.png')
# warm light pool around the hero (240 x 200; centre of the figure at x=120)
can = Image.new('RGBA', (960, 960), (0, 0, 0, 0)); F.pool(can, 240, 318)
half(can).crop((120, 200, 360, 400)).save(OUT + 'pool.png')
# shared bits from v2.4
for n in ['wx_rain', 'wx_snow', 'wx_cloudy', 'wx_storm', 'wx_fog', 'coin_gold', 'coin_red', 'coin_done', 'ecg', 'ic_bolt', 'glow', 'track_dash'] \
        + [f'heart_{i}' for i in range(6)] + [f'burst_{i:02d}' for i in range(20)]:
    shutil.copy(B4 + n + '.png', OUT + n + '.png')
for name, size in (('mask_fig', (160, 161)), ('mask_dog', (60, 86)), ('mask_txt', (480, 80))):
    Image.new('RGBA', size, (0, 0, 0, 0)).save(OUT + f'{name}_clear.png')
    Image.new('RGBA', size, (255, 255, 255, 255)).save(OUT + f'{name}_solid.png')
print('scene ok')
