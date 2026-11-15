# Tools

Run everything from the repository root (Python 3.11+, Pillow, NumPy, fontTools, Playwright with Google Chrome, `xmlschema`).

## Current face (v2.7 → v2.9)

| Script | What it does |
|---|---|
| `make_watchface_xml.py` | Writes `watchface/src/main/res/raw/watchface.xml` (Watch Face Format v2). Reads `art28.json` (where every bitmap goes) and `towers29.json` (the dot-text grid) |
| `dotfont.py` | Builds the **Hunt Dots** fonts into `res/font/`: `dots.ttf` (date / heart rate), `dots_heart.ttf` (the beating heart), `dots_time.ttf` (the clock) |
| `rig28.py` | The man's rig: 3D two-bone IK arms and legs, bending sleeves, posable hands, keyframe tracks with easing |
| `retriever.py` | The golden retriever: sitting pose, head, ears, swept tail, blinks |
| `v27.py` | Scene builder shared by the generators: outfits, umbrella, cups, jog, sleeping dog, festival props |
| `clip28.py` | The tap choreography (pat, coin flip, sip) and a motion-test video |
| `gen28.py` | Renders every mood, tap animation, festival and lighting grade into `res/drawable/` and updates `art28.json` (`--norender --only <prefix>` re-composes without re-rendering) |
| `extras28.py` | Scene extras: fireworks, diyas, string lights, wet reflections, masks, the always-on silhouette (set `PREV_RES` to the previous version's `res/` to carry assets over) |
| `preview_compositor.py`, `v25_check.py`, `v28_check.py`, `v29_check.py` | Composite still previews of the face (screenshots and the picker preview). `v29_check.py` needs the `h_base_*` stills: run `gen28.py --norender --only base` first, and delete them after |

## Earlier versions (still used for shared art)

| Script | What it does |
|---|---|
| `real_guy.py`, `coffee_guy.py`, `v25_frames.py` | The v2.4–2.6 hero: poses and animation frames |
| `dog2.py`, `dog3.py` | The v2.6 dog: drawing (dog2) and the rigged skeleton (dog3); `limb()` is reused by the new rig |
| `guy2.py` | Detail pass for the coffee guy (face, denim, boots, natural walk) |
| `duo.py`, `v26_check.py` | v2.6 man + dog interaction frames and previews (`duo_lists.json`) |
| `towers.py`, `v25_scene.py` | Full-height skyline, skies, sun, moon phases, light pool |
| `real_car.py`, `render_v24.py` | The classic car and the city backdrops (day/night), weather tiles |
| `render_v2.py`, `backdrops.py`, `color_poses.py`, `characters.py`, `styles.py`, `make_video.py` | Shared rendering helpers, the city art and the video tools |

Fonts used only by the preview/video tools live in `tools/fonts/`. Intermediate art is written to `build/`; final bitmaps go to `watchface/src/main/res/drawable/`.
