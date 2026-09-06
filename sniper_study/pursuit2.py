"""追击轨迹 v3:
驻留段: 选手 >=120s 位移<=80m(锚点)。
延迟接近(严格): 嫌疑人/对照在 t0-300~t0+120 期间与驻留点距离未显著缩短(<100m, 排除本来就在路上),
  且 t0+120 后距离持续缩短: 900s 内 minD < 0.6*d(t0+120) 且净缩短>=300m。
对照: 全体非选手、非嫌疑(n=1)玩家。输出 pursuit2.json"""
import json, math

CUP_T = json.load(open('sniper_study/mid_person.json', encoding='utf-8'))
mids = open('cup_match_ids.txt').read().split()
S = {s['acc']: s for s in json.load(open('sniper_study/suspects.json', encoding='utf-8'))}

def dist(a, b): return math.hypot(a[0]-b[0], a[1]-b[1]) / 100.0

def camp_segments(tr, landT, deathT):
    segs = []; i = 0; n = len(tr)
    while i < n:
        if tr[i][0] < landT - 5 or (deathT is not None and tr[i][0] > deathT):
            i += 1; continue
        anchor = tr[i]; j = i
        while j+1 < n and tr[j+1][0]-tr[j][0] < 90 and dist(tr[j+1][1:], anchor[1:]) <= 80 \
              and (deathT is None or tr[j+1][0] <= deathT):
            j += 1
        if tr[j][0] - tr[i][0] >= 120:
            segs.append((tr[i][0], tr[j][0], (anchor[1], anchor[2])))
        i = j + 1
    return segs

def pos_at(tr, t, tol=25):
    best = None
    for p in tr:
        if best is None or abs(p[0]-t) < best[0]: best = (abs(p[0]-t), p)
    return best[1] if best and best[0] <= tol else None

def approach_test(tr, t0, L, endT, deathT):
    """返回 dict 或 None"""
    horizon = min(t0 + 900, endT, (deathT or 1e9))
    p_pre = pos_at(tr, t0 - 300, 60); p0 = pos_at(tr, t0, 40); p120 = pos_at(tr, t0 + 120, 60)
    if not (p_pre and p0 and p120): return None
    d_pre, d0, d120 = dist(p_pre[1:], L), dist(p0[1:], L), dist(p120[1:], L)
    if d0 < 400: return None
    if d_pre - d0 > 100: return None           # 驻留开始前已在接近 → 排除
    if d120 - d0 > 100: return None            # 驻留后反而在远离 → 排除
    tmin = None; dmin = None
    for p in tr:
        if p[0] < t0 + 120 or p[0] > horizon: continue
        dd = dist(p[1:], L)
        if dmin is None or dd < dmin: dmin, tmin = dd, p[0]
    if dmin is None: return None
    if dmin > 350 or dmin > 0.6 * d120 or (d120 - dmin) < 300: return None
    return {'d_pre': round(d_pre), 'd0': round(d0), 'd120': round(d120),
            'minD': round(dmin), 'minT': round(tmin), 'closeDur': round(tmin - t0)}

cases = []; ctrl_cnt = ctrl_tot = 0; seg_total = 0; ctrl_approach = 0
for mid in mids:
    d = json.load(open(f'features/{mid}.json', encoding='utf-8'))
    endT = d['endT']
    cups = {a: c for a, c in d['chars'].items() if c['isCup'] and c.get('track')}
    if not cups: continue
    segs_all = []
    for ca, cc in cups.items():
        for (t0, t1, L) in camp_segments(cc['track'], cc.get('landT') or 0, cc['deathT']):
            if t1 < 240 or t0 > endT - 120: continue
            segs_all.append((ca, cc['name'], t0, t1, L))
    seg_total += len(segs_all)
    for ca, cname, t0, t1, L in segs_all:
        for a, c in d['chars'].items():
            if c['isCup'] or a.startswith('ai.'): continue
            if c['team'] == cups[ca]['team']: continue
            tr = c.get('track')
            if not tr: continue
            if c['deathT'] is not None and c['deathT'] < t0 + 120: continue
            is_sus = a in S and S[a]['n'] >= 2
            if not is_sus:
                ctrl_tot += 1
            r = approach_test(tr, t0, L, endT, c['deathT'])
            if not r: continue
            rec = {'mid': mid, 'dt': CUP_T[mid]['dt'], 'sus': a, 'susName': c['name'],
                   'n': S[a]['n'] if a in S else 0, 'isSus': is_sus,
                   'cupAcc': ca, 'cupName': cname, 't0': round(t0), 't1': round(t1), **r}
            if rec['isSus']: cases.append(rec)
            else:
                ctrl_tot += 1; ctrl_approach += 1
print('camping segments:', seg_total)
print(f'approach(严格): 嫌疑人(n>=2) {len(cases)} 例; 对照玩家 {ctrl_approach}/{ctrl_tot}')
sus_hits = [r for r in cases if 120 <= r['minT'] - r['t0'] <= 900]
print('minT-t0 in 120~900s:', len(sus_hits))
seen = set(); ded = []
for r in sorted(cases, key=lambda r: r['minT'] - r['t0']):
    k = (r['mid'], r['sus'], r['cupAcc'])
    if k in seen: continue
    seen.add(k); ded.append(r)
print('dedup:', len(ded))
for r in ded[:30]:
    print(f"  {r['mid'][:8]} {r['dt']} {r['susName']:20} n={r['n']} -> {r['cupName']:16} camp@{r['t0']}s d0={r['d0']}m minD={r['minD']}m 到达@+{r['minT']-r['t0']}s")
json.dump({'segments': seg_total, 'cases': ded, 'ctrl_tot': ctrl_tot, 'ctrl_approach': ctrl_approach},
          open('sniper_study/pursuit2.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
