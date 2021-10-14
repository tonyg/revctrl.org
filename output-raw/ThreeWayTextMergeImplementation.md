# Three-Way Text Merge Implementation

Three way merge is the old workhorse of version control systems. When a merge is to be done between THIS and OTHER, it picks a common ancestor, BASE, and uses it as a guide in determining how the merge should be done.

Selecting BASE can be very tricky, and sometimes there isn't any single correct ancestor, especially in the case of [CrissCrossMerge](CrissCrossMerge.md).

There are several ways to implement three-way merging.

= Inexact Patching =

Since the goal of merging is to apply the changes made in another branch to your own, a fairly direct approach is to diff BASE and OTHER, and apply the resulting patch to THIS.

Since this approach uses context diffs, it can sometimes apply patches to the wrong place, a problem fixed by exact patching.

This has the failing that it does not recognize when THIS and OTHER have both made the same change, thus it will produce more conflicts than other approaches.

= Exact patching =

Exact patching is similar to inexact patching, except it makes two diffs, one from BASE to THIS, and one from BASE to OTHER, then uses the patch from BASE to OTHER to determine the line offsets to apply the patch from BASE to THIS to. It doesn't have to use context lines like inexact patching does, and can recognize [AccidentalCleanMerge](AccidentalCleanMerge.md) as a special case (especially important for 3way, since it runs into lots of erroneous accidental clean merges when BASE is selected too conservatively).  This is known in the subversion world as [Variance Adjusted Patching](http://subversion.tigris.org/variance-adjusted-patching.html).  The same concept can also be extended to work with binary diffs.  In the binary case you usually want a 'buffer' around the edges of the patch that is used to catch conflicts.  Interestingly, this buffer could be extended using the semantics of the file being edited - either to the nearest newline, or the nearest set of braces, etc.

= Three-way compare =
This approach compares all three texts, and divides them up into sections where

 * all agree
 * this and other agree
 * this and base agree
 * base and other agree
 * none agree

A drawback of this approach is that it is hard to determine section breaks;  If none agree, and later THIS and OTHER agree, which lines of BASE belong in the first section, and which in the second?  As a result, this case is treated as a single 'none agree' section, increasing the number of conflict lines.

In some sense all these techniques are variants of three way compare, but with the details fleshed out in different ways.

= Two-way tie-break =
This approach first compares THIS and OTHER.  Only the differences are processed further.  In areas where THIS and OTHER differ, the THIS and OTHER texts are both compared to the BASE text to break the tie.  If THIS text is the same as the BASE text, it loses.  If the OTHER text is the same as the BASE text, it loses.  If neither matches BASE, it is considered a conflict.

A drawback of this approach is that conflicts are not clearly associated with particular lines in Base.

= Bzr implementation of three-way compare =
The bzr implementation does a three-way comparison like so:
 1. Compare BASE to OTHER
 1. Compare BASE to THIS
 1. Combine the comparisons so that the section breaks happen in the same places, relative to BASE
 1. In sections where THIS and BASE coincide, pick OTHER
 1. In sections where OTHER and BASE coincide, pick THIS
 1. Sections in which both OTHER and THIS differ from BASE are treated as conflicts
 1. (Optional) a two-way merge is performed in conflict regions, to reduce conflicts.  (This step is optional, because it loses the connection between BASE and conflict regions)
