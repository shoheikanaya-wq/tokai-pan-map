from pathlib import Path
import re
p=Path('index.html')
s=p.read_text(encoding='utf-8')

s=s.replace('<button id="tabAichi" class="active">愛知県</button><button id="tabGifu">岐阜県</button><button disabled>三重県</button>', '<button id="tabAichi" class="active">愛知県</button><button id="tabGifu">岐阜県</button><button id="tabMie">三重県</button>',1)
s=s.replace('</div>\n</section>\n<section id="ranking"', '''</div>
<div id="miePanel" class="hidden">
  <h2>北勢</h2><div class="cities"><button id="yokkaichi">四日市市</button><button id="kuwana">桑名市</button><button id="suzuka">鈴鹿市</button><button id="inabe">いなべ市</button></div>
  <h2>中勢・伊賀</h2><div class="cities"><button id="tsu">津市</button><button id="matsusaka">松阪市</button><button id="iga">伊賀市</button><button id="nabari">名張市</button></div>
  <h2>伊勢志摩・東紀州</h2><div class="cities"><button id="ise">伊勢市</button><button id="toba">鳥羽市</button><button id="shima">志摩市</button><button id="owase">尾鷲市</button><button id="kumano">熊野市</button></div>
  <div style="margin-top:18px"><button id="mieTop10">🏆 三重県 TOP10</button></div>
  <div class="notice">三重県対応を開始。主要13市の市別TOP10と三重県TOP10から順次拡大します。</div>
</div>
</section>
<section id="ranking"''',1)

s=s.replace("const tabAichi=byId('tabAichi'), tabGifu=byId('tabGifu'), aichiPanel=byId('aichiPanel'), gifuPanel=byId('gifuPanel');", "const tabAichi=byId('tabAichi'), tabGifu=byId('tabGifu'), tabMie=byId('tabMie'), aichiPanel=byId('aichiPanel'), gifuPanel=byId('gifuPanel'), miePanel=byId('miePanel');",1)
anchor="const gifuCity=byId('gifuCity')"
pos=s.find(anchor)
if pos<0: raise SystemExit('Gifu binding anchor not found')
line_end=s.find('\n',pos)
s=s[:line_end+1]+"const yokkaichi=byId('yokkaichi'), kuwana=byId('kuwana'), suzuka=byId('suzuka'), inabe=byId('inabe'), tsu=byId('tsu'), matsusaka=byId('matsusaka'), iga=byId('iga'), nabari=byId('nabari'), ise=byId('ise'), toba=byId('toba'), shima=byId('shima'), owase=byId('owase'), kumano=byId('kumano'), mieTop10=byId('mieTop10');\n"+s[line_end+1:]

old="""function selectPrefecture(pref){
  currentPrefecture=pref;
  const isAichi=pref==='愛知県';
  aichiPanel.classList.toggle('hidden',!isAichi);
  gifuPanel.classList.toggle('hidden',isAichi);
  tabAichi.classList.toggle('active',isAichi);
  tabGifu.classList.toggle('active',!isAichi);
}
tabAichi.onclick=()=>selectPrefecture('愛知県');
tabGifu.onclick=()=>selectPrefecture('岐阜県');"""
new="""function selectPrefecture(pref){
  currentPrefecture=pref;
  const isAichi=pref==='愛知県', isGifu=pref==='岐阜県', isMie=pref==='三重県';
  aichiPanel.classList.toggle('hidden',!isAichi);
  gifuPanel.classList.toggle('hidden',!isGifu);
  miePanel.classList.toggle('hidden',!isMie);
  tabAichi.classList.toggle('active',isAichi);
  tabGifu.classList.toggle('active',isGifu);
  tabMie.classList.toggle('active',isMie);
}
tabAichi.onclick=()=>selectPrefecture('愛知県');
tabGifu.onclick=()=>selectPrefecture('岐阜県');
tabMie.onclick=()=>selectPrefecture('三重県');"""
if old not in s: raise SystemExit('pref selector anchor not found')
s=s.replace(old,new,1)

