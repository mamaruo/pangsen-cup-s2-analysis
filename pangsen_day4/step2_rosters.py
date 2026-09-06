"""Step2: 12 场比赛 roster 提取 + Solo9 账号发现 + 成队校验 -> day4_rounds.json"""
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from pangsen_day5.pubg import rosters, match_meta

PAIRS = {
    'KeyS&Xnan':    ['WanM87342', 'Aixinzuimei'],
    'Boliang&iL1u': ['3Bbuff', 'DayDayOuO'],
    'MQQ&kk':       ['III7722II', 'OVOVOOOV'],
    'Shen&SpaceMan':['MICKEYMOUSEOK666', 'HelloKittyOK666'],
    'MP&Xbei':      ['dsdwfnygsaew', 'TOPM249-___-'],
    'Axidd&Solo9':  ['7Bebebe_'],
}
MATCHES = json.load(open('day4_matches.json'))
ACCTS = json.load(open(os.path.join(os.path.dirname(__file__), '..', 'pangsen_day5', 'known_accounts.json')))

rounds = []
for pair, mids in MATCHES.items():
    for mid in mids:
        rs = rosters(mid)
        meta = match_meta(mid)
        mine = [r for r in rs if any(m['name'] in PAIRS[pair] for m in r['members'])]
        assert len(mine) == 1, (pair, mid, [ [m['name'] for m in r['members']] for r in mine ])
        squad = mine[0]
        members = [(m['name'], m['pid'], m['kills'], m['surv']) for m in squad['members']]
        # Axidd&Solo9: 同队 4 人里挑出 7Bebebe_ 的队友(存活时间相近的非填充位)
        rounds.append(dict(pair=pair, mid=mid, start_meta=meta['created'], map=meta['map'],
                           rank=squad['rank'], members=members))
        print(pair, mid[:8], meta['map'], 'rank', squad['rank'], members, flush=True)

json.dump(rounds, open('day4_rounds.json', 'w'), indent=1, ensure_ascii=False)
print('done', len(rounds))
