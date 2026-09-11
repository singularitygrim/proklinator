#!/usr/bin/env python3
"""ПРОКЛИНАТОР — reproducible asset pipeline (v20.5, ASSETS_UPGRADE).

Every binary this script writes is derived either from an in-house source already in the repository or from a pinned
CC0 download, with no hand edits in between, so anyone can regenerate the set and diff it:

  altar   hero-altar.jpg (in-house, 864×1152)      → assets/splash/altar-9x16.jpg   true 9:16, 1080×1920, centre-safe crop
  icons   icons/icon-512.png (in-house master)     → icons/icon-192.png, icons/apple-touch-icon.png, icons/maskable-512.png
  fx      Kenney Particle Pack + Smoke Particles   → assets/fx/*.png                 CC0 sprites, downscaled, recoloured blood/ember
  grain   ambientCG Paper001 (1K JPG)              → assets/splash/paper-grain.jpg   CC0 paper grain, high-passed, tileable
  verify  checks dimensions / aspect / squareness of everything above (exit 1 on a mismatch)

    python3 tools/build_assets.py all            # rebuild everything (downloads the CC0 sources into --src-dir once)
    python3 tools/build_assets.py verify         # what CI / reviewers run

Requires Pillow (tested with 11.x). No numpy: the recolour is done with per-channel lookup tables so the output
is bit-identical across machines for the same Pillow major version. Downloads are verified against pinned SHA-256s.
"""
import argparse
import hashlib
import io
import os
import sys
import urllib.request
import zipfile

from PIL import Image, ImageChops, ImageFilter, ImageOps

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------------------------------------------------------------------------------------------------------------------
# Pinned third-party sources (all CC0 1.0 Universal — see ATTRIBUTIONS.md)
# ---------------------------------------------------------------------------------------------------------------------
SOURCES = {
    "kenney_particle-pack.zip": {
        "url": "https://kenney.nl/media/pages/assets/particle-pack/f8fe0f8cb8-1677578741/kenney_particle-pack.zip",
        "sha256": "b631d4b07f7002549fdcf155f01141ad482f79f3440e4e301eed49ce5f1d8958",
        "page": "https://kenney.nl/assets/particle-pack",
    },
    "kenney_smoke-particles.zip": {
        "url": "https://kenney.nl/media/pages/assets/smoke-particles/23249a0d35-1677695171/kenney_smoke-particles.zip",
        "sha256": "97a1d09c66e4fd6c247c8ea87f84c0cc59caaeceae19414c995afb1616a1e1c9",
        "page": "https://kenney.nl/assets/smoke-particles",
    },
    "Paper001_1K-JPG.zip": {
        "url": "https://ambientcg.com/get?file=Paper001_1K-JPG.zip",
        "sha256": "5be094ffad8a6343ed96ec728e6eda3d84ae542cd2b16c32bc2ad67bb57a0013",
        "page": "https://ambientcg.com/a/Paper001",
    },
}

SOOT = (11, 9, 8)           # --soot, the app background / manifest colours

# Colour ramps: intensity 0..1 (sprite luminance × alpha) → RGB. Baked into the PNGs so the shipped files already read
# as blood / ember / ash; the ritual shader still multiplies them by the power tint (whisper cools, anathema heats).
RAMPS = {
    "ember": [(0.00, (58, 6, 10)), (0.30, (179, 18, 31)), (0.65, (255, 92, 48)), (1.00, (255, 222, 168))],
    "spark": [(0.00, (120, 12, 24)), (0.45, (255, 90, 60)), (1.00, (255, 244, 226))],
    "ash":   [(0.00, (36, 28, 26)), (0.55, (116, 100, 94)), (1.00, (214, 198, 180))],
    "smoke": [(0.00, (24, 8, 10)), (0.60, (110, 34, 38)), (1.00, (168, 84, 80))],
    "glow":  [(0.00, (70, 8, 14)), (0.60, (200, 30, 40)), (1.00, (255, 132, 96))],
}

