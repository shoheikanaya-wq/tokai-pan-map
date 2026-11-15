/* ぷらっと不動産「計算の道具」
   計算は全部、見る人の端末の中でする。入れた数字は、どこにも送らない・覚えない。
   はじめの数字(建物の1㎡あたり・金利)は data/fudosan-suji.json から読む。
   上半分は計算だけ(テスト tests/fudosan-keisan.test.mjs から使う)。下半分は画面。 */
(function(root){
  'use strict';
  var TSUBO=3.30578; // 1坪 = 3.30578㎡
  var MAN=10000;
  var RATE_MAX=30; // 計算できる金利の上限。画面の入力は20%まで。「もしも」で足した分も計算できるように広めにしてある

  function parseNum(s){
    if(typeof s==='number')return s>=0?s:NaN;
    // 全角の数字・点・カンマを半角に直し、カンマと空白を取る
    s=String(s==null?'':s).replace(/[０-９．，]/g,function(c){return String.fromCharCode(c.charCodeAt(0)-0xFEE0)}).replace(/[,\s　]/g,'');
    if(!/^\d+(\.\d+)?$/.test(s))return NaN;
    return parseFloat(s);
  }
  function ok(v){return typeof v==='number'&&isFinite(v)&&v>=0}
  function toTsubo(m2){return m2/TSUBO}

  // 元利均等の月々(円。切り捨てる前)
  function monthlyExact(principal,ratePct,years){
    var n=Math.round(years*12);
    if(!(principal>0)||!(n>0))return 0;
    var r=ratePct/100/12;
    if(!(r>0))return principal/n;
    var p=Math.pow(1+r,n);
    if(!(p-1>1e-9)||!isFinite(p))return principal/n; // 金利がとても小さいときは、利息なしと同じにする
    return principal*r*p/(p-1);
  }
  // 円未満は切り捨て(フラット35サイトの試算と同じ切り方)
  function monthlyPayment(principal,ratePct,years){return Math.floor(monthlyExact(principal,ratePct,years)+1e-9)}

  /* input: {landMode:''|'own'|'buy', landArea(㎡), landUnit(万円/㎡), buildArea(㎡), buildUnit(万円/㎡),
            uplift(%), others:[{key,state:'in'|'none'|'unknown',amount(万円)}], cash(万円), rate(年%), years}
     金額はすべて「円」で返す。 */
  function compute(x){
    var out={ready:false,payReady:false,complete:false,missing:[],unknownOthers:[],cashAssumedZero:false,
      land:0,buildingBase:0,building:0,others:0,total:0,loan:0,monthly:0,repayTotal:0,interest:0};
    if(!(ok(x.buildArea)&&x.buildArea>0&&ok(x.buildUnit)&&x.buildUnit>0))return out;
    out.ready=true;

    if(x.landMode==='own'){out.land=0}
    else if(x.landMode==='buy'&&ok(x.landArea)&&x.landArea>0&&ok(x.landUnit)&&x.landUnit>0){out.land=Math.round(x.landArea*x.landUnit*MAN)}
    else{out.missing.push('land')}

    out.buildingBase=Math.round(x.buildArea*x.buildUnit*MAN);
    if(ok(x.uplift)){out.building=Math.round(x.buildArea*x.buildUnit*(1+x.uplift/100)*MAN)}
    else{out.building=out.buildingBase;out.missing.push('uplift')}

    var list=x.others||[];
    list.forEach(function(o){
      if(o.state==='in'&&ok(o.amount)){out.others+=Math.round(o.amount*MAN)}
      else if(o.state==='none'){/* 0円 */}
      else{out.unknownOthers.push(o.key)}
    });
    if(!list.length||out.unknownOthers.length)out.missing.push('others');

    out.total=out.land+out.building+out.others;
    var cash=0;
    if(ok(x.cash)){cash=Math.round(x.cash*MAN)}else{out.cashAssumedZero=true}
    out.loan=Math.max(0,out.total-cash);

    if(isFinite(out.total)&&ok(x.rate)&&x.rate<=RATE_MAX&&ok(x.years)&&x.years>=1&&x.years<=50){
      out.payReady=true;
      out.monthly=monthlyPayment(out.loan,x.rate,x.years);
      out.repayTotal=out.monthly*Math.round(x.years*12);
      out.interest=Math.max(0,out.repayTotal-out.loan);
    }
    out.complete=out.missing.length===0&&out.payReady;
    return out;
  }

  // 「もしも」: 金利が rateUp(%ポイント)上がる/建物の値段が buildUp(%)上がる
  function whatIf(x,opt){
    function copy(extra){var y={};for(var k in x)y[k]=x[k];for(var e in extra)y[e]=extra[e];return y}
    var base=compute(x);
    var a=compute(copy({rate:x.rate+opt.rateUp}));
    var b=compute(copy({buildUnit:x.buildUnit*(1+opt.buildUp/100)}));
    var c=compute(copy({rate:x.rate+opt.rateUp,buildUnit:x.buildUnit*(1+opt.buildUp/100)}));
    function pack(r){return {monthly:r.monthly,diff:r.monthly-base.monthly,loan:r.loan,loanDiff:r.loan-base.loan,repayTotal:r.repayTotal}}
    return {base:base,rateOnly:pack(a),buildOnly:pack(b),both:pack(c)};
  }

  var API={parseNum:parseNum,toTsubo:toTsubo,monthlyExact:monthlyExact,monthlyPayment:monthlyPayment,compute:compute,whatIf:whatIf};
  if(typeof module!=='undefined'&&module.exports){module.exports=API}
  root.FudosanKeisan=API;
  if(typeof document==='undefined')return;

  /* ---------- ここから画面 ---------- */
  var $=function(id){return document.getElementById(id)};
  function esc(s){return String(s==null?'':s).replace(/[&<>"']/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]})}
  function safeUrl(u){return /^https:\/\//.test(u||'')?u:''}
  function man(yen){return (yen/MAN).toLocaleString('ja-JP',{maximumFractionDigits:1})+'万円'}
  function yen(v){return Math.round(v).toLocaleString('ja-JP')+'円'}
  function signMan(v){return (v>=0?'+':'−')+man(Math.abs(v))}
  function signYen(v){return (v>=0?'+':'−')+yen(Math.abs(v))}
  var CAUTION='目安です。本当の見積もりではありません。';

  // そのほかの費用の項目。金額の目安は出さない(公的な目安がないため)。
  var OTHERS=[
    {key:'tax',name:'税金(印紙税・不動産取得税・登録免許税など)'},
    {key:'toki',name:'登記の費用(司法書士へのお礼など)'},
    {key:'loan',name:'ローンの手数料・保証料'},
    {key:'hoken',name:'火災保険・地震保険'},
    {key:'jiban',name:'地盤の改良'},
    {key:'gaiko',name:'外構(駐車場・塀・庭)',hint:'建設費の平均には「屋外附帯工事費」がもう入っています。見積もりで、重なっていないか確かめてください。'},
    {key:'suido',name:'水道の引き込み・加入金',hint:'建物の工事費に入っていることがあります。見積もりで確かめてください。'},
    {key:'chukai',name:'土地の仲介手数料',buyOnly:true},
    {key:'hikkoshi',name:'引っ越し・家具・家電'},
    {key:'hoka',name:'そのほか'}
  ];

  function landMode(){var r=document.querySelector('input[name="landMode"]:checked');return r?r.value:''}
  function othersHtml(){
    return OTHERS.map(function(o){
      var n='st_'+o.key;
      return '<div class="oitem" data-key="'+o.key+'"'+(o.buyOnly?' data-buy="1" hidden':'')+'>'+
        '<div class="oname">'+esc(o.name)+'</div>'+(o.hint?'<p class="hint">'+esc(o.hint)+'</p>':'')+
        '<div class="seg" role="radiogroup" aria-label="'+esc(o.name)+'">'+
        '<label><input type="radio" name="'+n+'" value="in"><span>入れた</span></label>'+
        '<label><input type="radio" name="'+n+'" value="none"><span>なし</span></label>'+
        '<label><input type="radio" name="'+n+'" value="unknown" checked><span>まだ分からない</span></label></div>'+
        '<div class="amt" hidden><input type="text" inputmode="decimal" autocomplete="off" id="amt_'+o.key+'" aria-label="'+esc(o.name)+'の金額(万円)" placeholder="金額"><span class="unit">万円</span></div>'+
        '</div>';
    }).join('');
  }
  // 入れてよい範囲。外れたら「入っていない」あつかいにして、欄を赤くする
  var LIMITS={landArea:[0.01,100000],landUnit:[0.01,10000],buildArea:[0.01,10000],buildUnit:[0.01,1000],uplift:[0,100],cash:[0,1000000],rate:[0,20],years:[1,50,true]};
  var AMT=[0,100000];
  function field(id,lim){
    var el=$(id),raw=el.value.trim(),v=parseNum(raw);
    if(!isNaN(v)&&(v<lim[0]||v>lim[1]||(lim[2]&&v!==Math.floor(v))))v=NaN;
    el.classList.toggle('bad',raw!==''&&isNaN(v));
    return v;
  }
  function readInput(){
    var buy=landMode()==='buy';
    var others=[];
    OTHERS.forEach(function(o){
      if(o.buyOnly&&!buy)return;
      var r=document.querySelector('input[name="st_'+o.key+'"]:checked');
      others.push({key:o.key,name:o.name,state:r?r.value:'unknown',amount:field('amt_'+o.key,AMT)});
    });
    var x={landMode:landMode(),others:others};
    for(var id in LIMITS)x[id]=field(id,LIMITS[id]);
    return x;
  }
  function row(k,v,cls){return '<div class="rrow'+(cls?' '+cls:'')+'"><span>'+k+'</span><b>'+v+'</b></div>'}

  function render(){
    var x=readInput(),r=compute(x),buy=x.landMode==='buy';
    $('landBuy').hidden=!buy;
    Array.prototype.forEach.call(document.querySelectorAll('.oitem'),function(el){
      if(el.dataset.buy)el.hidden=!buy;
      var st=el.querySelector('input[type="radio"]:checked');
      el.querySelector('.amt').hidden=!(st&&st.value==='in');
    });
    $('landTsubo').textContent=x.landArea>0?'約'+toTsubo(x.landArea).toFixed(1)+'坪':'';
    $('buildTsubo').textContent=x.buildArea>0?'約'+toTsubo(x.buildArea).toFixed(1)+'坪':'';
    $('landSum').textContent=(buy&&x.landArea>0&&x.landUnit>0)?'土地の値段:'+man(x.landArea*x.landUnit*MAN)+'(1坪あたり 約'+(x.landUnit*TSUBO).toFixed(1)+'万円)':'';
    $('buildSum').textContent=(x.buildArea>0&&x.buildUnit>0)?'上乗せの前:'+man(r.buildingBase)+'(1坪あたり 約'+(x.buildUnit*TSUBO).toFixed(1)+'万円)':'';
    var y=x.years,hint='';
    if(y>=15&&y<=20&&SUJI&&SUJI.rate15to20)hint='返す期間が15〜20年のとき、いちばん多い金利は年'+SUJI.rate15to20.value+'%です('+SUJI.rate15to20.asOf+')。';
    else if(y>0&&(y<15||y>35))hint='フラット35は、ふつう15〜35年です。この金利はあてはまりません。';
    $('yearsHint').textContent=hint;

    var h='<p class="caution">'+CAUTION+'</p>';
    if(!r.ready){
      $('result').innerHTML=h+'<p class="empty">「建物の広さ」を入れると、ここに結果が出ます。</p>';
      $('moshimo').hidden=true;return;
    }
    var warn=[];
    if(r.missing.indexOf('others')>=0)warn.push('<b>そのほかの費用が入っていません。</b>(「まだ分からない」か、金額が空のものが '+r.unknownOthers.length+'個あります)下の数字は、本当より安く出ています。');
    if(r.missing.indexOf('uplift')>=0)warn.push('<b>平屋の上乗せが、えらばれていません。</b>2階建てもまざった平均のままなので、平屋には安く出ています。');
    if(r.missing.indexOf('land')>=0)warn.push(x.landMode?'<b>土地の値段が入っていません。</b>':'<b>土地を「もう持っている/これから買う」からえらんでください。</b>');
    if(!r.payReady)warn.push('<b>金利と、返す年数を入れてください。</b>(金利は0〜20%。年数は1〜50年で、小数なし)');
    if(warn.length)h+='<div class="warn">'+warn.map(function(w){return '<p>⚠ '+w+'</p>'}).join('')+'</div>';

    var whole=r.missing.length===0;
    h+='<div class="total'+(whole?'':' part')+'"><span>'+(whole?'総額(目安)':'いま入っている分の合計(総額ではありません)')+'</span><b>'+man(r.total)+'</b></div>';
    h+=row('土地',x.landMode==='own'?'0円(もう持っている)':(r.missing.indexOf('land')>=0?'まだ入っていない':man(r.land)));
    h+=row('建物',man(r.building)+(ok(x.uplift)?'(上乗せ '+x.uplift+'% こみ)':'(上乗せなしのまま)'));
    h+=row('そのほかの費用',man(r.others)+(r.unknownOthers.length?'(入れた分だけ)':''));
    h+='<hr>';
    h+=row('手持ちのお金',r.cashAssumedZero?'0円として計算':man(Math.round(x.cash*MAN)));
    h+=row('借りる額',man(r.loan));
    if(r.payReady){
      h+='<div class="total pay"><span>月々の返済'+(whole?'(目安)':'(いま入っている分で計算)')+'</span><b>'+yen(r.monthly)+'</b></div>';
      h+=row('返す総額',man(r.repayTotal));
      h+=row('そのうち利息',man(r.interest));
      h+='<p class="hint">年'+x.rate+'%・'+x.years+'年・毎月同じ額を返す形(元利均等)・ボーナス払いなし・金利はずっと同じ、として計算しています。団体信用生命保険の特約料などは入っていません。</p>';
    }
    $('result').innerHTML=h;

    // もしも
    $('moshimo').hidden=!r.payReady;
    if(!r.payReady)return;
    var ru=parseFloat($('ifRate').value)||0,bu=parseFloat($('ifBuild').value)||0;
    $('ifRateOut').textContent='+'+ru.toFixed(1)+'%(年'+(Math.round((x.rate+ru)*100)/100)+'%)';
    $('ifBuildOut').textContent='+'+bu+'%';
    var w=whatIf(x,{rateUp:ru,buildUp:bu});
    var m='<p class="caution">'+CAUTION+'</p>'+(whole?'':'<p class="hint"><b>いま入っている分での見くらべです。</b>入っていない費用があります。</p>');
    m+=row('金利だけ上がると','月々 '+yen(w.rateOnly.monthly)+'<small>'+signYen(w.rateOnly.diff)+'</small>','stack');
    m+=row('建物の値段だけ上がると','月々 '+yen(w.buildOnly.monthly)+'<small>'+signYen(w.buildOnly.diff)+'</small><small>借りる額 '+signMan(w.buildOnly.loanDiff)+'</small>','stack');
    m+=row('両方いっしょだと','月々 '+yen(w.both.monthly)+'<small>'+signYen(w.both.diff)+'</small><small>返す総額 '+signMan(w.both.repayTotal-r.repayTotal)+'</small>','stack strong');
    $('ifOut').innerHTML=m;
  }

  function srcLine(f){
    var u=safeUrl(f.sourceUrl);
    return esc(f.sourceName)+(f.scope?'・'+esc(f.scope):'')+'。'+esc(f.asOf)+(f.count?'。件数 '+esc(f.count)+'件':'')+'。確かめた日 '+esc(f.checkedAt)+'。'+
      (u?' <a href="'+esc(u)+'" target="_blank" rel="noopener">出どころを見る</a>':'');
  }
  var SUJI=null;
  function applySuji(d){
    var f=d&&d.figures;
    if(!f||!f.buildUnit||!f.rate21to35){
      $('buildUnitSrc').textContent='はじめの数字を読みこめませんでした。自分で数字を入れてください。';
      $('rateSrc').textContent='はじめの数字を読みこめませんでした。自分で数字を入れてください。';
      return;
    }
    SUJI=f;
    if(!$('buildUnit').value)$('buildUnit').value=f.buildUnit.value;
    if(!$('rate').value)$('rate').value=f.rate21to35.value;
    $('buildUnitSrc').innerHTML='はじめの数字 '+esc(f.buildUnit.value)+'万円は、'+srcLine(f.buildUnit);
    $('buildUnitNotes').innerHTML=(f.buildUnit.notes||[]).map(function(t){return '<li>'+esc(t)+'</li>'}).join('');
    $('rateSrc').innerHTML='はじめの数字 年'+esc(f.rate21to35.value)+'%は、'+srcLine(f.rate21to35)+' '+esc((f.rate21to35.notes||[]).join(' '));
    if(f.buildArea)$('buildAreaRef').textContent='参考:愛知県の平均は '+f.buildArea.value+'㎡(約'+toTsubo(f.buildArea.value).toFixed(1)+'坪。2階建てもまざった平均。'+String(f.buildArea.asOf||'').replace(/[(（].*$/,'')+')';
  }

  $('others').innerHTML=othersHtml();
  document.addEventListener('input',render);
  document.addEventListener('change',render);
  $('clear').addEventListener('click',function(){
    Array.prototype.forEach.call(document.querySelectorAll('.panel input[type="text"]'),function(el){el.value=''});
    Array.prototype.forEach.call(document.querySelectorAll('input[name="landMode"]'),function(el){el.checked=false});
    Array.prototype.forEach.call(document.querySelectorAll('.oitem input[value="unknown"]'),function(el){el.checked=true});
    $('ifRate').value=0;$('ifBuild').value=0;$('years').value=35;
    if(SUJI){$('buildUnit').value=SUJI.buildUnit.value;$('rate').value=SUJI.rate21to35.value}
    render();$('panel').scrollTop=0;
  });
  render();
  fetch('data/fudosan-suji.json',{cache:'no-cache'}).then(function(r){if(!r.ok)throw 0;return r.json()}).catch(function(){return null}).then(function(d){applySuji(d);render()});
})(typeof window!=='undefined'?window:globalThis);
