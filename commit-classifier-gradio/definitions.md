**Bug-fixing commit (BFC)**

Any commit that fixes a bug introduced in a previous commit.
A bug is a software fault introduced in a certain commit.

**BFC of an obvious bug**

Any commit that fixes a bug which  is clearly detectable by usual testing, that is, which causes obvious misbehavior on every operation, or so frequently that the effects would be clearly noticeable during testing.

**Safety-related BFC**

Any commit that fixes a safety-related bug.
A safety-related bug is any bug with potential to affect safety-relevant behaviors, as indicated by the categorizations described below, even when it may not be detected by typical testing because occurrence is intermittent and/or rare.

**Timing and execution**

With respect to timing constraints, the effects of faults such as those listed below can be considered for the software elements executed in each software partition: blocking of execution, deadlocks, livelocks, incorrect allocation of execution time or incorrect synchronization between software elements.

**Memory**
With respect to memory, the effects of faults such as those listed below can be considered for software elements executed in each software partition: corruption of content. inconsistent data (e.g. due to update during data fetch),stack overflow or underflow or read or write access to memory allocated to another software element.

**Exchange of Information**
With respect to the exchange of information, the causes for faults or effects of faults such as those listed below can be considered for each sender or each receiver: repetition of information, loss of information, delay of information, insertion of information, masquerade or incorrect addressing of information, incorrect sequence of information, corruption of information, asymmetric information sent from a sender to multiple receivers, information from a sender received by only a subset of the receivers or blocking access to a communication channel.