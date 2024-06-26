## Comparison of 130 first commits

They were annotated by Michel (A), Abhishek (B) and David (C)

The file generated by Michel had 130 lines, but one commit was present twice. I removed the first one. That means that Michel had really 129 commits annotated, which means we have 129 commits annotated by three persons.

There are 33 commits in whcih one anntoator disagrees with the others.

### General notes

We definitely need a way to make a difference between patches fixing bugs and aptches improving the code somehow (making it faster, easier to understand, less proe to cause unforeseen errors in the future, etc.). Patches of the first class are really BFCs, patches of the second class are really quaility improvements.

Then, we also have patches adding new functionality, but those are more difficult to be confused with BFCs (they could in some cases, when for example, the new functionality improves somehow the quality of the code, for example dealing with a case in a conditional that was not dealt before, or that was dealt with in a wrong way).

A commit could be of several of these cases: for example, while adding new functionatlity, a bug could be fixed (maybe the new functionality was added to fix the bug)

On a different topic, I see two main problems for agreen on the annotation:

* Each anotator understand the commit in a different way, or some of them don't understand the commit at all. I think to decide these cases, we need at least (ideally three) deveolopers. If we have only one developer, maybe we could just ask him to explain it in terms that can be mapped to changes in the function of the system, in addition to ask for classification, so that we can also later annotate it with (hopefully) improved understanding.

* All annotators agree on the understanding on the commit, but don't agree on whether it is a bug fix or not. For this, likely we don't need developoers, probably we need a more specific definition of what is a bug fix (and/or a checklist), and maybe the opinion of stakeholders. But in the latter case, probably by using those commits as examples to improve the definition.


### Some things to consider

If any of this happens, it cannot be a BFC:

* Functionality is not changed: it cannot fix a bug if the functionality is the same. Example: refactoring, such as ab14f1802c

To discuss:

* What if a commit just fixes the effect of a bug, but not the bug itself (which happesn, for example, in a dependency, and maybe is still not exactly identified). See cc5095747e

* What if new functionality is added, but that new functionality allows a better (less "wrong") work of the system? See feb00b736a, ea90330fa3 (this ones prevents a kind of firmare file to not be loaded correctly)

Maybe we should focus on two different aspects for each commit (once we have refined the definition of bug fixing commit), when consdiered the set of "commits labeled as BFC). For this, a "real" BFC would be a BFC which a "perfect" observer would labe as BFC

* Ensure that all "real" BFCs are included in the set: if I cannot explain, with certainty, that it is not a BFC, we consider it as a "possible BFC"

* Ensure that the set only includes "real" BFCs: if I'm sure for any reason if it is a BFC, I should say it is not.

Of course, this assumes we can understand what the commit does "exactly", and the problem is only in the definition. But in the real world, this could be applied also in cases of unperfect knowledge about what does the commit (see above).

### Specific notes about commits


7d4a101c0b: F T F
  * A: Only add sanity check
  * C: Looks like an update more than a bug fixing
  * R: F
    * Adds a sanity check. Improves maintainabilit, but does not fix a bug

c579792562: F T T
  * A: It seems to simply change how files/functions are displayed
  * C: Initialization of a variable to 0; due to a bug
  * R: T
    * Static analysis tool reports a warning: "Undefined or garbage value returned to caller"
    * This is an intetresting case. A tool detects what apparently is a bug. Somethibg worth annoating? It could have been catched earlier, by running the tool
    * This is also interesting because A probably annotated the wrong commit

370d988cc5: F T T
  * A: Considered a fix but really just avoids a warning.
  * C: Fixing a warning; possible future bug
  * R: F
    * Apparently, there is code using a variable, but the code  is commented out after the line with the assignment to the variable. The code is uncommented (thus activated), which seems to add the functionality of reporting an error. This doesn't seem a bug, more a perfective commit. Maybe it could help to not have a bug in the future.

bf08387fb4: F T T
  * A: A condition is extended to cover only the necessary cases (and a section of code is not executed if it is not necessary).
  * C: It explains the behaviour of the bug and possible future consequences; and also it fixes it.
  * R: T
    * There is a bug, clearly defined: a scenario where the bug happens, an analysis of the cause, and the tix

