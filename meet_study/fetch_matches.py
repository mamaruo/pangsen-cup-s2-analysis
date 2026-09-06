"""批量拉取种子比赛列表去重后的全部比赛详情到本地 cache/match_{id}.json。

比赛端点官方不限速、无需鉴权，用多线程拉取；429/5xx 指数退避。可中断重跑（跳过已存在）。
输出: cache/*.json + fetch_log.json (成功/404 失败列表)。
"""
import json, sys, os, time, threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import urllib.request

SEED_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(SEED_DIR, 'cache')
WORKERS = 10
TIMEOUT = 60

_lock = threading.Lock()
ok_count = fail_count = 0
failed_ids = []


def fetch_one(mid):
    fp = os.path.join(CACHE, f'match_{mid}.json')
    if os.path.exists(fp):
        return 'skip'
    url = f"https://api.pubg.com/shards/steam/matches/{mid}"
    req = urllib.request.Request(url, headers={
        'Accept': 'application/vnd.api+json',
        'Accept-Encoding': 'gzip',
    })
    for attempt in range(6):
        try:
            with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
                raw = r.read()
            if raw[:2] == b'\x1f\x8b':
                import gzip
                raw = gzip.decompress(raw)
            tmp = fp + '.tmp'
            with open(tmp, 'wb') as f:
                f.write(raw)
            os.replace(tmp, fp)
            return 'ok'
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return '404'
            time.sleep(min(2 ** attempt, 30))
        except Exception:
            time.sleep(min(2 ** attempt, 30))
    return 'fail'


def main():
    global ok_count, fail_count
    os.makedirs(CACHE, exist_ok=True)
    histories = json.load(open(os.path.join(SEED_DIR, 'histories.json'), encoding='utf-8'))
    mids = sorted({m for v in histories.values() for m in v['match_ids']})
    todo = [m for m in mids if not os.path.exists(os.path.join(CACHE, f'match_{m}.json'))]
    print(f"种子比赛去重后共 {len(mids)} 场, 已缓存 {len(mids) - len(todo)}, 待拉取 {len(todo)}", flush=True)
    t0 = time.time()
    with ThreadPoolExecutor(WORKERS) as ex:
        futs = {ex.submit(fetch_one, m): m for m in todo}
        for i, fut in enumerate(as_completed(futs), 1):
            r = fut.result()
            with _lock:
                if r == 'fail':
                    failed_ids.append(futs[fut])
                elif r == '404':
                    failed_ids.append(futs[fut])
                else:
                    ok_count += 1
            if i % 100 == 0 or i == len(todo):
                rate = i / max(time.time() - t0, 1)
                print(f"[{i}/{len(todo)}] {rate:.1f} 场/秒, 失败 {len(failed_ids)}, "
                      f"耗时 {int(time.time() - t0)}s", flush=True)
    print(f"完成: 新拉取 {ok_count}, 失败/404 {len(failed_ids)}")
    json.dump(sorted(set(failed_ids)), open(os.path.join(SEED_DIR, 'fetch_log.json'), 'w'))


if __name__ == '__main__':
    main()
