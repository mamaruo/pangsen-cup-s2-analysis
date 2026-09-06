"""Day3 (8-31) 匹配: 账号搜索(含M/W串枚举) -> 比赛历史交集 -> day3_matches.json"""
import json, sys, os, itertools
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from pangsen_day5.pubg import search_player, player_matches, match

def beijing(created):
    from datetime import datetime, timedelta
    t = datetime.fromisoformat(created.replace('Z', '+00:00'))
    return t + timedelta(hours=8)

PAIRS = {
    'Xiyue&xs':    ['CandyBB-_', 'weirdo_im'],
    'HSmm&WINDah': ['4WM_ASQ0926', 'Cue4fizAQRA'],
    'Cui71&04NB':  ['GOD_98', 'DZ-HeZi-88330'],
    '11ovo&Chen':  ['BigHead_XxHD'],
    'Yishi&700':   ['94db', 'MMMWMMMMMMMMMMMMMW'],
    'DJinRong&roll':['2iDD', 'Meiguibb'],
}

def find(name):
    r = search_player(name)
    if r: return r[0]
    return None

# M/W 串枚举
acct = {}
for pair, names in PAIRS.items():
    for n in names:
        hit = find(n)
        if not hit and n.startswith('MMMW'):
            for k in range(8, 17):
                cand = 'MMMW' + 'M'*k + 'W'
                hit = find(cand)
                if hit:
                    print('枚举命中:', cand, hit, flush=True)
                    break
        print(pair, n, '->', hit, flush=True)
        if hit: acct[n] = hit
json.dump(acct, open('day3_accts.json', 'w'), indent=1, ensure_ascii=False)

def hist(pid):
    keep = []
    for mid in player_matches(pid):
        c = match(mid)['data']['attributes']['createdAt']
        b = beijing(c)
        # 8-31 晚 + 加赛跨午夜到 9-1 凌晨
        if (b.month, b.day) == (8, 31) and b.hour >= 18 or (b.month, b.day) == (9, 1) and b.hour < 2:
            keep.append((mid, b.strftime('%m-%d %H:%M')))
    keep.sort(key=lambda x: x[1])
    return keep

out = {}
for pair, names in PAIRS.items():
    ids = [n for n in names if n in acct]
    sets = [set(x[0] for x in hist(acct[n][0])) for n in ids]
    common = set.intersection(*sets) if sets else set()
    out[pair] = sorted(common)
    print(pair, {n: acct[n][1] for n in ids}, sorted(common), flush=True)

json.dump(out, open('day3_matches.json', 'w'), indent=1)
