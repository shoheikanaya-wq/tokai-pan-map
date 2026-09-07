from pathlib import Path
import re

p=Path('index.html')
s=p.read_text(encoding='utf-8')

helper="""function syncViewHistory(view,extra={}){
  const state={view,...extra};
  if(history.state?.view===view){
    history.replaceState(state,'');
  }else{
    history.pushState(state,'');
  }
}
function showHomeView(){
  ranking.classList.add('hidden');
  detail.classList.add('hidden');
  home.classList.remove('hidden');
}
function showRankingView(){
  home.classList.add('hidden');
  detail.classList.add('hidden');
  ranking.classList.remove('hidden');
}
function showDetailView(){
  home.classList.add('hidden');
  ranking.classList.add('hidden');
  detail.classList.remove('hidden');
}
"""
anchor='const home=document.querySelector'
if helper not in s:
    pos=s.index(anchor)
    s=s[:pos]+helper+s[pos:]

s=s.replace("back2.onclick = showRanking;\nbackDetailBottom.onclick = showRanking;", "back2.onclick = () => history.back();\nbackDetailBottom.onclick = () => history.back();")
s=s.replace("back.onclick = returnHomeFromRanking;\nbackBottom.onclick = returnHomeFromRanking;", "back.onclick = () => history.back();\nbackBottom.onclick = () => history.back();")

old_app="""appTitle.onclick = () => {
  ranking.classList.add('hidden');
  detail.classList.add('hidden');
  home.classList.remove('hidden');
};"""
if old_app in s:
    s=s.replace(old_app,"appTitle.onclick = () => { showHomeView(); history.replaceState({view:'home'},''); };",1)

old_detail="""  ranking.classList.add('hidden');
  detail.classList.remove('hidden');"""
if old_detail in s:
    s=s.replace(old_detail,"  showDetailView();\n  syncViewHistory('detail',{city:currentCity,index:i});",1)

# hook ranking navigation after ranking becomes visible in showRanking
marker="ranking.classList.remove('hidden');"
first=s.find(marker)
if first!=-1:
    s=s[:first]+marker+s[first+len(marker):]
# Add popstate handler near end if absent
pop="""
window.addEventListener('popstate',e=>{
  const view=e.state?.view||'home';
  if(view==='detail') showDetailView();
  else if(view==='ranking') showRankingView();
  else showHomeView();
});
if(!history.state?.view) history.replaceState({view:'home'},'');
"""
if pop not in s:
    s=s.replace('</script>',pop+'\n</script>',1)

# Add history push in showRanking when called from city selection, conservatively after title assignment if exact pattern exists
rank_pattern="ranking.classList.remove('hidden');\n  detail.classList.add('hidden');"
if rank_pattern in s:
    s=s.replace(rank_pattern,"ranking.classList.remove('hidden');\n  detail.classList.add('hidden');\n  syncViewHistory('ranking',{city:currentCity});",1)

s=s.replace('Ver.1.12','Ver.1.13')
notice='Ver.1.13：スマホの戻る操作を改善。店舗詳細→TOP10→ホームの順でブラウザ／端末の戻る操作が自然に動くよう画面履歴を管理し、アプリ内の戻るボタンも同じ挙動に統一しました。店舗詳細は営業状態・電話・地図・公式サイト・口コミを確認しやすく、TOP10精度改善にも対応。岐阜県・三重県は今後対応予定です。'
s=re.sub(r'Ver\.1\.13：[^<]{20,900}',notice,s,count=1)
p.write_text(s,encoding='utf-8')

sw=Path('sw.js')
u=sw.read_text(encoding='utf-8')
u=re.sub(r"const CACHE_NAME = 'tokai-pan-v\d+';","const CACHE_NAME = 'tokai-pan-v12';",u,count=1)
sw.write_text(u,encoding='utf-8')
