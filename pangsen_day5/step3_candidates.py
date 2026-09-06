import pubg, json, time
cands = ['OV0V000V','MICKEYMOUSE0K666','7bebebe_','January_BiG','HelloKitty0K666']
found = {}
for n in cands:
    res = pubg.search_player(n)
    print(n, '->', res)
    if res:
        found[n] = res[0][0]
        time.sleep(1)
json.dump(found, open('cand_accounts.json','w'))
for n, aid in found.items():
    print(f'--- {n} ---')
    for mid in pubg.player_matches(aid):
        meta = pubg.match_meta(mid)
        if meta['created'] >= '2026-09-02T10:00':
            print('  ', meta['created'], meta['map'], mid)
        time.sleep(0.5)
