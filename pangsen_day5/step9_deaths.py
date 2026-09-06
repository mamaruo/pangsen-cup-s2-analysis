import pubg, json
ids = json.load(open('prefix_ids.json'))
for label, p8, names in [
  ('大能爱国R1','e17eebd5',['TOPM249-___-','dsdwfnygsaew']),
  ('大能爱国R2','1c577902',['TOPM249-___-','dsdwfnygsaew']),
]:
    mid = ids[p8]
    tel = pubg.telemetry(mid)
    print(f'===== {label} =====')
    for e in tel:
        if e['_T']=='LogPlayerKillV2' and (e.get('victim') or {}).get('name') in names:
            k = e.get('killer') or {}
            kdi = e.get('killerDamageInfo') or {}
            vr = (e.get('victimGameResult') or {})
            print(f"  {e['_D'][11:23]} victim={e['victim']['name']} killer={k.get('name')} weapon={kdi.get('damageCauserName')} reason={kdi.get('damageReason')}")
    # 双方死亡前后 5 秒的所有事件类型
    for e in tel:
        if e['_T']=='LogPlayerKillV2' and (e.get('victim') or {}).get('name') in names:
            pass
