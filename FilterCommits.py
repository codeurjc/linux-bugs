import json

with open('linux-commits-2023-11-12_random-filtered.json') as fd:
    commits_json = json.load(fd)

with open('linux-commits-2023-11-12_random-filtered-130-230.json', 'w') as f:
    json.dump(commits_json[129:229], f)

