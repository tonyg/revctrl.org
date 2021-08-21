bk-merge is the merge algorithm used by the proprietary program [http://bitmover.com BitKeeper].  Obviously, we do not know how it actually works.  Nor are we particularly interested in finding out; there's no particular reason to believe bitmover actually knows more than we do about merge algorithm design, and we don't want intellectual property issues tainting our work (either legally or in terms of public opinion).

We do, however, have a pretty good guess how it works, due to a combination of three things:
  * Tridge's reverse-engineering and development of SourcePuller gave him some ideas how things fit together
  * About that same time, BramCohen, NathanielSmith, RossCohen and others developed SimpleWeaveMerge from scratch, and then discovered that Tridge's [http://loglibrary.com/show_page/view/126?Multiplier=3600&Interval=6&StartTime=1115689007 notes] on BK suddenly made a great deal of sense if interpreted in terms of their new theoretical framework.
  * It was then realized that SimpleWeaveMerge is very similar to the ancient ["SCCSMerge"], and that BK more or less just uses this well-known, decades old technology directly.  This makes worries about patents somewhat less urgent...

= Strengths =

  * Well-regarded, but we have no rigorous evaluation by people who know their merge algorithms.
  * The general strengths of [:WeaveMerge:WeaveMerges].

= Weaknesses =

  * Unknown, but may suffer from flaws with regards to ImplicitUndo (there is some kind of hunk rollback support, but we don't know any more than that) and the ordering problems that SimpleWeaveMerge has problems with.

= Used by =

BitKeeper

= Related =

["SCCSMerge"], SimpleWeaveMerge

----

CategoryMergeAlgorithm
