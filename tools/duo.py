"""v2.6 'together' frames: calm, smooth man + dog interactions (golden rigged dog + detailed coffee guy).
Outputs (OUT): man_wake_*, dog_wake_*, duo_base, duo_sip_*, duo_coin_*, duo_pat_*, duo_nuzzle_*, duo_notif_*,
dog_trot_*, dog3 stills, dog3 happy frames.  Duo box 150x161: dog box (60x66) at (0, 69.8), man box at (50, 0)."""
import asyncio, math, os, sys
sys.path.insert(0, 'tools'); sys.path.insert(0, 'tools')
import render_v2 as R
import guy2, real_guy as G, coffee_guy as C, dog2 as D2, dog3 as D
from PIL import Image, ImageDraw, ImageFont, ImageOps

OUT = sys.argv[1] if len(sys.argv) > 1 else 'watchface/src/main/res/drawable/'
SRC = 'build/v25/'          # v2.5 man frames (rim-lit)
RAW = 'build/duo_raw/'
os.makedirs(RAW, exist_ok=True); os.makedirs(OUT, exist_ok=True)
R.OUT = RAW
DOGY = 69.8
ease, lerp = D.ease, D.lerp
jobs = {}


def dog(name, svgbody):
    if name not in jobs:
        jobs[name] = ('dog', svgbody)
    return name


def man(name, body, w=100, vbw=240):
    if name not in jobs:
        jobs[name] = ('man', (body, w, vbw))
    return name


# ------------------------------------------------------------------ plans (lists of per-frame specs)
def wake_dog_plan(fps=20):
    plan = []
    for k in range(60):                                    # 3.0 s trot (12-frame cycle)
        plan.append(dog(f'trot_{k % 12:02d}', D.trot((k % 12) / 12)))
    n = int(1.8 * fps)
    for k in range(n):
        t = k / fps
        if t < 0.25:
            plan.append(dog('stand', D.stand_pose()))
        elif t < 0.85:
            u = (t - 0.25) / 0.6; q = round(u * 12) / 12
            plan.append(dog(f'sitdown_{q:.3f}', D.blend_sit(q)))
        elif t < 1.65:
            v = ease((t - 0.85) / 0.4) if t < 1.25 else 1 - ease((t - 1.35) / 0.3) if t > 1.35 else 1
            ha = round(lerp(-6, -28, v)); wag = round(10 * math.sin((t - 0.85) * 14)) if t < 1.5 else 0
            plan.append(dog(f'sit_h{ha}_w{wag}', D.sit_pose(head_a=ha, tail_a=wag)))
        else:
            plan.append(dog('sit_h-6_w0', D.sit_pose(head_a=-6)))
    return plan


def wake_man_plan(fps=16):
    plan = [('src', f'g_walk_{k % 24:02d}') for k in range(48)]  # 3.0 s walk
    n = int(1.8 * fps)
    for k in range(n):
        t = k / fps
        if t < 0.3:
            plan.append(('blend', f'g_walk_{(48 + k) % 24:02d}', man('front_0', C.front()), t / 0.3))
        else:
            if t < 0.75: v = 0
            elif t < 1.15: v = ease((t - 0.75) / 0.4)
            elif t < 1.45: v = 1
            else: v = 1 - ease((t - 1.45) / 0.3)
            q = round(v * 6) / 6
            plan.append(('man', man(f'front_l{q:.2f}', C.front(0, -7 * q, q, 0.6 * q))))
    return plan


def duo_sip(fps=20):
    out = []
    for k in range(32):
        u = k / 31
        raised = 1.0 if 0.1 < u < 0.55 else (u / 0.1 if u <= 0.1 else max(0, 1 - (u - 0.55) / 0.15))
        ha = round(lerp(-6, -26, ease(raised))); wag = round(8 * math.sin(k * 0.7))
        out.append(dict(man=('src', f'g_sip_{k:02d}'), dog=dog(f'sit_h{ha}_w{wag}', D.sit_pose(head_a=ha, tail_a=wag))))
    return out


def duo_coin(fps=20):
    out = []
    for k in range(40):
        fi = k * 29 / 39
        h = 4 * ((fi - 4) / 18) * (1 - (fi - 4) / 18) if 4 <= fi <= 22 else 0
        ha = round(lerp(-10, -42, h)); ears = 0.8 * h
        wag = round(6 * math.sin(k * 0.6)) if fi > 22 else 0
        out.append(dict(man=('src', f'g_coin_{k:02d}'), dog=dog(f'sit_h{ha}_w{wag}_e{ears:.1f}', D.sit_pose(head_a=ha, tail_a=wag, ears=ears))))
    return out


def duo_pat(base, fps=20):
    out = []
    for k in range(44):
        fi = k * 29 / 43
        touching = 6 <= fi <= 24
        ha = round(4 if touching else -6); wag = round(12 * math.sin(k * 0.9)) if touching else 0
        out.append(dict(man=('pat', man(f'patm_{k:02d}', C.pat_frame(fi, base), 130, 312)),
                        dog=dog(f'sit_h{ha}_w{wag}_c{int(touching)}', D.sit_pose(head_a=ha, tail_a=wag, eyes_closed=touching))))
    return out


