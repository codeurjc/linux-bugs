# Michel's observations 

- [COMMIT 59 - 316f710172] Not releasing memory (causing a memory leak) can result in critical errors in the application, which is why I consider it a Safety Related bug of the type "Memory".
- [COMMIT 61 - e3d5ea2c01] An infinite loop can result in a deadlock in execution and is therefore a safety related bug of the type "Timming and Execution".
- [COMMIT 64 - 32f1b53fe8] A hang in the application applies to a safety related error "Timming and Execution".
- [COMMIT 80 - c95aa2bab9] Build errors can be fixed, but never reach production (not really a functionality error)
- [COMMIT 940 - 228f324dc7] - Not consider as real changes the tests

More notes:
- Some goes wrong with the random commits. I feel that many commits are consecutive when annotated them. Examples: 352,353,354 ..
- Maybe "Perfective Commit" could have sub-classes. Change maintainers/doc its not the same as code refactor
- Commits 949, 951, and 975 are the same???