# -*- coding: utf-8 -*-
"""重扫 Day7 六个账号,列出 9-5 北京时间 19:00 后的所有比赛"""
import os, sys, json, datetime
sys.path.insert(0, os.path.abspath(os.path.join('..', 'pangsen_day5')))
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import pubg

ids = {
 'yin-0710': 'account.c416e2e00b254f57aa9ac5e8b46c8ef6',
 'dadenniluancuan1': 'account.eb9b15d4b5a4464f9c9466fb9d260a54',
 'iiiiLuckyOooo': 'account.a7d05690ea23400498ae0e325f290f15',
 'WANGZHEGUILAIOVO': 'account.158c0f6400524a58a89cb18f2dc3052b',
 'PSBGJSWD1122': 'account.cc40bc9ec02e412b8638b1a20ca35764',
 '5Bbuff': 'account.60e729fc9ed741ee92b3d7fd4c88f9ba',
}
seen = {}
for name, aid in ids.items():
    for mid in pubg.player_matches(aid):
        md = pubg.match(mid)
        created = md['data']['attributes']['createdAt']
        if created < '2026-09-05T11:00':  # UTC, = 北京 19:00
            continue
        seen.setdefault(mid, [created, []])[1].append(name)
for mid, (created, names) in sorted(seen.items(), key=lambda x: x[1][0]):
    bj = (datetime.datetime.fromisoformat(created.replace('Z', '+00:00')) + datetime.timedelta(hours=8)).strftime('%H:%M')
    print(mid[:8], bj, names)
