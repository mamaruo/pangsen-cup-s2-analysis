"""可疑对局前后局异常匹配分析:
对22个涉案嫌疑人, 在其可疑对局 createdAt±6h 窗口内建时间线, 标记:
  A 等待空档: 上一局结束→下一局开始 gap>=12min (正常连挖通常 2-6min)
  B 上局中途退出: 上一场 deathType=logout
  C 落地即退/自杀: 窗口内 deathType in (logout,suicide) 且 timeSurvived<200s
  D 落地即死: timeSurvived<180s 且 byplayer 且 damage<200 (落地两三分钟就死, 未接战)
含随机对照(种子队列, 同窗口口径)。输出 timeline_flags.json"""
import json, os, collections, datetime, random

DIR = os.path.dirname(os.path.abspath(__file__))
CUP_T = json.load(open(os.path.join(DIR, 'mid_person.json'), encoding='utf-8'))
mi = json.load(open(os.path.join(DIR, 'appearances.json'), encoding='utf-8'))['match_info']
T = json.load(open(os.path.join(DIR, 'suspect_targets.json'), encoding='utf-8'))
H = json.load(open(os.path.join(DIR, 'suspect_histories.json'), encoding='utf-8'))
S = {s['acc']: s for s in json.load(open(os.path.join(DIR, 'suspects.json'), encoding='utf-8'))}

def load(mid):
    for c in ['cache_top', '../meet_study/cache']:
        p = f'{DIR}/{c}/match_{mid}.json'
        if os.path.exists(p): return json.load(open(p, encoding='utf-8'))

def part_stats(d, aid):
    for p in d.get('included', []):
        if p['type'] == 'participant' and p['attributes']['stats'].get('playerId') == aid:
            return p['attributes']['stats']

def timeline(aid, center):
    """±6h 窗口内该账号的时间线"""
    rows = []
    for mid in H.get(aid, {}).get('match_ids', []):
        d = load(mid)
        if not d: continue
        at = d['data']['attributes']
        t = datetime.datetime.fromisoformat(at['createdAt'].replace('Z', '+00:00'))
        if abs((t - center).total_seconds()) > 6 * 3600: continue
        st = part_stats(d, aid)
        if not st: continue
        rows.append({'mid': mid, 't': t, 'dur': st['timeSurvived'],  # 实际参与时长(退出即结束)
                     'death': st['deathType'], 'ts': st['timeSurvived'], 'dmg': st['damageDealt'],
                     'kills': st['kills'], 'isCup': mid in CUP_MATCHIDS})
    rows.sort(key=lambda r: r['t'])
    return rows

CUP_MATCHIDS = set(open(os.path.join(DIR, '../cup_match_ids.txt')).read().split())
# suspect_targets 里的 mid 是 8 位前缀, 展开为完整 ID
_full = {m[:8]: m for m in CUP_MATCHIDS}
T = {a: {_full.get(m, m) for m in ms} for a, ms in T.items()}
FLAGS = []
gap_all = []          # baseline gaps
for aid, sus_mids in T.items():
    names = list(S[aid]['names']) if aid in S else [H.get(aid, {}).get('name', '?')]
    for sm in sus_mids:
        center = datetime.datetime.fromisoformat(mi[sm]['createdAt'].replace('Z', '+00:00'))
        tl = timeline(aid, center)
        for i, r in enumerate(tl):
            if i > 0:
                prev = tl[i-1]
                gap = (r['t'] - (prev['t'] + datetime.timedelta(seconds=prev['dur']))).total_seconds()
                gap_all.append(gap)
        flags = []
        for i, r in enumerate(tl):
            prev = tl[i-1] if i > 0 else None
            nxt = tl[i+1] if i+1 < len(tl) else None
            if prev:
                gap = (r['t'] - (prev['t'] + datetime.timedelta(seconds=prev['dur']))).total_seconds()
                if gap >= 600 and r['isCup']:
                    flags.append(f"★与上局间隔{int(gap/60)}min后进杯赛局(疑似等待)")
            if prev and prev['death'] == 'logout':
                flags.append(f"★上局中途退出(存活{int(prev['ts'])}s){'→直接进杯赛局' if r['isCup'] else ''}")
            if prev and prev['death'] == 'suicide' and prev['ts'] < 200 and r['isCup']:
                flags.append(f"★上局自杀({int(prev['ts'])}s)后进杯赛局")
                if prev['death'] == 'logout' and r['isCup']:
                    flags.append(f"上局logout(存活{int(prev['ts'])}s)后进杯赛局")
            if r is not None and not r['isCup'] and r['death'] == 'logout':
                flags.append(f"★窗口内中途退出一场(存活{int(r['ts'])}s,{'杯赛前' if nxt and nxt['isCup'] else ('杯赛后' if prev and prev['isCup'] else '窗口中')})")
            if r is not None and not r['isCup'] and r['death'] == 'suicide' and r['ts'] < 200:
                flags.append(f"★窗口内自杀({int(r['ts'])}s,{'杯赛前' if nxt and nxt['isCup'] else ('杯赛后' if prev and prev['isCup'] else '窗口中')})")
        # 账号整体早死率(全部缓存对局)
        tot=ed=0
        for m2 in H.get(aid, {}).get('match_ids', []):
            d2=load(m2)
            if not d2: continue
            st2=part_stats(d2,aid)
            if not st2: continue
            tot+=1
            if st2['deathType']=='byplayer' and st2['timeSurvived']<180 and st2['damageDealt']<200: ed+=1
        n_early=sum(1 for r in tl if not r['isCup'] and r['death']=='byplayer' and r['ts']<180 and r['dmg']<200)
        flags.append(f"窗口早死率 {n_early}/{len([r for r in tl if not r['isCup']])} vs 账号整体 {ed}/{tot} (对照17.7%)")
        if flags:
            FLAGS.append({'acc': aid, 'name': names[0], 'susMid': sm, 'susDt': CUP_T[sm]['dt'],
                          'window': [(r['t'].strftime('%H:%M'), 'CUP' if r['isCup'] else 'norm', int(r['ts']), r['death'], int(r['dmg'])) for r in tl],
                          'flags': flags})

