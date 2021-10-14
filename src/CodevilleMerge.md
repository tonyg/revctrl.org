# Codeville Merge

Traditional (or "Sloppy") Codeville merge is a [TwoWayMerge](TwoWayMerge.md) which makes use of additional annotation information in order to resolve conflicts.

Codeville's annotation is on the "slots" or spaces between lines, not on the lines themselves.  Each slot has associated with it a revision id.  When a line is added, both surrounding slots are set to the current change. When a line is deleted, the slot where that line used to be is set to the current change. Note: deletions are the motivation behind annotating slots rather than the lines themselves.

In addition to the annotation, Codeville merge maintains a list of all changes which have been applied.

For merging, there are 2 sides (versions of the given file) which are to be merged. Call them the left and the right. First, the [TwoWayMerge](TwoWayMerge.md) is run, resulting in an alternating set of matching and non-matching sections between the 2 sides. For each non-matching section it must be determined whether the left wins, the right wins or that there is a conflict.

Take lC as the set of changes in the annotation on the left side of a conflict section and rC as the set on the right. Take lA as the list of applied changes on the left and rA as the set on the right.

 - If lC - rA is non-empty, then the left side should win.
 - If rC - lA is non-empty, then the right side should win.
 - If both sides should win, then it's a conflict.
 - If _neither_ side should win, it's also a conflict. This is almost certainly non-obvious at first blush, but this situation can occur, albiet somewhat infrequently. This is what's known as an [AmbiguousCleanMerge](AmbiguousCleanMerge.md).

## Strengths

 * handles arbitrary history topologies
 * handles [StaircaseMerge](StaircaseMerge.md)
 * supports [AccidentalCleanMerge](AccidentalCleanMerge.md)

## Weaknesses

 * [Resolution](Resolution.md) can be inconsistent
 * susceptible to [AmbiguousCleanMerge](AmbiguousCleanMerge.md), which in turn can cause merge conflicts to repeat on every branch

## Used by

Codeville

## Related

[PreciseCodevilleMerge](PreciseCodevilleMerge.md)

----

[CategoryMergeAlgorithm](CategoryMergeAlgorithm.md)
