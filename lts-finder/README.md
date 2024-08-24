# Searching annotated commits in upstream commits from kernel stable branches

## Objetives

- Locate all upstream commits listed in kernel.org from the LTS releases.
- Analyze the annotated (by us) commits that also happen to be in LTS releases.

## Locate all upstream commits listed in kernel.org

To track the Long-Term Support (LTS) versions listed on kernel.org, we gather all commits for each of these branches. This can be done by checking the changelog files for each branch (e.g., 6.6.x, 6.1.x, 5.15.x, etc.). 

In summary, the script "upstreamCommitsFinder.py" accesses this online directory and retrieves all "upstream" commits for each branch.

The final output is a file per branch, named after the branch (e.g., 5.0.1), with each line containing an upstream commit hash.

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
python UpstreamCommitsFinder.py -b 6.1
```
- ```get_all():``` This function retrieves the current list of branches and uses get_branch() on each of them. In addition, it generates a CSV (_upstream_commits.csv_) with all upstream commits found from all branches. 
```bash
python UpstreamCommitsFinder.py --all
```


Additionally, there is a ```--cache``` that could be used to cache downloaded files. If this flag is present, the script should check if the file is already in the cache before downloading it. This would involve adding a caching boolean to the functions and using a `cache/` directory to store the downloaded files.

## Look for annotated commits in upstream commits

Open `UpstreamCommitsAnalyzer.ipynb` notebook.