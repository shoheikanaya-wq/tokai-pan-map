"""SA・PA と絶景のカード候補を作り、見くらべ用の1枚にまとめる。"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont

SRC, CUT, OUT = (Path(a) for a in sys.argv[1:4])
OUT.mkdir(parents=True, exist_ok=True)
W, H = 600, 660

CANDS = [
    # 名前, 元の絵, 切りとる場所, 上からのずらし, 猫, 犬, 猫の高さ, 犬の高さ
    ("sapa-A 券売機", "7.jpg", (622, 520, 918, 950), 40, "cat-beg", "dog-beg", 200, 210),
    ("sapa-B ピクニック", "7.jpg", (5, 1010, 302, 1440), 30, "cat-sit", "dog-smile", 190, 200),
    ("zekkei-A 山と富士山", "2.jpg", (623, 497, 912, 890), 0, "cat-sit", "dog-sit", 170, 180),
    ("zekkei-B 草原と空", "2.jpg", (623, 10, 912, 397), 0, "cat-loaf", "dog-loaf", 150, 165),
    ("zekkei-C 雪の日", "4.jpg", (318, 1445, 605, 1838), 0, "cat-sit", "dog-jump", 170, 180),
]


def load(name):
    return Image.open(CUT / f"{name}.png").convert("RGBA")


def fit_h(im, h):
    return im.resize((round(im.width * h / im.height), h), Image.LANCZOS)


def shadow_paste(canvas, im, xy):
    x, y = xy
    sh = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    blk = Image.new("RGBA", im.size, (60, 40, 20, 0))
    blk.putalpha(im.split()[3].point(lambda v: int(v * 0.35)))
    sh.paste(blk, (x + 4, y + 6), blk)
    canvas.alpha_composite(sh.filter(ImageFilter.GaussianBlur(5)))
    canvas.alpha_composite(im, (x, y))


font = ImageFont.truetype("C:/Windows/Fonts/meiryob.ttc", 26)
TW, TH = 300, 330
sheet = Image.new("RGB", (len(CANDS) * (TW + 14) + 14, TH + 70), (243, 239, 230))
d = ImageDraw.Draw(sheet)
for i, (name, f, box, top, cat, dog, ch, dh) in enumerate(CANDS):
    src = Image.open(SRC / f).convert("RGB").crop(box)
    big = src.resize((W, round(src.height * W / src.width)), Image.LANCZOS)
    top = max(0, min(top, big.height - H))
    c = big.crop((0, top, W, top + H)).convert("RGBA")
    ci, di = fit_h(load(cat), ch), fit_h(load(dog), dh)
    shadow_paste(c, ci, (6, H - ci.height - 4))
    shadow_paste(c, di, (W - di.width - 6, H - di.height - 4))
    key = name.split()[0]
    c.convert("RGB").save(OUT / f"card-{key}.webp", "WEBP", quality=84, method=6)
    x = 14 + i * (TW + 14)
    sheet.paste(c.convert("RGB").resize((TW, TH), Image.LANCZOS), (x, 14))
    d.text((x + TW // 2, TH + 40), name, font=font, fill=(90, 55, 20), anchor="mm")
sheet.save(OUT / "候補の見くらべ.png")
print("ok")
