# Definitions and instructions for annotators

Please, read carefully all these definitions and instructions. Have them in mind when annotating all commits.

For each commit, the main intention of the annotation is to discern:

* How much the annotator understands the commit, and a (very brief) description of the main purpose of it. This is to know to which extent the annotation is an "informed annotation", or maybe annotators have doubts on their understanding of it. The description will also allow us, in the future, to contrast that impression of understanding by consulting with experts in the Linux kernel.

* The relationship of the commit with bugs (defects). We are mainly interested in determining which commits are fixing a bug, but also in finding out other relationships with bugs. In any case, it is important to realize these categories are not completely independent. For example, BFC could also prevent some other future bugs (different from the fixed bug), which means that it could be labeled as "I'm sure it is a BFC" and "I'm sure it is a BPC". But it is important to notice that in this case, the "fixed bug" should be different from the "prevented bugs". Also, any commit preventing bugs is certainly a perfective commit. But for annotating it as both a BPC and a PRC, there should be some clear improvement besides preventing those bugs (if not, it will be labeled only as BPC). In other words, if a commit is in two categories, please be sure that is because there are different reasons for that: if the reason is the same, label it only in the first of the consdiered categories: BFC before BPC, or PRC before NFC). The categories are:
  * Does the commit fix a bug? (Bug Fixing Commit, BFC)
  * Does the commit prevent a bug? (Bug Preventing Commit, BPC)
  * Does the commit improve the code somehow, for instance by improving performance, improving the overall quality of the code, making it more readable, etc.? (Perfective Commit, PRC)
  * Does the commit include code for some new feature or a part of it? (New Feature Commit, NFC)



## For all commits

### Purpose of the commit

The purpose of the commit is the intention with which the code change (commit) was done. It will usually be a short text, which to some extent may be a summary of the commit message. But in the end, it is what the annotator understands as the purpose or intention of the code change.

The annotator will not always fully understand that purpose, because of technical complexities, unfamiliarity with the details mentioned, deficiencies in the commit message and associated information, or anything else.

## For commits dealing with known or potential failures

Failures are defined as erroneous behaviour of the software system, when the system deviates from its expected behavior, resulting in an inability to perform its intended functions or deliver the expected outputs. If the failure is caused by a software fault (a bug), it can be fixed only by some change to the software. Therefore, a commit that doesn't change the source code (including its default configuration or other assets that may influence in the behaviour of the system) cannot fix or prevent a bug.

### Bug-fixing commit (BFC)

Any commit that fixes a bug present in the source code, defined as a software fault that manifests as a failure when running in a certain way the version of the system previous to the commit.

### Bug-Preventing Commit (BPC)

Any commit that prevents a bug that could cause a failure in the future. This kind of commits doesn't fix known bugs, but possible, still undiscovered bugs, that could happen in the future. For example, they could improve the values returned by a function, in a way that is likely to prevent failures in code calling that function.

### Perfective Commit (PRC)

Any commit that improves the quality of the code. This includes refactoring, optimizations, code style improvements, adding comments, etc. The key aspect is that perfective commits do not fix bugs or add new features.

### New Feature Commit (NFC)

Any commit that adds new functionality or capabilities to the codebase. This includes adding support for new hardware, implementing new APIs, exposing new configuration options, etc. The key aspect is that new feature commits add new code to enable new behaviors not previously possible.

### Auto-Suggested Commit (ASC)

A commit made to follow the advice of a tool (for example, a static analysis tool), in order to improve the quality of the software, in terms of fixing bugs, preventing future bugs, and in general, reducing the likeness of failures. A commit may be an ASC, and also be (or not) a BFC or a BPC.

## In case the commit deals with a bug

### Obvious bug

An obvious bug is a bug which is clearly detectable by usual testing, that is, which causes obvious misbehavior on every operation, or so frequently that the effects would be clearly noticeable during testing.

### Safety-related bug

Any commit that fixes a safety-related bug.
A safety-related bug is any bug with potential to affect safety-relevant behaviors, as indicated by the categorizations described below, even when it may not be detected by typical testing because occurrence is intermittent and/or rare.

## In case it is a safety-related bug

### Timing and execution

With respect to timing constraints, the effects of faults such as those listed below can be considered for the software elements executed in each software partition: blocking of execution, deadlocks, livelocks, incorrect allocation of execution time or incorrect synchronization between software elements.

### Memory

With respect to memory, the effects of faults such as those listed below can be considered for software elements executed in each software partition: corruption of content. inconsistent data (e.g. due to update during data fetch),stack overflow or underflow or read or write access to memory allocated to another software element.

### Exchange of Information

With respect to the exchange of information, the causes for faults or effects of faults such as those listed below can be considered for each sender or each receiver: repetition of information, loss of information, delay of information, insertion of information, masquerade or incorrect addressing of information, incorrect sequence of information, corruption of information, asymmetric information sent from a sender to multiple receivers, information from a sender received by only a subset of the receivers or blocking access to a communication channel.

## In case it is a commit that belongs to a part of PATCH (commit train)


Some commits may belong to a larger series of commits called a "patch series" or "commit train". These can be identified by:
- A link in the commit message to the lore.kernel mailing list thread where the series was posted. The first commit in the series (with ID 0/00/000) is the "parent" commit.
- A "Search the commit title in the kernel.lore mailing list" link at the top of the commit message. This allows searching for the commit title to find the mailing list thread and parent commit. However, some commits may not appear in the search results.
- Checking if the commit ID contains a "patch series number" like 3/12 indicating it is part of a larger series.
- Looking at the diff content and commit message for any references to a patch series or other commits that are part of the same changes.
- 
By finding the parent commit and series, it can be determined if the commit belongs to a larger patch set. The context of the series and discussions on the mailing list may provide additional information.