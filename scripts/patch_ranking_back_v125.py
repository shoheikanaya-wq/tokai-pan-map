from pathlib import Path
import re

p=Path('index.html')
s=p.read_text(encoding='utf-8')
old="""function showRanking() {
  showAreaVisual(currentVisualKey || currentCity);
  home.classList.add('hidden');
  detail.classList.add('hidden');
  ranking.classList.remove('hidden');
"""
new="""function showRanking() {
  showAreaVisual(currentVisualKey || currentCity);
  home.classList.add('hidden');
  detail.classList.add('hidden');
  ranking.classList.remove('hidden');
  syncViewHistory('ranking',{prefecture:currentPrefecture,city:currentCity,visualKey:currentVisualKey});
"""
if old not in s:
    raise SystemExit('showRanking anchor not found')
s=s.replace(old,new,1)
s=s.replace('<div>Ver.1.24</div>：パンラッシュは愛知県内限定仕様に戻し、西三河耐久・三河縦断・愛知横断の3コースで運用します。通常の東海パンMAP本体は愛知・岐阜・三重の三県対応を継続します。','<div>Ver.1.25</div>：スマホで岐阜県TOP10・三重県TOP10などランキング画面の「戻る」が反応しない問題を修正しました。ランキング表示時に履歴状態を保持し、戻る操作でホームへ復帰できるようにしています。パンラッシュは愛知県内限定です。',1)
s=s.replace('<div>Ver.1.24</div>\n  <div>Personal Bakery Discovery Project</div>','<div>Ver.1.25</div>\n  <div>Personal Bakery Discovery Project</div>',1)
p.write_text(s,encoding='utf-8')

sw=Path('sw.js')
u=sw.read_text(encoding='utf-8')
u=re.sub(r"const CACHE_NAME = 'tokai-pan-v\d+';","const CACHE_NAME = 'tokai-pan-v24';",u,count=1)
sw.write_text(u,encoding='utf-8')
