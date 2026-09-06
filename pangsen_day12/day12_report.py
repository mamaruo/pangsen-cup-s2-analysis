# -*- coding: utf-8 -*-
"""胖森杯S2 Day1(8-29,A组) + Day2(8-30,B组) 报告生成"""
import json, os, sys, datetime
from collections import Counter
sys.path.insert(0, os.path.abspath(os.path.join('..', 'pangsen_day5')))
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import pubg

WPN_EN = json.load(open('damageCauserName.json', encoding='utf-8'))
WPN_CN = {'Frag Grenade': '破片手榴弹', 'Panzerfaust Projectile': '铁拳火箭筒', 'Blue Zone': '蓝圈', 'Red Zone': '轰炸区'}
def wname(code):
    if not code: return '未知'
    en = WPN_EN.get(code, code.replace('Weap', '').replace('_C', ''))
    return WPN_CN.get(en, en)

IDS = json.load(open('mid_ids.json'))
P = {  # 游戏名 -> (账号ID)
 'CandyBB--_': 'account.eb9b15d4b5a4464f9c9466fb9d260a54',
 'weirdo_im': 'account.0948de9e482b4d65abd9362281a04f3e',
 '4WM_ASQ0926': 'account.c416e2e00b254f57aa9ac5e8b46c8ef6',
 'Cue4fizAQRA': 'account.52c29debeab645279f5d3ab4d065291d',
 'GOD_98-': 'account.a7d05690ea23400498ae0e325f290f15',
 'DZ-HeZi-88330': 'account.453be1368e3e4e0e8e60af60a8a7a3c1',
 '76i2_-': 'account.cc40bc9ec02e412b8638b1a20ca35764',
 'BigHead_XxHD': 'account.daa1fc4c60ca4aa082584a0a048839f4',
 '2iDD-': 'account.158c0f6400524a58a89cb18f2dc3052b',
 'Meiguibb': 'account.3fd2f9c4ef7a45aaa96fc73f854b0caa',
 'MMMWMMMMMMMMMMMW': 'account.1b8cb332342046a9990a3be67869acf2',
 '94db': 'account.f067d098170b4ddaa65ba8fb306b3d68',
}
def R(n1, g1, n2, g2, mid8, note=''):
    return (n1, g1, n2, g2, IDS[mid8], note)

# Day2(B组): 映射经截图+积分榜双重验证
D2_ROUNDS = [
 R('JiaoYang','CandyBB--_','LongSkr','weirdo_im','4f13fa3b'),
 R('JiaoYang','CandyBB--_','LongSkr','weirdo_im','47e3db29'),
 R('PeeKk1ng','4WM_ASQ0926','SuiX1ngKK','Cue4fizAQRA','804abae9'),
 R('PeeKk1ng','4WM_ASQ0926','SuiX1ngKK','Cue4fizAQRA','51c92165'),
 R('xiaohaixxxx','GOD_98-','CRAZY112','DZ-HeZi-88330','ff87e7a7'),
 R('xiaohaixxxx','GOD_98-','CRAZY112','DZ-HeZi-88330','86f3169d'),
 R('Chue','BigHead_XxHD','HangZai','76i2_-','c07ac45a'),
 R('Chue','BigHead_XxHD','HangZai','76i2_-','8c648f1f'),
 R('鬼狙','Meiguibb','AI','2iDD-','38b5a9c8'),
 R('鬼狙','Meiguibb','AI','2iDD-','36e0f19b'),
 R('Yuyu','MMMWMMMMMMMMMMMW','Jing','94db','c01e2e0f'),
 R('Yuyu','MMMWMMMMMMMMMMMW','Jing','94db','e8bda60e'),
]
# Day1(A组): 狗子=GOD_98-、小鬼=CandyBB--_ 经 POV 截图+遥测验证;其余两对待确认
D1_ROUNDS = [
 R('Lilghost','CandyBB--_','Wenbo','weirdo_im','d2c0cfd7'),
 R('Lilghost','CandyBB--_','Wenbo','weirdo_im','c36be949'),
 R('MMing','4WM_ASQ0926','i26v6','Cue4fizAQRA','83490382'),
 R('MMing','4WM_ASQ0926','i26v6','Cue4fizAQRA','7274cc8c'),
 R('狗子','GOD_98-','99','DZ-HeZi-88330','47794c27'),
 R('狗子','GOD_98-','99','DZ-HeZi-88330','0aba02a0'),
 R('VX30','76i2_-','小飞','BigHead_XxHD','e607b483'),
 R('VX30','76i2_-','小飞','BigHead_XxHD','42293dbc'),
 R('OneDragon','2iDD-','HaoSkr','Meiguibb','32da2c7c'),
 R('OneDragon','2iDD-','HaoSkr','Meiguibb','32aff732'),
 R('Rain','94db','Shan','MMMWMMMMMMMMMMMW','0818a15f'),
 R('Rain','94db','Shan','MMMWMMMMMMMMMMMW','010551bc'),
]

