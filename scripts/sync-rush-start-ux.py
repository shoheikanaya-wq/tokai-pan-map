from pathlib import Path
import re

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
<h2>⚡ パンラッシュを始める</h2>
<p><b>迷ったら上の赤いボタンだけでOK。</b><br>おすすめ設定で候補店まで自動で進みます。</p>
<div class="rush-start-actions">
<button id="quickStart" class="primary" type="button">🔥 すぐ始める（おすすめ設定）</button>
<button id="customStart" class="dark" type="button">⚙ 自分で設定する</button>
</div>
<div class="rush-start-note">おすすめ設定：西三河／クロスカブ／現在時刻付近／1店10分／営業中優先</div>
</section>'''

EASY_STYLE = '''<style id="rush-easy-guide-style">
.easy-guide{margin:8px 0 10px;padding:9px 10px;border-radius:10px;background:#1d1712;border:1px solid #60452f;font-size:10px;line-height:1.55;color:#dcc7b2}
.easy-guide b{color:#ffca75}
.next-guide{margin:8px 0 10px;padding:10px;border-radius:10px;background:#2a2019;border:2px solid #b56b2f;font-size:11px;line-height:1.55;text-align:center}
.next-guide b{display:block;color:#ffca75;font-size:14px;margin-bottom:3px}
#settingsPanel>strong,#pick>strong{display:block;font-size:15px;margin-bottom:3px}
#plan{min-height:54px;font-size:15px}
@media(max-width:560px){.easy-guide{font-size:9px;padding:8px}.next-guide{font-size:10px}.next-guide b{font-size:13px}}
</style>'''

if 'rush-start-ux-style' not in s:
    s = s.replace('</head>', STYLE + '\n</head>', 1)
if 'rush-easy-guide-style' not in s:
    s = s.replace('</head>', EASY_STYLE + '\n</head>', 1)
else:
    s = re.sub(r'<style id="rush-easy-guide-style">.*?</style>', EASY_STYLE, s, count=1, flags=re.S)

hero_end = '<div class="copy">ベテラン勢が完走できるかどうかを競う、東海パンMAP最高難度モード。</div></section>'
if 'id="rushStart"' not in s:
    if hero_end not in s:
        raise SystemExit('hero marker not found')
    s = s.replace(hero_end, hero_end + START, 1)
else:
    s = re.sub(r'<section class="rush-start" id="rushStart">.*?</section>', START, s, count=1, flags=re.S)

if 'id="settingsPanel"' not in s:
    s = s.replace('<section class="panel"><div class="grid">', '<section class="panel" id="settingsPanel"><strong>自分で設定する</strong><div class="grid" style="margin-top:8px">', 1)

s = s.replace('<section class="panel" id="settingsPanel"><strong>STEP 1｜条件を決める</strong>', '<section class="panel" id="settingsPanel"><strong>自分で設定する</strong>', 1)
if 'class="easy-guide"' not in s:
    marker = '<section class="panel" id="settingsPanel"><strong>自分で設定する</strong>'
    guide = '<div class="easy-guide"><b>4つだけ決めればOK</b><br>①走る範囲 → ②移動手段 → ③出発時刻 → ④1店舗の滞在時間。迷う項目は初期値のままで大丈夫です。</div>'
    s = s.replace(marker, marker + guide, 1)

s = s.replace('<label>チャレンジ<select id="challenge">', '<label>① 走る範囲<select id="challenge">', 1)
s = s.replace('西三河耐久｜目標25店', '西三河（おすすめ）｜目標25店', 1)
s = s.replace('三河縦断｜目標35店', '三河全体｜目標35店', 1)
s = s.replace('愛知横断｜目標50店', '愛知県全体｜目標50店', 1)
s = s.replace('<label>移動手段<select id="vehicle">', '<label>② 移動手段<select id="vehicle">', 1)
s = s.replace('<label>スタート時刻<div class="timepick">', '<label>③ 出発時刻<div class="timepick">', 1)
s = s.replace('<label>1店舗滞在<input id="stay"', '<label>④ 1店舗の滞在時間<input id="stay"', 1)
s = s.replace('>この条件で店を選ぶ</button>', '>この条件で候補を見る</button>', 1)
s = s.replace("'この条件で店を選ぶ'", "'この条件で候補を見る'")
s = s.replace('条件を決めたら「この条件で店を選ぶ」を押してください。次に挑戦店舗を選びます。', '4項目を確認したら「この条件で候補を見る」を押してください。', 1)

# Make the candidate screen self-explanatory. Recommended start already checks the target number.
s = s.replace('<section id="pick" class="panel hidden"><strong>挑戦店舗</strong>', '<section id="pick" class="panel hidden"><strong>次はルートを作る</strong><div class="next-guide"><b>おすすめ設定なら、もう選ばなくてOK</b>候補店は目標数まで自動でチェック済みです。迷ったら一覧は触らず、下の赤い「このままルートを作る」を押してください。</div>', 1)
s = s.replace('>目標数を自動選択</button>', '>おすすめ数に戻す</button>', 1)
s = s.replace('🔥 24時間パンラッシュ計画を作る', '➡ このままルートを作る', 1)

# Repair the known syntax regression defensively.
broken = "return{wait:0,openAt:arrival,closeAt:null,state:'closed'}function arrivalRisk"
fixed = "return{wait:0,openAt:arrival,closeAt:null,state:'closed'}}function arrivalRisk"
if broken in s:
    s = s.replace(broken, fixed, 1)

new_start = '''function startWithRecommended(){
  $('challenge').value='nishi';
  $('vehicle').value='bike';
  $('stay').value='10';
  if($('openFirst'))$('openFirst').checked=true;
  savePrefs();
  $('status').innerHTML='<span class="good">おすすめ設定で候補を探しています…</span>';
  $('load')?.click();
}'''
s = re.sub(r"function startWithRecommended\(\)\{.*?\n\}", new_start, s, count=1, flags=re.S)

if 'function startWithRecommended()' not in s:
    marker = 'initTimeSelects();loadPrefs();'
    if marker not in s:
        raise SystemExit('init marker not found')
    js = new_start + '''\nif($('quickStart'))$('quickStart').addEventListener('click',startWithRecommended);\nif($('customStart'))$('customStart').addEventListener('click',()=>$('settingsPanel')?.scrollIntoView({behavior:'smooth',block:'start'}));\n'''
    s = s.replace(marker, js + marker, 1)

needle = "$('status').innerHTML='<span class=\"good\">取得完了。</span> '+cfg.name+' 候補 '+shops.length+'店';setLoadState(false);"
replacement = "$('status').innerHTML='<span class=\"good\">取得完了。</span> '+cfg.name+' 候補 '+shops.length+'店';setLoadState(false);setTimeout(()=>$('pick')?.scrollIntoView({behavior:'smooth',block:'start'}),120);"
if needle in s:
    s = s.replace(needle, replacement, 1)

p.write_text(s, encoding='utf-8')

sw = Path('sw.js')
sw_text = sw.read_text(encoding='utf-8')
m = re.search(r"tokai-pan-v(\d+)", sw_text)
if not m:
    raise SystemExit('cache version not found')
next_v = int(m.group(1)) + 1
sw_text = sw_text.replace(m.group(0), f'tokai-pan-v{next_v}', 1)
sw.write_text(sw_text, encoding='utf-8')

idx = Path('index.html')
idx_text = idx.read_text(encoding='utf-8')
idx_text = re.sub(r'panrush\.html\?v=[^"\']+', 'panrush.html?v=20260908-guide', idx_text, count=1)
idx_text = idx_text.replace('⚡ パンラッシュは「おまかせで始める」または条件指定から直感的に開始できます。', '⚡ パンラッシュは「すぐ始める」で候補店を自動選択し、そのままルート作成へ進めます。')
idx_text = idx_text.replace('⚡ パンラッシュは「すぐ始める」ならおすすめ設定で候補店まで自動で進みます。自分で設定する場合も4項目だけです。', '⚡ パンラッシュは「すぐ始める」で候補店を自動選択し、そのままルート作成へ進めます。')
idx.write_text(idx_text, encoding='utf-8')
