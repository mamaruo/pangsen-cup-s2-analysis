"""Day7 (9-5 复活赛) 按截图账号反查比赛"""
import json, sys, os
from datetime import datetime, timedelta
sys.path.insert(0, os.path.abspath(os.path.join('..', 'pangsen_day5')))
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from pubg import search_player, player_matches, match, rosters

NAMES = ['qwertyuiop_50541', 'dadenniluancuan1', 'ooluckyooo', 'iiiLuckyOooo',
         'WANGZHEGUILAIOVO', 'xiangjinjuesai', 'daydayday_-']
acct = {}
for n in NAMES:
    r = search_player(n)
    print(n, '->', r, flush=True)
    if r: acct[n] = r[0][0]
json.dump(acct, open('day7_accts.json', 'w'), indent=1)

def win(b):
    return (b.month, b.day) == (9, 5) and b.hour >= 17

for n, pid in acct.items():
    for mid in player_matches(pid):
        c = match(mid)['data']['attributes']['createdAt']
        b = datetime.fromisoformat(c.replace('Z', '+00:00')) + timedelta(hours=8)
        if not win(b): continue
        rs = rosters(mid)
        sq = next((x for x in rs if any(m['pid'] == pid for m in x['members'])), None)
        mem = [(m['name'], '*' if m['pid'] == pid else '', m['surv'], m['kills']) for m in sq['members']] if sq else None
        print(n, b.strftime('%H:%M'), mid[:8], f'r{sq["rank"] if sq else "?"}', mem, flush=True)
