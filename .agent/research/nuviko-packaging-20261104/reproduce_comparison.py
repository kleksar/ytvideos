import csv,json,statistics as st,datetime as dt,collections,pathlib,math
D=pathlib.Path('.agent/research/nuviko-packaging-20261104')
qs=collections.defaultdict(list)
for i,c,q in json.loads((D/'discovery.json').read_text()):qs[i].append(q)
rows=list(csv.DictReader((D/'catalog.csv').open())); g=collections.defaultdict(list)
for r in rows:
 r['views']=int(r['views']);r['seconds']=int(r['seconds']);r['day']=dt.date.fromisoformat(r['date'])
 g[r['channel_id']].append(r)
latest=set(json.loads((D/'latest_ids.json').read_text()));now=dt.date(2026,11,4); rank=[]
for rr in g.values():
 pool=[p for p in rr if p['id'] in latest]
 for r in rr:
  if r['id'] not in qs or not 181<=r['seconds']<=5400 or (now-r['day']).days<30 or (r['lang'] and not r['lang'].startswith('en')):continue
  peers=sorted((p for p in pool if p!=r and 181<=p['seconds'] and .5<=p['seconds']/r['seconds']<=2 and abs((p['day']-r['day']).days)<=365 and (now-p['day']).days>=30 and .5<=(now-p['day']).days/(now-r['day']).days<=2 and p['views']>0),key=lambda p:abs((p['day']-r['day']).days))[:10]
  if len(peers)<5:continue
  med=st.median(p['views'] for p in peers)
  rank.append(dict(id=r['id'],channel=r['channel'],title=r['title'],date=r['date'],seconds=r['seconds'],views=r['views'],ratio=round(r['views']/med,2),median=med,n=len(peers),peers=' '.join(p['id'] for p in peers),query=qs[r['id']][0],url=r['url'],thumbnail=r['thumbnail']))
rank.sort(key=lambda r:-r['ratio'])
with (D/'compared.csv').open('w') as f:w=csv.DictWriter(f,rank[0]);w.writeheader();w.writerows(rank)
print('total',len(rows),'channels',len(g),'candidate',len(rank),'over3',sum(r['ratio']>=3 for r in rank))
for i,r in enumerate(rank[:50]):print(i,r['id'],r['views'],r['ratio'],r['channel'],r['title'])
print('DIRECT',[(r['id'],r['title'],r['views']) for r in sorted(rows,key=lambda r:-r['views']) if any('Fawkes' in q or 'Bonfire' in q for q in qs[r['id']])][:15])
