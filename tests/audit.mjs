import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';

const root=path.resolve(process.cwd());
const read=rel=>fs.readFileSync(path.join(root,rel),'utf8');
const html=read('index.html');
const panrush=read('panrush.html');
const sw=read('sw.js');
const manifest=JSON.parse(read('manifest.webmanifest'));
const catalog=JSON.parse(read('data/static-catalog.json'));
const script=html.match(/<script>([\s\S]*)<\/script>/)?.[1];
assert.ok(script,'index inline app script exists');
new vm.Script(script);
const rushScript=panrush.match(/<script>([\s\S]*)<\/script>/)?.[1];
assert.ok(rushScript,'panrush inline app script exists');
new vm.Script(rushScript);

const AICHI=[
  '名古屋市','豊橋市','岡崎市','一宮市','瀬戸市','半田市','春日井市','豊川市','津島市','碧南市','刈谷市','豊田市','安城市','西尾市','蒲郡市','犬山市','常滑市','江南市','小牧市','稲沢市','新城市','東海市','大府市','知多市','知立市','尾張旭市','高浜市','岩倉市','豊明市','日進市','田原市','愛西市','清須市','北名古屋市','弥富市','みよし市','あま市','長久手市','東郷町','豊山町','大口町','扶桑町','大治町','蟹江町','飛島村','阿久比町','東浦町','南知多町','美浜町','武豊町','幸田町','設楽町','東栄町','豊根村'
];
const aichi=catalog.municipalities.filter(v=>v.prefecture==='愛知県');
assert.equal(aichi.length,54,'愛知県54市町村をカタログ管理');
assert.equal(new Set(aichi.map(v=>v.city)).size,54,'愛知県市町村の重複なし');
for(const city of AICHI) assert.ok(aichi.some(v=>v.city===city),`愛知県カタログ: ${city}`);
assert.equal(aichi.filter(v=>v.status==='ready').length,52,'愛知県ready 52');
assert.equal(aichi.filter(v=>v.status==='reviewed').length,2,'愛知県reviewed 2');
for(const entry of aichi){
  assert.ok(['ready','reviewed'].includes(entry.status),`${entry.city}: status`);
  if(entry.status==='ready'){
    assert.ok(entry.file && fs.existsSync(path.join(root,entry.file)),`${entry.city}: ready file exists`);
    const data=JSON.parse(read(entry.file));
    assert.ok(Array.isArray(data.shops) && data.shops.length>0,`${entry.city}: shops not empty`);
  }else{
    assert.equal(entry.file,null,`${entry.city}: reviewed has no fabricated file`);
    assert.ok(String(entry.note||'').trim(),`${entry.city}: reviewed reason exists`);
  }
}
const reviewedNames=aichi.filter(v=>v.status==='reviewed').map(v=>v.city).sort();
assert.deepEqual(reviewedNames,['南知多町','飛島村'].sort(),'南知多町・飛島村を明示的欠損管理');
const aichiFiles=fs.readdirSync(path.join(root,'data')).filter(v=>/^aichi-.*\.json$/.test(v));
assert.equal(aichiFiles.length,52,'data/aichi-*.json は52件');

function walkJson(dir){
  const out=[];
  for(const ent of fs.readdirSync(dir,{withFileTypes:true})){
    if(ent.name==='.git'||ent.name==='node_modules') continue;
    const full=path.join(dir,ent.name);
    if(ent.isDirectory()) out.push(...walkJson(full));
    else if(ent.isFile()&&ent.name.endsWith('.json')) out.push(full);
  }
  return out;
}
const jsonFiles=walkJson(root);
for(const file of jsonFiles) JSON.parse(fs.readFileSync(file,'utf8'));
assert.ok(jsonFiles.length>=120,'全JSONを列挙してparse');