handler_anchor="gifuCity.onclick=()=>selectCity(gifuCity,'岐阜市');"
miehandlers="""yokkaichi.onclick=()=>selectCity(yokkaichi,'四日市市');
kuwana.onclick=()=>selectCity(kuwana,'桑名市');
suzuka.onclick=()=>selectCity(suzuka,'鈴鹿市');
inabe.onclick=()=>selectCity(inabe,'いなべ市');
tsu.onclick=()=>selectCity(tsu,'津市');
matsusaka.onclick=()=>selectCity(matsusaka,'松阪市');
iga.onclick=()=>selectCity(iga,'伊賀市');
nabari.onclick=()=>selectCity(nabari,'名張市');
ise.onclick=()=>selectCity(ise,'伊勢市');
toba.onclick=()=>selectCity(toba,'鳥羽市');
shima.onclick=()=>selectCity(shima,'志摩市');
owase.onclick=()=>selectCity(owase,'尾鷲市');
kumano.onclick=()=>selectCity(kumano,'熊野市');

"""
s=s.replace(handler_anchor,miehandlers+handler_anchor,1)

anchor="  gifuTop10.onclick = async () => {"
mie_top="""  mieTop10.onclick = async () => {
  currentPrefecture='三重県'; currentVisualKey='三重県';
  const cachedTop10=getTop10Cache('三重県',AICHI_TOP10_TTL);
  if(cachedTop10){shops=cachedTop10.shops;currentCity='三重県';rankingTitle.textContent='三重県 パン屋 TOP10';showRanking();return;}
  const cities=['四日市市','桑名市','鈴鹿市','いなべ市','津市','松阪市','伊賀市','名張市','伊勢市','鳥羽市','志摩市','尾鷲市','熊野市'];
  mieTop10.disabled=true; mieTop10.textContent='取得中...';
  try{
    const local=buildTop10FromMunicipalityCache(cities);
    const wide=await fetchWideBakeryCandidates('パン屋 三重県');
    shops=mergeAndRankShops(wide,local.shops).filter(s=>String(s.address||'').includes('三重県')).slice(0,10);
    setTop10Cache('三重県',shops); currentCity='三重県'; rankingTitle.textContent='三重県 パン屋 TOP10'; showRanking();
  }catch(e){showLoadError('三重県ランキングを取得できませんでした。',()=>mieTop10.click());}
  finally{mieTop10.disabled=false;mieTop10.textContent='🏆 三重県 TOP10';}
};

"""
if anchor not in s: raise SystemExit('gifu top anchor not found')
s=s.replace(anchor,mie_top+anchor,1)

s=s.replace('''<div>Ver.1.19</div>：岐阜県42市町村すべてに対応。市町村別パン屋TOP10と岐阜県TOP10を利用できます。愛知県と同じく店舗写真・店舗固有の特色・営業時間・口コミ・地図・公式サイトなどを確認できます。愛知の軽微改善とパンラッシュ保守は自動継続し、次は三重県対応へ進みます。''','''<div>Ver.1.20</div>：三重県対応を開始。四日市・桑名・鈴鹿・津・松阪・伊勢など主要13市の市別パン屋TOP10と三重県TOP10を追加しました。愛知県・岐阜県と同じ店舗詳細方式に対応。岐阜県は42市町村すべてに対応済みです。''',1)
s=s.replace('<div>Ver.1.19</div>\n  <div>Personal Bakery Discovery Project</div>','<div>Ver.1.20</div>\n  <div>Personal Bakery Discovery Project</div>',1)
p.write_text(s,encoding='utf-8')
sw=Path('sw.js');u=sw.read_text(encoding='utf-8');u=re.sub(r"const CACHE_NAME = 'tokai-pan-v\d+';","const CACHE_NAME = 'tokai-pan-v19';",u,count=1);sw.write_text(u,encoding='utf-8')
