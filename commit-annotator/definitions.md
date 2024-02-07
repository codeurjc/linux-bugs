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