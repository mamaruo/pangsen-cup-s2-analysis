# -*- coding: utf-8 -*-
import os, sys, datetime
sys.path.insert(0, os.path.abspath('../pangsen_day5'))
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import pubg

ids = {
 'yin-0710': 'account.c416e2e00b254f57aa9ac5e8b46c8ef6',
 'qwertyuiop_50541': 'account.52c29debeab645279f5d3ab4d065291d',
 'dadenniluancuan1': 'account.eb9b15d4b5a4464f9c9466fb9d260a54',
 'YINYILINGZHU': 'account.0948de9e482b4d65abd9362281a04f3e',
 'iiiiLuckyOooo': 'account.a7d05690ea23400498ae0e325f290f15',
 'ooluckyooo': 'account.453be1368e3e4e0e8e60af60a8a7a3c1',
 'WANGZHEGUILAIOVO': 'account.158c0f6400524a58a89cb18f2dc3052b',
 'xiaogegeyimie': 'account.3fd2f9c4ef7a45aaa96fc73f854b0caa',
 'PSBGJSWD1122': 'account.cc40bc9ec02e412b8638b1a20ca35764',
 'xiangjinjuesai': 'account.daa1fc4c60ca4aa082584a0a048839f4',
 '5Bbuff': 'account.60e729fc9ed741ee92b3d7fd4c88f9ba',
 'daydayday_-': 'account.0a851679df5b4d91b4b831aa4dbfa302',
 '0VO1010VO(fill)': 'account.1b8cb332342046a9990a3be67869acf2',
 'WWWWVVVVNNN(fill)': 'account.f067d098170b4ddaa65ba8fb306b3d68',
}
seen = {}
for name, aid in ids.items():
    try:
        mids = pubg.player_matches(aid)
    except Exception as e:
        print('ERR', name, e); continue
    for mid in mids:
        created = pubg.match(mid)['data']['attributes']['createdAt']
        if created < '2026-09-05T11:00':
            continue
        seen.setdefault(mid, [created, []])[1].append(name)
for mid, (created, names) in sorted(seen.items(), key=lambda x: x[1][0]):
    bj = (datetime.datetime.fromisoformat(created.replace('Z', '+00:00')) + datetime.timedelta(hours=8)).strftime('%H:%M')
    print(mid[:8], bj, names)
