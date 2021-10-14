# Rollback

A desirable feature for VCSes/merge algorithms -- temporary rejection of integrated changes.  This is a use case that is very poorly supported by all basic DAG+merge systems.

To go into more detail: Imagine you have two branches, let's call them "stable" and "ultragizmo".  At some point, it's determined that the new ultragizmo feature is stable enough to integrate, so "ultragizmo" is merged into "stable".  A few days later, someone discovers a huge, horrible bug in the new code, that will take some time to fix.  We want to be able to do the following:
  * Back out the changes to "stable", to get back to a, well, stable state, while the bug is worked on
  * Continue to be able to merge stable->ultragizmo (so that the feature branch can track other changes occuring in the stable branch)
  * Continue to work on the ultragizmo branch, fixing the bugs.
  * Eventually repeat the merge from ultragizmo->stable.

## The problem

So suppose we do this naively:
```
    a
   /|
  / |
 b  a
 |\ |
 | \|
 |  b
 |  |
 b  a
```
Here 'b' is the unstable value and 'a' is the stable value.  The problem is that in backing out the change to the stable line, we reverted the a->b change by creating an "anti-patch" for it, and injecting that into the system.  Now that there is a b->a patch in the system, our merger will happily kill all 'b's, whereever they are found.  For instance, if we merge stable->ultragizmo, all of the work done on the ultragizmo will be silently reverted.  Even if we don't merge stable->ultragizmo, when we later try again to integrate the (now bug-free) ultragizmo code by merging from ultragizmo->stable, the changes will be stripped out and we will fail to actually get our changes into the stable branch.  Oops.

It's important to stress that in other cases, this is exactly the right behavior -- if we revert a patch because we have realized that it is simply a bad idea, and are rejecting it, then we _want_ this anti-patch to go out and kill every instance of 'b' that is is merged into.  It is also consistent with the rest of the system (e.g., if 'b' was replaced with 'c' instead of 'a', then obviously 'c' beating 'b' would be the right behavior).

This suggests that systems should, perhaps, provide some extra way for the user to indicate what behavior they want -- e.g., some way to say "I am only temporarily backing out this patch; I want my new 'a' to beat any 'b's that are descendents of the old 'a' -- e.g.:
```
    a
   /|
  / |
 b  a
  \ |
   \|
    b
    |\
    a b
```
here 'a' should win -- but it should lose to all other 'b's."

In real cases, of course, things are made more complex because we are generally dealing with textual merging rather than scalar merging, and so we need to think about situations where only certain hunks are being rolled back, etc.

Support rollback can create some counter-intuitive properties.  For instance, if the edge labeled R is a rollback, then the following case should be a clean win for 'b':
```
   a
  / \
 b   a
 |\  |
 | \ |
 |  \|
 |   b
 |   |R
 |   a
  \ /
   ?
```
which violates a rule of thumb used when evaluating merge algorithms -- that when merging A and B, where A is an ancestor of B, B should win unconditionally.

## Workarounds

### Double-revert

One way to work around this problem is to:
  * revert the changes to stable
  * merge from stable->ultragizmo
  * revert ultragizmo back to what it was before the merge
I.e., we essentially create an anti-anti-patch, and work off of that.  Doing this in such a way that we do not wipe out independent changes made on the stable branch, or interfere with any newer changes made on the unstable branch, requires care.  Here's one approach.  Given a complex situation like:
```

 S1
 | \
 |  \
 S2  U1
 |  / \
 | /   \
 S3     \
 |       U2
 S4
```
We want to preserve both the S1->S2 and S3->S4 changes (and leave open the possibility of merging them into the unstable branch), preserve the S1->U2 changes (and leave open the possibility of later merging them into the stable branch), while getting the U1->S3 changes out of the stable branch.

First, re-commit the S1 state as a child of S3, and then re-commit the S2 state as a child of that, both into the stable branch (or into a temporary branch, if your VCS only supports linear branches):
```
 S1
 | \
 |  \
 S2  U1
 |  / \
 | /   \
 S3     \
 | \     U2
 S4 \
     S1'
     |
     S2'
```
Now, re-commit the U1 state as child of S1', into the unstable branch (or, again, another temporary branch):
```
 S1
 | \
 |  \
 S2  U1
 |  / \
 | /   \
 S3     \
 | \     U2
 S4 \
     S1'
     |  \
     S2' \
         U1'
```

Now we can merge U1' and U2 into the unstable branch; the result should be identical to U2.  (Either because this happens naturally, as ImplicitUndo would produce, or because we force this result.)  We can also merge S2' with S4 into the stable branch; the result should contain the S1->S2 and S3->S4 changes, but not the bad S2->S3 changes:
```
 S1
 | \
 |  \
 S2  U1
 |  / \
 | /   \
 S3     \
 | \     U2
 S4 \     \
 |   S1'   \
 |   |  \   \
 |   S2' \   \
  \ /    U1' /
   S5      \/
           U2'
```
As you can see, we've essentially reproduced the entire old revision graph, but with the badness left out.  Fortunately, this trick does not require one to reproduce arbitrarily large graphs -- even if there were multiple commits between S1 and S2, they could be compressed down into a single one -- the trick is to re-commit the last stable->unstable branch point.

Adapting this trick to situations in which there is no unique branch point, where the stable and unstable graph are both bushier, when there has already been another merge from stable->unstable since the offending merge, etc., is left as an exercise for the reader.

Contrariwise, I'm pretty sure the approach can be simplified if we do want to merge stable->unstable (commonly true, but not fair to assume in the general case), and especially if the intermediate commits don't exist.

All of this requires a VCS that supports:
  * merging between arbitrary historical revisions, not just branch heads
  * [AccidentalCleanMerge](AccidentalCleanMerge.md) (see below)
One also has to take care with things like invertibility -- in many systems, a delete is not truly invertible; all that can be done is create a new file with the same name and contents as the old one.

An alternative is to simply discard the original development branch, and recreate it from the double-reverted base:
```
 S1
 | \
 |  \
 S2  U1
 |  / \
 | /   \
 S3     \
 | \     U2   (everyone pretend this revision doesn't exist!)
 S4 \
 |   S1'
 |   |  \
 |   S2' \
  \ /    U1' (double-revert)
   S5      \
           U2' (everyone should use this)
```
This may be appropriate in some cases, though care should be taken: it causes tricky coordination problems, may lose history, and may not be possible if, for instance, the two branches are controlled by different people/organizations (say the "stable" branch is Bob's Kernel Distro's kernel branch, and the "ultragizmo" branch is Linus's branch, and Linus doesn't care about Bob's travails).  The biggest advantage of the complex dance done above is that ordinary merge tools will work, even if more work has been done against U2 -- you can simply merge U3 and U2'.  (This is why [AccidentalCleanMerge](AccidentalCleanMerge.md) is important here, or possibly [Convergence](Convergence.md).)

The situation is symmetrical enough that you can also do things the other way around, discarding the bad part of the stable branch and recreating it:
```
    S1
    | \
    |  \
    S2  U1
   /|  / \
S4' | /   \
    S3     \
    |       U2
    |
    S4 (everyone ignore this!  use S4' instead!)
```

## Other

BramCohen says he has a way to punt on supporting this inside the merge algorithm, and can get the desired behavior entirely outside.  The purpose of this paragraph is to shame him into sharing it on the wiki ;-).

## Supported by

DARCS.

## Not supported by

Everything but DARCS.

----

[CategoryMergeExample](CategoryMergeExample.md)
