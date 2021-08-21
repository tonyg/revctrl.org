# Precise Codeville Merge

PreciseCodevilleMerge is the combination of a weave-based merge with a resolution algorithm based on unique lines, plus [Convergence](Convergence.md), [GenerationCounting](GenerationCounting.md), [LivingLinesFirst](LivingLinesFirst.md), and [EdgeVersioning](EdgeVersioning.md). If you wish to answer the existential question of whether a particular piece of merge code is a version of [PreciseCodevilleMerge](PreciseCodevilleMerge.md), go over that checklist of features and if they're all there then it qualifies.

[ImplicitUndo](ImplicitUndo.md) isn't included because it conflicts with other features and has internal inconsistencies. Dynamic line ordering isn't included because of technical difficulties, although it's hoped that eventually somebody will figure out how to implement a weave which does partial ordering.

[ConvergentScalarMerge](ConvergentScalarMerge.md) can be thought of as the scalar (and thus much simpler) cousin of [PreciseCodevilleMerge](PreciseCodevilleMerge.md).

attachment:precisecodevillemerge.py

Those wishing to understand how the code works can start by reading through the no frills code, which doesn't support resolving to living lines first and [EdgeVersioning](EdgeVersioning.md), and thus is simpler to understand, and still gives the same answer as the full version most of the time.

attachment:nofrillsprecisemerge.py

An even less featureful merge algorithm than no frills is [SimpleWeaveMerge](SimpleWeaveMerge.md), which, oddly, is more complicated to implement than no frills.

= Strengths =

  * supports [Convergence](Convergence.md)
  * supports [StaircaseMerge](StaircaseMerge.md)
  * supports [EdgeVersioning](EdgeVersioning.md)

= Weaknesses =

  * doesn't support [ImplicitUndo](ImplicitUndo.md)

= Used by =

  * will be used by [Codeville](Codeville.md)
  * available for [Mercurial](Mercurial.md)
  * has been prototyped for [Vesta](Vesta.md)

= Related =

This uses the [Patience sorting](http://en.wikipedia.org/wiki/Patience_sorting) algorithm  to find the longest common subset.

----

[CategoryMergeAlgorithm](CategoryMergeAlgorithm.md)
