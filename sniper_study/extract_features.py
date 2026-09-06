"""从85场杯赛对局遥测中提取紧凑行为特征, 输出 features/<mid>.json"""
import json, os, glob, datetime

CUP_ACCS = {'account.158c0f6400524a58a89cb18f2dc3052b','account.c416e2e00b254f57aa9ac5e8b46c8ef6',
 'account.cc40bc9ec02e412b8638b1a20ca35764','account.f067d098170b4ddaa65ba8fb306b3d68',
 'account.daa1fc4c60ca4aa082584a0a048839f4','account.eb9b15d4b5a4464f9c9466fb9d260a54',
 'account.52c29debeab645279f5d3ab4d065291d','account.453be1368e3e4e0e8e60af60a8a7a3c1',
 'account.a7d05690ea23400498ae0e325f290f15','account.1b8cb332342046a9990a3be67869acf2',
 'account.3fd2f9c4ef7a45aaa96fc73f854b0caa','account.0948de9e482b4d65abd9362281a04f3e',
 'account.60e729fc9ed741ee92b3d7fd4c88f9ba','account.0a851679df5b4d91b4b831aa4dbfa302'}

def find_tel(mid):
    for c in ['pangsen_day5/cache','pangsen_day4/cache','pangsen_day3/cache']:
        p = f'{c}/tel_{mid}.json'
        if os.path.exists(p): return p

def parse_ts(s):
    return datetime.datetime.fromisoformat(s.replace('Z','+00:00'))

def main():
    mids = open('cup_match_ids.txt').read().split()
    os.makedirs('features', exist_ok=True)
    for mid in mids:
        outp = f'features/{mid}.json'
        if os.path.exists(outp): continue
        tel = json.load(open(find_tel(mid), encoding='utf-8'))
        t0 = min(parse_ts(e['_D']) for e in tel)
        end_ev = [e for e in tel if e['_T'] == 'LogMatchEnd']
        end = parse_ts(end_ev[0]['_D']) if end_ev else parse_ts(tel[-1]['_D'])
        chars = {}   # acc -> info
        def get(acc, name=None, team=None):
            if acc not in chars:
                chars[acc] = {'acc': acc, 'name': name, 'team': team, 'isCup': acc in CUP_ACCS,
                              'lastT': None, 'deathT': None, 'groggyT': None, 'killer': None,
                              'deathType': None, 'kills': [], 'rpg': 0, 'track': [],
                              'landT': None, 'landPos': None, 'firstPos': None,
                              'firstCombatT': None, 'firstShotT': None}
            if name: chars[acc]['name'] = name
            if team: chars[acc]['team'] = team
            return chars[acc]

        for e in tel:
            t = (parse_ts(e['_D']) - t0).total_seconds()
            tt = e['_T']
            if tt == 'LogPlayerPosition':
                c = e['character']; veh = e.get('vehicle') or {}
                ch = get(c['accountId'], c.get('name'), veh.get('teamId') or c.get('teamId'))
                loc = c['location']
                ch['track'].append((round(t,1), round(loc['x'],1), round(loc['y'],1), round(loc['z'],1)))
            elif tt in ('LogPlayerKillV2', 'LogPlayerMakeGroggy'):
                v = e.get('victim', {})
                k = e.get('killer') or {}
                vc = get(v.get('accountId'), v.get('name'), v.get('teamId') if 'teamId' in v else None)
                kc = get(k.get('accountId'), k.get('name'), k.get('teamId') if 'teamId' in k else None) if k.get('accountId') else None
                w = (e.get('killerWeapon') or {}).get('itemId', '')
                if tt == 'LogPlayerKillV2':
                    vc['deathT'] = t; vc['killer'] = k.get('accountId'); vc['deathType'] = v.get('gameResultSpecific', None)
                    if kc:
                        di = e.get('finishDamageInfo') or e.get('killerDamageInfo') or {}
                        d = di.get('distance', 0)
                        w = di.get('damageCauserName', '')
                        kc['kills'].append({'victim': v.get('accountId'), 'vName': v.get('name'),
                                            'vCup': v.get('accountId') in CUP_ACCS, 't': round(t,1), 'weapon': w, 'dist': round(d,1)})
                else:
                    if vc['groggyT'] is None: vc['groggyT'] = t
            elif tt in ('LogPlayerTakeDamage', 'LogPlayerAttack'):
                if tt == 'LogPlayerTakeDamage':
                    v = e.get('victim') or {}; k = e.get('attacker') or {}
                    for sa in (v.get('accountId'), k.get('accountId')):
                        if sa:
                            ch2 = chars.get(sa)
                            if ch2 is not None and ch2['firstCombatT'] is None:
                                ch2['firstCombatT'] = t
                else:
                    c2 = e.get('attacker') or {}
                    if c2.get('accountId'):
                        ch2 = chars.get(c2['accountId'])
                        if ch2 is not None and ch2.get('firstShotT') is None:
                            ch2['firstShotT'] = t
            elif tt == 'LogItemPickup':
                c = e.get('character') or {}
                if not c.get('accountId'): continue
                ch = get(c['accountId'], c.get('name'))
                iid = (e.get('item') or {}).get('itemId', '')
                if 'PANZERFAUST' in iid.upper(): ch['rpg'] += 1
                elif 'MORTAR' in iid.upper() and 'Ammo' not in iid: ch['mortar'] = ch.get('mortar', 0) + 1
        # lastT from track tail + land detection
        import math
        for ch in chars.values():
            tr = ch['track']
            if tr:
                ch['lastT'] = tr[-1][0]
                ch['firstPos'] = tr[0][1:]
                # skip lobby (early static cluster) & plane: start after last fast/airborne point
                def spd(p, q): return math.hypot(q[1]-p[1], q[2]-p[2]) / max(q[0]-p[0], 1e-9)
                plane_end = 0
                for i in range(len(tr)):
                    if tr[i][3] > 30000:  # 300m 以上只可能是飞机/伞降(载具不会)
                        plane_end = i
                # landing: first point after plane_end with z<200m and next 2 points slow
                for i in range(plane_end, len(tr)-2):
                    if tr[i][3] < 20000 and spd(tr[i], tr[i+1]) < 800 and spd(tr[i+1], tr[i+2]) < 800:  # 8 m/s (cm/s)
                        ch['landT'], ch['landPos'] = tr[i][0], tr[i][1:]
                        break
                if ch['landT'] is None and plane_end < len(tr) - 2:
                    i = plane_end
                    if all(spd(tr[j], tr[j+1]) < 800 for j in range(i, min(i+2, len(tr)-1))):
                        ch['landT'], ch['landPos'] = tr[i][0], tr[i][1:]
                # air quit: left the match while airborne (after plane phase, z>300m, no death)
                if ch['deathT'] is None and plane_end < len(tr)-1 and tr[-1][3] > 30000:
                    ch['airQuit'] = True
            if ch['deathType'] is None and ch['deathT'] is not None:
                ch['deathType'] = 'killed'
        out = {'mid': mid, 't0': tel[0]['_D'], 'endT': round((end - t0).total_seconds(),1)}
        keep = set(chars)  # 全员轨迹: 追击分析需要普通玩家对照
        slim = {}
        for a, c in chars.items():
            d = {k: v for k, v in c.items() if k != 'track'}
            if a in keep: d['track'] = c['track']
            slim[a] = d
        out['chars'] = slim
        json.dump(out, open(outp, 'w', encoding='utf-8'))
        print(mid, len(chars), 'chars, endT', out['endT'], flush=True)

if __name__ == '__main__':
    main()