assert.match(html,/function shopDisplayName\(shop\)/,'店名fallback helper');
assert.match(html,/店舗名は地図で確認/,'店名fallback text');
assert.match(html,/function shopDisplayAddress\(shop\)/,'住所fallback helper');
assert.match(html,/住所は地図で確認/,'住所fallback text');
assert.match(html,/function shopDisplayFeature\(shop,factCopy\)/,'特色fallback helper');
assert.match(html,/特色は公式サイト・地図で確認/,'特色fallback text');
assert.match(html,/営業時間・定休日<\/strong><br>最新情報は公式サイト・地図で確認/,'営業時間fallback');
assert.match(html,/電話番号：公式サイト・地図で確認/,'電話番号fallback');

for(const file of fs.readdirSync(root).filter(v=>v.endsWith('.html'))){
  const body=read(file);
  assert.equal(/href\s*=\s*["']tel:/i.test(body),false,`${file}: tel hrefなし`);
  assert.equal(/(?:window\.)?location(?:\.href)?\s*=\s*["']tel:/i.test(body),false,`${file}: tel location遷移なし`);
  assert.equal(/\.href\s*=\s*["']tel:/i.test(body),false,`${file}: tel href代入なし`);
}
assert.equal(/電話する/.test(html),false,'電話するボタンなし');
assert.match(html,/dphone\.textContent=s\.phone \? `電話番号：\$\{s\.phone\}`/,'電話番号はtextContent表示のみ');

const shopNameSizes=[...html.matchAll(/#list \.shop-name\s*\{[^}]*font-size\s*:\s*(\d+)px/g)].map(m=>Number(m[1]));
assert.ok(shopNameSizes.length,'スマホ店舗名CSSを検出');
assert.ok(shopNameSizes.at(-1)>=16,'最終スマホ店舗名16px以上');
assert.match(html,/viewport-fit=cover/,'スマホviewport');

assert.equal(manifest.id,'./');
assert.equal(manifest.scope,'./');
const cacheVersion=sw.match(/CACHE_NAME\s*=\s*['"]tokai-pan-v(\d+)['"]/)?.[1];
const swRevision=html.match(/serviceWorker\.register\(['"]\.\/sw\.js\?rev=[^'"]*-(\d+)['"]\)/)?.[1];
assert.ok(cacheVersion,'Service Worker cache version found');
assert.ok(swRevision,'Service Worker registration revision found');
assert.equal(swRevision,cacheVersion,'SW登録revとCACHE_NAMEの版番号が同期');
assert.match(sw,/skipWaiting\(\)/,'SW immediate activation');
assert.match(sw,/clients\.claim\(\)/,'SW clients claim');

assert.match(panrush,/id="quickStart"/,'パンラッシュ: すぐ始めるボタン');
assert.match(panrush,/すぐ始める/,'パンラッシュ: すぐ始める文言');
assert.match(panrush,/id="planTop"[^>]*>🔥 このままルートを作る<\/button>/,'パンラッシュ: 上部ルート作成導線');
assert.match(panrush,/id="plan"[^>]*>🔥 このままルートを作る<\/button>/,'パンラッシュ: 下部ルート作成導線');
assert.match(panrush,/startWithRecommended/,'パンラッシュ: quick start handler');
assert.match(panrush,/id=\\"rushRetry\\"|id="+'"'+'rushRetry'+'"'+'/,'パンラッシュ: 通信失敗時の再試行');
assert.match(panrush,/addEventListener\\('online'/,'パンラッシュ: 通信復帰検知');
assert.match(panrush,/addEventListener\\('offline'/,'パンラッシュ: オフライン検知');
assert.match(panrush,/if\\(!groups\\.length\\)throw Error/,'パンラッシュ: 全地域通信失敗を候補0件と誤認しない');
assert.match(panrush,/24時間内立寄り可能/,'パンラッシュ: 24時間内立寄り可能数');
assert.match(panrush,/開店待ち/,'パンラッシュ: 待ち時間反映');
assert.match(panrush,/value="bike">クロスカブ/,'パンラッシュ: クロスカブ');
assert.match(panrush,/value="car">車/,'パンラッシュ: 車');
assert.match(panrush,/西三河耐久/);
assert.match(panrush,/三河縦断/);
assert.match(panrush,/愛知横断/);

console.log(`audit checks passed: 愛知54市町村 / JSON ${jsonFiles.length}件 / SW v${cacheVersion} / phone-display-only / panrush-route-flow`);
