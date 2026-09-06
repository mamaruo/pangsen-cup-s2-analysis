"""Day3 step1b: roster 挖掘 - 打印已知账号窗口期每场比赛的同队成员,挖搭档真实账号"""
import json, sys, os
from datetime import datetime, timedelta
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from pangsen_day5.pubg import player_matches, match, rosters

def beijing(created):
    t = datetime.fromisoformat(created.replace('Z', '+00:00'))
    return t + timedelta(hours=8)

KNOWN = {
    'CandyBB-_': 'account.1bc0caaf98bd434c9497f0030c4c1778',   # 汐月
    '94db': 'account.f067d098170b4ddaa65ba8fb306b3d68',        # 意识DT?
    'MMMWMMMMMMMMMMW': 'account.d6ccec79c58448fca3e91831ff05d559',  # 700
    '04NB?': 'account.453be1368e3e4e0e8e60af60a8a7a3c1',       # id.txt: 04NB
    'HSmm?': 'account.c416e2e00b254f57aa9ac5e8b46c8ef6',       # id.txt: HSmm
}
for label, pid in KNOWN.items():
    print('='*20, label, pid, flush=True)
    for mid in player_matches(pid):
        c = match(mid)['data']['attributes']['createdAt']
        b = beijing(c)
        if not (((b.month, b.day) == (8, 31) and b.hour >= 18) or ((b.month, b.day) == (9, 1) and b.hour < 2)):
            continue
        rs = rosters(mid)
        squad = next((r for r in rs if any(m['pid'] == pid for m in r['members'])), None)
        if squad:
            mem = [(m['name'], m['surv'], m['kills']) for m in squad['members']]
            print(b.strftime('%m-%d %H:%M'), mid[:8], 'rank', squad['rank'], mem, flush=True)
        else:
            print(b.strftime('%m-%d %H:%M'), mid[:8], '(不在场)', flush=True)
