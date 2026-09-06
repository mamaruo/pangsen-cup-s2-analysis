"""统计分析：种子玩家两两「同场不同队」撞车率 + 固定图/混合玩家分组对比。

口径：
- 相遇 = 同场比赛且不同队；同队≥2 次的对判定为疑似开黑，从随机撞车分析中剔除。
- 分析集 = 双方普通四排场次均 ≥ MIN_MATCHES 的种子对。
- 暴露量 exposure(对) = Σ_{日期×时段×地图格} m_a(格)×m_b(格)，
  即"两人本可能撞上"的机会总量，同时控制作息重合与地图选择两个混杂。
- 体量分层：任一方场次 ≥ ULTRA_N 的对归入「超高频」(疑似工作室/肝帝账号)，主对比只看普通对。
- 分组：固定-固定同图 / 固定-固定异图 / 固定-混合 / 混合-混合，bootstrap 95%CI。
- 置换检验：保留每人的 (时段,地图,场次) 结构，在格子内随机重排玩家→比赛槽位，
  得到玩家对相遇次数的 null 分布，用于标记异常对。
输出 analysis.json。
"""
import json, os, random, collections, itertools

SEED_DIR = os.path.dirname(os.path.abspath(__file__))
MIN_MATCHES = 10   # 进入分析的最少普通四排场次
ULTRA_N = 300      # 超高频阈值(14天普通四排场次)
MIN_BOOTS = 500    # bootstrap 重采样次数(大样本下组内对数很大, 500 次足够)
N_PERM = 500       # 置换检验次数
RNG_SEED = 20260906


