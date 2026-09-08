from pathlib import Path

p = Path('panrush.html')
s = p.read_text(encoding='utf-8')

STYLE = '''<style id="rush-start-ux-style">
.rush-start{background:#2a2019;border:2px solid #b56b2f;border-radius:15px;padding:12px;margin:10px 0;box-shadow:0 4px 18px #0005;text-align:center}
.rush-start h2{margin:0 0 5px;font-size:19px}
.rush-start p{margin:0 0 10px;font-size:11px;line-height:1.5;color:#d7c4b2}
.rush-start-actions{display:grid;grid-template-columns:1.25fr 1fr;gap:8px}
.rush-start-actions button{min-height:52px}
.rush-start-note{margin-top:7px;font-size:9px;color:#bda891}
#settingsPanel{scroll-margin-top:70px}
@media(max-width:560px){.rush-start{padding:10px}.rush-start h2{font-size:17px}.rush-start-actions{grid-template-columns:1fr}.rush-start-actions button{min-height:48px}}
</style>'''

START = '''<section class="rush-start" id="rushStart">
<h2>⚡ ここからパンラッシュ開始</h2>
<p>迷ったら「おまかせで始める」。自分で条件を決めたいときは右（スマホでは下）を選んでください。</p>
<div class="rush-start-actions">
<button id="quickStart" class="primary" type="button">🔥 おまかせで始める</button>
<button id="customStart" class="dark" type="button">⚙ 条件を決めて始める</button>
</div>
<div class="rush-start-note">おまかせ：西三河耐久／クロスカブ／現在時刻付近／滞在10分／営業中優先</div>
</section>'''

if 'rush-start-ux-style' not in s:
    s = s.replace('</head>', STYLE + '\n</head>', 1)

hero_end = '<div class="copy">ベテラン勢が完走できるかどうかを競う、東海パンMAP最高難度モード。</div></section>'
if 'id="rushStart"' not in s:
    if hero_end not in s:
        raise SystemExit('hero marker not found')
    s = s.replace(hero_end, hero_end + START, 1)

if 'id="settingsPanel"' not in s:
    s = s.replace('<section class="panel"><div class="grid">', '<section class="panel" id="settingsPanel"><strong>STEP 1｜条件を決める</strong><div class="grid" style="margin-top:8px">', 1)

s = s.replace('>候補店を一括取得</button>', '>この条件で店を選ぶ</button>', 1)
s = s.replace("'候補店を一括取得'", "'この条件で店を選ぶ'")
s = s.replace('候補を取得すると、複数市町村から耐久用の店舗プールを作成します。', '条件を決めたら「この条件で店を選ぶ」を押してください。次に挑戦店舗を選びます。', 1)

# Repair a syntax regression in visitWindow(): the function-closing brace was missing,
# which prevented every Pan Rush button handler from being registered.
broken = "return{wait:0,openAt:arrival,closeAt:null,state:'closed'}function arrivalRisk"
fixed = "return{wait:0,openAt:arrival,closeAt:null,state:'closed'}}function arrivalRisk"
if broken in s:
    s = s.replace(broken, fixed, 1)

JS = '''
function startWithRecommended(){
  $('challenge').value='nishi';
  $('vehicle').value='bike';
  $('stay').value='10';
  if($('openFirst'))$('openFirst').checked=true;
  savePrefs();
  $('settingsPanel')?.scrollIntoView({behavior:'smooth',block:'start'});
  setTimeout(()=>$('load')?.click(),220);
}
if($('quickStart'))$('quickStart').addEventListener('click',startWithRecommended);
if($('customStart'))$('customStart').addEventListener('click',()=>$('settingsPanel')?.scrollIntoView({behavior:'smooth',block:'start'}));
'''
if 'function startWithRecommended()' not in s:
    marker = 'initTimeSelects();loadPrefs();'
    if marker not in s:
        raise SystemExit('init marker not found')
    s = s.replace(marker, JS + marker, 1)

p.write_text(s, encoding='utf-8')

# Sync Service Worker cache because panrush.html meaningfully changed.
sw = Path('sw.js')
sw_text = sw.read_text(encoding='utf-8')
import re
m = re.search(r"tokai-pan-v(\d+)", sw_text)
if not m:
    raise SystemExit('cache version not found')
next_v = int(m.group(1)) + 1
sw_text = sw_text.replace(m.group(0), f'tokai-pan-v{next_v}', 1)
sw.write_text(sw_text, encoding='utf-8')

# Keep home annotation/link cache-buster aligned without changing main-map behavior.
idx = Path('index.html')
idx_text = idx.read_text(encoding='utf-8')
idx_text = re.sub(r'panrush\.html\?v=[^"\']+', 'panrush.html?v=20260908-start', idx_text, count=1)
if 'パンラッシュは「おまかせで始める」' not in idx_text:
    marker = '<div class="rush-entry-grid" id="rushEntryGrid">'
    note = '<div class="notice">⚡ パンラッシュは「おまかせで始める」または条件指定から直感的に開始できます。</div>'
    pos = idx_text.find(marker)
    if pos >= 0:
        idx_text = idx_text[:pos] + note + idx_text[pos:]
idx.write_text(idx_text, encoding='utf-8')
