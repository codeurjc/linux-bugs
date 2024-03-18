import json

with open('linux-commits-2023-11-12.json') as f:
    all_commits = f.readlines()
    
with open('commits-2022-123-1000.lst') as f:
    random_commits = list(map(lambda c: c.strip(), f.readlines()))

filtered_commits = []
for commit in all_commits:
    commit_json = json.loads(commit)
    if commit_json['data']['commit'] in random_commits:
        filtered_commits.append(commit_json)

with open('linux-commits-2023-11-12_new_random-filtered.json', 'w') as f:
  json.dump(filtered_commits, f)

