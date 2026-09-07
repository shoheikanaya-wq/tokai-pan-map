from pathlib import Path

p=Path('panrush.html')
s=p.read_text(encoding='utf-8')

s=s.replace(
'''<option value="nishi">西三河耐久｜目標25店</option><option value="mikawa">三河縦断｜目標35店</option><option value="aichi">愛知横断｜目標50店</option>''',
'''<option value="nishi">西三河耐久｜目標25店</option><option value="mikawa">三河縦断｜目標35店</option><option value="aichi">愛知横断｜目標50店</option><option value="gifu">岐阜縦断｜目標40店</option><option value="mie">三重縦断｜目標35店</option><option value="tokai">東海三県制覇｜目標60店</option>''',1)

old="""const SETS={nishi:{name:'西三河耐久',goal:25,cities:['豊田市','岡崎市','安城市','刈谷市','西尾市','碧南市','知立市','みよし市','幸田町']},mikawa:{name:'三河縦断',goal:35,cities:['豊田市','岡崎市','安城市','刈谷市','西尾市','豊橋市','豊川市','蒲郡市','新城市','田原市']},aichi:{name:'愛知横断',goal:50,cities:['豊田市','岡崎市','安城市','刈谷市','西尾市','豊橋市','豊川市','名古屋市','一宮市','春日井市','長久手市','日進市','半田市','常滑市','大府市']}};"""
new="""const SETS={nishi:{name:'西三河耐久',goal:25,cities:['豊田市','岡崎市','安城市','刈谷市','西尾市','碧南市','知立市','みよし市','幸田町']},mikawa:{name:'三河縦断',goal:35,cities:['豊田市','岡崎市','安城市','刈谷市','西尾市','豊橋市','豊川市','蒲郡市','新城市','田原市']},aichi:{name:'愛知横断',goal:50,cities:['豊田市','岡崎市','安城市','刈谷市','西尾市','豊橋市','豊川市','名古屋市','一宮市','春日井市','長久手市','日進市','半田市','常滑市','大府市']},gifu:{name:'岐阜縦断',goal:40,cities:['岐阜市','大垣市','各務原市','関市','美濃加茂市','多治見市','中津川市','郡上市','下呂市','高山市']},mie:{name:'三重縦断',goal:35,cities:['桑名市','四日市市','鈴鹿市','亀山市','津市','松阪市','伊勢市','鳥羽市','志摩市','尾鷲市','熊野市']},tokai:{name:'東海三県制覇',goal:60,cities:['名古屋市','豊田市','岡崎市','豊橋市','一宮市','岐阜市','大垣市','多治見市','高山市','桑名市','四日市市','鈴鹿市','津市','松阪市','伊勢市']}};"""
if old not in s: raise SystemExit('SETS anchor not found')
s=s.replace(old,new,1)
s=s.replace('東海パンMAP｜24時間耐久・上級者向けチャレンジ','東海パンMAP｜愛知・岐阜・三重 24時間耐久チャレンジ',1)
p.write_text(s,encoding='utf-8')

idx=Path('index.html')
i=idx.read_text(encoding='utf-8')
i=i.replace('<span class="rush-icon">⚡</span><span><strong>パンラッシュ</strong><small>愛知県全域・24時間耐久</small></span>','<span class="rush-icon">⚡</span><span><strong>パンラッシュ</strong><small>東海三県・24時間耐久</small></span>',1)
i=i.replace('panrush.html?v=20260907-3','panrush.html?v=20260907-4',1)
i=i.replace('<div>Ver.1.22</div>：三重県の亀山市漏れを修正し29市町すべてに対応。さらに愛知・岐阜・三重を横断した「東海三県TOP10」を追加しました。','<div>Ver.1.23</div>：パンラッシュを東海三県対応へ拡張。岐阜縦断・三重縦断・東海三県制覇の24時間耐久コースを追加しました。三重県29市町、岐阜県42市町村、愛知県全域と東海三県TOP10に対応しています。',1)
i=i.replace('<div>Ver.1.22</div>\n  <div>Personal Bakery Discovery Project</div>','<div>Ver.1.23</div>\n  <div>Personal Bakery Discovery Project</div>',1)
idx.write_text(i,encoding='utf-8')

sw=Path('sw.js')
u=sw.read_text(encoding='utf-8')
import re
u=re.sub(r"const CACHE_NAME = 'tokai-pan-v\d+';","const CACHE_NAME = 'tokai-pan-v22';",u,count=1)
sw.write_text(u,encoding='utf-8')
