import json, urllib.request, urllib.error, sys
API='https://tokai-pan-api-873562719766.asia-northeast1.run.app'
CASES=[
 ('愛知県','名古屋市'),('愛知県','豊田市'),('愛知県','豊根村'),
 ('岐阜県','岐阜市'),('岐阜県','高山市'),('岐阜県','東白川村'),
 ('三重県','四日市市'),('三重県','亀山市'),('三重県','紀宝町'),
]
rows=[]
for pref,city in CASES:
    body=json.dumps({'textQuery':f'パン屋 {pref}{city}'}).encode()
    req=urllib.request.Request(API,data=body,headers={'Content-Type':'application/json'},method='POST')
    try:
        with urllib.request.urlopen(req,timeout=30) as r:
            data=json.load(r)
        places=data.get('places',[])
        in_area=[p for p in places if pref in str(p.get('formattedAddress','')) and city in str(p.get('formattedAddress',''))]
        bakery=[p for p in in_area if 'bakery' in (p.get('types') or [])]
        rows.append({'prefecture':pref,'city':city,'http':200,'raw':len(places),'in_area':len(in_area),'bakery':len(bakery),'ok':len(bakery)>0})
    except urllib.error.HTTPError as e:
        rows.append({'prefecture':pref,'city':city,'http':e.code,'raw':0,'in_area':0,'bakery':0,'ok':False})
    except Exception as e:
        rows.append({'prefecture':pref,'city':city,'http':'ERR','raw':0,'in_area':0,'bakery':0,'ok':False,'error':str(e)})
print(json.dumps(rows,ensure_ascii=False,indent=2))
failed=[r for r in rows if not r['ok']]
print('\nSUMMARY',len(rows)-len(failed),'/',len(rows),'OK')
if failed:
    print('ATTENTION:', ', '.join(r['prefecture']+r['city'] for r in failed))
