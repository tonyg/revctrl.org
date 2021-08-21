# Die Die Die Merge

Proposed name for a widely used, but rarely formalized, BooleanMergeAlgorithm.

The rule is: if a 0 is a descendent of a 1, then that 0 beats all 1s.  otherwise, 1s beat 0s.

This algorithm never gives a conflict, and the user is not usually allowed to override its decision.

The main use is for modeling lifecycles of things like files.  A file's dead/alive state can be modeled by a boolean scalar, and add/deletes can be merged by using a boolean scalar merge algorithm.  This algorithm implements the simplest lifecycle -- a file is born once, lives for a time, but once dead it is permanently dead.  More complex lifecycles including resurrection can be implemented by swapping in more sophisticated merge algorithms, but this increases the complexity of the rest of the system.  Recording and tracking resurrections may be complex.  Resurrected files raise issues for content merging -- because arbitrarily many branches might have made conflicting changes, that were never resolved when the branches were merged because the files were removed first, but these conflicts must all be resolved when resurrecting the file (though this necessity depends on the content merge algorithm in use) -- and so on.  Therefore, several systems have decided to ignore or defer resurrection support for the time being, and use die-die-die-merge for lifecycles.

It may also be interesting theoretically, given the relation between ["BooleanMergeAlgorithm"]s and general ["ScalarMergeAlgorithm"]s.

= Strengths =

Very simple (simplest natural lifecycle model), gives very strong properties that ease design of other parts of the system.

= Weaknesses =

Only appropriate in very restricted cases.

= Used by =

["Monotone"], ["Codeville"], others?

= Related =

SimpleWeaveMerge uses this algorithm for the lifecycle of individual lines.

----

CategoryMergeAlgorithm
