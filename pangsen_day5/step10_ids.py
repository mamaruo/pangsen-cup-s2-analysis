import pubg, time, json
for mid in pubg.player_matches('account.0948de9e482b4d65abd9362281a04f3e'):
    if mid[:8] in ('89c96bcc','a3f7dcd7'):
        print(mid)
    time.sleep(1)
