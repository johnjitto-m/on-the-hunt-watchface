# Tools

Run everything from the repository root (Python 3.11+, Pillow, Playwright with Google Chrome, `xmlschema`).

| Script | What it does |
|---|---|
| `make_watchface_xml.py` | Writes `watchface/src/main/res/raw/watchface.xml` (Watch Face Format v2) |
| `real_guy.py`, `coffee_guy.py`, `v25_frames.py` | The hero (realistic style): every pose and animation frame |
| `dog2.py`, `dog3.py` | The golden dog: drawing (dog2) and the rigged skeleton for smooth stand/sit/trot (dog3) |
| `guy2.py` | Detail pass for the coffee guy (face, denim, boots, natural walk) |
| `duo.py` | Man + dog interaction frames (wake, scratch, coin, pat, coffee, notification) |
| `towers.py`, `v25_scene.py` | Full-height skyline, skies, sun, moon phases, light pool |
| `real_car.py`, `render_v24.py` | The classic car and the city backdrops (day/night), weather tiles |
| `support_art.py` | Mirrored frames, dog trick, confetti burst, skies, trail, masks |
| `preview_compositor.py`, `v26_check.py` | Composite still previews of the face (screenshots and the picker preview) |
| `render_v2.py`, `backdrops.py`, `color_poses.py`, `characters.py`, `styles.py` | Shared rendering helpers and the city art |

Intermediate art is written to `build/art/`; final bitmaps go to `watchface/src/main/res/drawable/`.