def duo_nuzzle(fps=20):
    out = []
    n = 48
    for k in range(n):
        t = k / fps
        if t < 0.4:                       # stands up
            u = 1 - t / 0.4; q = round(u * 8) / 8
            d = dog(f'sitdown_{q:.3f}', D.blend_sit(q)); arm = 0; look = 0; x = 0
        elif t < 0.8:                     # steps in, head up to his hand
            u = (t - 0.4) / 0.4; x = round(55 * ease(u)); ha = round(lerp(0, -38, ease(u)))
            d = dog(f'step_h{ha}_p{k}', D.pose(head_a=ha, fl=(10 * math.sin(u * math.pi), 0.6 * math.sin(u * math.pi)), hf=(8 * math.sin(u * math.pi), 0.5 * math.sin(u * math.pi))))
            arm = 12 * ease(u); look = ease(u)
        elif t < 1.75:                    # he scratches its head; it leans into his hand
            w = math.sin((t - 0.8) * 16)
            ha = round(-38 + 4 * w); wag = round(14 * math.sin((t - 0.8) * 18))
            d = dog(f'nuz_h{ha}_w{wag}', D.pose(head_a=ha, tail_a=wag, eyes_closed=True)); x = 55
            arm = 12 + 3 * w; look = 1
        elif t < 2.05:                    # steps back
            u = (t - 1.75) / 0.3; x = round(55 * (1 - ease(u))); ha = round(lerp(-38, 0, ease(u)))
            d = dog(f'back_h{ha}_{k}', D.pose(head_a=ha, hl=(-8 * math.sin(u * math.pi), 0.5 * math.sin(u * math.pi))))
            arm = 12 * (1 - ease(u)); look = 1 - ease(u)
        else:                             # sits again
            u = min(1, (t - 2.05) / 0.35); q = round(u * 8) / 8
            d = dog(f'sitdown_{q:.3f}', D.blend_sit(q)); arm = 0; look = 0; x = 0
        a, l = round(arm, 1), round(look * 4) / 4
        out.append(dict(man=('man', man(f'front_a{a}_l{l:.2f}', C.front(a, -9 * l, l, 0.8 * l))), dog=d, dog_top=True, dog_dx=x * 0.4))
    return out


def duo_notif(fps=20):
    out = []
    for k in range(40):
        t = k / fps
        bubble = 0
        if t < 0.4:
            q = round((1 - t / 0.4) * 8) / 8; d = dog(f'sitdown_{q:.3f}', D.blend_sit(q)); look = 0
        elif t < 1.5:
            bark = int((t - 0.4) / 0.27) % 2 == 0 and t < 1.2
            d = dog(f'bark_m{int(bark)}', D.pose(head_a=-14, mouth=bark, ears=1.0)); bubble = 1 if bark else 0
            look = ease(min(1, (t - 0.4) / 0.3))
        else:
            q = round(min(1, (t - 1.5) / 0.4) * 8) / 8; d = dog(f'sitdown_{q:.3f}', D.blend_sit(q)); look = 1 - ease(min(1, (t - 1.5) / 0.4))
        l = round(look * 4) / 4
        out.append(dict(man=('man', man(f'front_l{l:.2f}', C.front(0, -7 * l, l, 0))), dog=d, bubble=bubble))
    return out


