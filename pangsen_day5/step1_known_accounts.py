import pubg, json, datetime
known = {'3Bbuff': None, 'DayDayOuO': None, 'Aixinzuimei': None, 'WanM87342': None}
for name in known:
    res = pubg.search_player(name)
    print(name, '->', res)
    if res:
        known[name] = res[0][0]
json.dump(known, open('known_accounts.json', 'w'))
for name, aid in known.items():
    if not aid: continue
    print(f'--- {name} ({aid}) ---')
    for mid in pubg.player_matches(aid):
        meta = pubg.match_meta(mid)
        if meta['created'] >= '2026-09-02':  # Sept 2 only
            print('  ', meta['created'], meta['map'], mid)
