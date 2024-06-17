# Tool observations

- "Lore founded" is not saved
- When loading a CSV some fields are not stored/loaded right, I get sometimes the `TypeError: '>' not supported between instances of 'str' and 'int'` error. It could be fixed if we filled out automatically the empty fields with a NaN value (I think).

# Commits observations

- Similar commits appears in a row, it is supposed to be random but I'm note sure about this.
- We should save Merge commits in the CSV
- It is not clear to me ig analyzing a commit of a patchest makes sense instead of analyzing the patchset itself.
- Many fields to fill out lead to a long time to annotate.
