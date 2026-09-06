# -*- coding: utf-8 -*-
import json, sys, os
sys.path.insert(0, os.path.abspath('../pangsen_day5'))
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import pubg
ids = json.load(open('mid_ids.json'))
for m in pubg.player_matches('account.60e729fc9ed741ee92b3d7fd4c88f9ba'):
    if m.startswith('d78d7be1'):
        ids['d78d7be1'] = m
json.dump(ids, open('mid_ids.json', 'w'), indent=0)
print(ids.get('d78d7be1'))