def parse(t):
    return datetime.datetime.strptime(t[:23], '%Y-%m-%dT%H:%M:%S.%f').replace(tzinfo=datetime.timezone.utc)

def build(ROUNDS, title, mapping_note=''):
    foot, fn, accts, rows, pair_tot = [], 0, {}, [], {}
    for n1, g1, n2, g2, mid, note in ROUNDS:
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
        pair_tot.setdefault((g1, g2), []).append(base)
        for nm, g in ((n1, g1), (n2, g2)):
            accts.setdefault(g, (nm, P[g]))
    rows.sort(key=lambda r: r[0])
    out = [f'# {title}', '']
    if mapping_note: out += [mapping_note, '']
    out += ['| 日期时间 | 服务器 | 地图 | 选手1 | 选手2 | 第一阶段有效击杀 | 第二阶段有效击杀 | 吃鸡 | 总积分 | 备注 | 回放链接 |',
            '|---|---|---|---|---|---|---|---|---|---|---|']
    out += [r[1] for r in rows]
    out += ['', '## 账号对照', '', '| 游戏内名 | 账号ID |', '|---|---|']
    for g, (nm, aid) in sorted(accts.items()):
        out.append(f'| {g} | `{aid}` |')
    out += ['', '## 当日队伍总分(两轮取最高)', '', '| 账号对 | 第1轮 | 第2轮 | 日总分 |', '|---|---|---|---|']
    for (g1, g2), tots in pair_tot.items():
        out.append(f'| {g1} + {g2} | {tots[0]} | {tots[1]} | **{max(tots)}** |')
    out += [''] + foot
    return '\n'.join(out)

D2_NOTE = ('> 选手↔账号对应依据:小海/随性/Yuyu/骄阳/楚一/鬼狙 六张 POV 截图 + 当日积分榜面板逐对验证(62/52/30/108/8/76 全部吻合)。\n'
           '> 楚一=Chue、航仔=HangZai(分组.png)。\n'
           '> 当日积分榜面板:航仔&楚一 108、XTRyuyu&Jing 76、骄阳&龙Skr 62、随性&CTGpeekking 52、112&4AM小海 30、鬼狙&AI 8(与我算完全一致)。')
md2 = build(D2_ROUNDS, '胖森战神杯S2 Day2(8月30日,B组)计分', D2_NOTE)
open('day2_report.md', 'w', encoding='utf-8').write(md2)

D1_NOTE = ('> **选手↔账号对映射 6/6 全部确认(2026-09-03 用户逐对补图)**:狗子=GOD_98-(UMP)、17小鬼(Lilghost)=CandyBB--_(AKM)、大山(Shan)=MMMWMMMMMMMMMMMW(AUG)、PeRo26(i26v6)=Cue4fizAQRA(AKM)、小飞=BigHead_XxHD(RPD)、Haoskr=Meiguibb(死亡画面:本人被 P90 淘汰,与 19:42 场 Meiguibb 最后一条死亡记录 P90 LegShot 吻合);'
           '搭档由同队存活前二锁定:99=DZ-HeZi-88330、17文博(Wenbo)=weirdo_im、小雨(Rain)=94db、PeRo明明(MMing)=4WM_ASQ0926、VX30=76i2_-、TL一龙(OneDragon)=2iDD-。'
           '参照:B组(8-30)由同一批账号对服务,对应关系见 day2_report.md。')
md1 = build(D1_ROUNDS, '胖森战神杯S2 Day1(8月29日,A组)计分', D1_NOTE)
open('day1_report.md', 'w', encoding='utf-8').write(md1)
print(md2[:1500])
print('...')
print(md1[:800])
