from bs4 import BeautifulSoup
import requests
import re
import os
import argparse
import csv

CURRENT_BRANCHES = ["6.6", "6.1", "5.15", "5.10", "5.4", "4.19"]

BASE_URL = "https://cdn.kernel.org/pub/linux/kernel/"


def get_branch(branch_id, cache=False):
    upstream_commits = []
    release_range = "v%d.x" % int(branch_id.split(".")[0])
    # Change log page (e.g. https://cdn.kernel.org/pub/linux/kernel/v6.x)
    changelog_list_page = get_bsoup_document(BASE_URL + release_range, cache)
    for link in changelog_list_page.find_all('a', string=re.compile("^ChangeLog-" + branch_id)):
        # link is "ChangeLog-X.X"
        print(BASE_URL + release_range + "/" + link.get('href'))
        # HTML changelog page (e.g. https://cdn.kernel.org/pub/linux/kernel/v6.x/ChangeLog-6.6)
        changelog_page_html = get_html_document(BASE_URL + release_range + "/" + link.get('href'), cache)
        # Find commit hash using regex
        upstream_commits_in_changelog = re.findall("commit ([0-9a-f]{5,40}) upstream", changelog_page_html)
        print(" > Upstream commits found: %d" % len(upstream_commits_in_changelog))
        # Save upstream commits in a file
        with open('results/%s.txt' % link.get('href'), 'w') as f:
            for commit_hash in upstream_commits_in_changelog:
                f.write("%s\n" % commit_hash)
                upstream_commits.append((branch_id, commit_hash))
    return upstream_commits


def get_all(cache=False):
    all_upstream_commits = []
    for branch_id in CURRENT_BRANCHES:
        all_upstream_commits += get_branch(branch_id, cache=cache)

    with open('upstream_commits.csv', 'w') as out:
        csv_out = csv.writer(out)
        csv_out.writerow(['branch', 'commit'])
        for row in all_upstream_commits:
            csv_out.writerow(row)


def get_bsoup_document(url, cache=False):
    return BeautifulSoup(get_html_document(url, cache), 'html.parser')


def get_html_document(url, cache=False):
    file_name = url.split("/")[-1]
    if cache and os.path.isfile('cache/%s.txt' % file_name):
        with open('cache/%s.txt' % file_name, 'r') as f:
            content = f.read()
        return content
    else:
        response = requests.get(url)
        with open('cache/%s.txt' % file_name, 'w') as f:
            f.write(response.text)
        return response.text


if __name__ == "__main__":

    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--cache', action='store_true',
                        help='Use cache to avoid downloading the same page multiple times')
    parser.add_argument('--all', action='store_true', help='Get upstream commits in all branches')
    parser.add_argument('-b', type=str, choices=CURRENT_BRANCHES, help='Get upstream commits in a specific branch')
    args = parser.parse_args()

    if args.all:
        print("Finding upstream commits in all branches")
        get_all(cache=args.cache)
    elif args.branch:
        print("Finding upstream commits in branch: %s" % args.branch)
        get_branch(args.branch, cache=args.cache)
    else:
        exit("Please specify a branch (e.g. -b 6.6) or use -all to get all branches")
