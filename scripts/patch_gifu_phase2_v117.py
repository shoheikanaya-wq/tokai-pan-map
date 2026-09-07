from pathlib import Path
import re

p=Path('index.html')
s=p.read_text(encoding='utf-8')

# Expand Gifu city groups and add prefecture TOP10 button.
s=s.replace(
'''  <h2>岐阜・西濃</h2><div class="cities">
    <button id="gifuCity">岐阜市</button><button id="ogaki">大垣市</button><button id="kakamigahara">各務原市</button>
  </div>
  <h2>東濃・中濃</h2><div class="cities">
    <button id="tajimi">多治見市</button><button id="kani">可児市</button><button id="seki">関市</button>
  </div>
  <div class="notice">岐阜県は主要6市から順次拡大中です。市別TOP10は愛知県と同じランキング・店舗詳細方式で表示します。</div>''',
'''  <h2>岐阜・西濃</h2><div class="cities">
    <button id="gifuCity">岐阜市</button><button id="ogaki">大垣市</button><button id="kakamigahara">各務原市</button><button id="hashima">羽島市</button><button id="mizuho">瑞穂市</button>
  </div>
  <h2>東濃・中濃</h2><div class="cities">
    <button id="tajimi">多治見市</button><button id="kani">可児市</button><button id="seki">関市</button><button id="minokamo">美濃加茂市</button><button id="toki">土岐市</button><button id="ena">恵那市</button><button id="nakatsugawa">中津川市</button>
  </div>
  <div style="margin-top:18px"><button id="gifuTop10">🏆 岐阜県 TOP10</button></div>
  <div class="notice">岐阜県は主要12市へ拡大中です。市別TOP10と岐阜県TOP10を、愛知県と同じランキング・店舗詳細方式で表示します。</div>''',1)

s=s.replace(
"const gifuCity=byId('gifuCity'), ogaki=byId('ogaki'), kakamigahara=byId('kakamigahara'), tajimi=byId('tajimi'), kani=byId('kani'), seki=byId('seki');",
"const gifuCity=byId('gifuCity'), ogaki=byId('ogaki'), kakamigahara=byId('kakamigahara'), hashima=byId('hashima'), mizuho=byId('mizuho'), tajimi=byId('tajimi'), kani=byId('kani'), seki=byId('seki'), minokamo=byId('minokamo'), toki=byId('toki'), ena=byId('ena'), nakatsugawa=byId('nakatsugawa'), gifuTop10=byId('gifuTop10');",1)

s=s.replace(
"seki.onclick=()=>selectCity(seki,'関市');",
"seki.onclick=()=>selectCity(seki,'関市');\nhashima.onclick=()=>selectCity(hashima,'羽島市');\nmizuho.onclick=()=>selectCity(mizuho,'瑞穂市');\nminokamo.onclick=()=>selectCity(minokamo,'美濃加茂市');\ntoki.onclick=()=>selectCity(toki,'土岐市');\nena.onclick=()=>selectCity(ena,'恵那市');\nnakatsugawa.onclick=()=>selectCity(nakatsugawa,'中津川市');",1)

# Add Gifu prefecture-wide ranking before Aichi ranking handler.
anchor="  aichi.onclick = async () => {"
handler="""  gifuTop10.onclick = async () => {
  currentPrefecture='岐阜県';
  currentVisualKey='岐阜県';
  const cachedTop10=getTop10Cache('岐阜県',AICHI_TOP10_TTL);
  if(cachedTop10){
    shops=cachedTop10.shops;
    currentCity='岐阜県';
    rankingTitle.textContent='岐阜県 パン屋 TOP10';
    showRanking();
    return;
  }
  const cities=['岐阜市','大垣市','各務原市','羽島市','瑞穂市','多治見市','可児市','関市','美濃加茂市','土岐市','恵那市','中津川市'];
  gifuTop10.disabled=true; gifuTop10.textContent='取得中...';
  try{
    const local=buildTop10FromMunicipalityCache(cities);
    const wide=await fetchWideBakeryCandidates('パン屋 岐阜県');
    shops=mergeAndRankShops(wide,local.shops)
      .filter(s=>String(s.address||'').includes('岐阜県'))
      .slice(0,10);
    setTop10Cache('岐阜県',shops);
    currentCity='岐阜県';
    rankingTitle.textContent='岐阜県 パン屋 TOP10';
    showRanking();
  }catch(e){
    showLoadError('岐阜県ランキングを取得できませんでした。',()=>gifuTop10.click());
  }finally{
    gifuTop10.disabled=false; gifuTop10.textContent='🏆 岐阜県 TOP10';
  }
};

"""
if anchor not in s:
    raise SystemExit('Aichi TOP10 handler anchor not found')
s=s.replace(anchor,handler+anchor,1)

# Keep Aichi handlers explicitly in Aichi context.
s=s.replace("  aichi.onclick = async () => {\n  currentVisualKey = '愛知県';", "  aichi.onclick = async () => {\n  currentPrefecture='愛知県';\n  currentVisualKey = '愛知県';",1)
s=s.replace("  nishimikawa.onclick = async () => {\n  currentVisualKey = '西三河';", "  nishimikawa.onclick = async () => {\n  currentPrefecture='愛知県';\n  currentVisualKey = '西三河';",1)
s=s.replace("  higashimikawa.onclick = async () => {\n  currentVisualKey = '東三河';", "  higashimikawa.onclick = async () => {\n  currentPrefecture='愛知県';\n  currentVisualKey = '東三河';",1)

# Fix home annotation explicitly; previous regex could not cross the version div markup.
s=s.replace(
'''<div>Ver.1.16</div>：パンラッシュ／秋のパンラッシュを追加。愛知県の市町村別パン屋TOP10に対応。店舗写真・店舗ごとの特色・営業時間・口コミ・地図・公式サイトなどを確認できます。岐阜県・三重県は今後対応予定です。''',
'''<div>Ver.1.17</div>：岐阜県対応を拡大。主要12市の市別パン屋TOP10と岐阜県TOP10に対応しました。愛知県と同じく店舗写真・店舗固有の特色・営業時間・口コミ・地図・公式サイトなどを確認できます。愛知の軽微改善とパンラッシュ保守は自動継続し、三重県は今後対応予定です。''',1)
s=s.replace('<div>Ver.1.16</div>\n  <div>Personal Bakery Discovery Project</div>','<div>Ver.1.17</div>\n  <div>Personal Bakery Discovery Project</div>',1)

p.write_text(s,encoding='utf-8')

sw=Path('sw.js')
u=sw.read_text(encoding='utf-8')
u=re.sub(r"const CACHE_NAME = 'tokai-pan-v\d+';","const CACHE_NAME = 'tokai-pan-v16';",u,count=1)
sw.write_text(u,encoding='utf-8')
