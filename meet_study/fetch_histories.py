"""拉取种子玩家近 14 天比赛列表：/shards/steam/players?filter[playerIds]=...（10 人/批，10 RPM 限速）。

失败批次自动降级为单查。输出 histories.json: {aid: {"name": 现用名, "match_ids": [...]}}（无比赛的种子不写入）。
"""
import json, sys, os, time

sys.path.insert(0, os.path.abspath(os.path.join('..', 'pangsen_day5')))
from pubg import _get  # 复用共享客户端（含 429 退避；key 取自 env PUBG_API_KEY）

SEED_DIR = os.path.dirname(os.path.abspath(__file__))
BATCH = 10          # 官方文档上限
SLEEP = 6.5         # 10 次/分钟 → 批间隔


def fetch_batch(ids):
    url = f"https://api.pubg.com/shards/steam/players?filter[playerIds]={','.join(ids)}"
    d = _get(url)
    out = {}
    for p in d.get('data', []):
        out[p['id']] = [m['id'] for m in p.get('relationships', {}).get('matches', {}).get('data', [])]
    return out


def main():
    seeds = json.load(open(os.path.join(SEED_DIR, 'seeds.json'), encoding='utf-8'))
    out_path = os.path.join(SEED_DIR, 'histories.json')
    histories = {}
    if os.path.exists(out_path):  # 增量：已有者不再查询
        histories = json.load(open(out_path, encoding='utf-8'))
    aids = [s['aid'] for s in seeds
            if s['aid'] not in histories and not s['aid'].startswith('ai.')]
    name_of = {s['aid']: s['name'] for s in seeds}
    print(f"待查询 {len(aids)} 人 (已有 {len(histories)} 人跳过)", flush=True)
    failed = []
    for i in range(0, len(aids), BATCH):
        batch = aids[i:i + BATCH]
        try:
            got = fetch_batch(batch)
        except Exception as e:
            print(f"批量失败({batch[0][:20]}...): {e}，降级单查", flush=True)
            got = {}
            for aid in batch:
                try:
                    got.update(fetch_batch([aid]))
                except Exception as e2:
                    print(f"  单查失败 {aid}: {e2}", flush=True)
                    failed.append(aid)
                time.sleep(2)
        for aid in batch:
            if aid in got:
                histories[aid] = {'name': name_of[aid], 'match_ids': got[aid]}
        print(f"[{i + len(batch)}/{len(aids)}] 累计有效 {len(histories)}", flush=True)
        time.sleep(SLEEP)
    print(f"完成: 本次查询 {len(aids)} 人失败 {len(failed)}, 历史表共 {len(histories)} 人")
    json.dump(histories, open(os.path.join(SEED_DIR, 'histories.json'), 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1)
    if failed:
        json.dump(failed, open(os.path.join(SEED_DIR, 'histories_failed.json'), 'w'))


if __name__ == '__main__':
    main()
