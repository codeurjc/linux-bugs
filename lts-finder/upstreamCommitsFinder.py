import argparse
import dateutil.parser
import os
import re

import csv
from bs4 import BeautifulSoup
import requests

CURRENT_BRANCHES = ["6.6", "6.1", "5.15", "5.10", "5.4", "4.19", "4.14", "4.9", "4.4", "4.1"]

BASE_URL = "https://cdn.kernel.org/pub/linux/kernel/"

upstream_regex = "commit ([0-9a-f]{5,40}) upstream|Upstream commit:* ([0-9a-f]{20,40})"

def get_branch(branch_id, cache=False):
    """Get all upstream hashes for a branch (for example, 6.5)

    Returns a list of tuples (branch_id, minor_id, hash)"""
    upstream_commits = []
    release_range = f"v{branch_id.split(".")[0]}.x"
    # Change log page (e.g. https://cdn.kernel.org/pub/linux/kernel/v6.x)
    changelog_list_page = get_bsoup_document(BASE_URL + release_range, cache)

    for link in changelog_list_page.find_all('a', string=re.compile("^ChangeLog-" + branch_id)):
        cl_file = link.get('href')
        if cl_file.endswith('.sign'):
            # We're not interested in Changelog-x.y.z.sign files
            continue
        # cl_file is "ChangeLog-x.y.z" (maybe there is no z)
        cl_link = f"{BASE_URL}{release_range}/{cl_file}"
        cl_version = cl_file.split('-')[1]
        try:
            minor_id = cl_version.split('.')[2]
        except IndexError:
            minor_id = '0'
        print(branch_id, minor_id, cl_link)
        # HTML changelog page (e.g. https://cdn.kernel.org/pub/linux/kernel/v6.x/ChangeLog-6.6)
        changelog_page_html = get_document(cl_link, cache)
        # Find date of first commit of the changelog (date of the release)
        changelog_date = re.search("Date:(.*)", changelog_page_html)
        changelog_date = changelog_date.groups()[0].strip()
        changelog_date = dt = dateutil.parser.parse(changelog_date)
        with open(os.path.join('results', 'release_dates.csv'), 'a') as f:
            print(f"{branch_id},{minor_id},{changelog_date}", file=f)
        # Find upstream commit hashes using regex
        upstream_tuples_in_changelog = re.findall(upstream_regex, changelog_page_html)
        # We get tuples, because the regex has several groups. Get the actual commits from them
        upstream_commits_in_changelog = [next(s for s in i if s) for i in upstream_tuples_in_changelog]
        print(f" > Upstream commits found: {len(upstream_commits_in_changelog)}")
        # Save upstream commits in a file
        with open('results/%s.txt' % cl_file, 'w') as f:
            for hash in upstream_commits_in_changelog:
                f.write(f"{hash}\n")
                upstream_commits.append((branch_id, minor_id, hash))
    return upstream_commits


def get_all(cache=False):
    all_upstream_commits = []

    for branch_id in CURRENT_BRANCHES:
        all_upstream_commits += get_branch(branch_id, cache=cache)

    with open('upstream_commits.csv', 'w') as out:
        csv_out = csv.writer(out)
        csv_out.writerow(['branch', 'minor', 'commit'])
        for row in all_upstream_commits:
            csv_out.writerow(row)


def get_bsoup_document(url, cache=False):
    return BeautifulSoup(get_document(url, cache), 'html.parser')


def get_document(url, cache=False):
    file_name = url.split("/")[-1]
    path_name = os.path.join("cache", f"{file_name}.txt")
    if cache and os.path.isfile(path_name):
        with open(path_name, 'r') as f:
            content = f.read()
        return content
    else:
        response = requests.get(url)
        with open(path_name, 'w') as f:
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

    # Create the file for releases dates (overwriting the old one)
    with open(os.path.join('results', 'release_dates.csv'), 'w') as f:
        print("branch,minor,date", file=f)

    if args.all:
        print("Finding upstream commits in all branches")
        get_all(cache=args.cache)
    elif args.branch:
        print("Finding upstream commits in branch: %s" % args.branch)
        get_branch(args.branch, cache=args.cache)
    else:
        exit("Please specify a branch (e.g. -b 6.6) or use -all to get all branches")
