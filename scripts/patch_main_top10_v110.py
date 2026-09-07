from pathlib import Path
import re

p=Path('index.html')
s=p.read_text(encoding='utf-8')

helper="""function rankingScore(rating,reviews){
  const r=Number(rating)||0;
  const v=Math.max(0,Number(reviews)||0);
  const prior=4.2;
  const priorWeight=40;
  const adjusted=(v/(v+priorWeight))*r+(priorWeight/(v+priorWeight))*prior;
  const volume=Math.min(22,Math.log10(v+1)*8);
  return adjusted*20+volume;
}
"""
anchor="function normalizeShop"
if helper not in s:
    pos=s.index(anchor)
    s=s[:pos]+helper+s[pos:]

pattern=r"score:\s*\(\(p\.rating \|\| 0\) \* 20\) \+\s*Math\.min\(\s*30,\s*Math\.log10\(\(p\.userRatingCount \|\| 0\) \+ 1\) \* 12\s*\)"
s,n=re.subn(pattern,"score: rankingScore(p.rating,p.userRatingCount)",s)
if n<1:
    raise SystemExit('ranking score formula not found')

s=s.replace('Ver.1.9','Ver.1.10')
notice='Ver.1.10：TOP10ランキング精度を改善。評価点だけでなく口コミ件数による信頼度補正を入れ、口コミが少ない極端な高評価を過大評価しにくくしました。店舗固有特色の再取得安定化、店舗写真・営業時間・口コミ・地図・公式サイトにも対応。岐阜県・三重県は今後対応予定です。'
s=re.sub(r'Ver\.1\.10：[^<]{20,900}',notice,s,count=1)
p.write_text(s,encoding='utf-8')

sw=Path('sw.js')
u=sw.read_text(encoding='utf-8')
u=re.sub(r"const CACHE_NAME = 'tokai-pan-v\d+';","const CACHE_NAME = 'tokai-pan-v9';",u,count=1)
sw.write_text(u,encoding='utf-8')
