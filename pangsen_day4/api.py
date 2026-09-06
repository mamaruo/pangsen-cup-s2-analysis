import json, os, sys, urllib.request, urllib.parse, gzip, io

KEY = os.environ['PUBG_API_KEY']
BASE = 'https://api.pubg.com'

def get(url):
    req = urllib.request.Request(url, headers={
        'Authorization': 'Bearer ' + KEY,
        'Accept': 'application/vnd.api+json'})
    with urllib.request.urlopen(req) as r:
        data = r.read()
        if r.headers.get('Content-Encoding') == 'gzip' or data[:2] == b'\x1f\x8b':
            data = gzip.decompress(data)
        return json.loads(data)

if __name__ == '__main__':
    names = sys.argv[1].split(',')
    q = urllib.parse.quote(','.join(names))
    d = get(f'{BASE}/shards/steam/players?filter[playerNames]={q}')
    for p in d['data']:
        print(p['id'], p['attributes']['name'])
        for m in p['relationships']['matches']['data'][:15]:
            print('  ', m['id'], m['type'])
