# Definitions and instructions for annotators

Please, read carefully all these definitions and instructions. Have them in mind when annotating all commits.

For each commit, the main intention of the annotation is to discern:

* How much the annotator understands the commit, and a (very brief) description of the main purpose of it. This is to know to which extent the annotation is an "informed annotation", or maybe annotators have doubts on their understanding of it. The description will also allow us, in the future, to contrast that impression of understanding by consulting with experts in the Linux kernel.

* The relationship of the commit with bugs (defects). We are mainly interested in determining which commits are fixing a bug, but also in finding out other relationships with bugs. In any case, it is important to realize these categories are not completely independent.
  * For example, BFC could also prevent some other future bugs (different from the fixed bug), which means that it could be labeled as "I'm sure it is a BFC" and "I'm sure it is a BPC". But it is important to notice that in this case, the "fixed bug" should be different from the "prevented bugs".
  * Also, any commit preventing bugs is certainly a perfective commit. But for annotating it as both a BPC and a PRC, there should be some clear improvement besides preventing those bugs (if not, it will be labeled only as BPC).
  * In other words, if a commit is in two categories, please be sure that is because there are different reasons for that: if the reason is the same, label it only in the first of the consdiered categories: BFC before BPC, or PRC before NFC). The categories are:
    * Does the commit fix a bug? (Bug Fixing Commit, BFC)
    * Does the commit prevent a bug? (Bug Preventing Commit, BPC)
    * Does the commit improve the code somehow, for instance by improving performance, improving the overall quality of the code, making it more readable, etc.? (Perfective Commit, PRC)
    * Does the commit include code for some new feature or a part of it? (New Feature Commit, NFC)

* Some other features of the commit that may allow us to better understand them:
  * Merge commit.
    * Merge commits are usually just a mechanism for merging a patch set (a set of commits) into the kernel codebase. Therefore, usually they don't alter the code of the system by themselves, and therefore for now we can ignore them.
  * Commit in a patchset (set of commits).
    * Patchsets are usually found in the LORE as threads, with the subject of each message starting with `[PATCH vx m/n]` (for example `[PATCH v4 31/32]`) and then the first line of the commit message. If they are not in a patchset, the subject is usually just `[PATCH]`
      * `vx` means this is the x version of the patchset
      * `m/n` means this message refers to the m commit in a set of n commits
      * `0/n` is the message describing the patchset
    * A patchset is a set of commits that are reviewed and merged together. Either all of them are merged, or if  not, a new revision is asked for. Therefore, all patchsets that we see as commits in the kernel code were merged together. That means that they may be a coordinated set, with several or all commits in the patchset implementing some coordinated change to the code (but beware, in some cases this is not the case, and some or all commits are independent of each other).
    * When commits in the patchset are coordinated, we have to understand that coordination. A common case is that one of the commit changes the code in some way, and some of the others just adapt the code to that change.
    * For example, a commit may change an API (say, by adding a new parameter to a function), and then some other commits adapt code in the kernel calling that API, by adding the new parameter.
      * In this case, the "other" commits may seem, if isolated, as BFC, since they are adding "fixing" the missing parameter.
      * But when looked together, that was never a bug, since all commits entered the codebase at the same time, and the bug never materialized (the "bug" and its "patch" were merged together).
    * Therefore, for all commits we must check the LORE, to see if the commit is a part of a patchset. If the commit is a part of a patchset, we should at least check the main commit in the patchset (usually the one labeled as "0/n").
  * Commit related to a specification change.
    * Specification changes may cause NFCs when new functionality in the new specification is implemented.
    * But they may also convert into a bug something that was not a bug, but specified behavior (for example).
    * Capturing specificatios in the kernel is not always easy, because in many cases they are not documented anywhere. But have in mind that the comment in the commit, or the discussion in LORE maybe lead us to understand that the "collective mind" of the project is changing specifications.
      * For example, it may happen that a commit is for supporting some device that was previously not supported: that would mean that the previous "informal specification" didn't include the device, but the new one does.
      * Another example would be if some specific feature of some already supported hardware is now considered, such as a device that was supported, but only in read-only mode, and the commit adds support for read-write more. In this case, the commit record may show that the "informal specification" was to support it as read-only, but now it "specifies" it is read-write (and this would be that change of specifiation).
      * Of course, this is different from a case when the device was supposed to be supported read-write, but somebody reports that it works read-only, and the commit fixes that (in that case, we would consider it as a BFC, with no change in specifciations). In general, changes to specifications are likely to be relatively rare, but we won't know until we have more evidence.
  * Commit produced in response to an automated tool (Auto Suggested Commits, ASCs)
    * Commits can be produced because some tool detected a flaw, and it is fixed. In some cases the tools produce the change themselves. This can be the case, for example, of static analysis tools detecting memory leaks.
    * It is important to notice that usually these changes are done without actually checking if the flaw is causing a fault under some specific circumsntances. They are just done preventively. So, usually they are BPCs. However, they could be BFC if the developer somehow links them to a specific fault. They could also be PRCs if the tool is just restructuring the code (because it is not trying to prevent bugs, but finding more efficient procedures, for example).
    * There is a list of these kind of tools in [Development tools for the kernel](https://docs.kernel.org/dev-tools/index.html):
      * Dynamic analysis tools: kmemleak, KASAN, UBSAN, KCSAN, KFENCE, lockdep
      * Static analysis tools: Sparse, Smatch, Coccinelle
    * Important: that same document says "Errors and warns need to be evaluated carefully before attempting to fix them". That means, from our point of view, that if the commit was reviewed and merged, it was understood to at least prevent bugs (BPC).
  * Commit fixing an obvious bug
    * Some bugs clearly detectable by usual testing, because they cause obvious misbehavior on every operation, or so frequently that the effects would be clearly noticeable during testing.
    * These bugs will never reach production kernels, and therefore it is important to label them separately.
    * Of course, only BFCs may be fixing an obvious bug
  
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