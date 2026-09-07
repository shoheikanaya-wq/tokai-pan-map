from pathlib import Path
import re

p=Path('index.html')
s=p.read_text(encoding='utf-8')

helper="""function municipalityMatches(address,city){
  const a=String(address||'').replace(/\s+/g,'');
  const c=String(city||'').replace(/\s+/g,'');
  if(!a||!c) return false;
  return a.includes(c);
}
function isBakeryCandidate(shop){
  if(!shop?.types?.includes('bakery')) return false;
  const name=String(shop.name||'');
  if(/洋菓子|ケーキ|スイーツ|パティスリー|菓子店/.test(name)) return false;
  if(/コンビニ|ローソン|ファミリーマート|セブン-?イレブン|ミニストップ|ドラッグ|薬局|スーパーマーケット|スーパーセンター/.test(name)) return false;
  return true;
}
"""
anchor='function normalizeShopText'
if helper not in s:
    pos=s.index(anchor)
    s=s[:pos]+helper+s[pos:]

s=s.replace(".filter(s => !/洋菓子|ケーキ|スイーツ|パティスリー|菓子店/.test(s.name))\n  .filter(s => s.types.includes('bakery'))", ".filter(isBakeryCandidate)")
s=s.replace("shops = shops.filter(s => !/洋菓子|ケーキ|スイーツ|パティスリー|菓子店/.test(s.name));\n  shops = shops.filter(s => s.types.includes('bakery'));", "shops = shops.filter(isBakeryCandidate);")
s=s.replace("shops = shops.filter(s => s.address.includes(city));", "shops = shops.filter(s => municipalityMatches(s.address,city));")

s=s.replace('Ver.1.10','Ver.1.11')
notice='Ver.1.11：市町村TOP10の候補精度を改善。住所の市町村一致チェックを明確化し、bakery分類を維持しながらコンビニ・ドラッグストア・スーパー等の明らかな非パン屋候補を除外します。ランキングは口コミ件数による信頼度補正、店舗固有特色の再取得安定化にも対応。岐阜県・三重県は今後対応予定です。'
s=re.sub(r'Ver\.1\.11：[^<]{20,900}',notice,s,count=1)
p.write_text(s,encoding='utf-8')

sw=Path('sw.js')
u=sw.read_text(encoding='utf-8')
u=re.sub(r"const CACHE_NAME = 'tokai-pan-v\d+';","const CACHE_NAME = 'tokai-pan-v10';",u,count=1)
sw.write_text(u,encoding='utf-8')
