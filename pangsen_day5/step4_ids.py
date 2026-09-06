import pubg, time, json
accounts = ['account.0a851679df5b4d91b4b831aa4dbfa302',
            'account.daa1fc4c60ca4aa082584a0a048839f4',
            'account.c416e2e00b254f57aa9ac5e8b46c8ef6',
            'account.a7d05690ea23400498ae0e325f290f15',
            'account.3fd2f9c4ef7a45aaa96fc73f854b0caa']
ids = {}
for a in accounts:
    for mid in pubg.player_matches(a):
        ids[mid[:8]] = mid
        time.sleep(1.0)
json.dump(ids, open('prefix_ids.json','w'))
print(len(ids), 'matches collected')