ecd1a5f62e: F T F
  * A: There was a commented code and it is uncommented
  * C: Looks like a feature more than a fix
  * R: F
    * Looks like a new feature being added

5f2f539901: T T F
  * A: Indicated as a "Correct" but i didnt understand the change
  * C: It seems that they are refactoring more than fixing.
  * R: T ?
    * Interesting case. The commit explains how some registers are not well captured by the code, but it doesn't seen that is really fixing a bug, but seems more like a performance enhancement (with respect to the use of the cache) and/or refactoring. Maybe some of the changes also prevent future bugs, anyway. I fonally mark it as True, with doubt, because what is clear is that the prevouos code wqs erroneous, and now it seems to be right, so it fixes a bug.

62d5f9f711: F T T
  * A: It appears to fix a change introduced earlier; in this case to supplement a case not contemplated. I am not sure to what extent it is a fix
  * C: I would say that this commit is fixing a bug about a GPU error when initialization; maybe is considered as safety related.
  * R: T ?
    * Aparently, makes a call which is needed to unmap some mappings, which appatently should be make always, and was done previously only if device was unplugged. So, it seems it is correcting a not-yet-reported bug. But without the check the mappings would not be unmapped, but it should.

50b620303a: F T F
  * A: A condition is added so that when there are no interruptions; the code continues (saves time)
  * C: Moving a return; nothing related to a bug fixing.
  * R: F
    * Performance improvement

77dbd72b98: F T T
  * A: Does not look like a fix
  * C: They are fixing with this pull a livepatch bug; could be considered as safety related commit because it fixes an init fail of Livepatch.
  * R: T
    * Seems to fix a bug, or at least to fix code that was wrong. For example, I read "Avoid CPU hogging"

3ac5f2f257: F F T
  * A: It only adds a description to a parameter (comment)
  * C: They are fixing with this pull a livepatch bug; could be considered as safety related commit because it fixes an init fail of Livepatch.
  * R: F
    * C seems to be an error, because it is exactly the same description of the previous commit.
    * Description of a change in a comment, in this case describing an argument in a function sifnature (important: this comment can be used by automatic tools)

da8c94c065: F T F
  * A: A variable is renamed
  * C: Refactoring variable name.
  * R: F
    * Refactoring, changing the name of a variable

801db90bf2: F T F
  * A: Change oriented to debug
  * C: Refactoring for a better future debug.
  * R: F
    * Perfectihng the code, making it easier to do debugging later

d6986ce24f: F T T
  * A: Fixed a bug in the comprehension of some components
  * C: It is fixing a bug; but not related to safety.
  * R: T
    * An identifier was not having enough memory to show its whole name. This commit allocates more memory so that the identifier can be show in full. So, the earlier code was incorrect, because it didn't allow for showing the full name, so it was a bug, which is fixed.

202470d536: T T F
  * A: Seems to fix a performance problem
  * C: It is a perfomance feature; in my opinion (I think)
  * R: F
    * A says is a performance fix, but still labels it as BFC: maybe an error?
    * It seems to remove a check that is not wrong, but is not needed

fbe7e52003: F T F
  * A; It is not clear to me
  * C: Looks like a feature.
  * R: T ?
    * Apparently, it adds a call that should be there to have a correct fnctionality. But I have some doubt, since maybe this is just a different, more convenient way of doing the same thing (now, using a helper function).

6a4d333d54: F T T
  * A: I'm not sure; it doesn't look like a bug-fix.
  * C: It is fixing a bug realted to the type of an offset; but I'm not sure about the type.
  * R: F
    * Refactoring: use the specific type for the values, instead of aimplicit type case

0d7c1153d9: F T F
  * A: A warning is removed
  * C: Removing a false-positive warning.
  * R: F
    * Restructuring the code to avoid a compiler warning, with apparently no effect in functionality

25875aa71d: F T F
  * A: Just add a print for a log
  * B: can be considered under Time and Exchange of information category.
  * C: It seems they are adding information features.
  * R: F
    * Adds information in a virtual device to warn about a practice that could have implciations for security (new functionality)

16860a209c: F T F
  * A: A redundant check is deleted
  * C: Refactoring.
  * R: F
    Refactoring, removing a redundant branch. Apparently, no effect on functionality

