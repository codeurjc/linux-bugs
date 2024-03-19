TO DO: Improve this file

To generate a sample of commits from the +1.5M commits of the Linux Kernel:

```bash
python3 get_random_commits.py -i linux-commits-2023-11-12.json -y $YEAR -n $SIZE -s $SEED > commits-$YEAR-$SEED-$SIZE.lst
```

where:
- $SEED is the seed for random generation
- $SIZE is the size of the sample
- $YEAR is the year from which we want to obtain the commits

To obtain the same set of commits as our experiment, run the following command:

```bash
python3 get_random_commits.py -i linux-commits-2023-11-12.json -y 2022 -n 1000 -s 1 > commits-2022-1-1000.lst
```

To filter the original set of commits using this list:

```bash
python3 FilterCommits.py commits-2022-1-1000.lst
``` 