# Sprite sheet: output name → (zip, member, ramp, edge size, alpha gain). Sizes are the largest a particle is ever drawn.
FX_SPRITES = [
    ("ember-01.png",  "kenney_particle-pack.zip", "PNG (Transparent)/scorch_02.png", "ember", 128, 1.00),
    ("ember-02.png",  "kenney_particle-pack.zip", "PNG (Transparent)/circle_05.png", "ember", 64,  1.00),
    ("spark-01.png",  "kenney_particle-pack.zip", "PNG (Transparent)/star_07.png",   "spark", 128, 1.00),
    ("ash-01.png",    "kenney_particle-pack.zip", "PNG (Transparent)/dirt_01.png",   "ash",   128, 0.90),
    ("smoke-01.png",  "kenney_particle-pack.zip", "PNG (Transparent)/smoke_08.png",  "smoke", 256, 0.80),
    ("smoke-02.png",  "kenney_smoke-particles.zip", "PNG/Black smoke/blackSmoke12.png", "smoke", 256, 0.80),
    ("crack-01.png",  "kenney_particle-pack.zip", "PNG (Transparent)/spark_05.png",  "spark", 256, 1.00),
    ("sigil-glow.png", "kenney_particle-pack.zip", "PNG (Transparent)/light_02.png", "glow",  256, 0.85),
]


def log(msg):
    print(msg, flush=True)


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def fetch(name, src_dir):
    """Return the local path of a pinned source, downloading it once and refusing a hash mismatch."""
    meta = SOURCES[name]
    os.makedirs(src_dir, exist_ok=True)
    path = os.path.join(src_dir, name)
    if not os.path.exists(path):
        log("  downloading %s" % meta["url"])
        req = urllib.request.Request(meta["url"], headers={"User-Agent": "proklinator-build-assets/1.0"})
        with urllib.request.urlopen(req, timeout=120) as r, open(path, "wb") as f:
            f.write(r.read())
    digest = sha256(path)
    if digest != meta["sha256"]:
        raise SystemExit("SHA-256 mismatch for %s: %s (expected %s) — the upstream file changed; re-review the license and re-pin."
                         % (name, digest, meta["sha256"]))
    return path


# ---------------------------------------------------------------------------------------------------------------------
# altar: true 9:16 splash from the in-house hero
# ---------------------------------------------------------------------------------------------------------------------
ALTAR_SRC = os.path.join(ROOT, "hero-altar.jpg")
ALTAR_OUT = os.path.join(ROOT, "assets", "splash", "altar-9x16.jpg")
ALTAR_SIZE = (1080, 1920)


