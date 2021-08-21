# Accidental Clean Merge

When "the same change" is made independently on two branches, and they are then merged:

```
    a
   / \
  b   b
```

A change was made on both sides, so arguably this should be a conflict; however, the changes happen to be identical, so "accidentally" we get a clean merge after all.

An algorithm is said to support accidental clean merge if it gives no
conflict in this case.  [[Convergence]] implies AccidentalCleanMerge.

There are cases where AccidentalCleanMerge will perform a semantically 
incorrect merge. For example, two different people may add a line saying i++;
to the same location, and the correct merge of those two may be two lines both saying i++; rather than
a single line saying i++;. The frequency of such semantic errors is comparable to
the frequency of semantically invalid merges of code changes to lines of code
in disparate locations, which clean merge under all merge-based version control
systems.

Almost all systems support accidental clean merging of file deletion.
Systems which view a file's location as an integral part of its identity,
such as CVS, generally support accidental clean merge of file addition.
Systems which support file renames generally don't support accidental
clean merge of file addition, even if two files with identical contents were
added to identical trees. Ideally, one would like to be able to clean up
such conflicts with a suture command (if the files were in fact the same),
but nothing currently supports that feature.

= Supported by =

Many implementations of ThreeWayMerge (as a special case); multi-MarkMerge

= Not supported by =

DarcsMerge sees this as a conflict.

----

CategoryMergeExample
