# Glossary

 <span id="accidentalcleanmerge"></span>
 **accidental clean merge**:: when two people make "the same" change, and these are then merged.  Example:
```
    a
   / \
  b   b
```
See [AccidentalCleanMerge](AccidentalCleanMerge.md).

 <span id="aliasing"></span>
 **aliasing**:: aliasing is taking two logically distinct entities and causing them to be treated as equivalent, at least in certain contexts.  Aliasing is similar to suturing, but the assertion is weaker (`x == y`, not `x is y`), and is trivial to undo.

 <span id="ambiguouscleanmerge"></span>
 **ambiguous clean merge**:: See [AmbiguousCleanMerge](AmbiguousCleanMerge.md).

 <span id="branch"></span>
 **branch**:: A named line of development.  May be viewed either as a sequence of [changesets](#changeset) or as a sequence of [snapshots](#snapshot) (but see the warning about the non-duality of these representations under [snapshot](#snapshot)).  In the context of a [repository](#repository), a branch may be viewed as a subgraph of the repository [DAG](#DAG) with two distinguished vertices; the branch point where it diverges from other lines of development, and a [tip](#tip). Often branches are tied to a [repository](#repository) in a many-to-one relationship. But other implementations are possible, for instance, [Monotone](Monotone.md) supports fully distributed branches which do not exist exclusively on top of any particular [repository](#repository), while other systems such as [Darcs](Darcs.md) and [Bzr](Bzr.md) tie branches to repositories in a one-to-one fashion.

 <span id="changeset"></span>
 **changeset**:: A collection of [deltas](#delta) to a set of files, considered as a unit and (in modern VCSes) with metadata including a change comment and a timestamp attached.  To fully capture the history of a line of development, changesets must also record file additions (which may be modeled as a delta from an empty file), file deletions, and file renames.  See also [weave](#weave) and [snapshot](#snapshot).

 <span id="checkin"></span>
 **checkin**:: Synonym for [commit](#commit) used in older VCSes (SCCS, RCS, CVS). This is why "ci" sometime appears as an alias for the commit operation in the command-line interfaces of VCSes that emulate CVS/Subversions's UI.

 <span id="checkout"></span>
 **checkout**:: The operation of getting a [workspace](#workspace) copy of some file(s) from a repository.  Mainly used in first- and second-generation VCSes with [locking](#locking).  Recorded here because it's the reason "co" shows up in some command-line interfaces with a meaning different from [commit](#commit).

 <span id="commit"></span>
 **commit**:: Modern term for pushing changes from a [workspace](#workspace) into a [repository](#repository).  Older VCSes tended to use [checkin](#checkin).

 <span id="contentmerger"></span>
 **content merger**:: See [textual merger](#TextualMerger)

 <span id="convergence"></span>
 **convergence**:: The idea that if the "same change" is made independently at different places in a graph, then a merge algorithm should treat the two changes as if they were a single change. Example:
```
    a
   / \
  b   b
  |
  c
```
a convergent merge algorithm will make this a clean merge to c. See [Convergence](Convergence.md).

 <span id="convergentscalarmerge"></span>
 **convergent scalar merge**:: A scalar merge algorithm related to [PreciseCodevilleMerge](PreciseCodevilleMerge.md). See [ConvergentScalarMerge](ConvergentScalarMerge.md).

 <span id="DAG"></span>
 **Directed Acyclic Graph (DAG)**:: A diagram (graph) made up of points connected by arrows (directed), where no arrow can lead back to an earlier point; in other words, the arrows cannot form a loop (acyclic).  [Revisions](#revision) in a VCS may be viewed as nodes in a DAG and the [changesets](#changeset) connecting them as links expressing the "parent-of" relationship. [Tip](#tip) revisions will have valence 1, most ordinary revisions will have valence 2, and revisions representing a branch point or merge will have valence 3.

 <span id="delta"></span>
 **delta**:: A description of changes between two versions of a file, usually as a sequence of line-oriented additions and deletions and replacements.  Such line-oriented deltas are often represented in a standard notation derived from the output format of the Unix `diff(1)` command.  There is a well-defined concept of deltas between binary files as well, but no standard notation for expressiong them.

 <span id="firstgeneration"></span>
 **first-generation**:: See [generations](#vcsgenerations).

 <span id="implicitundo"></span>
 **implicit undo**:: See [ImplicitUndo](ImplicitUndo.md).

 <span id="locking"></span>
 **locking**:: Early VCSes (SCCS, RCS) avoided the merging problem by awarding developers temporary but exclusive write locks on files. This approach did not scale well and was abandoned in second- and third-generation VCSes.


 <span id="markmerge"></span>
 **mark-merge, *-merge**:: A family of scalar merge algorithms.  See [MarkMerge](MarkMerge.md).

 <span id="pcdv"></span>
 **pcdv**:: see [precise codeville merge](#precisecodevillemerge)

 <span id="precisecodevillemerge"></span>
 **precise codeville merge**:: A textual merge algorithm. See [PreciseCodevilleMerge](PreciseCodevilleMerge.md).

 <span id="rename"></span>
 **rename**:: the option where a file or directory is either moved to a new directory or has its name changed. It is sometimes useful to distinguish  between moves (which put a file into a different directory) and renames (which change only the file's name, not its location).  see [Renaming](Renaming.md)

 <span id="repository"></span>
 **repository**:: Physical storage of a full or partial history of changes or snapshots.

 <span id="resolution"></span>
 **resolution**:: The step where a system takes a user-edited file and heuristically determines what editing the user implicitly did. Not always 1 distinct step nor done at commit time.  See [Resolution](Resolution.md).

 <span id="revision"></span>
 **revision**:: A particular state (version) of files and directories which is stored in SCM.

 <span id="rollback"></span>
 **rollback**:: see [Rollback](Rollback.md)

 <span id="scalarmerger"></span>
 **scalar merger**:: A merge algorithm that works on a single atomic value.  An example is [mark-merge](#markmerge).  Concept explained [here](http://thread.gmane.org/gmane.comp.version-control.monotone.devel/4297).

 <span id="secondgeneration"></span>
 **second-generation**:: See [generations](#vcsgenerations).

 <span id="snapshot"></span>
 **snapshot**:: A collection of files and directories considered as a timestamped unit, possibly with metadata such as a revision comment attached.  The revision history of a project may be considered either as a sequence of snapshots or as a sequence of the [changesets](#changeset) connecting them.  However, these representations are not perfectly dual.  Notably, moving from a changeset-sequence representation to a snapshot-sequence representation loses information about file and directory add, delete, and rename operations. While additions and deletions can be reliably inferred by comparing snapshots, renames cannot be; this has some subtle and occasionally nasty ripple effects.

 <span id="staircasemerge"></span>
 **staircase merge**:: A simple merge example:
```
    a
   / \
  b   c
   \ / \
    c   d
```
A merge algorithm which supports [StaircaseMerge](StaircaseMerge.md) will cleanly merge this to d.

 <span id="suturing"></span>
 **suturing**:: suturing is taking two logically distinct entities and merging them into a single logical entity.  See [Suturing](Suturing.md).  Compare with [aliasing](#aliasing).

 <span id="textualmerger"></span>
 **textual merger**:: a merge algorithm that operates on text files (as opposed to, for instance a [tree merger](#treemerger) or [scalar merger](#scalarmerger))

 <span id="thirdgeneration"></span>
 **third-generation**:: See [generations](#vcsgenerations). Also, informally, 3G.

 <span id="threewaymerge"></span>
 **three way merge**:: a merge algorithm which operates on three versions of a text file. See [ThreeWayMerge](ThreeWayMerge.md).

 <span id="treemerger"></span>
 **tree merger**:: a merge algorithm that operates on trees of files (generally handling things like file/directory add/remove/rename).

 <span id="vcs"></span>
 **VCS**:: Version-Control System. The most common of a handful of competing acronyms for the software this site is about.  Others include SCM for Source Code Manager and (rarely) SCCS for Source Code Control System.  The latter is also the proper name of the original VCS.

 <span id="vcsgenerations"></span>
 **VCS generations**:: There have, broadly speaking, been three generations of VCSes.  The first was exemplified by SCCS and RCS -- centralized and [locking](#locking), without support for development distributed across a network.  The second generation was exemplified by CVS and Subversion, which introduced merging and added support for distributed development but retained the centralized model based on one master repository per project.  Third-generation VCSes support a fully decentralized model; master repositories may exist as a matter of per-project policy, but the tools are all designed to support history merges between peer repositories.

 <span id="weave"></span>
 **weave**:: A data structure representing a full ordering of lines for a particular file along with information about which lines exist for each historical revision. [SCCS](SCCS.md) is the classic example. A number of merge algorithms are based on weaves. See [Weave](Weave.md), [WeaveMerge](WeaveMerge.md).  One of the fundamental design desisions in a VCS is whether change history will be represented as a weave or a sequence of [deltas](#delta).

 <span id="workspace"></span>
 **workspace**:: An editable copy of the state of a repository at a particular revision (or merge of several revisions) where a user can resolve conflicts and make new changes, then record them as a new revision. Also "working copy".
