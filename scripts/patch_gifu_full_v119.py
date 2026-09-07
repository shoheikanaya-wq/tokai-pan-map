from pathlib import Path
import re

p=Path('index.html')
s=p.read_text(encoding='utf-8')

s=s.replace(
'''  <h2>岐阜・西濃</h2><div class="cities">
    <button id="gifuCity">岐阜市</button><button id="ogaki">大垣市</button><button id="kakamigahara">各務原市</button><button id="hashima">羽島市</button><button id="mizuho">瑞穂市</button>
  </div>''',
'''  <h2>岐阜・西濃</h2><div class="cities">
    <button id="gifuCity">岐阜市</button><button id="ogaki">大垣市</button><button id="kakamigahara">各務原市</button><button id="hashima">羽島市</button><button id="mizuho">瑞穂市</button><button id="ginan">岐南町</button><button id="kasamatsu">笠松町</button><button id="yoro">養老町</button><button id="tarui">垂井町</button><button id="sekigahara">関ケ原町</button><button id="godo">神戸町</button><button id="wanouchi">輪之内町</button><button id="anpachi">安八町</button><button id="ibigawa">揖斐川町</button><button id="onoGifu">大野町</button><button id="ikedaGifu">池田町</button><button id="kitagata">北方町</button>
  </div>''',1)

s=s.replace(
'''  <h2>東濃・中濃</h2><div class="cities">
    <button id="tajimi">多治見市</button><button id="kani">可児市</button><button id="seki">関市</button><button id="mino">美濃市</button><button id="gujo">郡上市</button><button id="minokamo">美濃加茂市</button><button id="toki">土岐市</button><button id="ena">恵那市</button><button id="nakatsugawa">中津川市</button>
  </div>''',
'''  <h2>東濃・中濃</h2><div class="cities">
    <button id="tajimi">多治見市</button><button id="kani">可児市</button><button id="seki">関市</button><button id="mino">美濃市</button><button id="gujo">郡上市</button><button id="minokamo">美濃加茂市</button><button id="toki">土岐市</button><button id="mizunami">瑞浪市</button><button id="ena">恵那市</button><button id="nakatsugawa">中津川市</button><button id="sakahogi">坂祝町</button><button id="tomika">富加町</button><button id="kawabe">川辺町</button><button id="hichiso">七宗町</button><button id="yaotsu">八百津町</button><button id="shirakawaTown">白川町</button><button id="higashishirakawa">東白川村</button><button id="mitake">御嵩町</button>
  </div>''',1)

s=s.replace(
'''  <h2>岐阜北部・飛騨</h2><div class="cities">
    <button id="yamagata">山県市</button><button id="motosu">本巣市</button><button id="kaizu">海津市</button><button id="gero">下呂市</button><button id="takayama">高山市</button><button id="hida">飛騨市</button>
  </div>''',
'''  <h2>岐阜北部・飛騨</h2><div class="cities">
    <button id="yamagata">山県市</button><button id="motosu">本巣市</button><button id="kaizu">海津市</button><button id="gero">下呂市</button><button id="takayama">高山市</button><button id="hida">飛騨市</button><button id="shirakawaVillage">白川村</button>
  </div>''',1)

s=s.replace('岐阜県は主要20市へ拡大。市別TOP10と岐阜県TOP10を、愛知県と同じランキング・店舗詳細方式で表示します。','岐阜県42市町村すべてに対応。市町村別TOP10と岐阜県TOP10を、愛知県と同じランキング・店舗詳細方式で表示します。',1)

old="const gifuCity=byId('gifuCity'), ogaki=byId('ogaki'), kakamigahara=byId('kakamigahara'), hashima=byId('hashima'), mizuho=byId('mizuho'), tajimi=byId('tajimi'), kani=byId('kani'), seki=byId('seki'), mino=byId('mino'), gujo=byId('gujo'), minokamo=byId('minokamo'), toki=byId('toki'), ena=byId('ena'), nakatsugawa=byId('nakatsugawa'), yamagata=byId('yamagata'), motosu=byId('motosu'), kaizu=byId('kaizu'), gero=byId('gero'), takayama=byId('takayama'), hida=byId('hida'), gifuTop10=byId('gifuTop10');"
new="const gifuCity=byId('gifuCity'), ogaki=byId('ogaki'), kakamigahara=byId('kakamigahara'), hashima=byId('hashima'), mizuho=byId('mizuho'), ginan=byId('ginan'), kasamatsu=byId('kasamatsu'), yoro=byId('yoro'), tarui=byId('tarui'), sekigahara=byId('sekigahara'), godo=byId('godo'), wanouchi=byId('wanouchi'), anpachi=byId('anpachi'), ibigawa=byId('ibigawa'), onoGifu=byId('onoGifu'), ikedaGifu=byId('ikedaGifu'), kitagata=byId('kitagata'), tajimi=byId('tajimi'), kani=byId('kani'), seki=byId('seki'), mino=byId('mino'), gujo=byId('gujo'), minokamo=byId('minokamo'), toki=byId('toki'), mizunami=byId('mizunami'), ena=byId('ena'), nakatsugawa=byId('nakatsugawa'), sakahogi=byId('sakahogi'), tomika=byId('tomika'), kawabe=byId('kawabe'), hichiso=byId('hichiso'), yaotsu=byId('yaotsu'), shirakawaTown=byId('shirakawaTown'), higashishirakawa=byId('higashishirakawa'), mitake=byId('mitake'), yamagata=byId('yamagata'), motosu=byId('motosu'), kaizu=byId('kaizu'), gero=byId('gero'), takayama=byId('takayama'), hida=byId('hida'), shirakawaVillage=byId('shirakawaVillage'), gifuTop10=byId('gifuTop10');"
if old not in s: raise SystemExit('binding anchor not found')
s=s.replace(old,new,1)

