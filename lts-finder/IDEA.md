I think it would be a matter of tracking LTSs listed in
https://www.kernel.org/category/releases.html (for example, now, it
would be 6.6, 6.1, 5.15, 5.10, 5.4, 4.19).

For getting all commits in each of those branches, it would be enough
to check in the changelog files for each of those six branches (6.6.x,
6.1.x, 5.15.x, etc), such as for example for the 5.x branches, those
changelogs in:

https://cdn.kernel.org/pub/linux/kernel/v5.x/

For each commit mentioned in those changelogs, we should look for the
"upstream commit" line in the commit comment, and then look for it in
the Linus repo (which is the one we're tracking) to see if we're
annotating that commit.

In other words, we need a script that goes to

https://cdn.kernel.org/pub/linux/kernel

and get all "upstream" commits for each branch.

For example, the final result could be one file per branch. The file
could be named like the branch (eg, 5.0.1), and the content could be
one hash per line, using the lines in the changelogs, such as:

"commit f612acfae86af7ecad754ae6a46019be9da05b8e upstream"

It could be a file with two main functions, one to retrieve data for a
branch, given its name, with a signature like:

function get_branch(branch_id): list of str

(list of str would be the list of hashes obtained)

and another one to get all data, by first getting the current list of
branches, and then using get_branch() on each of them (for gettint the
list of branches we could also have a function):

function get_all(): list of tuples of (str, str)

(the result would be a list of tuples, with each tuple being of the
form (branch_id, hash))

Then, we could call it as a script, so that if the  script is called
with a branch id just produces in its stdout the list of commits for
that branch_id, one per line, but if no branch_id is specified, it
produces as its stdout a CSV document with each line being branch_id,
hash.

It would be even better if an additional --cache option could be used,
which if present, causes the downloaded files to be cached (so that a
further run of the script checks if the file is already in the cache
before downloading it). This would mean adding a caching boolean to the
functions above, and using for example a .changelogs directory for
storing the downloaded files.

Then, we would need a list of LTS branches, and we could easily merge
that with the previous CSV file and the annotations CSV file to produce
the data we need.

