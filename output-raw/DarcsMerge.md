# Darcs Merge

For every patch `P` to be merged in the tree,

 1. Find a patch `T_n` in the current tree whose context is identical to that of `P`
 2. Bring all the patches `T_(n+1)..T_(max n)` that have been recorded after that patch into the context of `P` (creating patch `P'`)
 3. If some patch `T_x` cannot be brought to `P`'s context, change `P` into a conflict patch that cancels `P` and `T_x`, and continue bringing the rest of the patches into `P`'s context
 4. Apply patch `P'`

It's that simple!

There is a [thread](http://www.abridgegame.org/pipermail/darcs-users/2003/000221.html) on the darcs users mailing list comparing [DarcsMerge](DarcsMerge.md) and the exact patching form of [ThreeWayTextMergeImplementation](ThreeWayTextMergeImplementation.md).

= Strengths =

 * Is always able to apply patches that don't really conflict.
 * Merging branches with many changes on both sides does not make it less probable that the merge will succeed
 * Patches never apply "wrong".
 * A tree with the same set of patches always has the same content.
 * Allows orthogonal change types (e.g. identifier renames and hunks) to merge cleanly.
 * Does not lose patch identity in merge
 * Handles all merge "problems", such as [CrissCrossMerge](CrissCrossMerge.md), [AccidentalCleanMerge](AccidentalCleanMerge.md) or [StaircaseMerge](StaircaseMerge.md).  (These problems simply don't exist with this algorithm.)

= Weaknesses =

 * You cannot use "traditional" diffs internally.  They cannot accommodate conflict patches.
 * Conflict becomes a repository state, not a working-tree state.  (Some would consider this a pro)
 * The "same" patch may have a different content in different trees, if it has different context (i.e. patches are ordered differently in those trees)
 * Nobody has proved that the performance of conflict-conflict merge corner cases can be improved from `O(exp n)`
 * Requires additional work if you want to record who merged what and when.  (This is because the merge algorithm itself does not need this information.)

= Used by =

Darcs.

= Related =

Any merge algorithm that deals directly with patches.

----

[CategoryMergeAlgorithm](CategoryMergeAlgorithm.md)
