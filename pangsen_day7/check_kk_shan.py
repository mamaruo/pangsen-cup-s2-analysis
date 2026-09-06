# -*- coding: utf-8 -*-
import os, sys, datetime
sys.path.insert(0, os.path.abspath('../pangsen_day5'))
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import pubg

full = {}
for aid, nm in [('account.453be1368e3e4e0e8e60af60a8a7a3c1', 'kk'),
                ('account.daa1fc4c60ca4aa082584a0a048839f4', 'shan')]:
    for m in pubg.player_matches(aid):
        if m.startswith(('3b4ea846', '86f33fc2')):
            full[m[:8]] = m
for k, mid in full.items():
    md = pubg.match(mid)
    at = md['data']['attributes']
    bj = (datetime.datetime.fromisoformat(at['createdAt'].replace('Z', '+00:00')) + datetime.timedelta(hours=8)).strftime('%H:%M')
    print(f'== {k} {bj} map={at["mapName"]} squads={len(md["data"]["relationships"]["rosters"]["data"])}')
    for r in pubg.rosters(mid)[:4]:
        print('  ', [m['name'] for m in r['members']], 'rank', r.get('rank'))
