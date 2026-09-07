from pathlib import Path
import re

p=Path('index.html')
s=p.read_text(encoding='utf-8')

# 1) Fix broken detail helper introduced by navigation patch.
s=s.replace("""function showDetailView(){
  home.classList.add('hidden');
  showDetailView();
  syncViewHistory('detail',{city:currentCity,index:i});
}""", """function showDetailView(){
  home.classList.add('hidden');
  ranking.classList.add('hidden');
  detail.classList.remove('hidden');
}""", 1)

s=s.replace("""  ranking.classList.add('hidden');
  detail.classList.remove('hidden');

const areaName = getAreaName(currentCity);

drank.textContent =
  `愛知県 ＞ ${areaName ? areaName + ' ＞ ' : ''}${currentCity} ＞ ${i + 1}位 / Score ${Math.round(s.score)}`;""", """  showDetailView();
  syncViewHistory('detail',{city:currentCity,index:i});

const areaName = getAreaName(currentCity);

drank.textContent =
  `${currentPrefecture} ＞ ${areaName ? areaName + ' ＞ ' : ''}${currentCity} ＞ ${i + 1}位 / Score ${Math.round(s.score)}`;""", 1)

# 2) Prefecture tabs and panel split.
s=s.replace('<div class="tabs"><button class="active">愛知県</button><button disabled>岐阜県</button><button disabled>三重県</button></div>', '<div class="tabs"><button id="tabAichi" class="active">愛知県</button><button id="tabGifu">岐阜県</button><button disabled>三重県</button></div>', 1)

s=s.replace('</div><h2>西三河</h2>', '</div><div id="aichiPanel"><h2>西三河</h2>', 1)
needle='''<div style="margin-top:18px">\n  <button id="nishimikawa">🏆 西三河 TOP10</button>\n  <button id="higashimikawa">🏆 東三河 TOP10</button>\n  <button id="aichi">🏆 愛知県 TOP10</button>\n</div>\n</section>'''
replacement='''<div style="margin-top:18px">\n  <button id="nishimikawa">🏆 西三河 TOP10</button>\n  <button id="higashimikawa">🏆 東三河 TOP10</button>\n  <button id="aichi">🏆 愛知県 TOP10</button>\n</div>\n</div>\n<div id="gifuPanel" class="hidden">\n  <h2>岐阜・西濃</h2><div class="cities">\n    <button id="gifuCity">岐阜市</button><button id="ogaki">大垣市</button><button id="kakamigahara">各務原市</button>\n  </div>\n  <h2>東濃・中濃</h2><div class="cities">\n    <button id="tajimi">多治見市</button><button id="kani">可児市</button><button id="seki">関市</button>\n  </div>\n  <div class="notice">岐阜県は主要6市から順次拡大中です。市別TOP10は愛知県と同じランキング・店舗詳細方式で表示します。</div>\n</div>\n</section>'''
if needle not in s:
    raise SystemExit('Aichi panel close anchor not found')
s=s.replace(needle,replacement,1)

# 3) Prefecture-aware API query/filter for municipality lists.
s=s.replace("let currentVisualKey = '';", "let currentVisualKey = '';\nlet currentPrefecture = '愛知県';", 1)
s=s.replace("textQuery: `パン屋 愛知県${city}`,", "textQuery: `パン屋 ${currentPrefecture}${city}`,", 1)
s=s.replace("shops = shops.filter(s => municipalityMatches(s.address,city));", "shops = shops.filter(s => String(s.address||'').includes(currentPrefecture) && municipalityMatches(s.address,city));", 1)

# 4) Add Gifu controls to DOM bindings.
anchor="const nishimikawa=byId('nishimikawa'), higashimikawa=byId('higashimikawa'), aichi=byId('aichi');"
insert=anchor+"\nconst tabAichi=byId('tabAichi'), tabGifu=byId('tabGifu'), aichiPanel=byId('aichiPanel'), gifuPanel=byId('gifuPanel');\nconst gifuCity=byId('gifuCity'), ogaki=byId('ogaki'), kakamigahara=byId('kakamigahara'), tajimi=byId('tajimi'), kani=byId('kani'), seki=byId('seki');"
s=s.replace(anchor,insert,1)

# 5) Add tab switching and Gifu city handlers before existing city handlers.
handlers="""function selectPrefecture(pref){
  currentPrefecture=pref;
  const isAichi=pref==='愛知県';
  aichiPanel.classList.toggle('hidden',!isAichi);
  gifuPanel.classList.toggle('hidden',isAichi);
  tabAichi.classList.toggle('active',isAichi);
  tabGifu.classList.toggle('active',!isAichi);
}
tabAichi.onclick=()=>selectPrefecture('愛知県');
tabGifu.onclick=()=>selectPrefecture('岐阜県');

gifuCity.onclick=()=>selectCity(gifuCity,'岐阜市');
ogaki.onclick=()=>selectCity(ogaki,'大垣市');
kakamigahara.onclick=()=>selectCity(kakamigahara,'各務原市');
tajimi.onclick=()=>selectCity(tajimi,'多治見市');
kani.onclick=()=>selectCity(kani,'可児市');
seki.onclick=()=>selectCity(seki,'関市');

"""
city_anchor="toyota.onclick = () => selectCity(toyota, '豊田市');"
s=s.replace(city_anchor,handlers+city_anchor,1)

# Ensure Aichi city clicks restore Aichi prefecture when needed.
s=s.replace("  async function selectCity(button, city) {\ncurrentCity = city;", "  async function selectCity(button, city) {\ncurrentCity = city;", 1)

# Version / notice / cache.
s=s.replace('Ver.1.15','Ver.1.16')
notice='Ver.1.16：岐阜県対応を開始。岐阜市・大垣市・各務原市・多治見市・可児市・関市の市別パン屋TOP10を追加し、愛知県と同じ店舗写真・特色・営業時間・口コミ・地図・公式サイトの詳細表示に対応しました。あわせて店舗詳細画面の遷移不具合を修正。岐阜県は今後さらに市町村を拡大し、三重県も順次対応予定です。'
s=re.sub(r'Ver\.1\.16：[^<]{20,900}',notice,s,count=1)
p.write_text(s,encoding='utf-8')

sw=Path('sw.js')
u=sw.read_text(encoding='utf-8')
u=re.sub(r"const CACHE_NAME = 'tokai-pan-v\d+';","const CACHE_NAME = 'tokai-pan-v15';",u,count=1)
sw.write_text(u,encoding='utf-8')
