Name for the following merge example:

{{{
    a
   / \
  b   c
   \ / \
    c   d
}}}

An algorithm that supports StaircaseMerge will cleanly merge c and d to d.  The reasoning is that d, when created, defeated c; therefore, it should win cleanly.

This behavior is similar to ImplicitUndo because b was added and reverted, but while ImplicitUndo appears to be quite dangerous and tricky to implement, StaircaseMerge doesn't appear to cause any nasty edge cases and at least one technique for implementing it straightforwardly is known.

== Example: Repeated Staircase Merge ==

It's possible to have a repeated staircase merge

{{{
    a
   / \
  b   c
   \ / \
    c   d
     \ / \
      d   e
}}}

Note that this can easily continue as you repeatedly merge changes to a development branch into an unaltered branch. Most people agree that the user shouldn't have to repeatedly fix conflicts in this case, so it creates a compelling argument for clean merging of staircase.

== Example: Staircase vs. Convergence ==

This related case illustrates interesting complications which can arise:

{{{
    a
   / \
  b   c
   \ / \
    c   b
     \ / \
      b   e
}}}

Note that this is the same as the previous examples but with the "{{{d}}}"s changed to "{{{b}}}"s. Analogy with the previous example indicates that e should win cleanly, but GenerationCounting raises a conflict, because on the left "{{{b}}}" has been resurrected, and on the right it's alive for the first time). The theory behind this can be seen by comparing to the following case:

{{{
    a
   / \
  b   c
   \   \
    c   b
     \   \
      b   e
}}}

By ["Convergence"] we can ignore the "{{{c}}}"s, but since "{{{b}}}" was born, died, and re-born on the left, that's ["Convergence"] plus further history with the single birth of "{{{b}}}" on the right, so we have a conflict.

== Example: Convergence gets confused by Staircase ==

The following example illustrates a potential ambiguity in the semantics of Convergence when mixed with Staircase:

{{{
    a
    |\
    | \
    |  b
    |  |
    |  c
    d  |
    |\ |
    | \|
    |  d
    |  |
    c  |
    |  |
    b  c
}}}

In this case the decision of the branch on the right to go with d indicates that d wins over all of its history, so intuitively it would make sense for b to cleanly win at the bottom, because after d there is strictly convergent history with b winning. However, if GenerationCounting is used, then c wins cleanly.

Fixing this problem for a general text merger doesn't appear to be impossible. The following example clearly illustrates how this case should affect a boolean value, as is the case for line include/exclude as used in generation counting of text files:

{{{
    a
    |\
    | \
    |  b
    |  |
    b  a
    |\ |
    | \|
    |  b
    |  |
    a  |
    |  |
    b  a
}}}

A general algorithm for getting this right is unknown, although it feels notably similar to the problem of supporting staircase in a non-convergent scalar merge, which also doesn't have a good known algorithm.

= Supported by =

CodevilleMerge, ThreeWayMerge

= Not supported by =

MarkMerge

----

CategoryMergeExample
