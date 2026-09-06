import pubg, re, time, json
ids = json.load(open('prefix_ids.json'))
M = {'1909_Deston': 'b78ee504', '2119_Rondo': '1c577902', '2213_Rondo': 'a5559d48', '1950_Deston':'e17eebd5'}
for label, p8 in M.items():
    mid = ids[p8]
    rs = pubg.rosters(mid)
    print(f'===== {label} ({len(rs)} squads) =====')
    for r in rs:
        ms = r['members']
        # duo形队伍:前2存活>>后2 且含特殊名 或 含关键词
        flat = [m['name'] for m in ms]
        key_hit = any(re.search(r'7722|V[0O]V|ebebe|TOPM|MEOK|ttyOK', n, re.I) for n in flat)
        duo_shape = len(ms)==4 and ms[2]['surv']<250 and ms[0]['surv']>500
        if key_hit or duo_shape:
            print(f'  #{r["rank"]:>2}: ' + ' | '.join(f"{m['name']}(k{m['kills']},s{m['surv']},d{m['dmg']})" for m in ms))
    time.sleep(1)
