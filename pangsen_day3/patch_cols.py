# -*- coding: utf-8 -*-
"""给 day3/day4 报告脚本加 服务器/地图 两列"""
import io, os

BASE = os.path.dirname(os.path.abspath(__file__))
for fn in ('day3_report.py', os.path.join('..', 'pangsen_day4', 'day4_report.py')):
    p = os.path.normpath(os.path.join(BASE, fn))
    s = open(p, encoding='utf-8').read()
    if 'match_server' in s:
        print('skip(already)', p); continue
    s = s.replace("""    dtxt = f'9-{start.day} {start:%H:%M}'""",
                  """    dtxt = f'9-{start.day} {start:%H:%M}'
    server = pubg.match_server(mid)
    mapn = pubg.match_meta(mid)['map']""")
    s = s.replace("""    dtxt = f'{start.month}-{start.day} {start:%H:%M}'""",
                  """    dtxt = f'{start.month}-{start.day} {start:%H:%M}'
    server = pubg.match_server(mid)
    mapn = pubg.match_meta(mid)['map']""")
    s = s.replace("""    rows.append((start, f'| {dtxt} | {p1c}""",
                  """    rows.append((start, f'| {dtxt} | {server} | {mapn} | {p1c}""")
    s = s.replace("""       '| 日期时间 | 选手1 | 选手2 | 第一阶段有效击杀 | 第二阶段有效击杀 | 吃鸡 | 总积分 | 备注 | pubg.plus回放链接 |', '|---|---|---|---|---|---|---|---|---|']""",
                  """       '| 日期时间 | 服务器 | 地图 | 选手1 | 选手2 | 第一阶段有效击杀 | 第二阶段有效击杀 | 吃鸡 | 总积分 | 备注 | pubg.plus回放链接 |', '|---|---|---|---|---|---|---|---|---|---|---|']""")
    open(p, 'w', encoding='utf-8').write(s)
    print('patched', p)
