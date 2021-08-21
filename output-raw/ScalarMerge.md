# Scalar Merge

== What is Scalar Merge? ==

There are a number of different types of merge algorithm.  In order to introduce more theory into merge algorithms, these can be subdivided into a number of types.  One type of merge algorithm is the ''scalar merge'', so called because it assumes that each revision consists of only a single scalar.

Whereas traditional textual merge algorithms allow two different changes to a document to be merged, scalar merge simply decides which scalar wins cleanly, or that there is a conflict for the user to resolve.

A special case of scalar merge is the [BooleanMergeAlgorithm](BooleanMergeAlgorithm.md).  [DieDieDieMerge](DieDieDieMerge.md) is one example of such a boolean scalar merge algorithm.

== Converting to full merge ==

There is a general theory of building complex merge algorithms using a scalar merger as a primitive.  This description originated with Nathaniel Smith in a [revctrl mailing list post](http://article.gmane.org/gmane.comp.version-control.revctrl/189):

You provide:
  * the data structure you want to define a merger for.  E.g., directory trees, or sets, or something.  Note the invariants of this structure.  (E.g., in a directory tree, you cannot have two distinct files with the same name.)
  * a scheme to decompose any instance of this structure into a collection of scalar fields.  (E.g., for directory trees, you could have one scalar associated with each file, this scalar being a (parent directory pointer, basename) pair; for sets, you could have a scalar associated with each possible item which takes on the values True or False for whether that value is in the set at hand.)
  * a scheme to, given two structures A and B in a history graph, determine which scalar fields in the decomposition of A are "the same" as the which scalar fields in the decomposition of B.  (We can call this step Self:Resolution.)  (E.g., if you have arch/bzr-style directory trees, you associate a global unique id with each file/dir, and two fields match up if they go with the same entity id; or if you have monotone-style directory trees, you look at the add/rename/drop stanzas in the changeset between two trees and it tells you which files match up.)

Then to merge two structures:
   * for each scalar field in the result object, use the Self:Resolution to find all the corresponding fields in all the structures in the history graph; this gives you a scalar DAG.  Use your favorite scalar merge algorithm on this graph.  This may give a conflict, call this a primitive conflict if it happens.
   * after you have merged all the scalar fields, put your overall structure back together and check to see if any structural invariants from (1) are violated.  If so, flag these as conflicts ("structural conflicts") too.

This works perfectly well to get excellent tree mergers and set mergers, and probably other things.  I don't know how to use this approach to get a sequence merger (which is really the structure involved in text merging).  The obvious approach is to model a sequence as some kind of linked list, with the link pointers the scalar fields, and I played around with this some and it actually works more or less (and is very closely related to edge versioning, actually).  It might even work; I stopped playing with it because:
   * I wasn't sure how to get a good handle on the structural conflicts -- in principle after scalar merging your "linked list" could have arbitrarily wacky structure, complete with loops and stuff, and it's not clear how to turn this into a nice file-with-conflict-marked-sections representation for the user. Maybe in practice you can limit how wacky the structure gets, though, I dunno.
   * What I really want is a user model for text merging; this wasn't necessarily getting me any closer to that, so even if it all worked out, I wouldn't know whether I'd actually accomplished anything anyway.
   * Merge algorithms are fun, but we were already far enough developing all this theory that it was time to stop and actually implement stuff and come back to all this later, when there weren't a million other more practical things to spend time on :-).  (3-way text merging kind of sucks, but it's not like an urgent bug that users complain about every day.)

[Weave](Weave.md) merging can also be seen as a special case of this formalism, with the scalar fields being the boolean "does this line in the weave currently exist" values.

= Scalar Merge Algorithms =

To add a page to this category, add a link to this page on the last line of the page. You can add multiple categories to a page.

----

[CategoryCategory](CategoryCategory.md) [CategoryMergeAlgorithm](CategoryMergeAlgorithm.md)
