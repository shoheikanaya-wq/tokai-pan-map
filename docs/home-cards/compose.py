"""切り分けた絵から、ホーム用のカードの絵(600x660)を5枚作る。"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont

CUT = Path(sys.argv[1])
OUT = Path(sys.argv[2])
OUT.mkdir(parents=True, exist_ok=True)
W, H = 600, 660


def load(name):
    return Image.open(CUT / f"{name}.png").convert("RGBA")


def fit_h(im, h):
    return im.resize((round(im.width * h / im.height), h), Image.LANCZOS)


def shadow_paste(canvas, im, xy):
    """うすい影をつけてのせる。"""
    x, y = xy
    sh = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    a = im.split()[3].point(lambda v: int(v * 0.35))
    blk = Image.new("RGBA", im.size, (60, 40, 20, 0))
    blk.putalpha(a)
    sh.paste(blk, (x + 4, y + 6), blk)
    sh = sh.filter(ImageFilter.GaussianBlur(5))
    canvas.alpha_composite(sh)
    canvas.alpha_composite(im, (x, y))


def scene_card(scene, top, cat, dog, cat_h=210, dog_h=220):
    src = load(f"scene-{scene}")
    big = src.resize((W, round(src.height * W / src.width)), Image.LANCZOS)
    top = max(0, min(top, big.height - H))
    c = big.crop((0, top, W, top + H)).convert("RGBA")
    ci, di = fit_h(load(cat), cat_h), fit_h(load(dog), dog_h)
    shadow_paste(c, ci, (6, H - ci.height - 4))
    shadow_paste(c, di, (W - di.width - 6, H - di.height - 4))
    return c


def gradient(c1, c2):
    g = Image.new("RGBA", (W, H))
    d = ImageDraw.Draw(g)
    for y in range(H):
        t = y / (H - 1)
        d.line([(0, y), (W, y)], fill=tuple(round(a + (b - a) * t) for a, b in zip(c1, c2)) + (255,))
    return g


def trio(canvas, cat, dog, girl_h=560, cat_h=230, dog_h=240):
    g = fit_h(load("girl-stand"), girl_h)
    shadow_paste(canvas, g, ((W - g.width) // 2, H - g.height - 10))
    ci, di = fit_h(load(cat), cat_h), fit_h(load(dog), dog_h)
    shadow_paste(canvas, ci, (14, H - ci.height - 6))
    shadow_paste(canvas, di, (W - di.width - 14, H - di.height - 6))
    return canvas


def onsen_card():
    c = gradient((255, 243, 226), (250, 205, 170))
    d = ImageDraw.Draw(c)
    # のれん
    d.rectangle([0, 0, W, 120], fill=(41, 62, 110, 255))
    for x in range(0, W, 150):
        d.rectangle([x + 146, 60, x + 150, 120], fill=(255, 243, 226, 255))
    try:
        f = ImageFont.truetype("C:/Windows/Fonts/meiryob.ttc", 84)
        d.text((W // 2, 60), "ゆ", font=f, fill=(255, 250, 240, 255), anchor="mm")
    except OSError:
        pass
    # ゆげ
    steam = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(steam)
    for cx, cy, r in [(95, 215, 50), (505, 225, 54), (300, 165, 34)]:
        sd.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 255, 255, 150))
    c.alpha_composite(steam.filter(ImageFilter.GaussianBlur(18)))
    # 石の床
    d = ImageDraw.Draw(c)
    d.rectangle([0, H - 70, W, H], fill=(196, 170, 140, 255))
    return trio(c, "cat-sleep", "dog-loaf", girl_h=500, cat_h=170, dog_h=210)


def fudosan_card():
    c = gradient((205, 232, 250), (236, 246, 226))
    d = ImageDraw.Draw(c)
    d.rectangle([0, H - 80, W, H], fill=(150, 200, 120, 255))
    # 家
    d.polygon([(110, 250), (300, 110), (490, 250)], fill=(190, 84, 60, 255))
    d.rectangle([145, 250, 455, 590], fill=(255, 248, 232, 255), outline=(122, 75, 32, 255), width=5)
    d.rectangle([180, 300, 260, 380], fill=(170, 215, 240, 255), outline=(122, 75, 32, 255), width=5)
    d.rectangle([340, 300, 420, 380], fill=(170, 215, 240, 255), outline=(122, 75, 32, 255), width=5)
    d.rectangle([390, 150, 425, 215], fill=(150, 70, 50, 255))
    return trio(c, "cat-sit", "dog-smile", girl_h=470, cat_h=230, dog_h=240)


cards = {
    "zekkei": scene_card("castle", 0, "cat-sit", "dog-sit", 170, 165),
    "sapa-michi": scene_card("market", 70, "cat-beg", "dog-beg", 230, 235),
    "drive": scene_card("scooter", 140, "cat-wave", "dog-jump", 170, 190),
    "onsen": onsen_card(),
    "fudosan": fudosan_card(),
}
sheet = Image.new("RGB", (len(cards) * (W // 2 + 10) + 10, H // 2 + 20), (243, 239, 230))
for i, (name, im) in enumerate(cards.items()):
    im.convert("RGB").save(OUT / f"card-{name}.webp", "WEBP", quality=84, method=6)
    sheet.paste(im.convert("RGB").resize((W // 2, H // 2), Image.LANCZOS), (10 + i * (W // 2 + 10), 10))
sheet.save(CUT / "cards-check.png")
for p in sorted(OUT.glob("card-*.webp")):
    print(p.name, p.stat().st_size)
