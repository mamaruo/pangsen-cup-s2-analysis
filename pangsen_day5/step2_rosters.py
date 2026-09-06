import pubg
matches = {
 'R1_1847_Neon': '49f936bc-ad2e-4e27-8957-ec6c478e2de4',
 'R2_1919_Baltic': '510d960a-f0b7-4790-a4f9-67187e336235',
 'R3_2023_Tiger': '286b37d5-734d-4905-a6b7-d8c2c9bd7d95',
 'R4_2242_Baltic': 'f08ed8d1-6b83-4d5a-8311-013785ed310a',
 'R5_2259_Neon': '9269da01-09e3-4b15-a414-05d6569a6e32',
}
known = {'3Bbuff','DayDayOuO','Aixinzuimei','WanM87342'}
cand = ['OV0V000V','MICKEYMOUSE0K666','7bebebe_','January_BiG','HelloKitty0K666','TOPM249','III7722II','3Bbuff','DayDayOuO']
for label, mid in matches.items():
    meta = pubg.match_meta(mid)
    rs = pubg.rosters(mid)
    print(f'===== {label} {mid[:8]} {meta["created"]} {meta["map"]} squads={len(rs)} =====')
    for r in rs:
        names = [m['name'] for m in r['members']]
        hit = any(any(c in n for c in cand) or n in known for n in names)
        if hit:
            ms = ' | '.join(f"{m['name']}(k{m['kills']},s{m['surv']})" for m in r['members'])
            print(f'  #{r["rank"]:>2}: {ms}')
