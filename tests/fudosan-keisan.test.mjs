// ぷらっと不動産「計算の道具」のテスト。 走らせ方: node tests/fudosan-keisan.test.mjs
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import {createRequire} from 'node:module';

const root=path.resolve(process.cwd());
const require=createRequire(import.meta.url);
const K=require(path.join(root,'assets/fudosan-keisan.js'));
const read=rel=>fs.readFileSync(path.join(root,rel),'utf8');

// ---- 1. 返済の式(元利均等) ----
// 100万円・年3.81%・35年(420回)は、月々 約4,314.5円。円未満は切り捨て(公式の試算と同じ)。
assert.ok(Math.abs(K.monthlyExact(1000000,3.81,35)-4314.5)<0.1,'100万円・3.81%・35年の月々は約4,314.5円');
assert.equal(K.monthlyPayment(1000000,3.81,35),4314,'円未満は切り捨て');
assert.equal(K.monthlyPayment(1200000,0,10),10000,'金利0%は、元金÷回数');
assert.equal(K.monthlyPayment(0,3.81,35),0,'借りる額0円は0円');

assert.equal(K.monthlyPayment(1200000,1e-15,10),10000,'とても小さい金利でも、おかしな数字を出さない');
assert.ok(K.compute({landMode:'own',buildArea:100,buildUnit:36.1,uplift:0,others:[{key:'a',state:'none'}],cash:0,rate:23,years:35}).payReady,'「もしも」で20%を少しこえても計算できる');

// ---- 2. 公式の試算ページとくらべる ----
// フラット35サイト「借入希望金額から返済額を計算」(https://www.flat35.com/simulation/simu_01.html)に
// 2026-11-15 に同じ数字を入れて出た結果(元利均等・ボーナス払いなし)。
// 公式の画面は「万円」で、月々は0.1万円単位、総返済額は1万円単位に切り上げて出している。
const OFFICIAL=[
  // [借りる額(万円), 年数, 金利(年%), 公式の月々(万円), 公式の総返済額(万円)]
  [3000,35,3.81,13.0,5437],
  [4000,35,3.81,17.3,7249],
  [2500,20,3.49,14.5,3477],
  [3500,35,4.81,17.3,7242],
  [100,35,3.81,0.5,182],
  [4403,30,3.81,20.6,7395]
];
const ceilTo=(v,unit)=>Math.ceil(v/unit-1e-9)*unit;
for(const [man,years,rate,offMonthly,offTotal] of OFFICIAL){
  const m=K.monthlyPayment(man*10000,rate,years);
  const total=m*years*12;
  assert.equal(Math.round(ceilTo(m,1000)/1000),Math.round(offMonthly*10),`公式と同じ月々: ${man}万円 ${rate}% ${years}年`);
  // 総返済額は、公式は最後の回で端数を合わせるので、こちら(月々×回数)と1万円までずれてよい
  assert.ok(Math.abs(ceilTo(total,10000)/10000-offTotal)<=1,`公式と総返済額が1万円以内: ${man}万円 ${rate}% ${years}年`);
}

// ---- 3. 数字の読み取り ----
assert.equal(K.parseNum('1,234.5'),1234.5);
assert.equal(K.parseNum('１００'),100,'全角の数字も読む');
assert.equal(K.parseNum('３．８１'),3.81,'全角の点も読む');
assert.equal(K.parseNum(' 36.1 '),36.1);
assert.ok(Number.isNaN(K.parseNum('')),'空は「入っていない」');
assert.ok(Number.isNaN(K.parseNum('abc')));
assert.ok(Number.isNaN(K.parseNum('-5')),'マイナスは受けつけない');

// ---- 4. まとめの計算 ----
const full={
  landMode:'own',buildArea:100,buildUnit:36.1,uplift:10,
  others:[{key:'tax',state:'in',amount:50},{key:'jiban',state:'none',amount:NaN}],
  cash:500,rate:3.81,years:35
};
const r=K.compute(full);
assert.equal(r.complete,true,'全部そろえば「総額」と言える');
assert.equal(r.building,Math.round(100*36.1*1.1*10000),'建物 = 広さ×1㎡あたり×(1+上乗せ)');
assert.equal(r.land,0);
assert.equal(r.others,500000);
assert.equal(r.total,r.building+500000);
assert.equal(r.loan,r.total-5000000);
assert.equal(r.monthly,K.monthlyPayment(r.loan,3.81,35));
assert.equal(r.repayTotal,r.monthly*420);
assert.equal(r.interest,r.repayTotal-r.loan);

// 直し案1: そのほかの費用が「まだ分からない」のうちは、総額と言わない
const r1=K.compute({...full,others:[{key:'tax',state:'unknown',amount:NaN}]});
assert.equal(r1.complete,false);
assert.ok(r1.missing.includes('others'),'そのほかの費用が入っていない');
// 「入れた」をえらんで金額が空でも、入っていないあつかい
const r1b=K.compute({...full,others:[{key:'tax',state:'in',amount:NaN}]});
assert.ok(r1b.missing.includes('others'));
// 項目が1つもないときも、入っていないあつかい
assert.ok(K.compute({...full,others:[]}).missing.includes('others'));

