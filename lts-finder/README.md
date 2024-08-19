# Upstream Commits Finder

## Objetives

- Locate all upstream commits listed in kernel.org from the following releases/branches: 6.6, 6.1, 5.15, 5.10, 5.4, and 4.19
- From the 1000 commits annotated by us, check which ones are also upstreamed commits

## What script does

To track the Long-Term Support (LTS) versions listed on kernel.org (currently 6.6, 6.1, 5.15, 5.10, 5.4, and 4.19), we gather all commits for each of these branches. This can be done by checking the changelog files for each branch (e.g., 6.6.x, 6.1.x, 5.15.x, etc.). 

For each commit mentioned in these changelogs, we look for the "upstream commit" line in the commit comment. 
Then, we tried to find this commit in Linus Torvalds’ repository (which we are tracking) to see if we are annotating that commit.

In summary, the script accesses this directory and retrieves all "upstream" commits for each branch.

The final output is a file per branch, named after the branch (e.g., 5.0.1), with each line containing a commit hash.

## Usage

Requirements:
- Python +3.10
- pip +22.0

First, we need to download the dependencies

```
pip install -r ../requirements.txt
```

The script have two main functions:

- ```get_branch(branch_id):``` This function takes a branch ID (6.6, 6.1, 5.15, 5.10, 5.4 or 4.19) and returns a list of commit hashes for each changelog that will be store in `results/` folder using the name of the changelog
```bash
python UpstreamCommitsFinder.py ../linux-commits-2023-11-12_random-filtered-1.json --all
```
- ```get_all():``` This function retrieves the current list of branches and uses get_branch() on each of them. 
```bash
python UpstreamCommitsFinder.py ../linux-commits-2023-11-12_random-filtered-1.json -b 6.1
```


Additionally, there is a ```--cache``` that could be used to cache downloaded files. If this flag is present, the script should check if the file is already in the cache before downloading it. This would involve adding a caching boolean to the functions and using a `cache/` directory to store the downloaded files.