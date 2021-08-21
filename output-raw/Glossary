 <<Anchor(accidentalcleanmerge)>>
 accidental clean merge:: when two people make "the same" change, and these are then merged.  Example: {{{
    a
   / \
  b   b
}}} See AccidentalCleanMerge.

 <<Anchor(aliasing)>>
 aliasing:: aliasing is taking two logically distinct entities and causing them to be treated as equivalent, at least in certain contexts.  Aliasing is similar to suturing, but the assertion is weaker ({{{x == y}}}, not {{{x is y}}}), and is trivial to undo.

 <<Anchor(ambiguouscleanmerge)>>
 ambiguous clean merge:: See AmbiguousCleanMerge.

 <<Anchor(branch)>>
 branch:: A named line of development.  May be viewed either as a sequence of [[#changeset|changesets]] or as a sequence of [[#snapshot|snapshots]] (but see the warning about the non-duality of these representations under [[#snapshot|snapshot]]).  In the context of a [[#repository|repository]], a branch may be viewed as a subgraph of the repository [[#DAG|DAG]] with two distinguished vertices; the branch point where it diverges from other lines of development, and a [[#tip|tip]]. Often branches are tied to a [[#repository|repository]] in a many-to-one relationship. But other implementations are possible, for instance, [[Monotone]] supports fully distributed branches which do not exist exclusively on top of any particular [[#repository|repository]], while other systems such as [[Darcs]] and [[Bzr]] tie branches to repositories in a one-to-one fashion.

 <<Anchor(changeset)>>
 changeset:: A collection of [[#delta|deltas]] to a set of files, considered as a unit and (in modern VCSes) with metadata including a change comment and a timestamp attached.  To fully capture the history of a line of development, changesets must also record file additions (which may be modeled as a delta from an empty file), file deletions, and file renames.  See also [[#weave|weave]] and [[#snapshot|snapshot]].

 <<Anchor(checkin)>>
 checkin:: Synonym for [[#commit|commit]] used in older VCSes (SCCS, RCS, CVS). This is why "ci" sometime appears as an alias for the commit operation in the command-line interfaces of VCSes that emulate CVS/Subversions's UI.

 <<Anchor(checkout)>>
 checkout:: The operation of getting a [[#workspace|workspace]] copy of some file(s) from a repository.  Mainly used in first- and second-generation VCSes with [[#locking|locking]].  Recorded here because it's the reason "co" shows up in some command-line interfaces with a meaning different from [[#commit|commit]].

 <<Anchor(commit)>>
 commit:: Modern term for pushing changes from a [[#workspace|workspace]] into a [[#repository|repository]].  Older VCSes tended to use [[#checkin|checkin]].

 <<Anchor(contentmerger)>>
 content merger:: See [[#TextualMerger|textual merger]]

 <<Anchor(convergence)>>
 convergence:: The idea that if the "same change" is made independently at different places in a graph, then a merge algorithm should treat the two changes as if they were a single change. Example: {{{
    a
   / \
  b   b
  |
  c
 }}} a convergent merge algorithm will make this a clean merge to c. See [[Convergence]].

 <<Anchor(convergentscalarmerge)>>
 convergent scalar merge:: A scalar merge algorithm related to PreciseCodevilleMerge. See ConvergentScalarMerge.

 <<Anchor(DAG)>>
 Directed Acyclic Graph (DAG):: A diagram (graph) made up of points connected by arrows (directed), where no arrow can lead back to an earlier point; in other words, the arrows cannot form a loop (acyclic).  [[#revision|Revisions]] in a VCS may be viewed as nodes in a DAG and the [[#changeset|changesets]] connecting them as links expressing the "parent-of" relationship. [[#tip|Tip]] revisions will have valence 1, most ordinary revisions will have valence 2, and revisions representing a branch point or merge will have valence 3.

 <<Anchor(delta)>>
 delta:: A description of changes between two versions of a file, usually as a sequence of line-oriented additions and deletions and replacements.  Such line-oriented deltas are often represented in a standard notation derived from the output format of the Unix '''diff(1)''' command.  There is a well-defined concept of deltas between binary files as well, but no standard notation for expressiong them.

 <<Anchor(firstgeneration)>>
 first-generation:: See [[#vcsgenerations|generations]].

 <<Anchor(implicitundo)>>
 implicit undo:: See ImplicitUndo.

 <<Anchor(locking)>>
 locking:: Early VCSes (SCCS, RCS) avoided the merging problem by awarding developers temporary but exclusive write locks on files. This approach did not scale well and was abandoned in second- and third-generation VCSes.


 <<Anchor(markmerge)>>
 mark-merge, *-merge:: A family of scalar merge algorithms.  See MarkMerge.

 <<Anchor(pcdv)>>
 pcdv:: see [[#precisecodevillemerge|precise codeville merge]]

 <<Anchor(precisecodevillemerge)>>
 precise codeville merge:: A textual merge algorithm. See PreciseCodevilleMerge.

 <<Anchor(rename)>>
 rename:: the option where a file or directory is either moved to a new directory or has its name changed. It is sometimes useful to distinguish  between moves (which put a file into a different directory) and renames (which change only the file's name, not its location).  see [[Renaming]]

 <<Anchor(repository)>>
 repository:: Physical storage of a full or partial history of changes or snapshots.

 <<Anchor(resolution)>>
 resolution:: The step where a system takes a user-edited file and heuristically determines what editing the user implicitly did. Not always 1 distinct step nor done at commit time.  See [[Resolution]].

 <<Anchor(revision)>>
 revision:: A particular state (version) of files and directories which is stored in SCM.

 <<Anchor(rollback)>>
 rollback:: see [[Rollback]]

 <<Anchor(scalarmerger)>>
 scalar merger:: A merge algorithm that works on a single atomic value.  An example is [[#markmerge|mark-merge]].  Concept explained in [[http://thread.gmane.org/gmane.comp.version-control.monotone.devel/4297]].

 <<Anchor(secondgeneration)>>
 second-generation:: See [[#vcsgenerations|generations]].

 <<Anchor(snapshot)>>
 snapshot:: A collection of files and directories considered as a timestamped unit, possibly with metadata such as a revision comment attached.  The revision history of a project may be considered either as a sequence of snapshots or as a sequence of the [[#changeset|changesets]] connecting them.  However, these representations are not perfectly dual.  Notably, moving from a changeset-sequence representation to a snapshot-sequence representation loses information about file and directory add, delete, and rename operations. While additions and deletions can be reliably inferred by comparing snapshots, renames cannot be; this has some subtle and occasionally nasty ripple effects.

 <<Anchor(staircasemerge)>>
 staircase merge:: A simple merge example: {{{
    a
   / \
  b   c
   \ / \
    c   d
 }}} A merge algorithm which supports StaircaseMerge will cleanly merge this to d.

 <<Anchor(suturing)>>
 suturing:: suturing is taking two logically distinct entities and merging them into a single logical entity.  See [[Suturing]].  Compare with [[#aliasing|aliasing]].

 <<Anchor(textualmerger)>>
 textual merger:: a merge algorithm that operates on text files (as opposed to, for instance a [[#treemerger|tree merger]] or [[#scalarmerger|scalar merger]])

 <<Anchor(thirdgeneration)>>
 third-generation:: See [[#vcsgenerations|generations]]. Also, informally, 3G.

 <<Anchor(threewaymerge)>>
 three way merge:: a merge algorithm which operates on three versions of a text file. See ThreeWayMerge.

 <<Anchor(treemerger)>>
 tree merger:: a merge algorithm that operates on trees of files (generally handling things like file/directory add/remove/rename).

 <<Anchor(vcs)>>
 VCS:: Version-Control System. The most common of a handful of competing acronyms for the software this site is about.  Others include SCM for Source Code Manager and (rarely) SCCS for Source Code Control System.  The latter is also the proper name of the original VCS.

 <<Anchor(vcsgenerations)>>
 VCS generations:: There have, broadly speaking, been three generations of VCSes.  The first was exemplified by SCCS and RCS -- centralized and [[#locking|locking]], without support for development distributed across a network.  The second generation was exemplified by CVS and Subversion, which introduced merging and added support for distributed development but retained the centralized model based on one master repository per project.  Third-generation VCSes support a fully decentralized model; master repositories may exist as a matter of per-project policy, but the tools are all designed to support history merges between peer repositories.

 <<Anchor(weave)>>
 weave:: A data structure representing a full ordering of lines for a particular file along with information about which lines exist for each historical revision. [[SCCS]] is the classic example. A number of merge algorithms are based on weaves. See [[Weave]], WeaveMerge.  One of the fundamental design desisions in a VCS is whether change history will be represented as a weave or a sequence of [[#delta|deltas]].

 <<Anchor(workspace)>>
 workspace:: An editable copy of the state of a repository at a particular revision (or merge of several revisions) where a user can resolve conflicts and make new changes, then record them as a new revision. Also "working copy".