def main():
    rng = random.Random(RNG_SEED)
    ds = json.load(open(os.path.join(SEED_DIR, 'dataset.json'), encoding='utf-8'))
    cls = json.load(open(os.path.join(SEED_DIR, 'classification.json'), encoding='utf-8'))
    matches, events = ds['matches'], ds['events']

    # 每种子每格子场次
    cell_cnt = {}
    for aid, mids in ds['seed_match'].items():
        c = collections.Counter()
        for m in mids:
            if m in matches:
                mt = matches[m]
                c[(mt['date'], mt['daypart'], mt['map'])] += 1
        cell_cnt[aid] = c
    n_of = {aid: sum(c.values()) for aid, c in cell_cnt.items()}
    eligible = {aid for aid, n in n_of.items() if n >= MIN_MATCHES}
    ultra = {aid for aid in eligible if n_of[aid] >= ULTRA_N}

    # 玩家对: 同队/不同队计数
    pair_cnt = collections.defaultdict(lambda: [0, 0])
    for e in events:
        a, b = sorted(e['pair'])
        if a in eligible and b in eligible:
            pair_cnt[(a, b)][e['same']] += 1

    def exposure(a, b):
        ca, cb = cell_cnt[a], cell_cnt[b]
        return sum(v * cb[k] for k, v in ca.items() if k in cb)

    def group_of(a, b):
        fa, fb = cls[a]['fixed']['0.8'], cls[b]['fixed']['0.8']
        if fa and fb:
            return '固定-固定同图' if cls[a]['top_map'] == cls[b]['top_map'] else '固定-固定异图'
        if fa or fb:
            return '固定-混合'
        return '混合-混合'

    pairs = []
    for a, b in itertools.combinations(sorted(eligible), 2):  # 全部对,含零相遇
        diff_n, same_n = pair_cnt.get((a, b), [0, 0])
        pairs.append({'a': a, 'b': b, 'same': same_n, 'diff': diff_n,
                      'exposure': exposure(a, b), 'group': group_of(a, b),
                      'ultra': a in ultra or b in ultra,
                      'na': n_of[a], 'nb': n_of[b]})

    # --- 总体基线 ---
    n_eligible = len(eligible)
    n_all_pairs = n_eligible * (n_eligible - 1) // 2
    premade = [p for p in pairs if p['same'] >= 2]
    chance_pairs = [p for p in pairs if p['same'] < 2]
    ordinary = [p for p in chance_pairs if not p['ultra']]
    met = [p for p in chance_pairs if p['diff'] >= 1]
    dist = collections.Counter(min(p['diff'], 5) for p in chance_pairs)

    # --- 分组撞车率 (每千次暴露) + bootstrap CI ---
    def group_stats(gs):
        gs_by = collections.defaultdict(list)
        for p in gs:
            gs_by[p['group']].append(p)
        out = {}
        for g, lst in sorted(gs_by.items()):
            td = sum(p['diff'] for p in lst)
            te = sum(p['exposure'] for p in lst)
            r = td / te * 1000 if te else 0.0
            boots = []
            for _ in range(MIN_BOOTS):
                s = [lst[rng.randrange(len(lst))] for _ in lst]
                e = sum(p['exposure'] for p in s)
                if e:
                    boots.append(sum(p['diff'] for p in s) / e * 1000)
            boots.sort()
            out[g] = {'pairs': len(lst), 'meetings': td, 'exposure': te,
                      'rate1000': round(r, 4),
                      'ci95': [round(boots[int(0.025 * len(boots))], 4),
                               round(boots[int(0.975 * len(boots))], 4)] if boots else None}
        return out

    g_all = group_stats(chance_pairs)
    g_ord = group_stats(ordinary)

    # --- 置换检验：格子内重排玩家→槽位 ---
    # instances[aid] = [(cell, mid), ...]；每格子内把玩家标签随机重排到槽位集合上，
    # 槽位数=玩家实例数，保留每人的 (时段,地图) 场次计划，只打乱"谁打哪场比赛"。
    instances = collections.defaultdict(list)
    for aid in eligible:
        for m in ds['seed_match'][aid]:
            if m in matches:
                mt = matches[m]
                instances[aid].append(((mt['date'], mt['daypart'], mt['map']), m))
    slot_mult = collections.defaultdict(dict)
    for aid, inst in instances.items():
        for cell, mid in inst:
            slot_mult[cell][mid] = slot_mult[cell].get(mid, 0) + 1
    cnt_cell = {aid: collections.Counter(c for c, _ in inst) for aid, inst in instances.items()}

    def perm_fast():
        meets = collections.Counter()
        for cell, sm in slot_mult.items():
            slots = []
            for mid, n in sm.items():
                slots += [mid] * n
            players = []
            for aid, cc in cnt_cell.items():
                n = cc.get(cell, 0)
                if n:
                    players += [aid] * n
            if len(players) < 2:
                continue
            rng.shuffle(players)
            by_mid = collections.defaultdict(list)
            for aid, mid in zip(players, slots):
                by_mid[mid].append(aid)
            for mid, aids in by_mid.items():
                for x, y in itertools.combinations(sorted(aids), 2):
                    meets[(x, y)] += 1
        return meets

    perm_pair = collections.defaultdict(list)
    perm_group = collections.defaultdict(list)
    for _ in range(N_PERM):
        mt = perm_fast()
        for pk, v in mt.items():
            perm_pair[pk].append(v)
        gcnt = collections.Counter()
        for pk, v in mt.items():
            gcnt[group_of(*pk)] += v
        for g, v in gcnt.items():
            perm_group[g].append(v)

    obs_pair = {f"{p['a']}|{p['b']}": p['diff'] for p in pairs}
    anomalies = []
    for pk, vals in perm_pair.items():
        obs = obs_pair.get(f"{pk[0]}|{pk[1]}", 0)
        mu = sum(vals) / len(vals)
        if obs >= 4 and obs > max(vals):  # 大样本下 obs>=4 才视为强异常
            anomalies.append({'pair': list(pk), 'obs': obs, 'perm_mean': round(mu, 3),
                              'perm_max': max(vals)})
    anomalies.sort(key=lambda x: -x['obs'])
    perm_group_stats = {}
    for g in g_all:
        gs_g = [p for p in chance_pairs if p['group'] == g]
        vs = perm_group.get(g, [0])
        perm_group_stats[g] = {'obs': sum(p['diff'] for p in gs_g),
                               'obs_ordinary': sum(p['diff'] for p in ordinary if p['group'] == g),
                               'perm_mean': round(sum(vs) / len(vs), 2)}

    seed_table = [{'aid': aid, 'name': cls[aid]['name'], 'n': n_of[aid],
                   'volume': '超高频' if aid in ultra else '普通',
                   'top_map': cls[aid]['top_map'], 'top_share': cls[aid]['top_share'],
                   'fixed': cls[aid]['fixed']['0.8']}
                  for aid in sorted(eligible, key=lambda x: -n_of[x])]

    out = {'n_seeds': len(ds['seed_match']), 'n_eligible': n_eligible,
           'n_ultra': len(ultra), 'ultra_n': ULTRA_N, 'min_matches': MIN_MATCHES,
           'n_all_pairs': n_all_pairs, 'n_premade_pairs': len(premade),
           'n_chance_pairs': len(chance_pairs), 'n_chance_ordinary': len(ordinary),
           'n_met_pairs': len(met),
           'n_met_ordinary': sum(1 for p in ordinary if p['diff'] >= 1),
           'meet_dist': {str(k): v for k, v in sorted(dist.items())},
           'group_stats_all': g_all, 'group_stats_ordinary': g_ord,
           'perm_group_stats': perm_group_stats,
           'anomalies': anomalies[:20],
           'top_pairs': sorted(pairs, key=lambda x: -x['diff'])[:20],
           'premade_pairs': [{'a': p['a'], 'b': p['b'], 'same': p['same'], 'diff': p['diff']}
                             for p in premade],
           'seed_table': seed_table}
    json.dump(out, open(os.path.join(SEED_DIR, 'analysis.json'), 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1)

    print(f"有效种子 {n_eligible} (超高频 {len(ultra)}), 全部对 {n_all_pairs}, "
          f"疑似开黑对 {len(premade)} (剔除), 随机撞车分析对 {len(chance_pairs)} "
          f"(普通 {len(ordinary)})")
    print(f"发生过相遇的对: {len(met)} ({len(met) / max(len(chance_pairs), 1) * 100:.2f}%) | "
          f"普通对: {out['n_met_ordinary']} ({out['n_met_ordinary'] / max(len(ordinary), 1) * 100:.2f}%)")
    print("\n分组撞车率 (次/千暴露, bootstrap 95%CI) — 全部对:")
    for g, s in g_all.items():
        print(f"  {g}: {s['rate1000']}  CI{s['ci95']}  (对数 {s['pairs']}, 相遇 {s['meetings']})")
    print("— 仅普通对(剔除超高频):")
    for g, s in g_ord.items():
        print(f"  {g}: {s['rate1000']}  CI{s['ci95']}  (对数 {s['pairs']}, 相遇 {s['meetings']})")
    print("\n置换检验组均值 vs 实测:", perm_group_stats)
    print(f"\n异常对 (obs>perm_max 且 obs>=2): {len(anomalies)}")
    for a in anomalies[:5]:
        print(' ', a)


if __name__ == '__main__':
    main()
