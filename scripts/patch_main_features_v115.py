from pathlib import Path
import re

p=Path('index.html')
s=p.read_text(encoding='utf-8')

old="""function buildFactCatch(shop){
  // TOP10中央は店舗固有特色専用。定型の営業時間・評価文は出さない。
  const labels=Array.isArray(shop.featureLabels)?shop.featureLabels:[];
  if(shop.featureLoadError && !labels.length) return {catchphrase:'特色を再確認中…',highlights:[]};
  if(shop.featuresLoaded && !labels.length) return {catchphrase:'店舗固有情報を準備中',highlights:[]};
  if(!labels.length) return {catchphrase:'特色を確認中…',highlights:[]};
  return {
    catchphrase: labels[0],
"""
new="""function normalizeFeatureLabel(v){
  return String(v||'').replace(/\s+/g,' ').trim();
}
function buildFactCatch(shop,usedLabels){
  // TOP10中央は店舗固有特色専用。定型の営業時間・評価文は出さない。
  const labels=(Array.isArray(shop.featureLabels)?shop.featureLabels:[])
    .map(normalizeFeatureLabel).filter(Boolean);
  if(shop.featureLoadError && !labels.length) return {catchphrase:'特色を再確認中…',highlights:[]};
  if(shop.featuresLoaded && !labels.length) return {catchphrase:'店舗固有情報を準備中',highlights:[]};
  if(!labels.length) return {catchphrase:'特色を確認中…',highlights:[]};
  const used=usedLabels||new Set();
  const chosen=labels.find(v=>!used.has(v))||labels[0];
  used.add(chosen);
  return {
    catchphrase: chosen,
"""
if old not in s:
    raise SystemExit('buildFactCatch anchor not found')
s=s.replace(old,new,1)

# create used set once per ranking render
marker="list.innerHTML='';"
if marker in s and "const usedFeatureLabels=new Set();" not in s:
    s=s.replace(marker,marker+"\n  const usedFeatureLabels=new Set();",1)

s=s.replace('const factCopy=buildFactCatch(s);','const factCopy=buildFactCatch(s,usedFeatureLabels);')

s=s.replace('Ver.1.14','Ver.1.15')
notice='Ver.1.15：TOP10の店舗固有「特色・推し」を改善。同じTOP10内で同一の特色文が重なった場合は、その店舗の2番目・3番目の固有ラベルへ自動でずらし、似た文面が並びにくくしました。通信再試行、スマホ戻る操作、店舗詳細、ランキング信頼度補正にも対応。岐阜県・三重県は今後対応予定です。'
s=re.sub(r'Ver\.1\.15：[^<]{20,900}',notice,s,count=1)
p.write_text(s,encoding='utf-8')

sw=Path('sw.js')
u=sw.read_text(encoding='utf-8')
u=re.sub(r"const CACHE_NAME = 'tokai-pan-v\d+';","const CACHE_NAME = 'tokai-pan-v14';",u,count=1)
sw.write_text(u,encoding='utf-8')
