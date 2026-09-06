"""Day1/Day2 (8-29, 8-30) 按已知账号 ID 反查比赛并挖 roster"""
import json, sys, os
from datetime import datetime, timedelta
sys.path.insert(0, os.path.abspath(os.path.join('..', 'pangsen_day5')))
from pubg import player_matches, match, rosters

PIDS = {
 'eb9b15d4': 'account.eb9b15d4b5a4464f9c9466fb9d260a54',  # III7722II/明柒柒/汐月/CandyBB
 '0948de9e': 'account.0948de9e482b4d65abd9362281a04f3e',  # OVOVOOOV/kk/xs/weirdo_im
 'c416e2e0': 'account.c416e2e00b254f57aa9ac5e8b46c8ef6',  # MICKEY/Shen/HSmm/Dec12th
 '52c29deb': 'account.52c29debeab645279f5d3ab4d065291d',  # HelloKitty/SpaceMan/WINDah/SuZe
 'a7d05690': 'account.a7d05690ea23400498ae0e325f290f15',  # 3Bbuff/Boliang/GOD_98-/pd
 '453be136': 'account.453be1368e3e4e0e8e60af60a8a7a3c1',  # DayDayOuO/iL1u/04NB/DZ-HeZi
 'cc40bc9e': 'account.cc40bc9ec02e412b8638b1a20ca35764',  # dsdwfnygsaew/马平/大能/76i2
 'daa1fc4c': 'account.daa1fc4c60ca4aa082584a0a048839f4',  # TOPM249/小北/爱国/BigHead
 '158c0f64': 'account.158c0f6400524a58a89cb18f2dc3052b',  # WanM87342/KeyS/tiantian/2iDD
 '3fd2f9c4': 'account.3fd2f9c4ef7a45aaa96fc73f854b0caa',  # Aixinzuimei/Xnan/xwudd/Meiguibb
 '60e729fc': 'account.60e729fc9ed741ee92b3d7fd4c88f9ba',  # 7Bebebe_/小虎/Axidd
 '0a851679': 'account.0a851679df5b4d91b4b831aa4dbfa302',  # January_BiG/东东/Solo9
 '1b8cb332': 'account.1b8cb332342046a9990a3be67869acf2',  # MMMW.../700/Yuyu
 'f067d098': 'account.f067d098170b4ddaa65ba8fb306b3d68',  # 94db/意识DT
}
DAYS = {'D1': ((8, 29), (8, 30)), 'D2': ((8, 30), (8, 31))}

def in_window(b, day):
    d0, d1 = DAYS[day]
    return ((b.month, b.day) == d0 and b.hour >= 17) or ((b.month, b.day) == d1 and b.hour < 3)

for day in ('D1', 'D2'):
    print('#' * 30, day)
    for tag, pid in PIDS.items():
        for mid in player_matches(pid):
            c = match(mid)['data']['attributes']['createdAt']
            b = datetime.fromisoformat(c.replace('Z', '+00:00')) + timedelta(hours=8)
            if not in_window(b, day):
                continue
            rs = rosters(mid)
            sq = next((r for r in rs if any(m['pid'] == pid for m in r['members'])), None)
            if not sq:
                print(b.strftime('%m-%d %H:%M'), mid[:8], tag, '(不在场)')
                continue
            mem = [(m['name'], '*' if m['pid'] == pid else '', m['surv'], m['kills']) for m in sq['members']]
            print(b.strftime('%m-%d %H:%M'), mid[:8], f'r{sq["rank"]}', mem, flush=True)
