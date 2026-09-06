# -*- coding: utf-8 -*-
import os, sys, json, datetime
sys.path.insert(0, os.path.abspath(os.path.join('..', 'pangsen_day5')))
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import pubg

anchors = {'account.60e729fc9ed741ee92b3d7fd4c88f9ba': '5Bbuff',
           'account.c416e2e00b254f57aa9ac5e8b46c8ef6': 'yin-0710'}
want = ('64c8bf07', 'ead88c91', 'd78d7be1')
full = {}
for aid in anchors:
    for mid in pubg.player_matches(aid):
        for w in want:
            if mid.startswith(w):
                full[w] = mid
for w in want:
    mid = full[w]
    md = pubg.match(mid)
    at = md['data']['attributes']
    bj = (datetime.datetime.fromisoformat(at['createdAt'].replace('Z', '+00:00')) + datetime.timedelta(hours=8)).strftime('%m-%d %H:%M')
    print(f'== {w} {bj} map={at["mapName"]} squads={len(md["data"]["relationships"]["rosters"]["data"])}')
    for r in pubg.rosters(mid):
        names = [m['name'] for m in r['members']]
        print('  ', names, 'rank', r.get('rank', '?'), 'kills', r.get('kills', '?'))