if __name__ == '__main__':
    # pat target for the rigged dog's head (dog box at duo x 0, y 69.8; head point (34, 20) in the dog box)
    target = ((150 - 34) / (100 / 240) - 40, (DOGY + 20) / (100 / 240) - 26.667)
    best = None
    for dx in range(-30, 61, 2):
        b = C.solve_reach(target, C.KNEEL['lean'], dx, C.KNEEL['bob'])
        if best is None or b[0] < best[0][0] - 0.5: best = (b, dx)
    pat_base, C.KNEEL['dx'] = best
    print('pat reach', pat_base, 'dx', best[1])

    WD, WM = wake_dog_plan(), wake_man_plan()
    SEQ = dict(sip=duo_sip(), coin=duo_coin(), pat=duo_pat(pat_base), nuzzle=duo_nuzzle(), notif=duo_notif())
    base_dog = dog('sit_h-6_w0', D.sit_pose(head_a=-6))
    stills = {'dog_lie': D2.svg(D2.lying(0, 0, bone=False, head_up=0.0), D2.WALK_W, D2.WALK_H, D2.WALK_VB),
              'dog_lie_up': D2.svg(D2.lying(0, 0, bone=False, head_up=1.0), D2.WALK_W, D2.WALK_H, D2.WALK_VB)}
    happy = []
    for i in range(8):
        u = i / 8; hop = abs(math.sin(2 * math.pi * u))
        happy.append(dog(f'happy_{i}', D.pose(fl=(-30 * hop, 0.7 * hop), ff=(-24 * hop, 0.6 * hop), hl=(8 * hop, 0.2), hf=(4 * hop, 0.1),
                                              head_a=-18, mouth=True, ears=0.6, tail_a=-20 + 24 * math.sin(4 * math.pi * u), bob=-8 * hop, theta=-10 * hop)))
    R.JOBS.clear()
    for name, (kind, body) in jobs.items():
        if kind == 'dog':
            R.job('dg_' + name, D.svg(body), D.BW, D.BH)
        else:
            b, w, vbw = body
            R.job('mn_' + name, C.svgbox(b, w, 161, vbx=0, vbw=vbw), w, 161)
    for n, sv in stills.items():
        R.job(n, sv, D2.WALK_W, D2.WALK_H)
    print('rendering', len(R.JOBS))
    asyncio.run(R.main())

    import preview_compositor as F
    cache = {}
    def LD(n):
        if ('d', n) not in cache: cache[('d', n)] = F.rim(Image.open(RAW + 'dg_' + n + '.png').convert('RGBA'), strength=170)
        return cache[('d', n)]
    def LM(spec):
        kind = spec[0]
        if kind == 'src': return Image.open(SRC + spec[1] + '.png').convert('RGBA')
        if kind in ('man', 'pat'):
            k = ('m', spec[1])
            if k not in cache:
                im = Image.open(RAW + 'mn_' + spec[1] + '.png').convert('RGBA')
                if kind == 'pat': im = ImageOps.mirror(im)
                cache[k] = F.rim(im, strength=230)
            return cache[k]
        if kind == 'blend':
            a = Image.open(SRC + spec[1] + '.png').convert('RGBA'); b = LM(('man', spec[2]))
            return Image.blend(a, b, spec[3])
    FONT = ImageFont.truetype('watchface/src/main/res/font/bebas_neue.ttf', 44)

    def small_bubble():
        W, H = 44 * 4, 26 * 4
        b = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(b)
        d.rounded_rectangle([6, 6, W - 6, H - 30], radius=30, fill=(250, 246, 236, 255), outline=(30, 26, 20, 255), width=6)
        d.polygon([(40, H - 34), (24, H - 4), (70, H - 34)], fill=(250, 246, 236, 255))
        d.line([(40, H - 31), (24, H - 4), (70, H - 31)], fill=(30, 26, 20, 255), width=6)
        tw = d.textlength('WOOF', font=FONT)
        d.text(((W - tw) / 2, 14), 'WOOF', font=FONT, fill=(176, 28, 40, 255))
        return b.resize((44, 26), Image.LANCZOS)
    BUB = small_bubble()

    def duo(spec):
        im = Image.new('RGBA', (150, 161), (0, 0, 0, 0))
        mimg = LM(spec['man']); mx = 20 if spec['man'][0] == 'pat' else 50
        dimg = LD(spec['dog'])
        if spec.get('dog_top'):
            im.alpha_composite(mimg, (mx, 0)); im.alpha_composite(dimg, (int(round(spec.get('dog_dx', 0))), int(round(DOGY))))
        else:
            im.alpha_composite(dimg, (0, int(round(DOGY)))); im.alpha_composite(mimg, (mx, 0))
        if spec.get('bubble'):
            im.alpha_composite(BUB, (34, 52))
        return im

    for i, n in enumerate(WD): LD(n).save(OUT + f'dog_wake_{i:03d}.png') if False else None
    # dog wake: unique images + reference list (saved for the XML generator)
    uniq = {}
    seq = []
    for n in WD:
        if n not in uniq:
            uniq[n] = f'dw_{len(uniq):02d}'; LD(n).save(OUT + uniq[n] + '.png')
        seq.append(uniq[n])
    muniq, mseq = {}, []
    for spec in WM:
        key = spec if spec[0] != 'blend' else ('blend', spec[1], spec[2], round(spec[3], 2))
        if key not in muniq:
            muniq[key] = f'mw_{len(muniq):02d}'; LM(spec).save(OUT + muniq[key] + '.png')
        mseq.append(muniq[key])
    duo(dict(man=('man', man('front_0', C.front())), dog=base_dog)).save(OUT + 'duo_base.png')
    lists = dict(dog_wake=seq, man_wake=mseq)
    for name, frames in SEQ.items():
        names = []
        for k, spec in enumerate(frames):
            nm = f'duo_{name}_{k:02d}'; duo(spec).save(OUT + nm + '.png'); names.append(nm)
        lists[name] = names
    for i, n in enumerate(happy): LD(n).save(OUT + f'dog3_happy_{i:02d}.png')
    LD('sit_h-6_w0').save(OUT + 'dog3_sit.png'); LD('sit_h-24_w0').save(OUT + 'dog3_look.png') if ('d', 'sit_h-24_w0') in cache else None
    for n in stills: F.rim(Image.open(RAW + n + '.png').convert('RGBA'), strength=170).save(OUT + n + '.png')
    import json; json.dump(lists, open(OUT + '../../duo_lists.json', 'w'))
    print('duo done', {k: len(v) for k, v in lists.items()})
