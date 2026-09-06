"""种子抽样：从 pangsen_day5 缓存的 squad+official(普通匹配) 比赛中分层抽取种子玩家。

过滤口径：
  gameMode == 'squad' 且 matchType == 'official'   # competitive = 排位，排除
  排除 14 个胖森杯白名单账号 + 3 个反复出现的补位号 + AI 机器人(ai.*)
抽样方式：按 日期×地图 格子轮转、逐场轮流取 1 名随机参赛者（每场可被取多次，~2 人/场），
增量模式：保留 seeds.json 中已有种子(剔除 ai.*)，只补采到 TARGET_TOTAL 人。
同场多取造成的"同源对共享出生场次"由 build_dataset.py 剔除。
输出 seeds.json: [{aid, name, source_mid, date, map}]
"""
import json, glob, random, collections, os
from datetime import datetime, timedelta

SEED_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_GLOB = os.path.join(SEED_DIR, '..', 'pangsen_day5', 'cache', 'match_*.json')
TARGET_TOTAL = 600
SEED = 20260906

# 胖森杯白名单 14 账号（pangsen_day12/step1_day12.py）+ 补位号
EXCLUDE = {
    'account.eb9b15d4b5a4464f9c9466fb9d260a54',
    'account.0948de9e482b4d65abd9362281a04f3e',
    'account.c416e2e00b254f57aa9ac5e8b46c8ef6',
    'account.52c29debeab645279f5d3ab4d065291d',
    'account.a7d05690ea23400498ae0e325f290f15',
    'account.453be1368e3e4e0e8e60af60a8a7a3c1',
    'account.cc40bc9ec02e412b8638b1a20ca35764',
    'account.daa1fc4c60ca4aa082584a0a048839f4',
    'account.158c0f6400524a58a89cb18f2dc3052b',
    'account.3fd2f9c4ef7a45aaa96fc73f854b0caa',
    'account.60e729fc9ed741ee92b3d7fd4c88f9ba',
    'account.0a851679df5b4d91b4b831aa4dbfa302',
    'account.1b8cb332342046a9990a3be67869acf2',
    'account.f067d098170b4ddaa65ba8fb306b3d68',
    'account.aa518adaec2940348fe07cdd690f1bcb',  # Asia_LYB_
    'account.3fe8dd4321804332b935f16e48e17bdc',  # CandyBB-_-
    'account.a1d1c5e0c6e8421b830711f98982a3d3',  # GFLYB_No9
}


def main():
    rng = random.Random(SEED)
    seeds_path = os.path.join(SEED_DIR, 'seeds.json')
    keep = []
    if os.path.exists(seeds_path):
        keep = [s for s in json.load(open(seeds_path, encoding='utf-8'))
                if not s['aid'].startswith('ai.')]
    have = {s['aid'] for s in keep}
    print(f"已有种子(剔除AI后): {len(keep)}, 需补采 {max(TARGET_TOTAL - len(keep), 0)}")

    matches = []  # (mid, date, map, [(aid, name), ...])
    for fp in glob.glob(CACHE_GLOB):
        d = json.load(open(fp, encoding='utf-8'))
        a = d['data']['attributes']
        if a.get('gameMode') != 'squad' or a.get('matchType') != 'official':
            continue
        pids = {p['id']: p['attributes']['stats'] for p in d.get('included', [])
                if p['type'] == 'participant'}
        if len(pids) < 40:
            continue
        b = datetime.fromisoformat(a['createdAt'].replace('Z', '+00:00')) + timedelta(hours=8)
        cands = [(p.get('playerId'), p.get('name')) for p in pids.values()
                 if p.get('playerId')
                 and not p['playerId'].startswith('ai.')  # 排除普通匹配里的 AI 机器人
                 and p['playerId'] not in EXCLUDE]
        if cands:
            matches.append((d['data']['id'], b.strftime('%m-%d'), a.get('mapName'), cands))

    print(f"符合口径的比赛: {len(matches)} 场")
    need = TARGET_TOTAL - len(keep)
    # 按 日期×地图 分层轮转，逐场轮流取 1 名（无放回），直到补齐
    cells = collections.defaultdict(list)
    for m in matches:
        cells[(m[1], m[2])].append(m)
    picked, order = [], sorted(cells)
    exhausted = False
    while len(picked) < need and not exhausted:
        progressed = False
        for c in order:
            if len(picked) >= need:
                break
            pool = cells[c]
            if not pool:
                continue
            mi = rng.randrange(len(pool))
            mid, date, map_, cands = pool[mi]
            cands = [x for x in cands if x[0] not in have]
            if not cands:
                pool.pop(mi)
                continue
            aid, name = cands.pop(rng.randrange(len(cands)))
            have.add(aid)
            picked.append({'aid': aid, 'name': name, 'source_mid': mid,
                           'date': date, 'map': map_})
            if not cands:
                pool.pop(mi)
            progressed = True
        exhausted = not progressed
    seeds = keep + picked
    per_match = collections.Counter(s['source_mid'] for s in seeds)
    print(f"种子总量: {len(seeds)} 人（覆盖 {len({s['date'] for s in seeds})} 个日期, "
          f"{len({s['map'] for s in seeds})} 张地图, 单场最多 {max(per_match.values())} 人）")
    json.dump(seeds, open(seeds_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)


if __name__ == '__main__':
    main()
