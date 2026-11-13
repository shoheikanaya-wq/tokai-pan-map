/* ぷらっと東海 メイン共通の画面(SA・PA 道の駅/温泉/ドライブ/絶景)
   各ページは window.PURATTO に設定を書いてから、このファイルを読み込む。 */
(function(){
  var C=window.PURATTO||{};
  var PREFS=['愛知県','岐阜県','三重県','静岡県'];
  var KINDS=C.kinds||null; // [['all','すべて'],['SA','SA'],...] または null
  var q=new URLSearchParams(location.search);
  var pref=PREFS.indexOf(q.get('pref'))>=0?q.get('pref'):'愛知県';
  var kindKeys=KINDS?KINDS.map(function(k){return k[0]}):['all'];
  var kind=kindKeys.indexOf(q.get('kind'))>=0?q.get('kind'):'all';
  var all=[],view=[],cur=-1,listTop=0;
  var $=function(id){return document.getElementById(id)};
  function esc(s){return String(s==null?'':s).replace(/[&<>"']/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]})}
  function safeUrl(u){return /^https:\/\//.test(u||'')?u:''}
  function kcls(x){return C.kindClass?C.kindClass(x):'tag'}
  function load(u){return fetch(u,{cache:'no-cache'}).then(function(r){if(!r.ok)throw 0;return r.json()}).catch(function(){return null})}

  document.title=C.title||document.title;
  $('title').textContent=(C.emoji?C.emoji+' ':'')+(C.title||'');
  if(!KINDS)$('kinds').style.display='none';

  Promise.all((C.sources||[]).map(function(s){return load(s.url)})).then(function(res){
    res.forEach(function(d,i){
      if(!d||!d.shops)return;
      var src=C.sources[i];
      d.shops.forEach(function(x){
        var p=x.pref||PREFS.filter(function(P){return (x.address||'').indexOf(P)===0})[0];
        if(!p)return;
        var y={};for(var k in x)y[k]=x[k];
        y.pref=p;y._note=d.attribution||'';
        if(src.kind)y.kind=src.kind;
        all.push(y);
      });
    });
    if(!all.length){$('panel').innerHTML='<p class="empty">データを読みこめませんでした。<br>時間をおいて開き直してください。</p>';return}
    render();
  });

  function setUrl(){try{history.replaceState(null,'','?pref='+encodeURIComponent(pref)+(kind!=='all'?'&kind='+kind:''))}catch(e){}}
  function tabs(){
    $('prefs').innerHTML=PREFS.map(function(p){
      var n=all.filter(function(x){return x.pref===p}).length;
      return '<button data-p="'+p+'"'+(p===pref?' class="on" aria-pressed="true"':'')+'>'+p.replace('県','')+' <small>'+n+'</small></button>'}).join('');
    if(KINDS)$('kinds').innerHTML=KINDS.map(function(k){return '<button data-k="'+k[0]+'"'+(k[0]===kind?' class="on" aria-pressed="true"':'')+'>'+k[1]+'</button>'}).join('');
  }
  function group(x){return C.group?C.group(x):(x.area||'')}
  function filtered(){
    var a=all.filter(function(x){return x.pref===pref&&(kind==='all'||kcls(x)===kind)});
    var order=C.groupOrder||function(){return 0};
    a.forEach(function(x,i){x._i=i});
    a.sort(function(x,y){return (order(x)-order(y))||(group(x)<group(y)?-1:group(x)>group(y)?1:x._i-y._i)});
    return a;
  }
  function render(){
    tabs();setUrl();view=filtered();cur=-1;$('pager').hidden=true;$('back').textContent='← もどる';
    if(!view.length){$('panel').innerHTML='<p class="empty">この県の'+esc(C.noun||'データ')+'は準備中です。<br>少しずつ増えていきます。</p>';return}
    var h='',g=null;
    view.forEach(function(x,i){
      var grp=group(x);
      if(grp!==g){h+='<h3 class="grp">'+esc((C.groupIcon?C.groupIcon(x):'📍')+' '+grp)+'</h3>';g=grp}
      var nm=x.direction?x.name.replace(/[((][^))]*[))]$/,''):x.name;
      h+='<button class="row" data-i="'+i+'">'+(x.kind?'<span class="k '+kcls(x)+'">'+esc(x.kind)+'</span>':'')+'<span class="nm">'+esc(nm)+'</span>'+
        (x.direction?'<span class="dir">'+esc(x.direction)+'</span>':'<small>'+esc(C.rowRight?C.rowRight(x):'')+'</small>')+'</button>';
    });
    $('panel').innerHTML=h;$('panel').scrollTop=listTop;listTop=0;
  }
  function show(i){
    if(cur<0)listTop=$('panel').scrollTop;
    cur=i;var x=view[i];if(!x)return;
    var map='https://www.google.com/maps/search/?api=1&query='+encodeURIComponent(x.name.replace(/[((].*?[))]/g,' ')+' '+(x.address||''));
    var web=safeUrl(x.website);
    var h='<div class="card"><div class="meta">'+(x.kind?'<span class="k '+kcls(x)+'">'+esc(x.kind)+'</span>':'')+
      (x.direction?'<span class="dir">'+esc(x.direction)+'</span>':'')+'<span class="area">'+esc(x.area)+'</span>'+
      (x.road?'<span class="road">'+esc(x.road)+'</span>':'')+'</div>'+
      '<h2>'+esc(x.name)+'</h2><div class="cat">'+esc(x.catchphrase)+'</div>'+
      '<div class="chips">'+(x.highlights||[]).map(function(t){return '<span>'+esc(t)+'</span>'}).join('')+'</div>'+
      (x.stops&&x.stops.length?'<ol class="stops">'+x.stops.map(function(t){return '<li>'+esc(t)+'</li>'}).join('')+'</ol>':'')+
      (x.openingHours&&x.openingHours.length?'<div class="hours">🕒 '+x.openingHours.map(esc).join('<br>')+'</div>':'')+
      '<div class="addr">📍 '+esc(x.address)+'</div><div class="spacer"></div>'+
      '<div class="btns"><a href="'+map+'" target="_blank" rel="noopener">🗺 地図で見る</a>'+(web?'<a class="sub" href="'+esc(web)+'" target="_blank" rel="noopener">くわしく</a>':'')+'</div>'+
      '<p class="note">'+esc(x._note)+'</p></div>';
    $('panel').innerHTML=h;$('panel').scrollTop=0;
    $('pager').hidden=false;$('pos').textContent=(i+1)+'/'+view.length;
    $('prev').disabled=i===0;$('next').disabled=i===view.length-1;
    $('back').textContent='← 一覧';
  }
  $('prefs').addEventListener('click',function(e){var b=e.target.closest('button');if(b){pref=b.dataset.p;render()}});
  $('kinds').addEventListener('click',function(e){var b=e.target.closest('button');if(b){kind=b.dataset.k;render()}});
  $('panel').addEventListener('click',function(e){var b=e.target.closest('.row');if(b)show(+b.dataset.i)});
  $('prev').onclick=function(){show(cur-1)};$('next').onclick=function(){show(cur+1)};
  $('back').addEventListener('click',function(e){if(cur>=0){e.preventDefault();render()}});
})();
