# -*- coding: utf-8 -*-
"""胖森杯S2 Day5 计分流水线
计分: 阶段2(游戏时间10:00=LogPhaseChange phase2)前击杀4分;之后2分;吃鸡则之后也4分。
查重: 两名选手合并击杀列表,同一受害者第2次及以上出现不计分。
"""
import pubg, json, time
from collections import Counter

AID = {
 'WanM87342':'account.158c0f6400524a58a89cb18f2dc3052b',
 'Aixinzuimei':'account.3fd2f9c4ef7a45aaa96fc73f854b0caa',
 '3Bbuff':'account.a7d05690ea23400498ae0e325f290f15',
 'DayDayOuO':'account.453be1368e3e4e0e8e60af60a8a7a3c1',
 'TOPM249-___-':'account.daa1fc4c60ca4aa082584a0a048839f4',
 'dsdwfnygsaew':None,
 'MICKEYMOUSEOK666':'account.c416e2e00b254f57aa9ac5e8b46c8ef6',
 'HelloKittyOK666':'account.52c29debeab645279f5d3ab4d065291d',
 'January_BiG':'account.0a851679df5b4d91b4b831aa4dbfa302',
 '7Bebebe_':None,
 'III7722II':'account.eb9b15d4b5a4464f9c9466fb9d260a54',
 'OVOVOOOV':'account.0948de9e482b4d65abd9362281a04f3e',
}
# (轮次, 选手1, 账号1, 选手2, 账号2, matchId)
ROUNDS = [
 ('R1','爱国','TOPM249-___-','大能','dsdwfnygsaew','e17eebd5'),
 ('R2','爱国','TOPM249-___-','大能','dsdwfnygsaew','1c577902'),
 ('R1','tiantian','WanM87342','xwudd','Aixinzuimei','286b37d5'),
 ('R2','tiantian','WanM87342','xwudd','Aixinzuimei','f08ed8d1'),
 ('R1','Dec12th','MICKEYMOUSEOK666','SuZe','HelloKittyOK666','b78ee504'),
 ('R2','Dec12th','MICKEYMOUSEOK666','SuZe','HelloKittyOK666','997ef53e'),
 ('R1','pd','3Bbuff','lunlun','DayDayOuO','510d960a'),
 ('R2','pd','3Bbuff','lunlun','DayDayOuO','9269da01'),
 ('R1','XiaoHuxxXX','7Bebebe_','Dong','January_BiG','9742a9b3'),
 ('R2','XiaoHuxxXX','7Bebebe_','Dong','January_BiG','a5559d48'),
 ('R1','Xihan','III7722II','DouZiVv','OVOVOOOV','89c96bcc'),
 ('R2','Xihan','III7722II','DouZiVv','OVOVOOOV','a3f7dcd7'),
]
ids = json.load(open('prefix_ids.json'))
# 补充可能不在 prefix_ids 里的
for p8 in ['89c96bcc','a3f7dcd7']:
    if p8 not in ids:
        for mid in pubg.player_matches(AID['OVOVOOOV']):
            ids[mid[:8]] = mid
            time.sleep(1)

results = []
for rnd, n1, a1, n2, a2, p8 in ROUNDS:
    mid = ids[p8]
    meta = pubg.match_meta(mid)
    rs = pubg.rosters(mid)
    squad = next((r for r in rs if any(m['name']==a1 for m in r['members']) and any(m['name']==a2 for m in r['members'])), None)
    assert squad, f'{a1}/{a2} not same squad in {mid}'
    p2 = pubg.phase2_time(mid)
    merged = []
    for acct in (a1, a2):
        for k in pubg.kills_of(mid, acct):
            merged.append(dict(acct=acct, **k))
    merged.sort(key=lambda x: x['t'])
    cnt = Counter(m['victim'] for m in merged)
    seen = Counter()
    for m in merged:
        seen[m['victim']] += 1
        m['phase'] = 'P1' if m['t'] < p2 else 'P2'
        m['dup'] = seen[m['victim']] > 1
    win = squad['rank'] == 1
    def score(acct):
        pts = 0; det = []
        for m in merged:
            if m['acct'] != acct: continue
            if m['dup']: det.append((m['victim'], m['phase'], 0, 'DUP不计')); continue
            base = 4 if m['phase']=='P1' else (4 if win else 2)
            pts += base; det.append((m['victim'], m['phase'], base, ''))
        return pts, det
    s1, d1 = score(a1); s2, d2 = score(a2)
    m1 = next(m for m in squad['members'] if m['name']==a1)
    m2 = next(m for m in squad['members'] if m['name']==a2)
    if AID[a1] is None: AID[a1] = m1['pid']
    if AID[a2] is None: AID[a2] = m2['pid']
    results.append(dict(round=rnd, pair=f'{n1}&{n2}', match=mid, created=meta['created'], map=meta['map'],
                        rank=squad['rank'], win=win, phase2=p2,
                        p1=dict(name=n1, acct=a1, aid=AID[a1], stats_k=m1['kills'], surv=m1['surv'], score=s1, kills=d1),
                        p2=dict(name=n2, acct=a2, aid=AID[a2], stats_k=m2['kills'], surv=m2['surv'], score=s2, kills=d2)))
    print(f"[{n1}&{n2} {rnd}] {meta['created']} {meta['map']} rank={squad['rank']} win={win} "
          f"| {n1}({a1}) tel_kills={len(d1)} stats={m1['kills']} pts={s1} "
          f"| {n2}({a2}) tel_kills={len(d2)} stats={m2['kills']} pts={s2}")
    time.sleep(0.8)

json.dump(results, open('day5_scores.json','w'), ensure_ascii=False, indent=1)
print('\n=== 明细 ===')
for r in results:
    for side in ('p1','p2'):
        d = r[side]
        print(f"{r['pair']} {r['round']} {d['name']}({d['acct']}):")
        for v, ph, pt, note in d['kills']:
            print(f"    {v} [{ph} {pt}分] {note}")
