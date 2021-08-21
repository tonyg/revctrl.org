# User Model

= Concept =

A User Model is formal model of how a user understands their changes, and what they expect to cause a clean merge or a conflict.  This concept was first defined and articulated in the original MarkMerge paper: http://article.gmane.org/gmane.comp.version-control.codeville.devel/6

As that paper states:
{{{
Traditionally, merge algorithms are evaluated by coming up with some
set of examples, eyeballing them to make some guess as to what the
"correct" answer was, comparing that to the algorithm's output, and
then arguing with people whose intuitions were different.
Fundamentally, merging is about deterministically guessing the user's
intent in situations where the user has not expressed any intent.
Humans are very good at guessing intent; we have big chunks of squishy
hardware designed to form sophisticated models of others intents, and
it's completely impossible for a VCS to try and duplicate that in
full.  My suggestion here, with my "user model", is to seriously and
explicitly study this part of the problem.  There are complicated
trade-offs between accuracy (correctly modeling intention),
conservatism (avoiding incorrectly modeling intention), and
implementability (describing the user's thought processes exactly
isn't so useful if you can't apply it in practice).  It's hard to make
an informed judgement when we don't have a name for the thing we're
trying to optimize, and hard to evaluate an algorithm when we can't
even say what it's supposed to be doing.
}}}

In short, if we're going to have to make guesses about squishy things like "intention", we had better be very explicit about our assumptions.  Otherwise, we continue to invent algorithms that look great, until someone suggests a new example.  This is fundamentally non-viable, because we never know whether we've seen "all the bad examples" (especially since historically, every time we think this someone has come up with new ones).  If we keep progressing from one example to another, we're doomed, because there are infinitely many examples.  The hope is that by defining our assumptions about the user, critiques of merge algorithms can be reduced to arguments that the algorithm implements a user model that does not accurately reflect users (example: MarkMerge's failure to handle StaircaseMerge), or arguments that the algorithm does not properly implement its user model (example: unique-MarkMerge's failure to handle AccidentalCleanMerge).

If this works, then every nasty example will turn out to be signaling a general problem of one of these two types.  We like general problems ''much'' more than specific problems.

= Practice =

The only merge algorithm so far to adopt this approach explicitly is MarkMerge, and the only developer or analyst to have used the concept in writing is NathanielSmith.  He earnestly (and third-person-ly) hopes that future work will find the concept useful.

The user model used by MarkMerge is:
{{{
  1) whenever a user explicitly sets the value, they express a claim
     that their setting is superior to the old setting
  2) whenever a user chooses to commit a new revision, they implicitly
     affirm the validity of the decisions that led to that revision's
     parents
    Corollary of (1) and (2): whenever a user explicitly sets the
     value, they express that they consider their new setting to be
     superior to _all_ old settings
  3) A "conflict" should occur if, and only if, the settings on each
     side of the merge express parallel claims.
}}}

This language is necessarily pretty fuzzy, which opens the whole concept of a user model to objections.  Especially since, ideally, a user model should entirely determine the results of a full algorithm implementing it... it might be claimed that a user model is simply a fuzzy high-level description of the algorithm proper.  Nonetheless, it has shown some practical benefits in at least the MarkMerge case.

This model described is for scalar merge.  No potential user model has been formulated for textual merge, which may be part of why we have no predictably reliable textual mergers...
