"""PUBG API client with disk cache - 胖森杯S2 Day5 pipeline"""
import json, os, urllib.request, urllib.parse, gzip, time

KEY = os.environ['PUBG_API_KEY']
BASE = 'https://api.pubg.com'
CACHE = os.path.join(os.path.dirname(__file__), 'cache')
os.makedirs(CACHE, exist_ok=True)

def _get(url):
    req = urllib.request.Request(url, headers={
        'Authorization': 'Bearer ' + KEY, 'Accept': 'application/vnd.api+json'})
    last = None
    for attempt in range(8):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                data = r.read()
                if data[:2] == b'\x1f\x8b':
                    data = gzip.decompress(data)
                return json.loads(data)
        except urllib.error.HTTPError as e:
            last = e
            if e.code == 429:
                time.sleep(6 + 3 * attempt); continue
            if e.code >= 500:
                time.sleep(2 + attempt); continue
            raise
        except Exception as e:
            last = e
            time.sleep(2 + attempt)
    raise last

def search_player(name):
    q = urllib.parse.quote(name)
    try:
        d = _get(f'{BASE}/shards/steam/players?filter[playerNames]={q}')
        return [(p['id'], p['attributes']['name']) for p in d['data']]
    except Exception:
        return []

def player_matches(account_id):
    d = _get(f'{BASE}/shards/steam/players/{account_id}')
    node = d['data'][0] if isinstance(d['data'], list) else d['data']
    return [m['id'] for m in node['relationships']['matches']['data']]

def match(mid, force=False):
    fp = os.path.join(CACHE, f'match_{mid}.json')
    if force or not os.path.exists(fp):
        json.dump(_get(f'{BASE}/shards/steam/matches/{mid}'), open(fp, 'w'))
    return json.load(open(fp))

def telemetry(mid, force=False):
    fp = os.path.join(CACHE, f'tel_{mid}.json')
    if force or not os.path.exists(fp):
        m = match(mid)
        asset = [x for x in m['included'] if x['type'] == 'asset'][0]
        req = urllib.request.Request(asset['attributes']['URL'])
        raw = urllib.request.urlopen(req, timeout=120).read()
        if raw[:2] == b'\x1f\x8b': raw = gzip.decompress(raw)
        json.dump(json.loads(raw), open(fp, 'w'))
    return json.load(open(fp))

def rosters(mid):
    """squad list: [{rank, members:[{name,pid,surv,kills,place,dmg}]}]"""
    m = match(mid)
    parts = {x['id']: x['attributes']['stats'] for x in m['included'] if x['type'] == 'participant'}
    out = []
    for r in [x for x in m['included'] if x['type'] == 'roster']:
        ms = []
        for pid in r['relationships']['participants']['data']:
            s = parts[pid['id']]
            ms.append(dict(name=s['name'], pid=s['playerId'], surv=s['timeSurvived'],
                           kills=s['kills'], place=s['winPlace'], dmg=round(s['damageDealt'],1)))
        ms.sort(key=lambda x: -x['surv'])
        out.append(dict(rank=r['attributes'].get('stats', {}).get('rank'), members=ms))
    out.sort(key=lambda r: r['rank'] or 99)
    return out

def kills_of(mid, name):
    """LogPlayerKillV2 where killer==name"""
    tel = telemetry(mid)
    out = []
    for e in tel:
        if e['_T'] == 'LogPlayerKillV2' and (e.get('killer') or {}).get('name') == name:
            kdi = e.get('killerDamageInfo') or {}
            out.append(dict(t=e['_D'], victim=(e.get('victim') or {}).get('name'),
                            weapon=kdi.get('damageCauserName'), reason=kdi.get('damageReason')))
    return sorted(out, key=lambda x: x['t'])

def death_of(mid, name):
    tel = telemetry(mid)
    for e in tel:
        if e['_T'] == 'LogPlayerKillV2' and (e.get('victim') or {}).get('name') == name:
            k = e.get('killer') or {}
            kdi = e.get('killerDamageInfo') or {}
            return dict(t=e['_D'], killer=k.get('name'), weapon=kdi.get('damageCauserName'))
    return None

def phase2_time(mid):
    tel = telemetry(mid)
    for e in tel:
        if e['_T'] == 'LogPhaseChange' and e.get('phase') == 2:
            return e['_D']
    return None

def match_start(mid):
    tel = telemetry(mid)
    for e in tel:
        if e['_T'] == 'LogMatchStart':
            return e['_D']
    return None


# ---- 地图映射(来源: trevoedwards/pubg-api-assets dictionaries/telemetry/mapName.json) ----
_MAP_CN = {
    'Erangel (Remastered)': '艾伦格',
    'Erangel': '艾伦格', 'Miramar': '米拉玛', 'Taego': '泰戈', 'Rondo': '荣都',
    'Deston': '帝斯顿', 'Vikendi': '维寒迪', 'Karakin': '卡拉金', 'Sanhok': '萨诺',
    'Paramo': '帕拉莫', 'Haven': '避难所', 'Camp Jackal': '训练岛',
}
try:
    _MAP_RAW = json.load(open(os.path.join(os.path.dirname(__file__), 'mapName.json'), encoding='utf-8'))
except Exception:
    _MAP_RAW = {}

def map_name(raw):
    """API 地图代码 -> 中文名,未知的原样返回"""
    en = _MAP_RAW.get(raw, raw)
    return _MAP_CN.get(en, en)

def match_meta(mid):
    a = match(mid)['data']['attributes']
    return dict(created=a['createdAt'], map=map_name(a['mapName']), map_raw=a['mapName'], mode=a['gameMode'])

def match_server(mid):
    """从 telemetry LogMatchDefinition 的 MatchId 解析服务器区域代码(official.pc-2018-42.steam.squad.as.2026... 的 as),直接返回 AS/SEA 等原码"""
    for e in telemetry(mid):
        if e['_T'] == 'LogMatchDefinition':
            for p in (e.get('MatchId') or '').split('.'):
                if len(p) <= 5 and p.isalpha() and p in ('as', 'na', 'eu', 'sa', 'oc', 'sea', 'kr', 'jp', 'kakao'):
                    return p.upper()
            return '未知'
    return '未知'
