from pathlib import Path
import re

p=Path('index.html')
s=p.read_text(encoding='utf-8')

s=s.replace(
'''  <h2>北勢</h2><div class="cities"><button id="yokkaichi">四日市市</button><button id="kuwana">桑名市</button><button id="suzuka">鈴鹿市</button><button id="inabe">いなべ市</button></div>
  <h2>中勢・伊賀</h2><div class="cities"><button id="tsu">津市</button><button id="matsusaka">松阪市</button><button id="iga">伊賀市</button><button id="nabari">名張市</button></div>
  <h2>伊勢志摩・東紀州</h2><div class="cities"><button id="ise">伊勢市</button><button id="toba">鳥羽市</button><button id="shima">志摩市</button><button id="owase">尾鷲市</button><button id="kumano">熊野市</button></div>
  <div style="margin-top:18px"><button id="mieTop10">🏆 三重県 TOP10</button></div>
  <div class="notice">三重県対応を開始。主要13市の市別TOP10と三重県TOP10から順次拡大します。</div>''',
'''  <h2>北勢</h2><div class="cities"><button id="yokkaichi">四日市市</button><button id="kuwana">桑名市</button><button id="suzuka">鈴鹿市</button><button id="inabe">いなべ市</button><button id="kisosaki">木曽岬町</button><button id="toin">東員町</button><button id="komono">菰野町</button><button id="asahiMie">朝日町</button><button id="kawagoe">川越町</button></div>
  <h2>中勢・伊賀</h2><div class="cities"><button id="tsu">津市</button><button id="matsusaka">松阪市</button><button id="iga">伊賀市</button><button id="nabari">名張市</button><button id="taki">多気町</button><button id="meiwa">明和町</button><button id="odai">大台町</button></div>
  <h2>伊勢志摩・東紀州</h2><div class="cities"><button id="ise">伊勢市</button><button id="toba">鳥羽市</button><button id="shima">志摩市</button><button id="owase">尾鷲市</button><button id="kumano">熊野市</button><button id="tamaki">玉城町</button><button id="watarai">度会町</button><button id="taiki">大紀町</button><button id="minamiise">南伊勢町</button><button id="kihoku">紀北町</button><button id="mihamaMie">御浜町</button><button id="kiho">紀宝町</button></div>
  <div style="margin-top:18px"><button id="mieTop10">🏆 三重県 TOP10</button></div>
  <div class="notice">三重県29市町すべてに対応。市町別TOP10と三重県TOP10を利用できます。</div>''',1)

old="const yokkaichi=byId('yokkaichi'), kuwana=byId('kuwana'), suzuka=byId('suzuka'), inabe=byId('inabe'), tsu=byId('tsu'), matsusaka=byId('matsusaka'), iga=byId('iga'), nabari=byId('nabari'), ise=byId('ise'), toba=byId('toba'), shima=byId('shima'), owase=byId('owase'), kumano=byId('kumano'), mieTop10=byId('mieTop10');"
new="const yokkaichi=byId('yokkaichi'), kuwana=byId('kuwana'), suzuka=byId('suzuka'), inabe=byId('inabe'), kisosaki=byId('kisosaki'), toin=byId('toin'), komono=byId('komono'), asahiMie=byId('asahiMie'), kawagoe=byId('kawagoe'), tsu=byId('tsu'), matsusaka=byId('matsusaka'), iga=byId('iga'), nabari=byId('nabari'), taki=byId('taki'), meiwa=byId('meiwa'), odai=byId('odai'), ise=byId('ise'), toba=byId('toba'), shima=byId('shima'), owase=byId('owase'), kumano=byId('kumano'), tamaki=byId('tamaki'), watarai=byId('watarai'), taiki=byId('taiki'), minamiise=byId('minamiise'), kihoku=byId('kihoku'), mihamaMie=byId('mihamaMie'), kiho=byId('kiho'), mieTop10=byId('mieTop10');"
if old not in s: raise SystemExit('mie binding anchor not found')
s=s.replace(old,new,1)

anchor="kumano.onclick=()=>selectCity(kumano,'熊野市');"
extra="""kumano.onclick=()=>selectCity(kumano,'熊野市');
kisosaki.onclick=()=>selectCity(kisosaki,'木曽岬町');
toin.onclick=()=>selectCity(toin,'東員町');
komono.onclick=()=>selectCity(komono,'菰野町');
asahiMie.onclick=()=>selectCity(asahiMie,'朝日町');
kawagoe.onclick=()=>selectCity(kawagoe,'川越町');
taki.onclick=()=>selectCity(taki,'多気町');
meiwa.onclick=()=>selectCity(meiwa,'明和町');
odai.onclick=()=>selectCity(odai,'大台町');
tamaki.onclick=()=>selectCity(tamaki,'玉城町');
watarai.onclick=()=>selectCity(watarai,'度会町');
taiki.onclick=()=>selectCity(taiki,'大紀町');
minamiise.onclick=()=>selectCity(minamiise,'南伊勢町');
kihoku.onclick=()=>selectCity(kihoku,'紀北町');
mihamaMie.onclick=()=>selectCity(mihamaMie,'御浜町');
kiho.onclick=()=>selectCity(kiho,'紀宝町');"""
if anchor not in s: raise SystemExit('mie handler anchor not found')
s=s.replace(anchor,extra,1)

oldcities="const cities=['四日市市','桑名市','鈴鹿市','いなべ市','津市','松阪市','伊賀市','名張市','伊勢市','鳥羽市','志摩市','尾鷲市','熊野市'];"
newcities="const cities=['四日市市','桑名市','鈴鹿市','いなべ市','木曽岬町','東員町','菰野町','朝日町','川越町','津市','松阪市','伊賀市','名張市','多気町','明和町','大台町','伊勢市','鳥羽市','志摩市','尾鷲市','熊野市','玉城町','度会町','大紀町','南伊勢町','紀北町','御浜町','紀宝町'];"
if oldcities not in s: raise SystemExit('mie top10 cities anchor not found')
s=s.replace(oldcities,newcities,1)

s=s.replace('''<div>Ver.1.20</div>：三重県対応を開始。四日市・桑名・鈴鹿・津・松阪・伊勢など主要13市の市別パン屋TOP10と三重県TOP10を追加しました。愛知県・岐阜県と同じ店舗詳細方式に対応。岐阜県は42市町村すべてに対応済みです。''','''<div>Ver.1.21</div>：三重県29市町すべてに対応。市町別パン屋TOP10と三重県TOP10を利用できます。愛知県・岐阜県と同じ店舗詳細方式に対応し、これで愛知・岐阜・三重の東海三県をカバーしました。''',1)
s=s.replace('<div>Ver.1.20</div>\n  <div>Personal Bakery Discovery Project</div>','<div>Ver.1.21</div>\n  <div>Personal Bakery Discovery Project</div>',1)
p.write_text(s,encoding='utf-8')

sw=Path('sw.js')
u=sw.read_text(encoding='utf-8')
u=re.sub(r"const CACHE_NAME = 'tokai-pan-v\d+';","const CACHE_NAME = 'tokai-pan-v20';",u,count=1)
sw.write_text(u,encoding='utf-8')
