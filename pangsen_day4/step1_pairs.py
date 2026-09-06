"""Day4 (9-1) 匹配: 账号搜索 -> 比赛历史交集 -> 输出 day4_matches.json"""
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from pangsen_day5.pubg import search_player, player_matches, match, rosters

# 截图识别出的 游戏名 -> (选手1, 选手2) 成对
PAIRS = {
    'KeyS&Xnan':    ['WanM87342', 'Aixinzuimei'],
    'Boliang&iL1u': ['3Bbuff', 'DayDayOuO'],
    'MQQ&kk':       ['III7722II', 'OVOVOOOV'],
    'Shen&SpaceMan':['MICKEYMOUSEOK666', 'HelloKittyOK666'],
    'MP&Xbei':      ['dsdwfnygsaew', 'TOPM249-___-'],
    'Axidd&Solo9':  ['7Bebebe_'],
}

def beijing(created):
    from datetime import datetime, timedelta, timezone
    t = datetime.fromisoformat(created.replace('Z', '+00:00'))
    return t + timedelta(hours=8)

hist = {}
for pair, names in PAIRS.items():
    for n in names:
        r = search_player(n)
        if not r:
            print(f'!! {n} 搜索不到', flush=True)
            hist[n] = []
            continue
        pid = r[0][0]
        mids = player_matches(pid)
        # 只看 9-1 北京时间 18:00-24:00 的比赛
        keep = []
        for mid in mids:
            c = match(mid)['data']['attributes']['createdAt']
            b = beijing(c)
            if (b.month, b.day) == (9, 1) and 18 <= b.hour < 24:
                keep.append((mid, b.strftime('%H:%M')))
        keep.sort(key=lambda x: x[1])
        hist[n] = keep
        print(pair, n, pid, keep, flush=True)

out = {}
for pair, names in PAIRS.items():
    if len(names) == 2:
        a, b = set(x[0] for x in hist.get(names[0], [])), set(x[0] for x in hist.get(names[1], []))
        out[pair] = sorted(a & b)
    else:
        out[pair] = sorted(set(x[0] for x in hist.get(names[0], [])))
    print(pair, out[pair], flush=True)

json.dump(out, open('day4_matches.json', 'w'), indent=1)
