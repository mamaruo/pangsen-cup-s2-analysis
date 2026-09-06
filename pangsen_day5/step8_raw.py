import pubg, json
ids = json.load(open('prefix_ids.json'))
for label, p8 in [('小虎东东R2','a5559d48'), ('兮涵豆子R2','a3f7dcd7')]:
    mid = ids[p8]
    tel = pubg.telemetry(mid)
    p2 = pubg.phase2_time(mid)
    print(f'===== {label} {mid} phase2={p2} =====')
    for e in tel:
        if e['_T'] == 'LogPlayerKillV2':
            k = (e.get('killer') or {}).get('name')
            if k in ('January_BiG','7Bebebe_','III7722II','OVOVOOOV'):
                v = (e.get('victim') or {}).get('name')
                kdi = e.get('killerDamageInfo') or {}
                print(f"  {e['_D'][11:23]} {k} -> {v!r} [{kdi.get('damageCauserName')}] {'P1' if e['_D']<p2 else 'P2'}")
