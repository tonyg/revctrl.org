# Implicit Undo

An (arguably) beneficial property for a merge algorithm to have.

An algorithm that supports implicit undo is one in which someone can make a change, and then revert that change, and the merge algorithm will act as if the change never happened.

The simplest scalar example is:
```
   a
  / \
 b   c
 |
 a
```

An implicit undo supporting algorithm will make this a clean merge to `c`.

To make things trickier, the case:
```
   a
   |
   b
  / \
 a   b
```
should also be a clean merge, but with `a` winning.  The intuition is that if I undo some changes back to an earlier version, the undo should beat all the things that are undone, but should lose to all the things that beat the earlier version.

= Discussion =

This is a problem that has arisen only with the development of more advanced merge algorithms; 3-way merge does not have this problem, because it simply ignores almost all historical information.  However, there is a direct trade-off -- 3-way merge faces more [resolution](Resolution.md) ambiguities as a result. More disturbingly, a series of clean merges using 3-way merge can cause an undo of a change to silently disappear, with no user editing whatsoever.

The use case for this is reasonably common (people making changes, and then reverting them), and users have some expectation that it will work, since 3-way merge works this way.  Not supporting implicit undo also puts a heavier burden on conflict resolution UIs, because it may be entirely obscure to the user why they are seeing a particular conflict.

However, it is a somewhat controversial feature, because its is not clear what effect supporting it will have on the global stability and transparency of the merge system -- if not done carefully, there is a danger of introducing new failure modes, extremely complex causes, and spooky action at a distance.  There is not yet consensus on whether the possible benefits outweigh the possible risks, especially as no-one has yet produced a fully working algorithm that supports implicit undo.  This is an active research area.

Implicit undo in its strongest form has been shown to be internally inconsistent. See http://article.gmane.org/gmane.comp.version-control.revctrl/89. A weaker version may still prove workable.

Handling implicit undo is particularly tricky for textual merge algorithms, because it is not enough to build on top of an implicit undo supporting scalar merge algorithm; one must also modify one's [resolution](Resolution.md) algorithm.

In some cases implicit undo and ["convergence"](Convergence.md) give conflicting answers. The following is the simplest example:

```
   a
  / \
 b   b
 |
 a
```

Convergence clearly dictates that the above should merge to a, while implicit undo indicates that it should merge to b. The general consensus is that convergence is more important in this case than implicit undo.

Partially because of this case, the best hope of having working implicit undo at this point is to make a conservative implementation whose only behavior is to in some cases take conflicts given by a convergence-supporting merge algorithm and resolve them cleanly.

The above example is particularly bad for textual merges, because a line deletion may or may not count as being convergent depending on whether it's done as part of another change. For example with `AXB -> AB -> AXB` versus `AXB -> AYB`, the `AYB` wins by implicit undo, but with `AXB -> AB -> AXB` versus `AXB -> AB -> AYB`, there is convergence, but each individual line has the same history in both examples.

Implicit undo can cause a descendant with is different from either ancestor, for example:

```
   a
  / \
 b   b
 |\ /|
 a X a
 |/ \|
 b   b
```

If one supports full-blown implicit undo, then in this case both b's at the bottom were clean merges, because they were examples of the previous example, but since both b's have already been overridden, then merging these two b's together should result in a. This example doesn't hit an internal inconsistency in implicit undo, but it does conflict with the obvious principle that the descendant of two identical ancestors should cleanly merge to those ancestors, and it's a much simpler example than the one which demonstrates an internal inconsistency.

Fortunately this example is also one which heavily relies on a case where implicit undo doesn't conflict with convergence, so applying convergence first and only if that doesn't give an answer applying implicit undo continues to appear promising.

The following is a case where convergence prevents implicit undo from working:

```
   a
  / \
 c   c
 |   |
 a   b
```

Here's a strange edge case:

```
        a
        |\
        | \
        |  \
        |   p
        |   |
        b   a
        |\ /|
        | X |
        |/ \|
        b   a
```

Note that there is no convergence here.

In this case, if we assume no implicit undo then we clearly have a conflict, but if we assume implicit undo then both nodes at the bottom would have resolved to the same b, and one of them was overwritten by a, so clearly a should win. The problem here is that we're making strong assumptions about what merge algorithms were used in the construction of ancestor nodes, and those assumptions are likely to be violated in practice.

Here is another edge case:

```
        a
       / \
      /   \
     b     p
     |\    |
     | \   a
     r  \ /|
     |   X |
     b  / \|
     | /   q
     |/    |
     b     a
```

Again note the lack of convergence.

This is sort of like an ambiguous clean merge for implicit undo - each side has defeated an identical ancestor of the other, so we have a conflict by both sides winning.

The above examples in aggregate seem to indicate that supporting implicit undo is a fairly sketchy proposition. Perhaps it's better to support explicit undo, by having a command which rewrites local history (which hasn't been commited elsewhere) to pretend that a particular section of code never got changed in the first place.

= Supported by =

[ThreeWayMerge](ThreeWayMerge.md)

= Not supported by =

[DarcsMerge](DarcsMerge.md), [MarkMerge](MarkMerge.md), [SimpleWeaveMerge](SimpleWeaveMerge.md), others

----

[CategoryMergeExample](CategoryMergeExample.md)
