# Precise Codeville Merge

PreciseCodevilleMerge is the combination of a weave-based merge with a resolution algorithm based on unique lines, plus [[Convergence]], GenerationCounting, LivingLinesFirst,  and EdgeVersioning. If you wish to answer the existential question of whether a particular piece of merge code is a version of PreciseCodevilleMerge, go over that checklist of features and if they're all there then it qualifies.

ImplicitUndo isn't included because it conflicts with other features and has internal inconsistencies. Dynamic line ordering isn't included because of technical difficulties, although it's hoped that eventually somebody will figure out how to implement a weave which does partial ordering.

ConvergentScalarMerge can be thought of as the scalar (and thus much simpler) cousin of PreciseCodevilleMerge.

attachment:precisecodevillemerge.py

Those wishing to understand how the code works can start by reading through the no frills code, which doesn't support resolving to living lines first and EdgeVersioning, and thus is simpler to understand, and still gives the same answer as the full version most of the time.

attachment:nofrillsprecisemerge.py

An even less featureful merge algorithm than no frills is SimpleWeaveMerge, which, oddly, is more complicated to implement than no frills.

= Strengths =

  * supports [[Convergence]]
  * supports StaircaseMerge
  * supports EdgeVersioning

= Weaknesses =

  * doesn't support ImplicitUndo

= Used by =

  * will be used by [[Codeville]]
  * available for [[Mercurial]]
  * has been prototyped for [[Vesta]]

= Related =

This uses the [[http://en.wikipedia.org/wiki/Patience_sorting|Patience sorting]] algorithm  to find the longest common subset.

----

CategoryMergeAlgorithm
