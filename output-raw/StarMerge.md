`star-merge` is the merge command used by tla.  It refers to a star topology, where both branches participating in the merge have a common ancestor or merge point.  The merge base selected is always[[FootNote(The documentation of star-merge is nearly impossible to decipher, and it does appear that in some rare cases it will accidentally pick a non-ancestor.)]] an ancestor in one of the two branches.  The limited selection of base revisions and the fact that merges are, by default, applied with diff and patch, mean that there are more conflicts than a ThreeWayMerge would necessarily have.

[[FootNote]]

Documented at: http://wiki.gnuarch.org/Merging_20with_20Arch
