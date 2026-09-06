"""胖森杯选手小号 赛前(8-29 开赛前)比赛历史扫描 + 落地死判定"""
import json, sys, os
sys.path.insert(0, os.path.abspath('../pangsen_day5'))
from pubg import player_matches, match
from datetime import datetime, timedelta

PIDS = {
 'eb9b15d4': 'account.eb9b15d4b5a4464f9c9466fb9d260a54',
 '0948de9e': 'account.0948de9e482b4d65abd9362281a04f3e',
 'c416e2e0': 'account.c416e2e00b254f57aa9ac5e8b46c8ef6',
 '52c29deb': 'account.52c29debeab645279f5d3ab4d065291d',
 'a7d05690': 'account.a7d05690ea23400498ae0e325f290f15',
 '453be136': 'account.453be1368e3e4e0e8e60af60a8a7a3c1',
 'cc40bc9e': 'account.cc40bc9ec02e412b8638b1a20ca35764',
 'daa1fc4c': 'account.daa1fc4c60ca4aa082584a0a048839f4',
 '158c0f64': 'account.158c0f6400524a58a89cb18f2dc3052b',
 '3fd2f9c4': 'account.3fd2f9c4ef7a45aaa96fc73f854b0caa',
 '60e729fc': 'account.60e729fc9ed741ee92b3d7fd4c88f9ba',
 '0a851679': 'account.0a851679df5b4d91b4b831aa4dbfa302',
 '1b8cb332': 'account.1b8cb332342046a9990a3be67869acf2',
 'f067d098': 'account.f067d098170b4ddaa65ba8fb306b3d68',
}
# 开赛前的界定:Day1 正赛最早 8-29 19:01 北京,warmup 更早一点;取 8-29 16:00 北京
CUTOVER_BJ = datetime(2026, 8, 29, 16, 0)

out = {}
for tag, pid in PIDS.items():
    rows = []
    for mid in player_matches(pid):
        m = match(mid)
        c = m['data']['attributes']['createdAt']
        b = datetime.fromisoformat(c.replace('Z', '+00:00')) + timedelta(hours=8)
        n_squads = len([x for x in m['included'] if x['type'] == 'roster'])
        st = next((x['attributes']['stats'] for x in m['included']
                   if x['type'] == 'participant' and x['attributes']['stats']['playerId'] == pid), None)
        rows.append(dict(mid=mid[:8], bj=b.strftime('%m-%d %H:%M'), utc=c,
                         squads=n_squads,
                         surv=st['timeSurvived'] if st else None,
                         kills=st['kills'] if st else None,
                         dbnos=st['DBNOs'] if st else None,
                         rev=st.get('revives') if st else None))
    rows.sort(key=lambda r: r['utc'])
    out[tag] = rows
    pre = [r for r in rows if datetime.strptime(r['bj'], '%m-%d %H:%M').replace(year=2026) < CUTOVER_BJ]
    print(f"{tag}: {len(rows)} 场, 最早 {rows[0]['bj']} ({rows[0]['mid']}), 赛前 {len(pre)} 场", flush=True)

json.dump(out, open('history.json', 'w'), ensure_ascii=False, indent=1)