// 直し案2: 平屋の上乗せが空のうちは、総額と言わない(0% と入れたら言える)
const r2=K.compute({...full,uplift:NaN});
assert.equal(r2.complete,false);
assert.ok(r2.missing.includes('uplift'));
assert.equal(r2.building,Math.round(100*36.1*10000),'空のときは上乗せなしで仮に計算');
assert.equal(K.compute({...full,uplift:0}).complete,true);

// 土地
const r3=K.compute({...full,landMode:''});
assert.ok(r3.missing.includes('land'),'土地をえらんでいない');
const r4=K.compute({...full,landMode:'buy',landArea:200,landUnit:NaN});
assert.ok(r4.missing.includes('land'),'買うのに値段が空');
const r5=K.compute({...full,landMode:'buy',landArea:200,landUnit:10});
assert.equal(r5.land,20000000);
assert.equal(r5.complete,true);

// 建物が空なら、結果を出さない
assert.equal(K.compute({...full,buildArea:NaN}).ready,false);
// 手持ちが総額より多ければ、借りる額は0円
const r6=K.compute({...full,cash:99999});
assert.equal(r6.loan,0);assert.equal(r6.monthly,0);
// 手持ちが空なら0円として計算し、そのことを知らせる
const r7=K.compute({...full,cash:NaN});
assert.equal(r7.loan,r7.total);assert.equal(r7.cashAssumedZero,true);

// 「もしも」: 金利と建物の値段を上げる
const w=K.whatIf(full,{rateUp:1,buildUp:10});
assert.equal(w.rateOnly.monthly,K.compute({...full,rate:4.81}).monthly);
assert.equal(w.buildOnly.monthly,K.compute({...full,buildUnit:36.1*1.1}).monthly);
assert.ok(w.both.monthly>w.rateOnly.monthly&&w.both.monthly>w.buildOnly.monthly);
assert.ok(w.rateOnly.diff>0&&w.buildOnly.diff>0);
assert.equal(K.whatIf(full,{rateUp:0,buildUp:0}).both.diff,0);

// 坪
assert.ok(Math.abs(K.toTsubo(100)-30.25)<0.01,'100㎡は約30.25坪');

// ---- 5. 数字のファイル ----
const suji=JSON.parse(read('data/fudosan-suji.json'));
assert.equal(suji.pref,'愛知県','1版は愛知県だけ');
for(const key of ['buildUnit','rate21to35','rate15to20']){
  const x=suji.figures[key];
  assert.ok(x,`${key} がある`);
  assert.equal(typeof x.value,'number',`${key}: 数字`);
  for(const f of ['unit','asOf','sourceName','sourceUrl','checkedAt']) assert.ok(String(x[f]||'').trim(),`${key}: ${f} が書いてある`);
  assert.match(x.sourceUrl,/^https:\/\//,`${key}: 出どころは https`);
  assert.match(x.checkedAt,/^\d{4}-\d{2}-\d{2}$/,`${key}: 確かめた日`);
}
assert.equal(suji.figures.buildUnit.value,36.1);
assert.equal(suji.figures.buildUnit.count,244,'件数を書く');
assert.equal(suji.figures.rate21to35.value,3.81);

// ---- 6. ページの決まり ----
const html=read('fudosan-keisan.html');
const js=read('assets/fudosan-keisan.js');
assert.ok((html.match(/目安です。本当の見積もりではありません/g)||[]).length+(js.match(/目安です。本当の見積もりではありません/g)||[]).length>=2,'注意書きが、上と結果のすぐ上にある');
// 直し案3: 何も覚えない・どこにも送らない
for(const [name,body] of [['html',html],['js',js]]){
  assert.equal(/localStorage|sessionStorage|indexedDB|document\.cookie/.test(body),false,`${name}: 端末に覚えない`);
  assert.equal(/XMLHttpRequest|sendBeacon|WebSocket|<form\b/i.test(body),false,`${name}: 送る仕組みがない`);
  assert.equal(/history\.(?:push|replace)State|location\.(?:search|hash)\s*=/.test(body),false,`${name}: 数字をアドレスに書かない`);
}
const fetches=[...js.matchAll(/fetch\(([^)]*)\)/g)].map(m=>m[1]);
assert.equal(fetches.length,1,'読みこむのは数字のファイル1つだけ');
assert.match(js,/data\/fudosan-suji\.json/,'数字は data/fudosan-suji.json から読む');
assert.equal(/autocomplete="(?!off)/.test(html),false,'入力の自動記憶をさせない');
// 直し案2: 上乗せのはじめの数字は空
assert.match(html,/id="uplift"[^>]*value=""/,'平屋の上乗せは、はじめ空');
assert.match(html,/2階建てもまざった平均です/);
// 直し案4: 二重に足さない注意
assert.match(html,/二重に足さない/);
// 入口: 地域カードから入れる
assert.match(read('fudosan.html'),/href="fudosan-keisan\.html"/,'地域カードから計算の道具へ入れる');
for(const m of html.matchAll(/<a\b[^>]*target=["']_blank["'][^>]*>/gi)) assert.match(m[0],/rel=["'][^"']*noopener/i,'target=_blank は noopener');

console.log('fudosan-keisan tests passed: 返済の式 / 公式の試算と6例 / 総額と言わない条件 / 数字のファイル / 覚えない・送らない');