# baseline: 预载120名种子的全部对局一次, 再对每场杯赛±6h窗口统计
SS = json.load(open(os.path.join(DIR, '../meet_study/seeds.json'), encoding='utf-8'))
SH = json.load(open(os.path.join(DIR, '../meet_study/histories.json'), encoding='utf-8'))
byaid = {}
for x in SS: byaid.setdefault(x['aid'], x)
random.seed(3)
seeds_ok = [aid for aid, s in byaid.items()
            if not aid.startswith('ai.') and aid not in S and s['source_mid'] not in CUP_MATCHIDS
            and aid in SH]
random.shuffle(seeds_ok)
seeds_ok = seeds_ok[:120]
recs_seed = []   # (aid, t, ts, death, dmg) 仅普通四排official
for aid in seeds_ok:
    for m2 in SH[aid]['match_ids']:
        if m2 in CUP_MATCHIDS: continue
        d = load(m2)
        if not d: continue
        at = d['data']['attributes']
        if at['gameMode'] != 'squad' or at.get('matchType') != 'official': continue
        st = part_stats(d, aid)
        if not st: continue
        t = datetime.datetime.fromisoformat(at['createdAt'].replace('Z', '+00:00'))
        recs_seed.append((aid, t, st['timeSurvived'], st['deathType'], st['damageDealt']))
b_logout = b_suicide = b_earlydie = b_rows = 0
for mid in CUP_MATCHIDS:
    center = datetime.datetime.fromisoformat(mi[mid]['createdAt'].replace('Z', '+00:00'))
    for aid, t, ts2, dth, dmg in recs_seed:
        if abs((t - center).total_seconds()) > 6 * 3600: continue
        b_rows += 1
        if dth == 'logout' and ts2 < 200: b_logout += 1
        if dth == 'suicide' and ts2 < 200: b_suicide += 1
        if dth == 'byplayer' and ts2 < 180 and dmg < 200: b_earlydie += 1

import statistics
print('suspect flags:', len(FLAGS))
for f in FLAGS:
    print(f"  {f['name']:22} {f['susDt']} {f['susMid'][:8]}")
    for fl in f['flags']: print('     -', fl)
    print('     窗口:', f['window'])
print(f"\nbaseline (对照, 杯赛对局±6h窗口内的非杯赛局): logout<200s {b_logout}/{b_rows}, suicide<200s {b_suicide}, 落地即死 {b_earlydie}")
print('gap(suspect) median:', round(statistics.median(gap_all)) if gap_all else None,
      'p90:', round(sorted(gap_all)[int(len(gap_all)*0.9)]) if gap_all else None,
      '>=720s:', sum(1 for g in gap_all if g >= 720), '/', len(gap_all))
json.dump({'flags': FLAGS, 'baseline': {'rows': b_rows, 'logout': b_logout, 'suicide': b_suicide, 'earlydie': b_earlydie},
           'gaps': {'n': len(gap_all), 'median': statistics.median(gap_all) if gap_all else None,
                    'ge720': sum(1 for g in gap_all if g >= 720)}},
          open(os.path.join(DIR, 'timeline_flags.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
