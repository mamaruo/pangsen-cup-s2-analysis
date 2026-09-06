import pubg, json, time, itertools
found = {}
# III7722II: 6个 bar 位 (3前2后) -> I/l;  拆成两批
bars = [''.join(c) for c in itertools.product('Il', repeat=6)]
names7722 = [b[:3]+'7722'+b[3:] for b in bars]
# OV0V000V: 位1,3,5,6,7 -> O/0
namesOV = [''.join(c) for c in itertools.product('O0', repeat=5)]
namesOV = [n[0]+'V'+n[1]+'V'+n[2]+n[3]+n[4]+'V' for n in namesOV]
def batch_search(names, tag):
    for i in range(0, len(names), 30):
        chunk = names[i:i+30]
        try:
            q = pubg.urllib.parse.quote(','.join(chunk))
            d = pubg._get(f'{pubg.BASE}/shards/steam/players?filter[playerNames]={q}')
            for p in d['data']:
                print(tag, 'FOUND:', p['id'], repr(p['attributes']['name']))
                found[p['attributes']['name']] = p['id']
        except Exception as e:
            print(tag, 'batch err', str(e)[:80])
        time.sleep(1.5)
batch_search(names7722, '7722')
batch_search(namesOV, 'OV')
json.dump(found, open('brute_found.json','w'), ensure_ascii=False)
print('total found:', found)
