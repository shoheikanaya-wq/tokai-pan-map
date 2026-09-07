from pathlib import Path
import re

p=Path('index.html')
s=p.read_text(encoding='utf-8')

css="""
.load-error{margin:10px 0;padding:12px;border:1px solid #c77d67;border-radius:12px;background:#fff4ef;color:#6d2f23;font-size:13px;line-height:1.45}
.load-error button{margin-top:8px;min-height:40px}
"""
if css not in s:
    s=s.replace('</style>',css+'</style>',1)

helper="""function showLoadError(message,retry){
  const box=document.createElement('div');
  box.className='load-error';
  const text=document.createElement('div');
  text.textContent=message;
  const btn=document.createElement('button');
  btn.type='button';
  btn.textContent='もう一度試す';
  btn.onclick=()=>{ box.remove(); retry?.(); };
  box.append(text,btn);
  const host=!home.classList.contains('hidden')?home:(!ranking.classList.contains('hidden')?ranking:detail);
  host.prepend(box);
}
"""
anchor='async function loadBakeries'
if helper not in s:
    pos=s.index(anchor)
    s=s[:pos]+helper+s[pos:]

# Replace municipality alert with retryable UI
s=s.replace("alert('パン屋情報の取得に失敗しました：' + e.message);", "showLoadError('パン屋情報の取得に失敗しました。通信状態を確認して再試行してください。',()=>button.click());")
s=s.replace("alert('西三河ランキングの取得に失敗しました：'+e.message);", "showLoadError('西三河ランキングを取得できませんでした。',()=>nishimikawa.click());")
s=s.replace("alert('東三河ランキングの取得に失敗しました：'+e.message);", "showLoadError('東三河ランキングを取得できませんでした。',()=>higashimikawa.click());")
s=s.replace("alert('愛知県ランキングの取得に失敗しました：' + e.message);", "showLoadError('愛知県ランキングを取得できませんでした。',()=>aichi.click());")

s=s.replace('Ver.1.13','Ver.1.14')
notice='Ver.1.14：第三者配布前の通信耐性を改善。TOP10取得に失敗した場合は画面内にエラーと「もう一度試す」を表示し、通信回復後にその場で再取得できます。スマホ戻る操作、店舗詳細、TOP10候補精度、口コミ信頼度補正にも対応。岐阜県・三重県は今後対応予定です。'
s=re.sub(r'Ver\.1\.14：[^<]{20,900}',notice,s,count=1)
p.write_text(s,encoding='utf-8')

sw=Path('sw.js')
u=sw.read_text(encoding='utf-8')
u=re.sub(r"const CACHE_NAME = 'tokai-pan-v\d+';","const CACHE_NAME = 'tokai-pan-v13';",u,count=1)
sw.write_text(u,encoding='utf-8')
