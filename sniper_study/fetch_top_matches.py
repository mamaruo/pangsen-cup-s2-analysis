"""并发拉取 top 嫌疑人(n>=3)的非杯赛比赛详情到 sniper_study/cache_top/。"""
import json, os, time, threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import urllib.request

DIR = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(DIR, 'cache_top')
WORKERS = 12
TIMEOUT = 60
_lock = threading.Lock()
ok = fail = 0

def fetch_one(mid):
    fp = os.path.join(CACHE, f'match_{mid}.json')
    if os.path.exists(fp): return 'skip'
    url = f"https://api.pubg.com/shards/steam/matches/{mid}"
    req = urllib.request.Request(url, headers={'Accept': 'application/vnd.api+json', 'Accept-Encoding': 'gzip'})
    for attempt in range(6):
        try:
            with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
                raw = r.read()
            if raw[:2] == b'\x1f\x8b':
                import gzip; raw = gzip.decompress(raw)
            tmp = fp + '.tmp'
            with open(tmp, 'wb') as f: f.write(raw)
            os.replace(tmp, fp)
            return 'ok'
        except urllib.error.HTTPError as e:
            if e.code == 404: return '404'
            time.sleep(min(2 ** attempt, 30))
        except Exception:
            time.sleep(min(2 ** attempt, 30))
    return 'fail'

def main():
    global ok, fail
    os.makedirs(CACHE, exist_ok=True)
    mids = json.load(open(os.path.join(DIR, 'top_match_ids.json')))
    todo = [m for m in mids if not os.path.exists(os.path.join(CACHE, f'match_{m}.json'))]
    print(f'待拉取 {len(todo)}', flush=True)
    with ThreadPoolExecutor(WORKERS) as ex:
        for i, r in enumerate(ex.map(fetch_one, todo), 1):
            with _lock:
                if r == 'ok': ok += 1
                elif r == 'fail': fail += 1
            if i % 500 == 0: print(f'{i}/{len(todo)} ok={ok} fail={fail}', flush=True)
    print(f'done ok={ok} fail={fail}')

if __name__ == '__main__':
    main()
