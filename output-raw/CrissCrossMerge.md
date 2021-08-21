# Criss Cross Merge

A criss-cross merge is an ancestry graph in which minimal common ancestors are not unique.  The simplest example with scalars is something like:

```
   a
  / \
 b1  c1
 |\ /|
 | X |
 |/ \|
 b2  c2
```

---- /!\ '''Edit conflict - other version:''' ----
The story one can tell here is that Bob and Claire made some change independently, then each merged the changes together.  They conflicted, and Bob (of course) decided his change was better, while Claire (typically) picked her version.  Now, we need to merge again.  This should be a conflict.
Note that this can happen equally well with a textual merger -- they have each edited the same place in the file, and when resolving the conflict  they each choose to make the resulting text identical to their original version (i.e., they don't munge the two edits together somehow, they just pick one to win).

This is one of the key examples that has driven development of merge algorithms; there is currently no textual merge algorithm that fully handles this case (probably - see below).

---- /!\ '''Edit conflict - your version:''' ----
The story one can tell here is that Bob and Claire made some change independently, then each merged the changes together.  They conflicted, and Bob (of course) decided his change was better, while Claire (typically) picked her version.  Now, we need to merge again.  This should be a conflict.

Note that this can happen equally well with a textual merger -- they have each edited the same place in the file, and when resolving the conflict  they each choose to make the resulting text identical to their original version (i.e., they don't munge the two edits together somehow, they just pick one to win).

This is one of the key examples that has driven development of merge algorithms; there is currently no textual merge algorithm that fully handles this case (probably - see below).


---- /!\ '''End of edit conflict''' ----

= Three way merge =

[ThreeWayMerge](ThreeWayMerge.md) has obvious problems here -- there are two "least" (or more properly, "minimal") common ancestors it could use.

---- /!\ '''Edit conflict - other version:''' ----

---- /!\ '''Edit conflict - your version:''' ----

---- /!\ '''End of edit conflict''' ----
Furthermore, using ''either'' of them as a base for the merge will give an incorrectly clean merge -- if b1 as used as a base, it will appear that b2 is unchanged while c2 has changed, therefore c2 will win.  If c1 is used as a base, the opposite occurs.

One possible solution is to use 'a' as the common ancestor for the merge; this is the approach taken by [Monotone](Monotone.md), when it uses the [LCA+DOM](LCA+DOM.md) rather than [LCA](LCA.md) as a merge base.  However, this approach has its own problems.

---- /!\ '''Edit conflict - other version:''' ----

== Recursive three-way merge ==
Another possible solution is to first merge 'b1' and 'c1' to a temporary node (basically, imagine that the 'X' in the diagram is actually a revision, not just edges crossing) and then use that as a base for merging 'b2' and 'c2'. The interesting part is when merging 'b1' and 'c1' results in conflicts - the trick is that in that case, 'X' is included ''with the conflicts recorded inside'' (e.g. using the classical conflict markers). Since both 'b2' and 'c2' had to resolve the same conflict, in the case they resolved it the same way they both remove the conflicts from 'X' in the same way and a clean merge results; if they resolved it in different ways, the conflicts from 'X' get propagated to the final merge result. If a merge would result in more than two bases ('b1', 'c1, 'd1'), they are merged consecutively - first 'b1' with 'c1' and then the result with 'd1' .

This is what [Git](Git.md)'s "recursive merge" strategy does.

Recursive three-way merge _usually_ provides the right answer, however there are some edge cases. For example, conflict markers can be matched incorrectly, because they aren't given any special semantic meaning for the merge algorithm, and are simply treated as lines. In particular, there are (somewhat complicated) cases where the conflict markers of two unrelated conflicts get matched against each other, even though the content sections of them are totally unrelated.

Also, recursive merge can do some of the same invalid merges as [SimpleWeaveMerge](SimpleWeaveMerge.md) does, which are described below, although exactly what it does under those circumstances is highly dependant on the details of the 3 way merge algorithm, but it isn't clear that tweaking the 3-way merge algorithm to be more conservative about showing conflicts will make such problems go away. Basically, including the conflict is creating a weave, and that introduces the problems which weaves have.

Finally, recursive three-way merge has all the inherent problems of [ImplicitUndo](ImplicitUndo.md). In particular, merging together multiple things which merge cleanly will sometimes give different answers depending on the order in which the merges happen. In fact, it's possible in a never-ending criss-cross case for a value to flip-flop until the end of time without ever getting a single unclean merge. This is a very fundamental problem, and fixing it requires first deciding what one wants to have happen in such cases, because what is appropriate behavior is unclear.

---- /!\ '''Edit conflict - your version:''' ----

== Recursive three-way merge ==

Another possible solution is to first merge 'b1' and 'c1' to a temporary node (basically, imagine that the 'X' in the diagram is actually a revision, not just edges crossing) and then use that as a base for merging 'b2' and 'c2'. The interesting part is when merging 'b1' and 'c1' results in conflicts - the trick is that in that case, 'X' is included ''with the conflicts recorded inside'' (e.g. using the classical conflict markers). Since both 'b2' and 'c2' had to resolve the same conflict, in the case they resolved it the same way they both remove the conflicts from 'X' in the same way and a clean merge results; if they resolved it in different ways, the conflicts from 'X' get propagated to the final merge result. If a merge would result in more than two bases ('b1', 'c1, 'd1'), they are merged consecutively - first 'b1' with 'c1' and then the result with 'd1' .

This is what [Git](Git.md)'s "recursive merge" strategy does.

Recursive three-way merge _usually_ provides the right answer, however there are some edge cases. For example, conflict markers can be matched incorrectly, because they aren't given any special semantic meaning for the merge algorithm, and are simply treated as lines. In particular, there are (somewhat complicated) cases where the conflict markers of two unrelated conflicts get matched against each other, even though the content sections of them are totally unrelated.

Also, recursive merge can do some of the same invalid merges as [SimpleWeaveMerge](SimpleWeaveMerge.md) does, which are described below, although exactly what it does under those circumstances is highly dependant on the details of the 3 way merge algorithm, but it isn't clear that tweaking the 3-way merge algorithm to be more conservative about showing conflicts will make such problems go away. Basically, including the conflict is creating a weave, and that introduces the problems which weaves have.

Finally, recursive three-way merge has all the inherent problems of [ImplicitUndo](ImplicitUndo.md). In particular, merging together multiple things which merge cleanly will sometimes give different answers depending on the order in which the merges happen. In fact, it's possible in a never-ending criss-cross case for a value to flip-flop until the end of time without ever getting a single unclean merge. This is a very fundamental problem, and fixing it requires first deciding what one wants to have happen in such cases, because what is appropriate behavior is unclear.

---- /!\ '''End of edit conflict''' ----

= Scalar codeville merge =
Traditional [CodevilleMerge](CodevilleMerge.md) on scalar values gives an [AmbiguousCleanMerge](AmbiguousCleanMerge.md) here -- the last-changed revision for b2 is b1, which is an ancestor of c2, and thus c2 should win cleanly; similarly, the last-changed revision for c2 is c1, which is an ancestor of b2, and thus b2 should win cleanly.

This somewhat anomalous case is normally presented to the user as a conflict (what else can one do?), which is the right result.  But there is a more subtle problem:

```
   a
  / \
 b1  c1
 |\ /|
 | X |
 |/ \|
 b2  c2
  \ / \
   b3  c3
```

---- /!\ '''Edit conflict - other version:''' ----
Suppose someone else commits another version under c2, in which they didn't touch this scalar at all -- they are blissfully ignorant of Bob and Claire's shenanigans.  Now, this should merge cleanly -- someone has resolved the b2/c2 conflict, someone else has made no changes at all, all should be fine. But it's not; it's another ambiguous clean merge, because the last-changed revisions for b3 and c3 are still b1 and c1, respectively.  In fact, this can continue arbitrarily long:

---- /!\ '''Edit conflict - your version:''' ----
Suppose someone else commits another version under c2, in which they didn't touch this scalar at all -- they are blissfully ignorant of Bob and Claire's shenanigans.  Now, this should merge cleanly -- someone has resolved the b2/c2 conflict, someone else has made no changes at all, all should be fine. But it's not; it's another ambiguous clean merge, because the last-changed revisions for b3 and c3 are still b1 and c1, respectively.  In fact, this can continue arbitrarily long:

---- /!\ '''End of edit conflict''' ----

```
   a
  / \
 b1  c1
 |\ /|
 | X |
 |/ \|
 b2  c2
  \ / \
   b3  c3
    \ / \
     b4  c4
```
This is yet another conflict.  These conflicts continue so long as new versions are committed that do not have the ambiguous-clean resolution as an ancestor.

(Of course, if at any point someone resolves one of these repeated conflicts in favor of c, then things get even more complicated.

= *-merge =
[MarkMerge](MarkMerge.md) *-merge handles this case well.  The graph, annotated with *s, is:

```
   a*
  / \
 b1* c1*
 |\ /|
 | X |
 |/ \|
 b2* c2*
```

---- /!\ '''Edit conflict - other version:''' ----
Note that the two conflicting merges at the end cause b2 and c2 to be marked. This the key to *-merge's success in this case.  *(b2) = b2, and *(c2) = c2, neither of c2 and b2 are an ancestor of the other, so a conflict is reported.

---- /!\ '''Edit conflict - your version:''' ----
Note that the two conflicting merges at the end cause b2 and c2 to be marked. This the key to *-merge's success in this case.  *(b2) = b2, and *(c2) = c2, neither of c2 and b2 are an ancestor of the other, so a conflict is reported.

---- /!\ '''End of edit conflict''' ----

Nor does *-merge suffer from the indefinite procession of repeated conflicts:

```
   a*
  / \
 b1* c1*
 |\ /|
 | X |
 |/ \|
 b2* c2*
  \ / \
   b3* c3
```

---- /!\ '''Edit conflict - other version:''' ----
Because b2 and c2 conflicted, b3 is marked; c3, however, is not changed from its parent, so it is not marked.  Therefore b3 wins this merge cleanly.

---- /!\ '''Edit conflict - your version:''' ----
Because b2 and c2 conflicted, b3 is marked; c3, however, is not changed from its parent, so it is not marked.  Therefore b3 wins this merge cleanly.

---- /!\ '''End of edit conflict''' ----

*-merge does perform sub-optimally in a similar case:

```
    a*
   / \
  b1* c1*
  |\ /|
  | X |
  |/ \|
  b2* c2*
 / \ /
d*  b3*
```

---- /!\ '''Edit conflict - other version:''' ----
Here it reports a conflict, rather than merging cleanly to d.  However, this is because this is a [StaircaseMerge](StaircaseMerge.md), and has nothing to do with the criss-cross merge at all. 

---- /!\ '''Edit conflict - your version:''' ----
Here it reports a conflict, rather than merging cleanly to d.  However, this is because this is a [StaircaseMerge](StaircaseMerge.md), and has nothing to do with the criss-cross merge at all. 

---- /!\ '''End of edit conflict''' ----


[[Anchor(orderingambiguities)]]

= Simple weave merge =
[SimpleWeaveMerge](SimpleWeaveMerge.md) handles the simple form of criss-cross correctly.  However, it runs into problems on a slightly different example, that only arise in the textual merging case:

```
    xy
   /  \
 xby  xcy
  | \/ |
  | /\ |
  |/  \|
xbcy  xcby
```
(each letter represents a line in a file)

Here Bob and Claire have managed to overcome their differences somewhat -- they each actually include the other's new lines when they merge -- but they both insist that their own line must come _first_.


---- /!\ '''Edit conflict - other version:''' ----
[SimpleWeaveMerge](SimpleWeaveMerge.md) will silently clean merge this to either `xcby` or `xbcy` -- which it picks is somewhat random, and depends on the details of the [Resolution](Resolution.md) and global ordering it uses.

---- /!\ '''Edit conflict - your version:''' ----
[SimpleWeaveMerge](SimpleWeaveMerge.md) will silently clean merge this to either `xcby` or `xbcy` -- which it picks is somewhat random, and depends on the details of the [Resolution](Resolution.md) and global ordering it uses.

---- /!\ '''End of edit conflict''' ----


= DARCS merge =

The DARCS merge algorithm would generate something like this:

```
      a
     / \
    b1  c1
    |\ /|
    | X |
    |/ \|
m(b,c) m(b,c)
    |   |
    b2  c2
```

Where `m(b,c)` is a "merger" patch for `b1` and `c1`.  The end result is that DARCS behaves the same as Git does with its recursive three way merge, except that DARCS uses a special form for its 'merger patch' rather than normal conflict markers.  This makes sure that there are no problems with textual merge and conflict markers (such as mis-matched delimiters, etc).

----

[CategoryMergeExample](CategoryMergeExample.md)
