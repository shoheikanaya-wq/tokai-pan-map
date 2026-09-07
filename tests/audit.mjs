import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';

const html=fs.readFileSync(new URL('../index.html',import.meta.url),'utf8');
const sw=fs.readFileSync(new URL('../sw.js',import.meta.url),'utf8');
const manifest=JSON.parse(fs.readFileSync(new URL('../manifest.webmanifest',import.meta.url),'utf8'));
const script=html.match(/<script>([\s\S]*)<\/script>/)?.[1];
assert.ok(script,'inline app script');
new vm.Script(script);

assert.match(html,/bakeryCacheKey\(prefecture,city\)/);
assert.match(html,/tokai-pan:\$\{BAKERY_CACHE_VERSION\}:\$\{prefecture\}:\$\{city\}/);
assert.match(html,/loadBakeries\(selectedPrefecture,city\)/);
assert.match(html,/currentPrefecture!==selectedPrefecture \|\| currentCity!==city/);

assert.match(html,/fetchWideBakeryCandidates\('パン屋 岐阜県',\['岐阜県'\]\)/);
assert.match(html,/fetchWideBakeryCandidates\('パン屋 三重県',\['三重県'\]\)/);
assert.match(html,/mergeAndRankShops\(\['愛知県','岐阜県','三重県'\]/);
assert.match(html,/const key=s\.placeId \|\|/);

const commonTop10=html.indexOf('</div>\n<div style="margin-top:18px"><button id="tokaiTop10"');
assert.ok(commonTop10>0,'東海三県TOP10 is outside the Mie-only panel');
assert.equal((html.match(/id="tokaiTop10"/g)||[]).length,1);

assert.match(html,/syncViewHistory\('detail',\{prefecture:currentPrefecture/);
assert.match(html,/showDetail\(e\.state\.index,false\)/);
assert.match(html,/if\(e\.state\?\.prefecture\) currentPrefecture=e\.state\.prefecture/);

assert.equal(/href=["']tel:/i.test(html),false);
assert.equal(/電話する/.test(html),false);
assert.match(html,/dphone\.textContent=`電話番号：\$\{s\.phone\}`/);
assert.match(html,/パンラッシュは愛知県内限定/);

assert.equal(manifest.id,'./');
assert.equal(manifest.scope,'./');
assert.match(sw,/tokai-pan-v26/);
assert.match(html,/sw\.js\?rev=20260907-30/);
assert.match(html,/@media\(max-width:600px\)/);
assert.match(html,/viewport-fit=cover/);

console.log('audit checks: 24 passed');
