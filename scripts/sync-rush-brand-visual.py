from pathlib import Path

STYLE = '''<style id="tokai-pan-brand-visual-style">
.brand-visual{display:block;width:100%;max-width:820px;max-height:190px;object-fit:cover;object-position:center 42%;margin:0 auto 10px;border-radius:0 0 15px 15px}
@media(max-width:600px){.brand-visual{max-height:128px;margin-bottom:7px;border-radius:0 0 12px 12px}}
</style>'''
IMAGE = '<img src="tokai-pan-home.png" class="brand-visual" alt="東海パンMAPの女子高生と猫と犬">'

for filename in ('panrush.html', 'autumn-rush.html'):
    path = Path(filename)
    text = path.read_text(encoding='utf-8')
    if 'tokai-pan-brand-visual-style' not in text:
        text = text.replace('</head>', STYLE + '\n</head>', 1)
    if 'class="brand-visual"' not in text:
        marker = '<main>'
        if marker not in text:
            raise SystemExit(f'{filename}: <main> not found')
        text = text.replace(marker, marker + '\n' + IMAGE, 1)
    path.write_text(text, encoding='utf-8')
