# -*- coding: utf-8 -*-
"""Day1/Day2 计分(配对级) -> day12_scores.json,并对照 Day2 积分榜"""
import json, os, sys, datetime
sys.path.insert(0, os.path.abspath(os.path.join('..', 'pangsen_day5')))
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import pubg

IDS = json.load(open('mid_ids.json'))
def F(p8): return IDS[p8]

# 账号对: (对内成员1 pid, 名字; 成员2)
POOL = {
 'eb9b15d4': ('CandyBB--_', 'account.eb9b15d4b5a4464f9c9466fb9d260a54'),
 '0948de9e': ('weirdo_im', 'account.0948de9e482b4d65abd9362281a04f3e'),
 'c416e2e0': ('4WM_ASQ0926', 'account.c416e2e00b254f57aa9ac5e8b46c8ef6'),
 '52c29deb': ('Cue4fizAQRA', 'account.52c29debeab645279f5d3ab4d065291d'),
 'a7d05690': ('GOD_98-', 'account.a7d05690ea23400498ae0e325f290f15'),
 '453be136': ('DZ-HeZi-88330', 'account.453be1368e3e4e0e8e60af60a8a7a3c1'),
 'cc40bc9e': ('76i2_-', 'account.cc40bc9ec02e412b8638b1a20ca35764'),
 'daa1fc4c': ('BigHead_XxHD', 'account.daa1fc4c60ca4aa082584a0a048839f4'),
 '158c0f64': ('2iDD-', 'account.158c0f6400524a58a89cb18f2dc3052b'),
 '3fd2f9c4': ('Meiguibb', 'account.3fd2f9c4ef7a45aaa96fc73f854b0caa'),
 '1b8cb332': ('MMMWMMMMMMMMMMMW', 'account.1b8cb332342046a9990a3be67869acf2'),
 'f067d098': ('94db', 'account.f067d098170b4ddaa65ba8fb306b3d68'),
}
PAIRS = [('eb9b15d4','0948de9e'), ('c416e2e0','52c29deb'), ('a7d05690','453be136'),
         ('cc40bc9e','daa1fc4c'), ('158c0f64','3fd2f9c4'), ('1b8cb332','f067d098')]
ROUNDS = {
 'D1': [('eb9b15d4','0948de9e','d2c0cfd7'), ('eb9b15d4','0948de9e','c36be949'),
        ('c416e2e0','52c29deb','83490382'), ('c416e2e0','52c29deb','7274cc8c'),
        ('a7d05690','453be136','47794c27'), ('a7d05690','453be136','0aba02a0'),
        ('cc40bc9e','daa1fc4c','e607b483'), ('cc40bc9e','daa1fc4c','42293dbc'),
        ('158c0f64','3fd2f9c4','32da2c7c'), ('158c0f64','3fd2f9c4','32aff732'),
        ('1b8cb332','f067d098','0818a15f'), ('1b8cb332','f067d098','010551bc')],
 'D2': [('eb9b15d4','0948de9e','4f13fa3b'), ('eb9b15d4','0948de9e','47e3db29'),
        ('c416e2e0','52c29deb','804abae9'), ('c416e2e0','52c29deb','51c92165'),
        ('a7d05690','453be136','ff87e7a7'), ('a7d05690','453be136','86f3169d'),
        ('cc40bc9e','daa1fc4c','c07ac45a'), ('cc40bc9e','daa1fc4c','8c648f1f'),
        ('158c0f64','3fd2f9c4','38b5a9c8'), ('158c0f64','3fd2f9c4','36e0f19b'),
        ('1b8cb332','f067d098','c01e2e0f'), ('1b8cb332','f067d098','e8bda60e')],
}
def parse(t):
    return datetime.datetime.strptime(t[:23], '%Y-%m-%dT%H:%M:%S.%f').replace(tzinfo=datetime.timezone.utc)

out = {}
for day, rs in ROUNDS.items():
    for ga, gb, p8 in rs:
        mid = F(p8)
        tel = pubg.telemetry(mid)
        ms = next(e for e in tel if e['_T'] == 'LogMatchStart')
        start = parse(ms['_D']) + datetime.timedelta(hours=8)
        p2t = next(e['_D'] for e in tel if e['_T'] == 'LogPhaseChange' and e.get('phase') == 2)
        rank = next(r['rank'] for r in pubg.rosters(mid)
                    if {m['pid'] for m in r['members']} >= {POOL[ga][1], POOL[gb][1]})
        win = rank == 1
        res = {}
        for tag in (ga, gb):
            ks = pubg.kills_of(mid, POOL[tag][0])
            k1 = sum(1 for k in ks if k['t'] < p2t)
            k2 = len(ks) - k1
            res[tag] = dict(k1=k1, k2=k2, raw=len(ks))
        allk = pubg.kills_of(mid, POOL[ga][0]) + pubg.kills_of(mid, POOL[gb][0])
        victims = [k['victim'] for k in allk]
        ndup = len(victims) - len(set(victims))
        e1 = res[ga]['k1'] + res[gb]['k1']; e2 = res[ga]['k2'] + res[gb]['k2']
        base = e1*4 + e2*(4 if win else 2)
        extra = 0
        from collections import Counter
        c = Counter((v, k['t'] < p2t) for v, k in zip(victims, sorted(allk, key=lambda x: x['t'])))
        # 重算去重分(比赛全程按受害者首次出现)
        seen = set(); cnt1 = cnt2 = 0
        for k in sorted(allk, key=lambda x: x['t']):
            if k['victim'] in seen: continue
            seen.add(k['victim'])
            if k['t'] < p2t: cnt1 += 1
            else: cnt2 += 1
        base_d = cnt1*4 + cnt2*(4 if win else 2)
        out.setdefault(day, {})[p8] = dict(pair=ga+'+'+gb, start=start.strftime('%m-%d %H:%M'),
            rank=rank, map=pubg.match_meta(mid)['map'], server=pubg.match_server(mid),
            per=res, kills=[e1, e2], dedup=[cnt1, cnt2], ndup=ndup,
            base=base, base_dedup=base_d, mid=mid)
        print(day, p8, start.strftime('%H:%M'), POOL[ga][0], '+', POOL[gb][0],
              'rank', rank, 'kills', e1, e2, 'dedup', cnt1, cnt2, 'score', base_d, flush=True)

json.dump(out, open('day12_scores.json', 'w'), ensure_ascii=False, indent=1)

print('\n=== Day2 两轮取最高 vs 积分榜 ===')
panel = {'eb9b15d4+0948de9e': ('骄阳&龙Skr', 62), 'c416e2e0+52c29deb': ('随性&CTGpeekking', 52),
         'a7d05690+453be136': ('112&4AM小海', 30), 'cc40bc9e+daa1fc4c': ('航仔&楚一', 108),
         '158c0f64+3fd2f9c4': ('鬼狙&AI', 8), '1b8cb332+f067d098': ('XTRyuyu&Jing', 76)}
tots = {}
for p8, v in out['D2'].items():
    tots.setdefault(v['pair'], []).append(v['base_dedup'])
for pr, (name, pv) in panel.items():
    print(pr, name, tots.get(pr), '榜:', pv)
