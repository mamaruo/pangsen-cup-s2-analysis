"""Day3 step2: 从已知比赛 roster 提取账号ID -> 用填充位 Asia_LYB_ 拉全部正赛 -> 打印所有队伍"""
import sys, os, json
from datetime import datetime, timedelta
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from pangsen_day5.pubg import rosters, match, player_matches

SEEDS = ['f887ba76-5f13-40ac-b544-2f1165c7174c',
         'b1dfe084-f6e2-4594-8302-65a355083ed5',
         '155c4e31-4473-4d51-a6b2-3741c162158c',
         '9886329e-ffb5-4366-a3ba-e48b5adcd860',
         '513ebf4f-a96e-46c9-a37e-c6cd280038b1',
         '09f40150-5bb8-4f1a-8d8f-187f309f59a2',
         'edb48bf2-85f0-461d-aa8b-1b0287f7c56e']
def full(mid8):
    return mid8

name2pid = {}
for s in SEEDS:
    mid = full(s)
    for r in rosters(mid):
        for m in r['members']:
            name2pid.setdefault(m['name'], m['pid'])
print(json.dumps(name2pid, indent=1, ensure_ascii=False))
json.dump(name2pid, open('day3_name2pid.json', 'w'), ensure_ascii=False, indent=1)

filler = name2pid.get('Asia_LYB_')
print('Asia_LYB_ pid =', filler, flush=True)

def beijing(c):
    t = datetime.fromisoformat(c.replace('Z', '+00:00'))
    return t + timedelta(hours=8)

tours = []
for mid in player_matches(filler):
    c = match(mid)['data']['attributes']['createdAt']
    b = beijing(c)
    if ((b.month, b.day) == (8, 31) and b.hour >= 17) or ((b.month, b.day) == (9, 1) and b.hour < 3):
        tours.append((b, mid))
tours.sort()
print(f'正赛数: {len(tours)}', flush=True)
allt = {}
for b, mid in tours:
    rs = rosters(mid)
    print('=' * 8, b.strftime('%m-%d %H:%M'), mid, flush=True)
    squads = []
    for r in rs:
        mem = [(m['name'], m['surv'], m['kills']) for m in r['members']]
        squads.append(mem)
        print(' rank', r['rank'], mem, flush=True)
    allt[mid] = dict(start=b.strftime('%m-%d %H:%M'), squads=squads)
json.dump(allt, open('day3_tournaments.json', 'w'), ensure_ascii=False, indent=1)
