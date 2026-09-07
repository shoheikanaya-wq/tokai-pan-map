from pathlib import Path
import re

p=Path('index.html')
s=p.read_text(encoding='utf-8')

s=s.replace(
'''  <h2>東濃・中濃</h2><div class="cities">
    <button id="tajimi">多治見市</button><button id="kani">可児市</button><button id="seki">関市</button><button id="minokamo">美濃加茂市</button><button id="toki">土岐市</button><button id="ena">恵那市</button><button id="nakatsugawa">中津川市</button>
  </div>
  <div style="margin-top:18px"><button id="gifuTop10">🏆 岐阜県 TOP10</button></div>
  <div class="notice">岐阜県は主要12市へ拡大中です。市別TOP10と岐阜県TOP10を、愛知県と同じランキング・店舗詳細方式で表示します。</div>''',
'''  <h2>東濃・中濃</h2><div class="cities">
    <button id="tajimi">多治見市</button><button id="kani">可児市</button><button id="seki">関市</button><button id="mino">美濃市</button><button id="gujo">郡上市</button><button id="minokamo">美濃加茂市</button><button id="toki">土岐市</button><button id="ena">恵那市</button><button id="nakatsugawa">中津川市</button>
  </div>
  <h2>岐阜北部・飛騨</h2><div class="cities">
    <button id="yamagata">山県市</button><button id="motosu">本巣市</button><button id="kaizu">海津市</button><button id="gero">下呂市</button><button id="takayama">高山市</button><button id="hida">飛騨市</button>
  </div>
  <div style="margin-top:18px"><button id="gifuTop10">🏆 岐阜県 TOP10</button></div>
  <div class="notice">岐阜県は主要20市へ拡大。市別TOP10と岐阜県TOP10を、愛知県と同じランキング・店舗詳細方式で表示します。</div>''',1)

s=s.replace(
"const gifuCity=byId('gifuCity'), ogaki=byId('ogaki'), kakamigahara=byId('kakamigahara'), hashima=byId('hashima'), mizuho=byId('mizuho'), tajimi=byId('tajimi'), kani=byId('kani'), seki=byId('seki'), minokamo=byId('minokamo'), toki=byId('toki'), ena=byId('ena'), nakatsugawa=byId('nakatsugawa'), gifuTop10=byId('gifuTop10');",
"const gifuCity=byId('gifuCity'), ogaki=byId('ogaki'), kakamigahara=byId('kakamigahara'), hashima=byId('hashima'), mizuho=byId('mizuho'), tajimi=byId('tajimi'), kani=byId('kani'), seki=byId('seki'), mino=byId('mino'), gujo=byId('gujo'), minokamo=byId('minokamo'), toki=byId('toki'), ena=byId('ena'), nakatsugawa=byId('nakatsugawa'), yamagata=byId('yamagata'), motosu=byId('motosu'), kaizu=byId('kaizu'), gero=byId('gero'), takayama=byId('takayama'), hida=byId('hida'), gifuTop10=byId('gifuTop10');",1)

s=s.replace(
"nakatsugawa.onclick=()=>selectCity(nakatsugawa,'中津川市');",
"nakatsugawa.onclick=()=>selectCity(nakatsugawa,'中津川市');\nmino.onclick=()=>selectCity(mino,'美濃市');\ngujo.onclick=()=>selectCity(gujo,'郡上市');\nyamagata.onclick=()=>selectCity(yamagata,'山県市');\nmotosu.onclick=()=>selectCity(motosu,'本巣市');\nkaizu.onclick=()=>selectCity(kaizu,'海津市');\ngero.onclick=()=>selectCity(gero,'下呂市');\ntakayama.onclick=()=>selectCity(takayama,'高山市');\nhida.onclick=()=>selectCity(hida,'飛騨市');",1)

s=s.replace(
"const cities=['岐阜市','大垣市','各務原市','羽島市','瑞穂市','多治見市','可児市','関市','美濃加茂市','土岐市','恵那市','中津川市'];",
"const cities=['岐阜市','大垣市','各務原市','羽島市','瑞穂市','多治見市','可児市','関市','美濃市','郡上市','美濃加茂市','土岐市','恵那市','中津川市','山県市','本巣市','海津市','下呂市','高山市','飛騨市'];",1)

s=s.replace(
'''<div>Ver.1.17</div>：岐阜県対応を拡大。主要12市の市別パン屋TOP10と岐阜県TOP10に対応しました。愛知県と同じく店舗写真・店舗固有の特色・営業時間・口コミ・地図・公式サイトなどを確認できます。愛知の軽微改善とパンラッシュ保守は自動継続し、三重県は今後対応予定です。''',
'''<div>Ver.1.18</div>：岐阜県対応を主要20市まで拡大。市別パン屋TOP10と岐阜県TOP10に対応し、飛騨・中濃・西濃まで対象を広げました。愛知県と同じく店舗写真・店舗固有の特色・営業時間・口コミ・地図・公式サイトなどを確認できます。愛知の軽微改善とパンラッシュ保守は自動継続し、三重県は今後対応予定です。''',1)
s=s.replace('<div>Ver.1.17</div>\n  <div>Personal Bakery Discovery Project</div>','<div>Ver.1.18</div>\n  <div>Personal Bakery Discovery Project</div>',1)
p.write_text(s,encoding='utf-8')

sw=Path('sw.js')
u=sw.read_text(encoding='utf-8')
u=re.sub(r"const CACHE_NAME = 'tokai-pan-v\d+';","const CACHE_NAME = 'tokai-pan-v17';",u,count=1)
sw.write_text(u,encoding='utf-8')
