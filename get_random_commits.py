#!/usr/bin/python3

import argparse
import json
import gzip
import random
import sys

# Parse command line arguments
parser = argparse.ArgumentParser(
    description = "Get a random sample of commits from a Perceval on-line JSON list of commits"
    )
parser.add_argument("-i", "--input",
                    help = "File with JSONs created by perceval (can be a gzipped file)")
parser.add_argument("-y", "--year",
                    help = "Year of the commits to choose from")
parser.add_argument("-n", "--number",
                    help = "Number of commits to choose")
parser.add_argument("-s", "--seed",
                    help = "Seed integer, for reproducibility")
parser.add_argument("-c", "--count",
                    action='store_true',
                    help = "Count commits for the selected year")
args = parser.parse_args()

commitsList = []

if args.input.endswith('gz'):
    func = gzip.open
elif args.input.endswith('json'):
    func = open

with func(args.input) as inputfile:
    count = 0
    for line in inputfile:
        commit = json.loads(line)
        year = commit['data']['CommitDate'].split()[4] # Get year of commit
        if year == args.year:
            count += 1
            commitsList.append(commit['data']['commit'])

if args.number:
    random.seed(args.seed)
    chosen = random.sample(commitsList, int(args.number))
    print('\n'.join(chosen))
if args.count:
    if args.year:
        year = args.year
    else:
        year = 'all'
    print(f"Number of commits for year {year}: {count}", file=sys.stderr)

