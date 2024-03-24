# Context for annotators

Please, read carefully this context information. Have them in mind when annotating all commits.

## Main intention of the annotation

For each commit, the main intention of the annotation is to discern:

* How much the annotator understands the commit, and a (very brief) description of the main purpose of it. This is to know to which extent the annotation is an "informed annotation", or maybe annotators have doubts on their understanding of it. The description will also allow us, in the future, to contrast that impression of understanding by consulting with experts in the Linux kernel.

* The relationship of the commit with bugs (defects). We are mainly interested in determining which commits are fixing a bug, but also in finding out other relationships with bugs. In any case, it is important to realize these categories are not completely independent.
  * For example, BFC could also prevent some other future bugs (different from the fixed bug), which means that it could be labeled as "I'm sure it is a BFC" and "I'm sure it is a BPC". But it is important to notice that in this case, the "fixed bug" should be different from the "prevented bugs".
  * Also, any commit preventing bugs is certainly a perfective commit. But for annotating it as both a BPC and a PRC, there should be some clear improvement besides preventing those bugs (if not, it will be labeled only as BPC).
  * In other words, if a commit is in two or more categories, please be sure that is because there are different reasons for that: if the reason is the same, label it only in the first of the considered categories: BFC before BPC, or PRC before NFC). The categories are:
    * Does the commit fix a bug? (Bug Fixing Commit, BFC)
    * Does the commit prevent a bug? (Bug Preventing Commit, BPC)
    * Does the commit improve the code somehow, for instance by improving performance, improving the overall quality of the code, making it more readable, etc.? (Perfective Commit, PRC)
    * Does the commit include code for some new feature or a part of it? (New Feature Commit, NFC)

* If the commit is a BFC, whether it is safety-related.
  * To decide if the commit is safety-related, check the bug it fixes has an impact on safety (check the corresponding definition in [definitions.md](definitions.md)).
  * We also want to know in which of three categories related to safety we can classify the bug. It could be in more than one, but only if it fits all of them marked for any specific reason. Maybe it could also happen that it fits no category: if that is the case, ensure you explain your reasons with some detail.
  * Ensure you understand the definitions for safety-related, and the three categories, since that will be fundamental for our classification. And ensure you think about the bug which is fixed by the commit: it is the bug which is safety-related, not the commit itself. For example, a timing and execution bug could touch nothing specifically related to timing and execution, but maybe change some condition, which happens to fix a bug which causes some problem related to timing and execution.

## Other features

Some other features of the commit that may allow us to better understand them:

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
  * Specification changes may cause NFCs when new functionality in the new specification is implemented, but they may also convert into a bug something that was not a bug, but specified behavior (for example).
  * Capturing specifications in the kernel is not always easy, because in many cases they are not documented anywhere. But have in mind that the comment in the commit, or the discussion in LORE maybe lead us to understand that the "collective mind" of the project is changing specifications.
    * For example, it may happen that a commit is for supporting some device that was previously not supported: that would mean that the previous "informal specification" didn't include the device, but the new one does.
    * Another example would be if some specific feature of some already supported hardware is now considered, such as a device that was supported, but only in read-only mode, and the commit adds support for read-write more. In this case, the commit record may show that the "informal specification" was to support it as read-only, but now it "specifies" it is read-write (and this would be that change of specification).
    * Of course, this is different from a case when the device was supposed to be supported read-write, but somebody reports that it works read-only, and the commit fixes that (in that case, we would consider it as a BFC, with no change in specifications). In general, changes to specifications are likely to be relatively rare, but we won't know until we have more evidence.
  * In summary, the commit will be "related to a specification change" if the commit itself includes information that signals a change in specifications, or if the messages in the commit suggest that specifications changed since the code touched by the commit was written.

* Commit produced in response to an automated tool (Auto Suggested Commits, ASCs)
  * Commits can be produced because some tool detected a flaw, and it is fixed. In some cases the tools produce the change themselves. This can be the case, for example, of static analysis tools detecting memory leaks.
  * It is important to notice that usually these changes are done without actually checking if the flaw is causing a fault under some specific circumstances. They are just done preventively. So, usually they are BPCs. However, they could be BFC if the developer somehow links them to a specific fault. They could also be PRCs if the tool is just restructuring the code (because it is not trying to prevent bugs, but finding more efficient procedures, for example).
  * There is a list of these kind of tools in [Development tools for the kernel](https://docs.kernel.org/dev-tools/index.html):
    * Dynamic analysis tools: kmemleak, KASAN, UBSAN, KCSAN, KFENCE, lockdep
    * Static analysis tools: Sparse, Smatch, Coccinelle
  * Important: that same document says "Errors and warns need to be evaluated carefully before attempting to fix them". That means, from our point of view, that if the commit was reviewed and merged, it was understood to at least prevent bugs (BPC).
  * Testing: It is unlikely that we find commits fixing bugs detected during regular regression testing, because they are usually caught and fixed well before they reach the codebase. But just in case, let's keep an eye on them: if a commit refers that it fix a regression test, it is obviously a BFC.

* Commit fixing an obvious bug
  * Some bugs clearly detectable by usual testing, because they cause obvious misbehavior on every operation, or so frequently that the effects would be clearly noticeable during testing.
  * These bugs will never reach production kernels, and therefore it is important to label them separately.
  * Of course, only BFCs may be fixing an obvious bug
