# -*- coding: utf-8 -*-
"""胖森杯S2 Day6(9-3,F组) 计分 + Markdown 报告"""
import json, os, sys, datetime
sys.path.insert(0, os.path.abspath(os.path.join('..', 'pangsen_day5')))
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import pubg

WPN_EN = json.load(open('damageCauserName.json', encoding='utf-8'))
WPN_CN = {'Frag Grenade': '破片手榴弹', 'Panzerfaust Projectile': '铁拳火箭筒', 'Blue Zone': '蓝圈', 'Red Zone': '轰炸区'}
def wname(code):
    if not code: return '未知'
    en = WPN_EN.get(code, code.replace('Weap', '').replace('_C', ''))
    return WPN_CN.get(en, en)

P = {
 'III7722II': 'account.eb9b15d4b5a4464f9c9466fb9d260a54',
 'OVOVOOOV': 'account.0948de9e482b4d65abd9362281a04f3e',
 'MICKEYMOUSEOK666': 'account.c416e2e00b254f57aa9ac5e8b46c8ef6',
 'HelloKittyOK666': 'account.52c29debeab645279f5d3ab4d065291d',
 '3Bbuff': 'account.a7d05690ea23400498ae0e325f290f15',
 'DayDayOuO': 'account.453be1368e3e4e0e8e60af60a8a7a3c1',
 'dsdwfnygsaew': 'account.cc40bc9ec02e412b8638b1a20ca35764',
 'TOPM249-___-': 'account.daa1fc4c60ca4aa082584a0a048839f4',
 '7Bebebe_': 'account.60e729fc9ed741ee92b3d7fd4c88f9ba',
 'January_BiG': 'account.0a851679df5b4d91b4b831aa4dbfa302',
 'czczzsodjjd222': None, 'BAOBAONO1_': None,  # roster 挖
}
def R(n1, g1, n2, g2, mid8, note=''):
    return (n1, g1, n2, g2, mid8, note)

ROUNDS = [
 R('tte','III7722II','nan','OVOVOOOV','aa679aba'),
 R('tte','III7722II','nan','OVOVOOOV','71d39b1c'),
 R('沐白(MuBai)','MICKEYMOUSEOK666','新一(XinYi)','HelloKittyOK666','c892be8c'),
 R('沐白(MuBai)','MICKEYMOUSEOK666','新一(XinYi)','HelloKittyOK666','c6df7c8e'),
 R('不知名','3Bbuff','走马','DayDayOuO','55492d77'),
 R('不知名','3Bbuff','走马','DayDayOuO','3ca46262'),
 R('阔澜','dsdwfnygsaew','苏宇','TOPM249-___-','fa807f95'),
 R('阔澜','dsdwfnygsaew','苏宇','TOPM249-___-','704d9fe4'),
 R('fffeng','7Bebebe_','03','January_BiG','dc69b071'),
 R('fffeng','7Bebebe_','03','January_BiG','6ef77937'),
 R('KKong','BAOBAONO1_','小白','czczzsodjjd222','61a06e4b'),
 R('KKong','BAOBAONO1_','小白','czczzsodjjd222','46676089'),
]

# 挖新账号 ID
import json as _json
IDS = _json.load(open('mid_ids.json'))
if P['czczzsodjjd222'] is None:
    for r in pubg.rosters(IDS['61a06e4b']):
        for m in r['members']:
            if m['name'] in ('czczzsodjjd222', 'BAOBAONO1_'):
                P[m['name']] = m['pid']

def parse(t):
    return datetime.datetime.strptime(t[:23], '%Y-%m-%dT%H:%M:%S.%f').replace(tzinfo=datetime.timezone.utc)

foot, fn, accts, rows, pair_tot = [], 0, {}, [], {}
for n1, g1, n2, g2, mid8, note in ROUNDS:
    mid = IDS[mid8]
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
    server = pubg.match_server(mid); mapn = pubg.match_meta(mid)['map']
    p1c = f'{n1}<br>({g1})'; p2c = f'{n2}<br>({g2})'
    links = f'[PL](https://pubglookup.com/players/steam/{g1}/matches/{mid})<br>[PP](https://pubg.plus/en/replay?matches={mid}&player={g2})'
    rows.append((start, f'| {dtxt} | {server} | {mapn} | {p1c} | {p2c} | {cell(e1,len(p1k))} | {cell(e2,len(p2k))} | {"🐔 是" if win else "否"} | {total} | {remark} | {links} |'))
    pair_tot.setdefault((n1, g1, n2, g2), []).append(base)
    for nm, g in ((n1, g1), (n2, g2)):
        accts.setdefault(g, (nm, P[g]))

rows.sort(key=lambda r: r[0])
out = ['# 胖森战神杯S2 Day6(9月3日,F组)计分', '',
       '> 选手↔账号映射依据:小白/空空/03/苏宇/走马/新一/沐白 7 张 POV 截图(击杀者/死亡画面)+ 遥测武器时间核对。',
       '',
       '| 日期时间 | 服务器 | 地图 | 选手1 | 选手2 | 第一阶段有效击杀 | 第二阶段有效击杀 | 吃鸡 | 总积分 | 备注 | 回放链接 |',
       '|---|---|---|---|---|---|---|---|---|---|---|']
out += [r[1] for r in rows]
out += ['', '## 账号对照', '', '| 游戏内名 | 账号ID |', '|---|---|']
for g, (nm, aid) in sorted(accts.items()):
    out.append(f'| {g} | `{aid}` |')
out += ['', '## 当日队伍总分(两轮取最高)', '', '| 选手 | 第1轮 | 第2轮 | 日总分 |', '|---|---|---|---|']
for (n1, g1, n2, g2), tots in pair_tot.items():
    t2 = tots[1] if len(tots) > 1 else '—'
    out.append(f'| {n1} & {n2} | {tots[0]} | {t2} | **{max(tots)}** |')
out += [''] + foot
md = '\n'.join(out)
open('day6_report.md', 'w', encoding='utf-8').write(md)
print(md)
