# Convergent Scalar Merge

Convergent scalar merge is a scalar merge algorithm based on the property that if A and B are merged and A has an ancestor whose history is isomorphic to B's history, then A should win. It's similar to [MarkMerge](MarkMerge.md), and can be thought of as the scalar version of [PreciseCodevilleMerge](PreciseCodevilleMerge.md) (in fact, they were developed in tandem).

attachment:ConvergentScalarMerge.py

= Strengths =

  * supports [Convergence](Convergence.md)
  * handles [StaircaseMerge](StaircaseMerge.md)
  * has a conceptually simple motivation

= Weaknesses =

  * doesn't support [ImplicitUndo](ImplicitUndo.md)

= Used by =

  * Will be used by [Codeville](Codeville.md)

= Related =

  * [MarkMerge](MarkMerge.md)

----

[CategoryMergeAlgorithm](CategoryMergeAlgorithm.md)