anchor="hida.onclick=()=>selectCity(hida,'飛騨市');"
extra="""hida.onclick=()=>selectCity(hida,'飛騨市');
ginan.onclick=()=>selectCity(ginan,'岐南町');
kasamatsu.onclick=()=>selectCity(kasamatsu,'笠松町');
yoro.onclick=()=>selectCity(yoro,'養老町');
tarui.onclick=()=>selectCity(tarui,'垂井町');
sekigahara.onclick=()=>selectCity(sekigahara,'関ケ原町');
godo.onclick=()=>selectCity(godo,'神戸町');
wanouchi.onclick=()=>selectCity(wanouchi,'輪之内町');
anpachi.onclick=()=>selectCity(anpachi,'安八町');
ibigawa.onclick=()=>selectCity(ibigawa,'揖斐川町');
onoGifu.onclick=()=>selectCity(onoGifu,'大野町');
ikedaGifu.onclick=()=>selectCity(ikedaGifu,'池田町');
kitagata.onclick=()=>selectCity(kitagata,'北方町');
mizunami.onclick=()=>selectCity(mizunami,'瑞浪市');
sakahogi.onclick=()=>selectCity(sakahogi,'坂祝町');
tomika.onclick=()=>selectCity(tomika,'富加町');
kawabe.onclick=()=>selectCity(kawabe,'川辺町');
hichiso.onclick=()=>selectCity(hichiso,'七宗町');
yaotsu.onclick=()=>selectCity(yaotsu,'八百津町');
shirakawaTown.onclick=()=>selectCity(shirakawaTown,'白川町');
higashishirakawa.onclick=()=>selectCity(higashishirakawa,'東白川村');
mitake.onclick=()=>selectCity(mitake,'御嵩町');
shirakawaVillage.onclick=()=>selectCity(shirakawaVillage,'白川村');"""
if anchor not in s: raise SystemExit('handler anchor not found')
s=s.replace(anchor,extra,1)

oldcities="const cities=['岐阜市','大垣市','各務原市','羽島市','瑞穂市','多治見市','可児市','関市','美濃市','郡上市','美濃加茂市','土岐市','恵那市','中津川市','山県市','本巣市','海津市','下呂市','高山市','飛騨市'];"
newcities="const cities=['岐阜市','大垣市','各務原市','羽島市','瑞穂市','岐南町','笠松町','養老町','垂井町','関ケ原町','神戸町','輪之内町','安八町','揖斐川町','大野町','池田町','北方町','多治見市','可児市','関市','美濃市','郡上市','美濃加茂市','土岐市','瑞浪市','恵那市','中津川市','坂祝町','富加町','川辺町','七宗町','八百津町','白川町','東白川村','御嵩町','山県市','本巣市','海津市','下呂市','高山市','飛騨市','白川村'];"
if oldcities not in s: raise SystemExit('gifu top10 cities anchor not found')
s=s.replace(oldcities,newcities,1)

s=s.replace('''<div>Ver.1.18</div>：岐阜県対応を主要20市まで拡大。市別パン屋TOP10と岐阜県TOP10に対応し、飛騨・中濃・西濃まで対象を広げました。愛知県と同じく店舗写真・店舗固有の特色・営業時間・口コミ・地図・公式サイトなどを確認できます。愛知の軽微改善とパンラッシュ保守は自動継続し、三重県は今後対応予定です。''','''<div>Ver.1.19</div>：岐阜県42市町村すべてに対応。市町村別パン屋TOP10と岐阜県TOP10を利用できます。愛知県と同じく店舗写真・店舗固有の特色・営業時間・口コミ・地図・公式サイトなどを確認できます。愛知の軽微改善とパンラッシュ保守は自動継続し、次は三重県対応へ進みます。''',1)
s=s.replace('<div>Ver.1.18</div>\n  <div>Personal Bakery Discovery Project</div>','<div>Ver.1.19</div>\n  <div>Personal Bakery Discovery Project</div>',1)
p.write_text(s,encoding='utf-8')

sw=Path('sw.js')
u=sw.read_text(encoding='utf-8')
u=re.sub(r"const CACHE_NAME = 'tokai-pan-v\d+';","const CACHE_NAME = 'tokai-pan-v18';",u,count=1)
sw.write_text(u,encoding='utf-8')
