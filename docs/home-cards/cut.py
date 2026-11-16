"""届いた絵から、場面のコマと、猫・柴犬・女の子の切りぬきを作る。"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

SRC = Path(sys.argv[1])
OUT = Path(sys.argv[2])
OUT.mkdir(parents=True, exist_ok=True)

SCENES = {
    "market": ("6.jpg", (10, 10, 298, 397)),
    "castle": ("4.jpg", (625, 948, 912, 1350)),
    "scooter": ("5.jpg", (318, 480, 605, 862)),
    "hike": ("2.jpg", (623, 497, 912, 890)),
}
COLS = [(8, 300), (316, 608), (624, 916)]
CAT_ROWS = [(85, 550), (566, 1010), (1026, 1490), (1506, 1990)]
DOG_ROWS = [(25, 500), (520, 1005), (1026, 1465), (1486, 1990)]
CUTS = {
    "cat-sit": ("10.jpg", CAT_ROWS, 0, 0),
    "cat-loaf": ("10.jpg", CAT_ROWS, 1, 2),
    "cat-beg": ("10.jpg", CAT_ROWS, 2, 0),
    "cat-wave": ("10.jpg", CAT_ROWS, 3, 0),
    "cat-sleep": ("10.jpg", CAT_ROWS, 1, 1),
    "dog-sit": ("9.jpg", DOG_ROWS, 0, 0),
    "dog-jump": ("9.jpg", DOG_ROWS, 0, 1),
    "dog-loaf": ("9.jpg", DOG_ROWS, 1, 2),
    "dog-beg": ("9.jpg", DOG_ROWS, 2, 0),
    "dog-bow": ("9.jpg", DOG_ROWS, 2, 2),
    "dog-smile": ("9.jpg", DOG_ROWS, 3, 0),
}


def cutout(im, thr=243):
    """ふちとつながった白だけを透明にする。"""
    im = im.convert("RGB")
    w, h = im.size
    near = im.point(lambda v: 255 if v > thr else 0).convert("L")
    # 3色とも白に近い所だけ
    r, g, b = im.split()
    mask = Image.eval(r, lambda v: 255 if v > thr else 0)
    for ch in (g, b):
        m2 = Image.eval(ch, lambda v: 255 if v > thr else 0)
        mask = Image.composite(mask, Image.new("L", (w, h), 0), m2)
    pad = Image.new("L", (w + 2, h + 2), 255)
    pad.paste(mask, (1, 1))
    ImageDraw.floodfill(pad, (0, 0), 128)
    bg = pad.crop((1, 1, w + 1, h + 1)).point(lambda v: 255 if v == 128 else 0)
    alpha = Image.eval(bg, lambda v: 255 - v)
    alpha = alpha.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(0.7))
    out = im.convert("RGBA")
    out.putalpha(alpha)
    box = alpha.point(lambda v: 255 if v > 20 else 0).getbbox()
    return out.crop(box) if box else out


for name, (f, box) in SCENES.items():
    Image.open(SRC / f).convert("RGB").crop(box).save(OUT / f"scene-{name}.png")

for name, (f, rows, r, c) in CUTS.items():
    x0, x1 = COLS[c]
    y0, y1 = rows[r]
    cutout(Image.open(SRC / f).crop((x0, y0, x1, y1))).save(OUT / f"{name}.png")

cutout(Image.open(SRC / "11.webp").crop((120, 150, 800, 1850))).save(OUT / "girl-stand.png")

# 確かめ用の一覧(色つきの背景にのせて、ふちの白残りを見る)
names = sorted(p for p in OUT.glob("*.png") if p.name != "check.png")
sheet = Image.new("RGB", (5 * 220, ((len(names) + 4) // 5) * 260), (120, 170, 140))
for i, p in enumerate(names):
    im = Image.open(p).convert("RGBA")
    im.thumbnail((210, 250))
    sheet.paste(im, ((i % 5) * 220 + 5, (i // 5) * 260 + 5), im)
sheet.save(OUT / "check.png")
print(len(names), "files")
