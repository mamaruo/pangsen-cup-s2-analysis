import pubg, json, time
# 批量搜名字变体(每次一个请求,间隔1.5s)
groups = {
 'TOPM249': ['TOPM249-___-','TOPM249-___','TOPM249-__-','TOPM249-_-','TOPM249--'],
 'MICKEY':  ['MICKEYMOUSEOK666','MICKEYMOUSE0K666','MickeyMouseOK666'],
 'KITTY':   ['HelloKittyOK666','HelloKitty0K666','hellokittyok666'],
 'OV0V':    ['OV0V000V','0V0V000V','OV0VOOOV','0V0VOOOV','OV0V00OV'],
 'BEBE':    ['7bebebe_','7bebebe','7bebebe-'],
}
found = {}
for key, names in groups.items():
    try:
        q = pubg.urllib.parse.quote(','.join(names))
        d = pubg._get(f'{pubg.BASE}/shards/steam/players?filter[playerNames]={q}')
        for p in d['data']:
            print(key, 'FOUND:', p['id'], repr(p['attributes']['name']))
            found[p['attributes']['name']] = p['id']
    except Exception as e:
        print(key, 'none of', names)
    time.sleep(1.5)
json.dump(found, open('cand_accounts.json','w'))
print('--- matches of found ---')
for n, aid in found.items():
    print(f'--- {n} ---')
    try:
        for mid in pubg.player_matches(aid):
            meta = pubg.match_meta(mid)
            if meta['created'] >= '2026-09-02T10:00':
                print('  ', meta['created'], meta['map'], mid)
            time.sleep(1.2)
    except Exception as e:
        print('   ERR', e)
        time.sleep(3)
