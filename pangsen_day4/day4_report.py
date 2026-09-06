# -*- coding: utf-8 -*-
"""胖森杯S2 Day4(9-1) 计分 + Markdown 报告(与 Day5 gen_report.py 同一逻辑)"""
import json, os, datetime
import pubg

WPN_EN = json.load(open('damageCauserName.json', encoding='utf-8'))
WPN_CN = {'Frag Grenade': '破片手榴弹', 'Panzerfaust Projectile': '铁拳火箭筒', 'Blue Zone': '蓝圈', 'Red Zone': '轰炸区'}
def wname(code):
    if not code: return '未知'
    en = WPN_EN.get(code, code.replace('Weap', '').replace('_C', ''))
    return WPN_CN.get(en, en)

# (选手1, 游戏名1, id1, 选手2, 游戏名2, id2, matchId)
ROUNDS = [
 ('KeyS','WanM87342','account.158c0f6400524a58a89cb18f2dc3052b','Xnan','Aixinzuimei','account.3fd2f9c4ef7a45aaa96fc73f854b0caa','7b4af720-915a-42a8-b790-00fa006d72fe'),
 ('KeyS','WanM87342','account.158c0f6400524a58a89cb18f2dc3052b','Xnan','Aixinzuimei','account.3fd2f9c4ef7a45aaa96fc73f854b0caa','bf3dfe2f-b684-46de-b94e-7911556a202b'),
 ('Boliang','3Bbuff','account.a7d05690ea23400498ae0e325f290f15','iL1u','DayDayOuO','account.453be1368e3e4e0e8e60af60a8a7a3c1','039ca015-162b-486d-a0e2-ec7158782145'),
 ('Boliang','3Bbuff','account.a7d05690ea23400498ae0e325f290f15','iL1u','DayDayOuO','account.453be1368e3e4e0e8e60af60a8a7a3c1','b6dfc346-6236-4132-8eb7-36333956d4da'),
 ('明柒柒','III7722II','account.eb9b15d4b5a4464f9c9466fb9d260a54','kk','OVOVOOOV','account.0948de9e482b4d65abd9362281a04f3e','35679c02-7600-43e7-8b28-41ffa904c528'),
 ('明柒柒','III7722II','account.eb9b15d4b5a4464f9c9466fb9d260a54','kk','OVOVOOOV','account.0948de9e482b4d65abd9362281a04f3e','217ad582-f008-48c6-989d-2485d85a5dd4'),
 ('Shen','MICKEYMOUSEOK666','account.c416e2e00b254f57aa9ac5e8b46c8ef6','SpaceMan','HelloKittyOK666','account.52c29debeab645279f5d3ab4d065291d','8dc6f63c-c553-4ec7-9820-5194a5f62212'),
 ('Shen','MICKEYMOUSEOK666','account.c416e2e00b254f57aa9ac5e8b46c8ef6','SpaceMan','HelloKittyOK666','account.52c29debeab645279f5d3ab4d065291d','e654ffe5-cf35-4b0a-9f2e-02f736310ce3'),
 ('马平','dsdwfnygsaew','account.cc40bc9ec02e412b8638b1a20ca35764','Xbei','TOPM249-___-','account.daa1fc4c60ca4aa082584a0a048839f4','1df6617d-6fd1-45f4-8abf-baa27a769a1e'),
 ('马平','dsdwfnygsaew','account.cc40bc9ec02e412b8638b1a20ca35764','Xbei','TOPM249-___-','account.daa1fc4c60ca4aa082584a0a048839f4','99b73b1a-f4b7-4073-ba70-9ebdd8cf8e69'),
 ('Axidd','7Bebebe_','account.60e729fc9ed741ee92b3d7fd4c88f9ba','Solo9','January_BiG','account.0a851679df5b4d91b4b831aa4dbfa302','e5eaf37a-7643-45ba-8523-cb07c8c56927'),
 ('Axidd','7Bebebe_','account.60e729fc9ed741ee92b3d7fd4c88f9ba','Solo9','January_BiG','account.0a851679df5b4d91b4b831aa4dbfa302','a933c9cd-093b-4ab6-bddd-7519297125b8'),
]

def parse(t):
    return datetime.datetime.strptime(t[:23], '%Y-%m-%dT%H:%M:%S.%f').replace(tzinfo=datetime.timezone.utc)

foot, fn, accts, rows, pair_tot = [], 0, {}, [], {}
for n1, g1, i1, n2, g2, i2, mid in ROUNDS:
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
    remark = f'重复击杀 {marks}' if marks else '—'
    dtxt = f'9-{start.day} {start:%H:%M}'
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
out = ['# 胖森战神杯S2 Day4(9月1日)计分', '',
       '| 日期时间 | 服务器 | 地图 | 选手1 | 选手2 | 第一阶段有效击杀 | 第二阶段有效击杀 | 吃鸡 | 总积分 | 备注 | 回放链接 |', '|---|---|---|---|---|---|---|---|---|---|---|']
out += [r[1] for r in rows]
out += ['', '## 账号对照', '', '| 游戏内名 | 账号ID |', '|---|---|']
for g, (nm, aid) in sorted(accts.items(), key=lambda x: x[1][0]):
    out.append(f'| {g} | `{aid}` |')
out += ['', '## 当日队伍总分(两轮取最高)', '', '| 选手 | 第1轮 | 第2轮 | 日总分 |', '|---|---|---|---|']
for (n1, n2), tots in pair_tot.items():
    out.append(f'| {n1} & {n2} | {tots[0]} | {tots[1]} | **{max(tots)}** |')
out += [''] + foot
md = '\n'.join(out)
open('day4_report.md', 'w', encoding='utf-8').write(md)
print(md)
