import pubg, json, time, itertools
# 1) OVOVOOOV 的 9月2日对局
print('--- OVOVOOOV matches ---')
for mid in pubg.player_matches('account.0948de9e482b4d65abd9362281a04f3e'):
    meta = pubg.match_meta(mid)
    if meta['created'] >= '2026-09-02T10:00':
        print('  ', meta['created'], meta['map'], mid)
    time.sleep(1.2)
# 2) III7722II: 5 个 bar 位
found = json.load(open('brute_found.json'))
bars = [''.join(c) for c in itertools.product('Il', repeat=5)]
names = [b[:3]+'7722'+b[3:] for b in bars]
for i in range(0, len(names), 30):
    chunk = names[i:i+30]
    try:
        q = pubg.urllib.parse.quote(','.join(chunk))
        d = pubg._get(f'{pubg.BASE}/shards/steam/players?filter[playerNames]={q}')
        for p in d['data']:
            print('7722 FOUND:', p['id'], repr(p['attributes']['name']))
            found[p['attributes']['name']] = p['id']
    except Exception as e:
        print('7722 batch err', str(e)[:60])
    time.sleep(1.5)
json.dump(found, open('brute_found.json','w'), ensure_ascii=False)
