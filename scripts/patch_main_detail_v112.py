from pathlib import Path
import re

p=Path('index.html')
s=p.read_text(encoding='utf-8')

css="""
.detail-status{font-size:18px;font-weight:900;margin:2px 0 8px;line-height:1.25}
.detail-status.open{color:#246b35}.detail-status.closed{color:#9a3428}.detail-status.unknown{color:#6b6258}
.detail-phone-link{display:inline-flex;align-items:center;gap:6px;min-height:38px;padding:6px 10px;border:1px solid #b98a55;border-radius:9px;background:#ead3ad;color:#332316;text-decoration:none;font-weight:800}
@media(max-width:600px){.detail-status{font-size:16px}.detail-phone-link{min-height:40px;font-size:13px}}
"""
if css not in s:
    s=s.replace('</style>',css+'</style>',1)

old="""if (s.openNow === true) {
  dopening.innerHTML = '<strong>🟢 現在営業中</strong><br>';
} else if (s.openNow === false) {
  dopening.innerHTML = '<strong>🔴 営業時間外</strong><br>';
} else {
  dopening.innerHTML = '<strong>⚪ 営業状況不明</strong><br>';
}

  if (s.openingHours && s.openingHours.length) {
    dopening.innerHTML +=
      '<strong>営業時間</strong><br>' +
      s.openingHours.join('<br>');
  } else {
   dopening.innerHTML += '営業時間：情報なし';
  }

  // 電話番号
  dphone.textContent =
    s.phone ? `☎ ${s.phone}` : '電話番号：情報なし';
"""
new="""if (s.openNow === true) {
  dopening.innerHTML = '<div class=\"detail-status open\">🟢 現在営業中</div>';
} else if (s.openNow === false) {
  dopening.innerHTML = '<div class=\"detail-status closed\">🔴 現在は営業時間外</div>';
} else {
  dopening.innerHTML = '<div class=\"detail-status unknown\">⚪ 現在の営業状況は要確認</div>';
}

  if (s.openingHours && s.openingHours.length) {
    dopening.innerHTML += '<strong>営業時間</strong><br>' + s.openingHours.join('<br>');
  } else {
    dopening.innerHTML += '<strong>営業時間</strong><br>情報なし';
  }

  // 電話番号：スマホではワンタップ発信
  if(s.phone){
    const tel=String(s.phone).replace(/[^0-9+]/g,'');
    dphone.innerHTML=`<a class=\"detail-phone-link\" href=\"tel:${tel}\">☎ ${s.phone} に電話</a>`;
  }else{
    dphone.textContent='電話番号：情報なし';
  }
"""
if old not in s:
    raise SystemExit('detail hours/phone block not found')
s=s.replace(old,new,1)

s=s.replace('Ver.1.11','Ver.1.12')
notice='Ver.1.12：店舗詳細を実用化。現在営業中・営業時間外・要確認を大きく表示し、電話番号がある店舗はワンタップで発信できます。地図・公式サイト・口コミ・営業時間を店へ行く前に確認しやすい構成へ整理。TOP10は市町村一致、非パン屋除外、口コミ信頼度補正にも対応。岐阜県・三重県は今後対応予定です。'
s=re.sub(r'Ver\.1\.12：[^<]{20,900}',notice,s,count=1)
p.write_text(s,encoding='utf-8')

sw=Path('sw.js')
u=sw.read_text(encoding='utf-8')
u=re.sub(r"const CACHE_NAME = 'tokai-pan-v\d+';","const CACHE_NAME = 'tokai-pan-v11';",u,count=1)
sw.write_text(u,encoding='utf-8')
