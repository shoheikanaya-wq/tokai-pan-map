from pathlib import Path
import re
p=Path('index.html')
s=p.read_text(encoding='utf-8')

s=s.replace("<button id=\"tsu\">津市</button><button id=\"matsusaka\">松阪市</button><button id=\"iga\">伊賀市</button>","<button id=\"tsu\">津市</button><button id=\"matsusaka\">松阪市</button><button id=\"kameyama\">亀山市</button><button id=\"iga\">伊賀市</button>",1)
s=s.replace("<div class=\"notice\">三重県29市町すべてに対応。市町別TOP10と三重県TOP10を利用できます。</div>","<div class=\"notice\">三重県29市町すべてに対応。市町別TOP10と三重県TOP10を利用できます。</div>\n  <div style=\"margin-top:18px\"><button id=\"tokaiTop10\">🏆 東海三県 TOP10</button></div>",1)

s=s.replace("matsusaka=byId('matsusaka'), iga=byId('iga')","matsusaka=byId('matsusaka'), kameyama=byId('kameyama'), iga=byId('iga')",1)
s=s.replace("mieTop10=byId('mieTop10');","mieTop10=byId('mieTop10'), tokaiTop10=byId('tokaiTop10');",1)
s=s.replace("matsusaka.onclick=()=>selectCity(matsusaka,'松阪市');","matsusaka.onclick=()=>selectCity(matsusaka,'松阪市');\nkameyama.onclick=()=>selectCity(kameyama,'亀山市');",1)
s=s.replace("'津市','松阪市','伊賀市'","'津市','松阪市','亀山市','伊賀市'",1)

anchor="  gifuTop10.onclick = async () => {"
handler="""  tokaiTop10.onclick = async () => {
  currentPrefecture='東海三県'; currentVisualKey='東海三県';
  const cachedTop10=getTop10Cache('東海三県',AICHI_TOP10_TTL);
  if(cachedTop10){shops=cachedTop10.shops;currentCity='東海三県';rankingTitle.textContent='東海三県 パン屋 TOP10';showRanking();return;}
  tokaiTop10.disabled=true; tokaiTop10.textContent='取得中...';
  try{
    const a=getTop10Cache('愛知県',AICHI_TOP10_TTL)?.shops||[];
    const g=getTop10Cache('岐阜県',AICHI_TOP10_TTL)?.shops||[];
    const m=getTop10Cache('三重県',AICHI_TOP10_TTL)?.shops||[];
    const [aw,gw,mw]=await Promise.all([
      a.length?Promise.resolve([]):fetchWideBakeryCandidates('パン屋 愛知県'),
      g.length?Promise.resolve([]):fetchWideBakeryCandidates('パン屋 岐阜県'),
      m.length?Promise.resolve([]):fetchWideBakeryCandidates('パン屋 三重県')
    ]);
    shops=mergeAndRankShops([...a,...g,...m],[...aw,...gw,...mw])
      .filter(s=>/愛知県|岐阜県|三重県/.test(String(s.address||'')))
      .slice(0,10);
    setTop10Cache('東海三県',shops); currentCity='東海三県'; rankingTitle.textContent='東海三県 パン屋 TOP10'; showRanking();
  }catch(e){showLoadError('東海三県ランキングを取得できませんでした。',()=>tokaiTop10.click());}
  finally{tokaiTop10.disabled=false;tokaiTop10.textContent='🏆 東海三県 TOP10';}
};

"""
if anchor not in s: raise SystemExit('anchor not found')
s=s.replace(anchor,handler+anchor,1)

s=s.replace('''<div>Ver.1.21</div>：三重県29市町すべてに対応。市町別パン屋TOP10と三重県TOP10を利用できます。愛知県・岐阜県と同じ店舗詳細方式に対応し、これで愛知・岐阜・三重の東海三県をカバーしました。''','''<div>Ver.1.22</div>：三重県の亀山市漏れを修正し29市町すべてに対応。さらに愛知・岐阜・三重を横断した「東海三県TOP10」を追加しました。''',1)
s=s.replace('<div>Ver.1.21</div>\n  <div>Personal Bakery Discovery Project</div>','<div>Ver.1.22</div>\n  <div>Personal Bakery Discovery Project</div>',1)
p.write_text(s,encoding='utf-8')
sw=Path('sw.js');u=sw.read_text(encoding='utf-8');u=re.sub(r"const CACHE_NAME = 'tokai-pan-v\d+';","const CACHE_NAME = 'tokai-pan-v21';",u,count=1);sw.write_text(u,encoding='utf-8')
