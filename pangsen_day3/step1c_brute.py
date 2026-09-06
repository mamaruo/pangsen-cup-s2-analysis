"""Day3 step1c: 歧义字符暴力枚举搜索"""
import sys, os, json, itertools
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from pangsen_day5.pubg import search_player

AMB = {'i': 'ilI1', 'l': 'lI1i', 'I': 'Il1i', '1': '1liI', 'o': 'o0O', 'O': 'O0o',
       '0': '0Oo', 'B': 'B8', '8': '8B', 'S': 'S5', '5': '5S', 'Z': 'Z2', '2': '2Z',
       'b': 'b8', 'g': 'g9', '9': '9g', 'q': 'q9', 'x': 'xX', 'X': 'Xx'}

def variants(name, max_comb=4000):
    pools = [AMB.get(c, c) for c in name]
    n = 1
    for p in pools:
        n *= len(p) if isinstance(p, str) else 1
    if n > max_comb:
        # 只替换 i/l/I/1 和 0/o/O
        pools = [({'i': 'ilI', 'l': 'lIi', 'I': 'Ili', '1': '1li', 'o': 'o0', 'O': 'O0',
                   '0': '0O'}.get(c, c)) for c in name]
    return (''.join(p) for p in itertools.product(*pools)), n

TARGETS = ['Asia_LYB_', 'CandyBB-_-', 'Meiguibb', 'weirdo_im', 'BigHead_XxHD', '2iDD']
found = {}
for t in TARGETS:
    gen, n = variants(t)
    print(f'--- {t} ({n} variants)', flush=True)
    hit = None
    batch = []
    def flush_batch():
        global batch
        if not batch: return
        try:
            names = ','.join(batch[:50])
            import urllib.parse
            from pangsen_day5.pubg import _get
            d = _get('https://api.pubg.com/shards/steam/players?filter[playerNames]=' + urllib.parse.quote(names))
            for p in d['data']:
                found[p['attributes']['name']] = p['id']
                print('HIT:', p['attributes']['name'], p['id'], flush=True)
        except Exception:
            pass
        batch = []
    for v in gen:
        batch.append(v)
        if len(batch) >= 50:
            flush_batch()
    flush_batch()
    if not found:
        print(t, '未命中', flush=True)

json.dump(found, open('day3_brute.json', 'w'), indent=1)
print(json.dumps(found, indent=1))
