# -*- coding: utf-8 -*-
"""胖森杯S2 Day3(8-31) 计分 + Markdown 报告(与 Day5 gen_report.py 同一逻辑)"""
import json, os, datetime
import pubg

WPN_EN = json.load(open('damageCauserName.json', encoding='utf-8'))
WPN_CN = {'Frag Grenade': '破片手榴弹', 'Panzerfaust Projectile': '铁拳火箭筒', 'Blue Zone': '蓝圈', 'Red Zone': '轰炸区'}
def wname(code):
    if not code: return '未知'
    en = WPN_EN.get(code, code.replace('Weap', '').replace('_C', ''))
    return WPN_CN.get(en, en)

P = json.load(open('day3_pids.json'))
def R(n1, g1, n2, g2, mid, note=''):
    return (n1, g1, P[g1], n2, g2, P[g2], mid, note)

# (选手1, 游戏名1, id1, 选手2, 游戏名2, id2, matchId, 备注)
ROUNDS = [
 R('汐月','CandyBB--_','xs','weirdo_im','c21cb548-8db9-4b97-bb12-7cc009917a3d'),
 R('汐月','CandyBB--_','xs','weirdo_im','5b5a2387-3ecb-44da-be5e-57302effe3f7'),
 R('HSmm','4WM_ASQ0926','WINDah','Cue4fizAQRA','9886329e-ffb5-4366-a3ba-e48b5adcd860'),
 R('HSmm','4WM_ASQ0926','WINDah','Cue4fizAQRA','155c4e31-4473-4d51-a6b2-3741c162158c'),
 R('Cui71','GOD_98-','04NB','DZ-HeZi-88330','f887ba76-5f13-40ac-b544-2f1165c7174c'),
 R('Cui71','GOD_98-','04NB','DZ-HeZi-88330','b1dfe084-f6e2-4594-8302-65a355083ed5'),
 R('11ovo','76i2_-','陈','BigHead_XxHD','f4f36acf-0f5d-4162-82ed-d92a6cd74265'),
 R('11ovo','76i2_-','陈','BigHead_XxHD','c6542a66-269a-45ff-a453-f4958987c8bb'),
 R('意识DT','94db','700','MMMWMMMMMMMMMMMW','513ebf4f-a96e-46c9-a37e-c6cd280038b1'),
 R('意识DT','94db','700','MMMWMMMMMMMMMMMW','09f40150-5bb8-4f1a-8d8f-187f309f59a2'),
 R('DJinRong','2iDD-','roll','Meiguibb','92f57d3f-d895-4a91-80e3-9e44e38852d8'),
 R('DJinRong','2iDD-','roll','Meiguibb','edb48bf2-85f0-461d-aa8b-1b0287f7c56e'),
 R('DJinRong','2iDD-','roll','Meiguibb','1607076a-c84d-4227-b88c-cacf32e7f22f','加赛'),
]

def parse(t):
    return datetime.datetime.strptime(t[:23], '%Y-%m-%dT%H:%M:%S.%f').replace(tzinfo=datetime.timezone.utc)

foot, fn, accts, rows, pair_tot = [], 0, {}, [], {}
for n1, g1, i1, n2, g2, i2, mid, note in ROUNDS:
    tel = pubg.telemetry(mid)
    ms = next(e for e in tel if e['_T'] == 'LogMatchStart')
    start = parse(ms['_D']) + datetime.timedelta(hours=8)
    p2t = next(e['_D'] for e in tel if e['_T'] == 'LogPhaseChange' and e.get('phase') == 2)
    rank = next(r['rank'] for r in pubg.rosters(mid)
                if {m['name'] for m in r['members']} >= {g1, g2})
    win = rank == 1
    kills = []
    for g, who in ((g1, n1), (g2, n2)):
        for k in pubg.kills_of(mid, g):
            k['who'] = who; k['gname'] = g
            kills.append(k)
    kills.sort(key=lambda x: x['t'])
    byv = {}
    for k in kills: byv.setdefault(k['victim'], []).append(k)
    dups = {v: ks for v, ks in byv.items() if len(ks) > 1}
    seen = set()
    for k in kills:
        k['cnt'] = k['victim'] not in seen
        seen.add(k['victim'])
    p1k = [k for k in kills if k['t'] < p2t]; p2k = [k for k in kills if k['t'] >= p2t]
    e1 = sum(1 for k in p1k if k['cnt']); e2 = sum(1 for k in p2k if k['cnt'])
    def cell(e, raw): return str(e) if e == raw else f'{e}({raw})'
    base = e1 * 4 + e2 * (4 if win else 2)
    if dups:
        extra = sum(4 if k['t'] < p2t else (4 if win else 2) for ks in dups.values() for k in ks[1:] if not k['cnt'])
        total = f'{base}({base + extra})'
    else:
        total = str(base)
    marks = ''
    for v, ks in dups.items():
        fn += 1
        parts = []
        for i, k in enumerate(ks):
            adv = '' if i == 0 else '再次'
            delta = int((parse(k['t']) - parse(ms['_D'])).total_seconds())
            parts.append(f"在{delta//60:02d}:{delta%60:02d}被{k['gname']}（{k['who']}）{adv}用{wname(k['weapon'])}淘汰")
        foot.append(f"[^{fn}]: {v}{'，'.join(parts)}。")
        marks += f'[^{fn}]'
    remark = '重复击杀 ' + marks if not note and marks else (f'{note}；重复击杀 {marks}' if marks else (note or '—'))
    dtxt = f'{start.month}-{start.day} {start:%H:%M}'
    server = pubg.match_server(mid)
    mapn = pubg.match_meta(mid)['map']
    p1c = f'{n1}<br>({g1})'
    p2c = f'{n2}<br>({g2})'
    links = f'[PL](https://pubglookup.com/players/steam/{g1}/matches/{mid})<br>[PP](https://pubg.plus/en/replay?matches={mid}&player={g2})'
    rows.append((start, f'| {dtxt} | {server} | {mapn} | {p1c} | {p2c} | {cell(e1,len(p1k))} | {cell(e2,len(p2k))} | {"🐔 是" if win else "否"} | {total} | {remark} | {links} |'))
    pair_tot.setdefault((n1, n2), []).append(base)
    for nm, g, aid in ((n1, g1, i1), (n2, g2, i2)):
        accts.setdefault(g, (nm, aid))

rows.sort(key=lambda r: r[0])
out = ['# 胖森战神杯S2 Day3(8月31日)计分', '',
       '| 日期时间 | 服务器 | 地图 | 选手1 | 选手2 | 第一阶段有效击杀 | 第二阶段有效击杀 | 吃鸡 | 总积分 | 备注 | 回放链接 |', '|---|---|---|---|---|---|---|---|---|---|---|']
out += [r[1] for r in rows]
out += ['', '## 账号对照', '', '| 游戏内名 | 账号ID |', '|---|---|']
for g, (nm, aid) in sorted(accts.items(), key=lambda x: x[1][0]):
    out.append(f'| {g} | `{aid}` |')
out += ['', '## 当日队伍总分(两轮取最高)', '', '| 选手 | 第1轮 | 第2轮 | 加赛 | 日总分 |', '|---|---|---|---|---|']
for (n1, n2), tots in pair_tot.items():
    t3 = tots[2] if len(tots) > 2 else '—'
    out.append(f'| {n1} & {n2} | {tots[0]} | {tots[1]} | {t3} | **{max(tots)}** |')
out += [''] + foot
md = '\n'.join(out)
open('day3_report.md', 'w', encoding='utf-8').write(md)
print(md)
