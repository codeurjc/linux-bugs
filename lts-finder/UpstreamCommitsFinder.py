import json
from bs4 import BeautifulSoup 
import requests 
import re 
import os
import argparse

CURRENT_RELEASES = ["6.6", "6.1", "5.15", "5.10", "5.4", "4.19"]

BASE_URL = "https://cdn.kernel.org/pub/linux/kernel/"

class UpstreamCommitsFinder():
    
    def __init__(self, commit_collection_path):
        self.annotated_commits_dict = dict()
        
        self.annotated_commits_found_count=0
        self.annotated_commits_found_set=set() # To track repeated commits
        
        self.upstream_commits_count=0
        self.upstream_commits_found_set=set() # To track repeated commits
        
        with open(commit_collection_path) as fd:
            commit_collection = json.load(fd)
            for commit in commit_collection:
                c_hash = commit['data']['commit']
                self.annotated_commits_dict[c_hash] = commit

    def get_branch(self, branch_id, cache=False):
        # Change log page (e.g. https://cdn.kernel.org/pub/linux/kernel/v6.x)
        release_range = "v%d.x"%int(branch_id.split(".")[0])
        changelog_list_page = self._getBsoupDocument(BASE_URL+release_range, cache)
        for link in changelog_list_page.find_all('a', string=re.compile("^ChangeLog-"+branch_id)): 
            # link is "ChangeLog-X.X"
            print(BASE_URL+release_range+"/"+link.get('href'))
            # changelog_page_html represent the page of changelog (e.g. https://cdn.kernel.org/pub/linux/kernel/v6.x/ChangeLog-6.6)
            changelog_page_html = self._getHTMLDocument(BASE_URL+release_range+"/"+link.get('href'), cache)
            # Find commit hash using regex. Also save if its a normal commit (Author) or a Merge commit (Merge)
            upstream_commits_in_changelog = re.findall("commit ([0-9a-f]{5,40}) upstream", changelog_page_html)
            self.upstream_commits_count += len(upstream_commits_in_changelog)
            print(" > Upstream commits found: %d"%len(upstream_commits_in_changelog))
            # List to store commits in the changelog that exists in our list of annotated commits
            annotated_commits_found = []
            # Search for changelog commits in our annotated commit collection
            for commit_hash in upstream_commits_in_changelog:
                # Store unique upstream commits
                if commit_hash not in self.upstream_commits_found_set:
                    self.upstream_commits_found_set.add(commit_hash)
                if commit_hash in self.annotated_commits_dict:
                    self.annotated_commits_found_count+=1
                    annotated_commits_found.append(commit_hash)
                    # Store unique upstream commits that were annotated
                    if commit_hash not in self.annotated_commits_found_set:
                        self.annotated_commits_found_set.add(commit_hash)
            # If at least one commit is found, it is saved in a file "ChangeLog-X.X.X".
            print(" > Upstream commits match with annotated commits: %d"%len(annotated_commits_found))
            if len(annotated_commits_found) > 0:
                with open('results/%s.txt'%link.get('href'), 'w') as f:
                    for commit in annotated_commits_found:
                        f.write("%s\n" % commit)
                        
    def get_all(self, cache=False):
        for branch_id in CURRENT_RELEASES:
            self.get_branch(branch_id, cache=cache)

    def print_stats(self):
        print("\nUpstream commits found: %d"%self.upstream_commits_count)
        print("Unique upstream commits found: %d"%len(self.upstream_commits_found_set))
        print("Annotated commits found in upstream commits: %d"%self.annotated_commits_found_count)
        print("Unique annotated commits found in upstream commits: %d"%len(self.annotated_commits_found_set))

    def _getBsoupDocument(self, url,cache=False): 
        return BeautifulSoup(self._getHTMLDocument(url,cache) , 'html.parser')
        
    def _getHTMLDocument(self, url,cache=False):
        fileName = url.split("/")[-1]
        if cache and os.path.isfile('cache/%s.txt'%fileName):
            response = requests.get(url)
            with open('cache/%s.txt'%fileName, 'r') as f:
                content = f.read()
            return content
        else:
            response = requests.get(url)
            with open('cache/%s.txt'%fileName, 'w') as f:
                f.write(response.text)
            return response.text
        
if __name__ == "__main__":
    
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help='Path to the annotated commits collection in json format')
    parser.add_argument('--cache', action='store_true', help='Use cache to avoid downloading the same page multiple times')
    parser.add_argument('--all', action='store_true', help='Get upstream commits in all branches')
    parser.add_argument('-b', type=str, choices=CURRENT_RELEASES, help='Get upstream commits in a specific branch')
    args = parser.parse_args()

    finder = UpstreamCommitsFinder(args.filename)
    
    if args.all:
        print("Finding upstream commits in all branches")
        finder.get_all(cache=args.cache)
    elif args.branch:
        print("Finding upstream commits in branch: %s"%args.branch)
        finder.get_branch(args.branch, cache=args.cache)
    else:
        exit("Please specify a branch (e.g. -b 6.6) or use -all to get all branches")
    finder.print_stats()