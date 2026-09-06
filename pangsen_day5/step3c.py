import pubg, time
print('--- January_BiG matches ---')
for mid in pubg.player_matches('account.0a851679df5b4d91b4b831aa4dbfa302'):
    meta = pubg.match_meta(mid)
    if meta['created'] >= '2026-09-02T10:00':
        print('  ', meta['created'], meta['map'], mid)
    time.sleep(1.2)
