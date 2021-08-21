Resolution is the process where a version control system takes a file which has been edited by a user and implicitly heuristically determines what the changes which have been made are. All version control systems (except for distant relatives which hook into editors like microsoft word) must perform resolution at some point.

Most version control systems have to do some kind of resolution to do regular merging, which sometimes makes the distinction between merging and resolution unclear. As a rule of thumb, if something has to do a diff-like operation, it's doing resolution.

Resolution is generally done against either one or two ancestors. When there are two ancestors, it's frequently done as separate diffs against either one, or sometimes as a single diff against a combination of the two (or a combination of all ancestors, in the case of a weave). As a result, most version control systems manage to have a single function for comparing two line-delimited files against each other and pairing up matching lines. Many of them literally use an external diff program.

== approaches to diff ==

There are two basic approaches to doing a diff. One is to find a longest common substring on the two files, then fix that substring as a match and do divide and conquer on the sections before and after. This approach can be led very astray if there are two files with a lot of short matching sequences throughout but a single slightly longer matching sequence at the beginning of one and the end of the other.

The other approach is to find a longest common subsequence on the two files.
This can sometimes result in very bad matches which pair up lots of unrelated open and close curly bracket lines. An improvement to this approach is to do a longest common subsequence on only the lines which appear exactly once in both files, then extend matches forward and backward, and do divide and conquer on the unmatched sections (because lines might be unique within a subsection even if they aren't unique for the whole file). It may be necessary to have a final regular LCS pass in that case to reasonably handle files which are almost entirely repeated lines.

''(Is there a diff algorithm that recognizes "moves" of entire paragraphs (or functions) from one location to another as "less of a change" than a delete followed by an insert?)''

== further reading ==

  * the [http://en.wikipedia.org/wiki/longest_common_subsequence_problem longest common subsequence] is the longest sequence of items that is present in both original sequences in the same order.
  * the longest common substring is the longest *consecutive* sequence of items that is present in both original sequences.
  * [http://bramcohen.livejournal.com/37690.html "The diff problem has been solved"].
  * [http://en.wikipedia.org/wiki/diff Wikipedia:diff]
  * The [http://en.wikipedia.org/wiki/Levenshtein_distance Levenshtein distance] between two strings is given by the minimum number of operations needed to transform one string into the other, where an operation is an insertion, deletion, or substitution of a single character.
  * [http://en.wikibooks.org/wiki/Algorithm_implementation/Strings/Longest_common_subsequence Wikibooks: Algorithm implementation/Strings/Longest common subsequence]
