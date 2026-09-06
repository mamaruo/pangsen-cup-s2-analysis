import pubg, json
mid = 'a3f7dcd7-f96e-4fd3-a457-71b3ac9e8634'
tel = pubg.telemetry(mid)
p2 = pubg.phase2_time(mid)
print('phase2 =', p2)
for e in tel:
    if e['_T'] == 'LogPlayerKillV2':
        k = (e.get('killer') or {}).get('name')
        if k in ('III7722II','OVOVOOOV'):
            v = (e.get('victim') or {}).get('name')
            kdi = e.get('killerDamageInfo') or {}
            print(f"  {e['_D'][11:23]} {k} -> {v!r} [{kdi.get('damageCauserName')}] {'P1' if e['_D']<p2 else 'P2'}")
rs = pubg.rosters(mid)
for r in rs:
    if any(m['name'] in ('III7722II','OVOVOOOV') for m in r['members']):
        print('squad rank', r['rank'], [(m['name'], m['kills'], m['surv']) for m in r['members']])
