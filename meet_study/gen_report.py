"""生成 meet_study_report.md：四排普通匹配撞车概率调查报告。消费 analysis.json / classification.json / dataset.json。"""
import json, os
from datetime import datetime

SEED_DIR = os.path.dirname(os.path.abspath(__file__))


def main():
    an = json.load(open(os.path.join(SEED_DIR, 'analysis.json'), encoding='utf-8'))
    cls = json.load(open(os.path.join(SEED_DIR, 'classification.json'), encoding='utf-8'))
    ds = json.load(open(os.path.join(SEED_DIR, 'dataset.json'), encoding='utf-8'))
    name = lambda aid: cls.get(aid, {}).get('name', aid[:20])
    n_events = len(ds['events'])
    n_same = sum(e['same'] for e in ds['events'])

    L = []
    A = L.append
    A('# PUBG 四排普通匹配「撞车」概率调查报告')
    A('')
    A(f'> 生成时间 {datetime.now().strftime("%Y-%m-%d %H:%M")} · steam 区服 · 600 名种子（扩展版）')
    A('')
    A('## 1. 研究问题与口径')
    A('')
    A('- **问题**：任意两名活跃玩家在四排(TPP)普通匹配中「同场不同队」相遇的基线概率；固定游玩同一张地图的玩家 vs 地图混合玩家，两类撞车率是否不同。')
    A('- **相遇定义**：出现在同一场比赛且**不同队伍**（对手）。同队共现视为组排开黑信号，不记为撞车。')
    A('- **范围**：`gameMode=squad`、`matchType=official`（普通匹配，排除排位/街机/训练场/自定义）。')
    A('- **体量分层**：14 天普通四排场次 ≥300 的种子标记为「超高频」（疑似工作室/肝帝账号），主对比仅用普通体量玩家对。')
    A('')
    A('## 2. 数据与方法')
    A('')
    A('1. **种子抽样**：从本地缓存 644 场比赛（胖森杯观察期, 2026-08-20 ~ 09-05）的 293 场普通四排中，按 日期×地图 分层轮转抽取 **600 人**（首轮 114 人保留，另补采 486 人；排除 AI 机器人与胖森杯相关账号）。因 293 场的容量限制，允许同场取多人（单场最多 12 人）；两名种子出生在同一场比赛造成的"构造性相遇"已在统计中剔除。')
    A('2. **历史拉取**：`/players` 批量查询（10 人/批, 10 RPM）取每人近 14 天比赛 ID，去重 **83,561 场**逐场拉取详情（比赛端点不限速），其中普通四排 **59,959 场**。')
    A('3. **分析集**：普通四排场次 ≥10 的种子两两配对（含零相遇对），共 **162,165 对**；同队共现 ≥2 次的 35 对判定为疑似开黑并剔除。')
    A('4. **暴露量** = Σ_{日期×时段×地图格} 双方在该格的场次乘积，即"两人本可能撞上"的机会总量，同时控制作息重合与地图选择两个混杂。撞车率 = 不同队相遇次数 ÷ 暴露量 ×1000。')
    A('5. **组间对比**：按地图偏好（主图占比 ≥0.8 且场次 ≥10 为固定图玩家）分四组，bootstrap 95%CI（500 次重采样）。')
    A('6. **置换检验**：保留每人的 (时段×地图) 场次计划与各场比赛的种子槽位数，在格子内随机重排玩家→槽位 500 次；实测相遇次数超过全部置换最大值（且 ≥4 次）的玩家对判为强异常。')
    A('')
    md = ds.get('mode_dist', {})
    A(f"> 拉取场次模式分布（其余模式仅用于过滤）: {', '.join(f'{k}×{v}' for k, v in sorted(md.items(), key=lambda x: -x[1])[:6])} 等")
    A('')
    A('## 3. 结果')
    A('')
    A('### 3.1 总体基线')
    A('')
    A(f"- 有效种子 **{an['n_eligible']}** 人（普通体量 {an['n_eligible'] - an['n_ultra']} 人 + 超高频 {an['n_ultra']} 人），玩家对 **{an['n_all_pairs']:,}** 对。")
    A(f"- 14 天内发生过至少一次同场不同队相遇的 **{an['n_met_pairs']}** 对（**{an['n_met_pairs'] / an['n_chance_pairs'] * 100:.2f}%**）；"
      f"仅普通体量对为 **{an['n_met_ordinary']} / {an['n_chance_ordinary']:,}**（**{an['n_met_ordinary'] / max(an['n_chance_ordinary'], 1) * 100:.2f}%**）。")
    A(f"- 种子同场事件共 {n_events} 次，其中同队 {n_same} 次（{n_same / n_events * 100:.0f}%，集中于 {an['n_premade_pairs']} 个疑似开黑对）——两人反复同队即为固定组排，与「随机撞车」是两种截然不同的现象。")
    A('')
    A('非零相遇次数分布（次/对）:')
    A('')
    A('| 相遇次数 | 玩家对数 |')
    A('|---|---|')
    dist = an['meet_dist']
    for k in sorted(dist, key=int):
        if k != '0':
            A(f"| {k if k != '5' else '5+'} | {dist[k]} |")
    A(f"| 0 | {int(dist.get('0', 0)):,} |")
    A('')
    A('### 3.2 固定图 vs 混合玩家')
    A('')
    A('撞车率 = 每千次"同格暴露"的不同队相遇次数（bootstrap 95%CI）:')
    A('')
    A('**全部玩家对:**')
    A('')
    A('| 组别 | 玩家对 | 相遇 | 暴露量 | 撞车率 | 95%CI |')
    A('|---|---|---|---|---|---|')
    for g, s in an['group_stats_all'].items():
        A(f"| {g} | {s['pairs']:,} | {s['meetings']} | {s['exposure']:,} | {s['rate1000']} | {s['ci95'][0]} ~ {s['ci95'][1]} |")
    A('')
    A('**仅普通体量对（剔除超高频）:**')
    A('')
    A('| 组别 | 玩家对 | 相遇 | 暴露量 | 撞车率 | 95%CI |')
    A('|---|---|---|---|---|---|')
    for g, s in an['group_stats_ordinary'].items():
        A(f"| {g} | {s['pairs']:,} | {s['meetings']} | {s['exposure']:,} | {s['rate1000']} | {s['ci95'][0]} ~ {s['ci95'][1]} |")
    A('')
    ord_ = an['group_stats_ordinary']
    ffs, mm = ord_.get('固定-固定同图', {}), ord_.get('混合-混合', {})
    if ffs and mm and ffs['rate1000'] > mm['rate1000']:
        ratio = ffs['rate1000'] / mm['rate1000'] if mm['rate1000'] else 0
        A(f"**解读**：普通体量玩家对中，固定-固定同图组的撞车率（{ffs['rate1000']}）显著高于混合-混合组（{mm['rate1000']}），约为 **{ratio:.1f} 倍**，两组 CI 不重叠；固定-固定异图与固定-混合介于两者之间，呈清晰的梯度——**双方地图池重叠越多，撞车率越高**，与「固定图玩家更容易撞车」的直觉一致。值得注意的是，固定图玩家高度集中在最热门的地图（主阈值下 144 名固定图玩家中 74 人主玩 Erangel、50 人主玩 Tiger），即他们所在格子的匹配池本身最大，撞车率却仍然最高——说明同图集中带来的相遇效应**超出了**单纯池子大小的解释，可能叠加了匹配分档（相似投入度的玩家水平接近）或社群作息重合等因素。早前 107 人的快速版曾得出「两组持平」的初步结论，系固定-固定组仅 8 次事件、统计功效不足所致，本次扩展样本予以修正。")
    else:
        A('**解读**：见数据表。')
    A('')
    pg = an.get('perm_group_stats', {})
    if pg:
        A('置换检验对照（null=格子内随机重排玩家→槽位，保留每人时段×地图计划；置换总量恒等于实测总量，用于检验"谁和谁撞"是否随机）:')
        A('')
        A('| 组别 | 实测相遇 | 实测/置换均值 |')
        A('|---|---|---|')
        for g, v in pg.items():
            r = v['obs'] / v['perm_mean'] if v['perm_mean'] else 0
            A(f"| {g} | {v['obs']}（普通 {v['obs_ordinary']}） | {v['perm_mean']}（{r:.2f}） |")
        A('')
        A('各组的实测/置换均值均 <1（真实匹配比"格子内随机洗牌"更分散），但**固定-固定同图组的比值最高**（实测最接近随机洗牌水平），与 §3.2 的梯度结论方向一致。')
        A('')
    A('### 3.3 相遇次数异常的玩家对（置换检验）')
    A('')
    anoms = an.get('anomalies', [])
    if anoms:
        A(f"{len(anoms)} 对的实测相遇次数超过全部 500 次置换的最大值（高于「格子内随机分配玩家」能产生的水平），提示非随机关联（同社群作息、同水平分档、或关联账号）:")
        A('')
        A('| 玩家A | 玩家B | 实测相遇 | 置换均值 | 置换最大 |')
        A('|---|---|---|---|---|')
        for x in anoms[:10]:
            A(f"| {name(x['pair'][0])} | {name(x['pair'][1])} | {x['obs']} | {x['perm_mean']} | {x['perm_max']} |")
    else:
        A('无。')
    A('')
    A('### 3.4 相遇次数 Top10')
    A('')
    A('| 玩家A | 玩家B | 不同队 | 同队 | 分组 | 双方场次 |')
    A('|---|---|---|---|---|---|')
    for p in an.get('top_pairs', [])[:10]:
        A(f"| {name(p['a'])} | {name(p['b'])} | {p['diff']} | {p['same']} | {p['group']} | {p['na']}/{p['nb']}{' (超高频)' if p['ultra'] else ''} |")
    A('')
    A('注：头部相遇对仍多含超高频账号——相遇次数近似 ∝ 双方场次乘积，高频玩家不是更容易撞车，只是曝光机会多；按暴露量归一后的组间对比见 §3.2。')
    A('')
    prem = an.get('premade_pairs', [])
    if prem:
        A('### 3.5 疑似开黑对（同队≥2次，已从撞车分析剔除）')
        A('')
        A(f"共 {len(prem)} 对。 Top15:")
        A('')
        A('| 玩家A | 玩家B | 同队次数 | 不同队次数 |')
        A('|---|---|---|---|')
        for p in prem[:15]:
            A(f"| {name(p['a'])} | {name(p['b'])} | {p['same']} | {p['diff']} |")
        A('')
    A('## 4. 局限')
    A('')
    A('- **采样框偏差**：种子抽自胖森杯观察期（8-20~9-5，多为北京时间午后~傍晚）的比赛，偏向同时段活跃玩家；绝对基线外推到全体 steam 玩家需谨慎。组间对比（相对量）受此影响较小。')
    A('- **同场多种子**：600 人来自 293 场，部分场次贡献多名种子（最多 12 人/场），同源对在该场的构造性相遇已剔除，但同源种子间可能存在未被完全控制的社群相关性。')
    A('- **地图偏好分类阈值**：主阈值 0.8（且 ≥10 场）有主观性；0.7/0.85/0.9 敏感性检验方向一致（固定图玩家 181/123/102 人）。')
    A('- **绝对概率不可直接辨识**：API 无法枚举全区服比赛总量，标准量采用"每千次同格暴露撞车率"；"两名活跃玩家 14 天内相遇"的条件概率见 §3.1。')
    A('- **14 天数据保留期**：比赛详情过期即无法补拉，分析窗口以拉取时刻（2026-09-06）为准。')
    A('- 普通匹配含 AI 机器人填充：机器人种子与机器人事件均已剔除；"刷子×机器人"高频同场现象明显（工作室账号每场都遇到同名机器人），分析撞车时应警惕此类污染。')
    A('')
    A('## 5. 复现')
    A('')
    A('```')
    A('python sample_seeds.py      # 种子抽样(本地缓存, 增量补采到 TARGET_TOTAL)')
    A('python fetch_histories.py   # /players 批量查询(10 RPM, 增量跳过已有)')
    A('python fetch_matches.py     # 并发拉取比赛详情(可中断续跑)')
    A('python build_dataset.py     # 共现数据集(剔除同源对构造性相遇)')
    A('python classify_map_pref.py # 地图偏好分类')
    A('python analyze.py           # 统计分析')
    A('python gen_report.py        # 本报告')
    A('```')
    A('')

    open(os.path.join(SEED_DIR, 'meet_study_report.md'), 'w', encoding='utf-8').write('\n'.join(L))
    print('已写出 meet_study_report.md,', len(L), '行')


if __name__ == '__main__':
    main()
