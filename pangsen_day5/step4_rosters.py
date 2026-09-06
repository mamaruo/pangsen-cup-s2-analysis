import pubg, json, time
ids = json.load(open('prefix_ids.json'))
M = {
 '1909_Deston': 'b78ee504',
 '1919_Deston': '510d960a',
 '1950_Deston': 'e17eebd5',
 '2013_Deston': '9742a9b3',
 '2023_Taego':   '286b37d5',
 '2046_Rondo':   '997ef53e',
 '2119_Rondo':   '1c577902',
 '2213_Rondo':   'a5559d48',
 '2242_Deston': 'f08ed8d1',
 '2259_Rondo':   '9269da01',
}
cand = ['TOPM249','MICKEYMOUSEOK','HelloKittyOK','January_BiG','3Bbuff','DayDayOuO','Aixinzuimei','WanM87342','III7722','7bebebe','OV0V','0V0V','lunlun','IAMPETE']
out = {}
for label, p8 in M.items():
    mid = ids[p8]
    meta = pubg.match_meta(mid)
    rs = pubg.rosters(mid)
    out[label] = mid
    print(f'===== {label} {meta["created"]} {meta["map"]} squads={len(rs)} =====')
    for r in rs:
        names = [m['name'] for m in r['members']]
        if any(any(c in n for c in cand) for n in names):
            ms = ' | '.join(f"{m['name']}(k{m['kills']},s{m['surv']},d{m['dmg']})" for m in r['members'])
            print(f'  #{r["rank"]:>2}: {ms}')
    time.sleep(1.0)
json.dump(out, open('day5_matches.json','w'), ensure_ascii=False, indent=1)
