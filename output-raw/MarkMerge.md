# Mark Merge

A scalar merge algorithm, related to [CodevilleMerge](CodevilleMerge.md).  Generally referred to as "mark-merge" or "*-merge" (but never [StarMerge](StarMerge.md), which is something else entirely).

Detailed writeup of original version: http://thread.gmane.org/gmane.comp.version-control.monotone.devel/4297 ("unique-*-merge")

Detailed writeup of updated version (handles accidental clean merges): http://article.gmane.org/gmane.comp.version-control.revctrl/93 ("multi-*-merge")

Other links: http://article.gmane.org/gmane.comp.version-control.revctrl/92, http://article.gmane.org/gmane.comp.version-control.revctrl/197 ("deterministic-*-merge")

The most interesting things about *-merge are:
  * has a [UserModel](UserModel.md)
  * has a formal analysis showing that it is fully well-defined, and implements the [UserModel](UserModel.md)

= Strengths =

  * best formal analysis of any current merge algorithm
  * believed to never clean merge without justification (conservative)
  * "deterministic \*-merge" (basically multi-\*-merge but easier to make formal statements about) is commutative and associative (i.e., satisfies [OperationalTransformation](OperationalTransformation.md) theory's properties TP1 and TP2).

= Weaknesses =

  * unique-\*-merge does not handle accidental clean merges; multi-\*-merge does
  * does not handle [StaircaseMerge](StaircaseMerge.md)
  * does not attempt [Convergence](Convergence.md)
  * does not attempt implicit rollback

= Used by =

[Monotone](Monotone.md)

= Related =

[CodevilleMerge](CodevilleMerge.md)

----

[CategoryMergeAlgorithm](CategoryMergeAlgorithm.md) [CategoryScalarMerge](CategoryScalarMerge.md)
