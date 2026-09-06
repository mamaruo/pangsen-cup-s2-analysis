"""构建共现数据集：扫描本地 cache/match_*.json，提取 squad+official(普通四排) 的
比赛属性（北京时间/地图/人数）与 roster 队伍分组，产出：

- dataset.json
  - matches:  {mid: {date, hour, map, k}}                      全部普通四排场次
  - seed_match: {aid: [mid, ...]}                              每个种子的普通四排场次
  - events:   [{mid, pair: [aidA, aidB], same: 0|1}]           种子两两同场事件(同队/不同队)
  - team_of:  {mid: {aid: teamId}}                             含≥2种子的场次的队伍归属(供置换检验)
  - mode_dist: 拉取的全部场次按 gameMode×matchType 分布(供报告口径说明)
"""
import json, glob, os, collections
from datetime import datetime, timedelta

SEED_DIR = os.path.dirname(os.path.abspath(__file__))


def daypart(hour):
    if hour < 8:
        return '凌晨'
    if hour < 17:
        return '白天'
    return '晚间'


def main():
    seeds = json.load(open(os.path.join(SEED_DIR, 'seeds.json'), encoding='utf-8'))
    seed_set = {s['aid'] for s in seeds if not s['aid'].startswith('ai.')}  # 排除 AI 机器人种子

    matches, seed_match = {}, collections.defaultdict(list)
    events, team_of = [], {}
    mode_dist = collections.Counter()
    # 同源对：两名种子出生在同一场比赛，该场的相遇是抽样构造的，不计入撞车
    source_of = {s['aid']: s['source_mid'] for s in seeds}
    for fp in glob.glob(os.path.join(SEED_DIR, 'cache', 'match_*.json')):
        mid = os.path.basename(fp)[6:-5]
        try:
            d = json.load(open(fp, encoding='utf-8'))
        except Exception as e:
            print('解析失败', fp, e)
            continue
        a = d['data']['attributes']
        mode_dist[f"{a['gameMode']}|{a['matchType']}"] += 1
        if a['gameMode'] != 'squad' or a['matchType'] != 'official':
            continue
        b = datetime.fromisoformat(a['createdAt'].replace('Z', '+00:00')) + timedelta(hours=8)
        parts = {p['id']: p['attributes']['stats'] for p in d['included'] if p['type'] == 'participant'}
        # roster → teamId
        t_of = {}
        for r in d['included']:
            if r['type'] != 'roster':
                continue
            tid = r['attributes']['stats']['teamId']
            for pr in r['relationships']['participants']['data']:
                st = parts.get(pr['id'])
                if st and st.get('playerId'):
                    t_of[st['playerId']] = tid
        k = len(parts)
        matches[mid] = {'date': b.strftime('%m-%d'), 'hour': b.hour, 'daypart': daypart(b.hour),
                        'map': a['mapName'], 'k': k}
        seeds_here = [pid for pid in t_of if pid in seed_set]
        for aid in seeds_here:
            seed_match[aid].append(mid)
        if len(seeds_here) >= 2:
            team_of[mid] = {aid: t_of[aid] for aid in seeds_here}
            for i in range(len(seeds_here)):
                for j in range(i + 1, len(seeds_here)):
                    x, y = seeds_here[i], seeds_here[j]
                    if source_of.get(x) == mid and source_of.get(y) == mid:
                        continue  # 同源对的构造性相遇
                    events.append({'mid': mid, 'pair': [x, y],
                                   'same': int(t_of[x] == t_of[y])})

    ds = {'matches': matches,
          'seed_match': dict(seed_match),
          'events': events,
          'team_of': team_of,
          'mode_dist': dict(mode_dist)}
    json.dump(ds, open(os.path.join(SEED_DIR, 'dataset.json'), 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1)
    diff = sum(1 for e in events if not e['same'])
    print(f"普通四排场次 {len(matches)}, 种子-场次对 {sum(len(v) for v in seed_match.values())}, "
          f"种子同场事件 {len(events)} (不同队 {diff}, 同队 {len(events) - diff}), "
          f"含≥2种子场次 {len(team_of)}")
    print("拉取场次模式分布:", dict(mode_dist.most_common()))


if __name__ == '__main__':
    main()