def build_altar():
    src = Image.open(ALTAR_SRC).convert("RGB")
    w, h = src.size
    # Cover-crop to 9:16 around the horizontal centre: the crown sits on the vertical axis of hero-altar.jpg, the
    # candles / skull / books at the sides are what gets trimmed. (For 864×1152 that is a 648×1152 window at x=108.)
    tw = round(h * 9 / 16)
    if tw > w:
        th = round(w * 16 / 9)
        box = (0, (h - th) // 2, w, (h - th) // 2 + th)
    else:
        box = ((w - tw) // 2, 0, (w - tw) // 2 + tw, h)
    crop = src.crop(box)
    out = crop.resize(ALTAR_SIZE, Image.LANCZOS)
    # The source is 648 px wide inside the window, so 1080 is a 1.67× enlargement — a mild unsharp mask brings the rune
    # edges back; the splash sits under a 50 % soot scrim anyway.
    out = out.filter(ImageFilter.UnsharpMask(radius=1.4, percent=55, threshold=3))
    os.makedirs(os.path.dirname(ALTAR_OUT), exist_ok=True)
    out.save(ALTAR_OUT, "JPEG", quality=84, optimize=True, progressive=True, subsampling=0)
    log("  altar: %s → crop %s → %s (%d bytes)" % (src.size, crop.size, out.size, os.path.getsize(ALTAR_OUT)))


# ---------------------------------------------------------------------------------------------------------------------
# icons: derivatives of the in-house 512 master
# ---------------------------------------------------------------------------------------------------------------------
ICONS_DIR = os.path.join(ROOT, "icons")
ICON_MASTER = os.path.join(ICONS_DIR, "icon-512.png")
SAFE_ZONE = 0.80            # maskable: the OS may crop anything outside the central circle of 80 % diameter


def ring_radius(master):
    """Outer radius (px) of the red sigil ring, measured along the middle row of the master — keeps the maskable
    derivation honest instead of hard-coding a scale."""
    w, h = master.size
    px = master.convert("RGBA").load()
    cy = h // 2
    for x in range(0, w // 2):
        r, g, b, a = px[x, cy]
        if a > 200 and r > 90 and r > g * 2 and r > b * 2:
            return w / 2 - x
    return w * 0.42


def build_icons():
    master = Image.open(ICON_MASTER).convert("RGBA")
    if master.size != (512, 512):
        raise SystemExit("icons/icon-512.png must be the 512×512 master, got %s" % (master.size,))

    # 192 any-purpose: straight downscale, alpha kept.
    master.resize((192, 192), Image.LANCZOS).save(os.path.join(ICONS_DIR, "icon-192.png"), optimize=True)

    # apple-touch-icon 180: iOS ignores alpha and applies its own mask, so flatten onto the soot background first.
    flat = Image.new("RGB", master.size, SOOT)
    flat.paste(master, mask=master.split()[3])
    flat.resize((180, 180), Image.LANCZOS).save(os.path.join(ICONS_DIR, "apple-touch-icon.png"), optimize=True)

    # maskable 512: opaque canvas in the icon's own edge tone, the master scaled so the sigil ring stays inside the safe zone.
    edge = master.convert("RGB").resize((1, 1), Image.BOX).getpixel((0, 0))  # mean tone of the plate
    r_ring = ring_radius(master)
    scale = min(0.94, (256 * SAFE_ZONE - 10) / r_ring)
    side = int(round(512 * scale))
    canvas = Image.new("RGB", (512, 512), edge)
    inner = master.resize((side, side), Image.LANCZOS)
    off = (512 - side) // 2
    canvas.paste(inner, (off, off), inner.split()[3])
    canvas.save(os.path.join(ICONS_DIR, "maskable-512.png"), optimize=True)
    log("  icons: master 512 → 192, apple 180 (flattened on #0B0908), maskable 512 (ring r=%.0f px, content at %.0f %%, edge tone %s)"
        % (r_ring, scale * 100, edge))


# ---------------------------------------------------------------------------------------------------------------------
# fx: Kenney CC0 sprites → blood / ember / ash
# ---------------------------------------------------------------------------------------------------------------------
FX_DIR = os.path.join(ROOT, "assets", "fx")


def ramp_luts(stops):
    """Three 256-entry lookup tables (R, G, B) for a piecewise-linear colour ramp."""
    luts = ([], [], [])
    for i in range(256):
        t = i / 255.0
        lo, hi = stops[0], stops[-1]
        for a, b in zip(stops, stops[1:]):
            if a[0] <= t <= b[0]:
                lo, hi = a, b
                break
        span = (hi[0] - lo[0]) or 1.0
        k = (t - lo[0]) / span
        for c in range(3):
            luts[c].append(int(round(lo[1][c] + (hi[1][c] - lo[1][c]) * k)))
    return luts


def recolor(sprite, ramp, size, alpha_gain):
    sprite = sprite.convert("RGBA")
    # Kenney's transparent-background sprites carry the shape in both luminance and alpha; their product is the
    # intensity that the ramp maps (hot core → pale, thin edges → deep blood).
    lum = sprite.convert("L")
    alpha = sprite.split()[3]
    intensity = ImageChops.multiply(lum, alpha)
    luts = ramp_luts(RAMPS[ramp])
    rgb = Image.merge("RGB", [intensity.point(l) for l in luts])
    if alpha_gain != 1.0:
        alpha = alpha.point(lambda v: min(255, int(round(v * alpha_gain))))
    out = Image.merge("RGBA", (*rgb.split(), alpha))
    return out.resize((size, size), Image.LANCZOS)


def build_fx(src_dir):
    os.makedirs(FX_DIR, exist_ok=True)
    zips = {}
    for out_name, zip_name, member, ramp, size, gain in FX_SPRITES:
        if zip_name not in zips:
            zips[zip_name] = zipfile.ZipFile(fetch(zip_name, src_dir))
        sprite = Image.open(io.BytesIO(zips[zip_name].read(member)))
        img = recolor(sprite, ramp, size, gain)
        path = os.path.join(FX_DIR, out_name)
        img.save(path, optimize=True)
        log("  fx: %-14s ← %s/%s  %s ramp, %d px, %d bytes" % (out_name, zip_name, member, ramp, size, os.path.getsize(path)))
    # The CC0 notice travels with the derived files.
    with zipfile.ZipFile(fetch("kenney_particle-pack.zip", src_dir)) as z:
        lic = z.read("License.txt").decode("utf-8", "replace")
    with open(os.path.join(FX_DIR, "LICENSE-kenney.txt"), "w", encoding="utf-8", newline="\n") as f:
        f.write(lic.replace("\r\n", "\n"))
        f.write("\n\n---\nThe PNGs in this folder are downscaled, recoloured derivatives of the Kenney Particle Pack / Smoke Particles "
                "sprites listed in tools/build_assets.py (FX_SPRITES). CC0 1.0 Universal: https://creativecommons.org/publicdomain/zero/1.0/\n")


# ---------------------------------------------------------------------------------------------------------------------
# grain: ambientCG Paper001 → neutral, tileable grain for the splash surface (used at ≤ 6 % opacity)
# ---------------------------------------------------------------------------------------------------------------------
GRAIN_OUT = os.path.join(ROOT, "assets", "splash", "paper-grain.jpg")
GRAIN_SIZE = (640, 375)     # the whole 1024×600 tile scaled down, so the seamless edges survive


def build_grain(src_dir):
    with zipfile.ZipFile(fetch("Paper001_1K-JPG.zip", src_dir)) as z:
        color = Image.open(io.BytesIO(z.read("Paper001_1K-JPG_Color.jpg"))).convert("L")
    w, h = color.size
    # High-pass on a 3×3 tiling so the blur wraps and the result stays seamless; then normalise around mid-grey.
    tiled = Image.new("L", (w * 3, h * 3))
    for i in range(3):
        for j in range(3):
            tiled.paste(color, (i * w, j * h))
    low = tiled.filter(ImageFilter.GaussianBlur(radius=18)).crop((w, h, 2 * w, 2 * h))
    high = ImageChops.subtract(color, low, scale=1.0, offset=128)
    grain = ImageOps.autocontrast(high, cutoff=0.5)
    grain = grain.resize(GRAIN_SIZE, Image.LANCZOS)
    grain.save(GRAIN_OUT, "JPEG", quality=86, optimize=True, progressive=True)
    log("  grain: Paper001 %s → %s (%d bytes)" % (color.size, grain.size, os.path.getsize(GRAIN_OUT)))


# ---------------------------------------------------------------------------------------------------------------------
# verify
# ---------------------------------------------------------------------------------------------------------------------
def verify():
    ok = True

    def check(cond, msg):
        nonlocal ok
        log(("  ok   " if cond else "  FAIL ") + msg)
        ok = ok and cond

    def dims(path):
        with Image.open(path) as im:
            return im.format, im.size, im.mode

    fmt, size, _ = dims(ALTAR_OUT)
    check(fmt == "JPEG" and size == ALTAR_SIZE and abs(size[0] / size[1] - 9 / 16) < 1e-6,
          "assets/splash/altar-9x16.jpg is %s %dx%d (true 9:16)" % (fmt, size[0], size[1]))
    stale = os.path.join(ROOT, "assets", "splash", "altar-9x16.png")
    check(not os.path.exists(stale), "the mislabeled 1280×720 altar-9x16.png is gone")

    for name, want in (("icon-512.png", 512), ("icon-192.png", 192), ("apple-touch-icon.png", 180), ("maskable-512.png", 512)):
        fmt, size, mode = dims(os.path.join(ICONS_DIR, name))
        check(fmt == "PNG" and size == (want, want), "icons/%s is %s %dx%d %s (square)" % (name, fmt, size[0], size[1], mode))

    for out_name, _z, _m, _r, want, _g in FX_SPRITES:
        path = os.path.join(FX_DIR, out_name)
        if not os.path.exists(path):
            check(False, "assets/fx/%s missing" % out_name)
            continue
        fmt, size, mode = dims(path)
        check(fmt == "PNG" and size == (want, want) and mode == "RGBA", "assets/fx/%s is %s %dx%d %s" % (out_name, fmt, size[0], size[1], mode))
    check(os.path.exists(os.path.join(FX_DIR, "LICENSE-kenney.txt")), "assets/fx/LICENSE-kenney.txt present")

    fmt, size, _ = dims(GRAIN_OUT)
    check(fmt == "JPEG" and size == GRAIN_SIZE, "assets/splash/paper-grain.jpg is %s %dx%d" % (fmt, size[0], size[1]))

    if not ok:
        raise SystemExit(1)
    log("all asset checks passed")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("steps", nargs="*", default=["verify"], help="altar icons fx grain verify all (default: verify)")
    ap.add_argument("--src-dir", default=os.path.join(ROOT, ".asset-sources"),
                    help="where pinned downloads are cached (git-ignored; default .asset-sources/)")
    args = ap.parse_args()
    steps = args.steps
    if "all" in steps:
        steps = ["altar", "icons", "fx", "grain", "verify"]
    for step in steps:
        log("[%s]" % step)
        if step == "altar":
            build_altar()
        elif step == "icons":
            build_icons()
        elif step == "fx":
            build_fx(args.src_dir)
        elif step == "grain":
            build_grain(args.src_dir)
        elif step == "verify":
            verify()
        else:
            raise SystemExit("unknown step: %s" % step)


if __name__ == "__main__":
    main()