f2c281204b: F T F
  * A: Just add a waning
  * C: Feature adding a warning
  * R: F
    * Add a warning (new functionality)

b1bbd3a57b: F T F
  * A: Just a documentation change
  * C: comment: Doc change
  * R: F
    * Just cahnges documentation

86c2457a8e: T F T
  * A: It seems to indicate that it is a fix
  * C: The message explains that it fixes bug.
  * R: F
    * New funcitionality: some registers or variables are exposed

67b56134ce: F T F
  * A: It seems that the PR only includes cleanups
  * C: I would say that is not a bug-fixing commit because it says "cleanups" in the message; but not totally sure because there are many changes in the commit.
  * R: F
    * Cleanup

cc5095747e: F T T
  * A: It seems that it tries to give a warning instead of an error for a certain bug. It is not clear to me that it actually fixes the bug.
  * C: It is a bug; but related to some info messagese.
  * R: T ?
    * This is a mitigation for a bug that is happening in a dependency. I think the key is "mark the page as clean to avoid unprivileged denial of service attacks until the problem can be properly fixed". In other words, a real problem with functionality is fixed, even when the real fix should be in a dependency (that is, the root cause for the bug happens elsewhere).

feb00b736a: T F F
  * A: It seems that it was introduced as a condition that a controller had to have read/write permissions when it really only needed to have at least one of the two.
  * C: For me; it is a refactor or a feature.
  * R: F ?
    * New functionality: allow a call to be R, W, or RW (was RW earlier). It seesm that new functionality is allowed. However, it could also be that the call was wrong, since it should allow the three modes, but it didn´t 

2acfab7101: F T F
  * A: An unneeded memory allocation is deleted
  * C: Refactoring.
  * R: F
    * Improvement (a buffer not needed is not allocated)

ad1c2f39fd: F T F
  * A: Use add instead of pop to counter (not a fix)
  * C: Refactor or feature; changing a method; but similar result
  * R: F
    * Seems like a performance improvement / refactoring

ea90330fa3: F T T
  * A: Maybe is a fix; maybe not. Just extend a check for a specific case
  * C: Looks like a fix; but not sure about the type.
  * R: T
    * It seems this is an adaptation to some kinds of firmware, which wouldn't load well. There is no hint this was reported as a bug, and it is likely that it is just an extension of requirements, to have into account those files. I'm labeling it as a bug just because it fixes a possible malfunction (the file wouldn't load).

18c91bb2d8: F T T
  * A: Remove unnecesary code
  * C: They are preventing future bugs/issues.
  * R: F
    * I think this is clearly a performance improvement. They change the way in which locks work, and they even mention the improvement thy measure.

e45cce30ea: F T F
  * A: An adjustment to ensure that no workers are left uncleaned
  * C: A feature; in my opinion.
  * R: F
    * This seems like an improvement: a better way of dealing with kthreads in a cgroup, by removing them earlier. It doesn't seem to have an effect on the overal functionality of the system (at least in terms of failures).

ab14f1802c: F T F
  * A: I do not understand the change
  * C: For me; it is a performance feature.
  * R: F
    * Refactoring (some calculus is done in a different place, the net result seems to be the same)

920a9fa27e: F T F
  * A: It seems that it only adds error handling (sanity check); although it is indicated as a fix.
  * C: Adding a feature about an error handling; it is not a bug fixing commit.
  * R: T
    * Syzbot is fuzzer, checking for bugs in the Linux kernel, https://github.com/google/syzkaller/blob/master/docs/syzbot.md In this case, it found one ("Syzbot once again hit uninit(ialized) value in asix driver"), which is fixed by adding a sanity check for a problem when reading from a USB driver, and code to check it in other places of the driver.

3e18bcb778: T F F
  * A: Many changes on the PR, i see some fix on them, but hard to identify it
  * B: After reading the mesage; I can conclude that the commit is not fixing a bug; it is refactoring and adding support (feature).
  * R: F
    * Changes are summarized at the begining of the comment. The frist change is changing how logs are logged (change in functionality), the second one adds support for a new device (added functionality). So, I don't see any BFC here.
