# -*- coding: utf-8 -*-
"""胖森杯S2 最终 Markdown 报告生成器(队伍级合并计分 + GFM 脚注)"""
import json, os, datetime
import pubg

WPN_EN = json.load(open('damageCauserName.json', encoding='utf-8'))
WPN_CN = {'Frag Grenade': '破片手榴弹', 'Panzerfaust Projectile': '铁拳火箭筒', 'Blue Zone': '蓝圈', 'Red Zone': '轰炸区'}
def wname(code):
    if not code: return '未知'
    en = WPN_EN.get(code, code.replace('Weap', '').replace('_C', ''))
    return WPN_CN.get(en, en)


# (选手1, 游戏名1, id1, 选手2, 游戏名2, id2, matchId)  id 为 None 时走 D4AID
ROUNDS = [
 ('大能','dsdwfnygsaew','account.cc40bc9ec02e412b8638b1a20ca35764','爱国','TOPM249-___-','account.daa1fc4c60ca4aa082584a0a048839f4','e17eebd5'),
 ('大能','dsdwfnygsaew','account.cc40bc9ec02e412b8638b1a20ca35764','爱国','TOPM249-___-','account.daa1fc4c60ca4aa082584a0a048839f4','1c577902'),
 ('tiantian','WanM87342','account.158c0f6400524a58a89cb18f2dc3052b','xwudd','Aixinzuimei','account.3fd2f9c4ef7a45aaa96fc73f854b0caa','286b37d5'),
 ('tiantian','WanM87342','account.158c0f6400524a58a89cb18f2dc3052b','xwudd','Aixinzuimei','account.3fd2f9c4ef7a45aaa96fc73f854b0caa','f08ed8d1'),
 ('Dec12th','MICKEYMOUSEOK666','account.c416e2e00b254f57aa9ac5e8b46c8ef6','SuZe','HelloKittyOK666','account.52c29debeab645279f5d3ab4d065291d','b78ee504'),
 ('Dec12th','MICKEYMOUSEOK666','account.c416e2e00b254f57aa9ac5e8b46c8ef6','SuZe','HelloKittyOK666','account.52c29debeab645279f5d3ab4d065291d','997ef53e'),
 ('pd','3Bbuff','account.a7d05690ea23400498ae0e325f290f15','lunlun','DayDayOuO','account.453be1368e3e4e0e8e60af60a8a7a3c1','510d960a'),
 ('pd','3Bbuff','account.a7d05690ea23400498ae0e325f290f15','lunlun','DayDayOuO','account.453be1368e3e4e0e8e60af60a8a7a3c1','9269da01'),
 ('XiaoHuxxXX','7Bebebe_','account.60e729fc9ed741ee92b3d7fd4c88f9ba','Dong','January_BiG','account.0a851679df5b4d91b4b831aa4dbfa302','9742a9b3'),
 ('XiaoHuxxXX','7Bebebe_','account.60e729fc9ed741ee92b3d7fd4c88f9ba','Dong','January_BiG','account.0a851679df5b4d91b4b831aa4dbfa302','a5559d48'),
 ('Xihan','III7722II','account.eb9b15d4b5a4464f9c9466fb9d260a54','DouZiVv','OVOVOOOV','account.0948de9e482b4d65abd9362281a04f3e','89c96bcc'),
 ('Xihan','III7722II','account.eb9b15d4b5a4464f9c9466fb9d260a54','DouZiVv','OVOVOOOV','account.0948de9e482b4d65abd9362281a04f3e','a3f7dcd7'),
]
ids = json.load(open('prefix_ids.json', encoding='utf-8'))
ids.setdefault('89c96bcc', '89c96bcc-29df-4ff7-8bb2-cbbb5f5e1b44')
ids.setdefault('a3f7dcd7', 'a3f7dcd7-f96e-4fd3-a457-71b3ac9e8634')

foot, fn = [], 0
accts = {}
rows = []
for n1, g1, i1, n2, g2, i2, p8 in ROUNDS:
    mid = ids[p8]
    tel = pubg.telemetry(mid)
    ms = next(e for e in tel if e['_T'] == 'LogMatchStart')
    start = datetime.datetime.strptime(ms['_D'][:23], '%Y-%m-%dT%H:%M:%S.%f').replace(tzinfo=datetime.timezone.utc) + datetime.timedelta(hours=8)
    p2t = next(e['_D'] for e in tel if e['_T'] == 'LogPhaseChange' and e.get('phase') == 2)
    rank = next(r['rank'] for r in pubg.rosters(mid)
                if any(m['name'] in (g1, g2) for m in r['members']) and
                   {m['name'] for m in r['members']} >= {g1, g2})
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
            delta = int((datetime.datetime.strptime(k['t'][:23], '%Y-%m-%dT%H:%M:%S.%f').replace(tzinfo=datetime.timezone.utc)
                     - datetime.datetime.strptime(ms['_D'][:23], '%Y-%m-%dT%H:%M:%S.%f').replace(tzinfo=datetime.timezone.utc)).total_seconds())
            parts.append(f"在{delta//60:02d}:{delta%60:02d}被{k['gname']}（{k['who']}）{adv}用{wname(k['weapon'])}淘汰")
        foot.append(f"[^{fn}]: {v}{'，'.join(parts)}。")
        marks += f'[^{fn}]'
    remark = f'重复击杀 {marks}' if marks else '—'
    dtxt = f'9-{start.day} {start:%H:%M}'
    server = pubg.match_server(mid)
    mapn = pubg.match_meta(mid)['map']
    AID1, AID2 = i1, i2
    p1c = f'{n1}<br>({g1})'
    p2c = f'{n2}<br>({g2})'
    links = f'[PL](https://pubglookup.com/players/steam/{g1}/matches/{mid})<br>[PP](https://pubg.plus/en/replay?matches={mid}&player={g2})'
    rows.append((start, f'| {dtxt} | {server} | {mapn} | {p1c} | {p2c} | {cell(e1,len(p1k))} | {cell(e2,len(p2k))} | {"🐔 是" if win else "否"} | {total} | {remark} | {links} |'))
    for nm, g, aid in ((n1, g1, AID1), (n2, g2, AID2)):
        accts.setdefault(g, (nm, aid))

rows.sort(key=lambda r: r[0])
out = ['| 日期时间 | 服务器 | 地图 | 选手1 | 选手2 | 第一阶段有效击杀 | 第二阶段有效击杀 | 吃鸡 | 总积分 | 备注 | 回放链接 |', '|---|---|---|---|---|---|---|---|---|---|---|']
out += [r[1] for r in rows]
out += ['', '## 账号对照', '', '| 游戏内名 | 账号ID |', '|---|---|']
for g, (nm, aid) in accts.items():
    out.append(f'| {g} | `{aid}` |')
out += [''] + foot
md = '\n'.join(out)
open('pangsen_report.md', 'w', encoding='utf-8').write(md)
print(md)
