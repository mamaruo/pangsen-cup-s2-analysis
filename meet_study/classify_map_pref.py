"""地图偏好分类：按每名种子的普通四排地图分布，划分「固定图玩家」与「混合玩家」。

主阈值：主图占比 ≥0.8 且场次 ≥10 → 固定图；另对 0.7/0.85/0.9 做敏感性检验。
输出 classification.json + 控制台摘要。
"""
import json, os, collections

SEED_DIR = os.path.dirname(os.path.abspath(__file__))
THRESHOLDS = [0.7, 0.8, 0.85, 0.9]
MAIN_MIN = 10  # 分类最少场次


def main():
    ds = json.load(open(os.path.join(SEED_DIR, 'dataset.json'), encoding='utf-8'))
    matches, seed_match = ds['matches'], ds['seed_match']
    name_of = {s['aid']: s['name'] for s in
               json.load(open(os.path.join(SEED_DIR, 'seeds.json'), encoding='utf-8'))}

    out = {}
    for aid, mids in seed_match.items():
        maps = [matches[m]['map'] for m in mids if m in matches]
        n = len(maps)
        cnt = collections.Counter(maps)
        top_map, top_n = cnt.most_common(1)[0] if cnt else (None, 0)
        hhi = sum((c / n) ** 2 for c in cnt.values()) if n else 0
        # 单日多图行为：当日 ≥2 场时平均每天玩几张图
        by_day = collections.defaultdict(set)
        for m in mids:
            if m in matches:
                by_day[matches[m]['date']].add(matches[m]['map'])
        multi = [len(v) for v in by_day.values() if len(v) >= 2]
        out[aid] = {
            'name': name_of.get(aid, aid[:20]),
            'n': n,
            'top_map': top_map,
            'top_share': round(top_n / n, 3) if n else 0,
            'hhi': round(hhi, 3),
            'avg_maps_per_active_day': round(sum(multi) / len(multi), 2) if multi else None,
            'fixed': {t: bool(n >= MAIN_MIN and top_n / n >= t) for t in THRESHOLDS},
        }
    json.dump(out, open(os.path.join(SEED_DIR, 'classification.json'), 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1)

    print(f"{'阈值':>6} | 固定图 | 混合 | 场次不足")
    for t in THRESHOLDS:
        f = sum(1 for v in out.values() if v['fixed'][t])
        ins = sum(1 for v in out.values() if v['n'] < MAIN_MIN)
        print(f"{t:>6} | {f:>6} | {len(out) - f - ins:>4} | {ins:>8}")
    print("\n主阈值 0.8 下的固定图玩家地图分布:")
    print(' ', dict(collections.Counter(v['top_map'] for v in out.values() if v['fixed'][0.8])))
    top10 = sorted(out.items(), key=lambda kv: -kv[1]['top_share'])[:10]
    print("\n集中度 Top10:")
    for aid, v in top10:
        print(f"  {v['name']:<20} n={v['n']:>3} 主图={v['top_map']} 占比={v['top_share']:.2f} HHI={v['hhi']:.2f}")


if __name__ == '__main__':
    main()
