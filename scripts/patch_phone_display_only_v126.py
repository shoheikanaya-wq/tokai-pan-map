from pathlib import Path
import re

p=Path('index.html')
s=p.read_text(encoding='utf-8')
old="""  // 電話番号：スマホではワンタップ発信
  if(s.phone){
    const tel=String(s.phone).replace(/[^0-9+]/g,'');
    dphone.innerHTML=`<a class=\"detail-phone-link\" href=\"tel:${tel}\">☎ ${s.phone} に電話</a>`;
  }else{
    dphone.textContent='電話番号：情報なし';
  }
"""
new="""  // 電話番号：表示のみ。誤発信防止のため tel: リンクや発信ボタンは付けない。
  if(s.phone){
    dphone.textContent=`電話番号：${s.phone}`;
  }else{
    dphone.textContent='電話番号：情報なし';
  }
"""
if old not in s:
    raise SystemExit('phone call anchor not found')
s=s.replace(old,new,1)
s=s.replace('<div>Ver.1.25</div>：スマホで岐阜県TOP10・三重県TOP10などランキング画面の「戻る」が反応しない問題を修正しました。ランキング表示時に履歴状態を保持し、戻る操作でホームへ復帰できるようにしています。パンラッシュは愛知県内限定です。','<div>Ver.1.26</div>：店舗詳細の電話番号は表示専用に変更しました。誤発信を防ぐため、電話番号タップによる発信や「電話する」リンクは使用しません。TOP10の戻る修正と、愛知県内限定パンラッシュ仕様も継続します。',1)
s=s.replace('<div>Ver.1.25</div>\n  <div>Personal Bakery Discovery Project</div>','<div>Ver.1.26</div>\n  <div>Personal Bakery Discovery Project</div>',1)
p.write_text(s,encoding='utf-8')

sw=Path('sw.js')
u=sw.read_text(encoding='utf-8')
u=re.sub(r"const CACHE_NAME = 'tokai-pan-v\d+';","const CACHE_NAME = 'tokai-pan-v25';",u,count=1)
sw.write_text(u,encoding='utf-8')
