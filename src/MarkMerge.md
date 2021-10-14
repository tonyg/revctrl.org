# Mark Merge

A scalar merge algorithm, related to [CodevilleMerge](CodevilleMerge.md).  Generally referred to as "mark-merge" or "*-merge" (but never [StarMerge](StarMerge.md), which is something else entirely).

Detailed writeup of original version: <http://thread.gmane.org/gmane.comp.version-control.monotone.devel/4297> ("unique-*-merge"; [available below](#unique-mark-marge))

Detailed writeup of updated version (handles accidental clean merges): <http://article.gmane.org/gmane.comp.version-control.revctrl/93> ("multi-*-merge"; [available below](#multi-mark-merge))

Other links: <http://article.gmane.org/gmane.comp.version-control.revctrl/92> ([available below](#more-on-mark-merge)), <http://article.gmane.org/gmane.comp.version-control.revctrl/197> ("deterministic-*-merge")

The most interesting things about *-merge are:
  * has a [UserModel](UserModel.md)
  * has a formal analysis showing that it is fully well-defined, and implements the [UserModel](UserModel.md)

## Strengths

  * best formal analysis of any current merge algorithm
  * believed to never clean merge without justification (conservative)
  * "deterministic \*-merge" (basically multi-\*-merge but easier to make formal statements about) is commutative and associative (i.e., satisfies [OperationalTransformation](OperationalTransformation.md) theory's properties TP1 and TP2).

## Weaknesses

  * unique-\*-merge does not handle accidental clean merges; multi-\*-merge does
  * does not handle [StaircaseMerge](StaircaseMerge.md)
  * does not attempt [Convergence](Convergence.md)
  * does not attempt implicit rollback

## Used by

[Monotone](Monotone.md)

## Related

[CodevilleMerge](CodevilleMerge.md)

----

[CategoryMergeAlgorithm](CategoryMergeAlgorithm.md) [CategoryScalarMerge](CategoryScalarMerge.md)

---

# Emails relating to MarkMerge

> *Editor's note.* The `gmane.org` links above do not work reliably.
> The following text is the majority of the content of [the Monotone
> Wiki MarkMerge page](https://wiki.monotone.ca/MarkMerge/), and may
> include the text of the messages referred to above.

## <span id="unique-mark-marge"></span> Initial mark-merge proposal

This appears to be the text of the
`gmane.comp.version-control.monotone.devel` message numbered 4297
referred to above.

    From: Nathaniel Smith <njs <at> pobox.com>
    Subject: [cdv-devel] more merging stuff (bit long...)
    Newsgroups: gmane.comp.version-control.codeville.devel, gmane.comp.version-control.monotone.devel
    Date: 2005-08-06 09:08:09 GMT

    I set myself a toy problem a few days ago: is there a really, truly,
    right way to merge two heads of an arbitrary DAG, when the object
    being merged is as simple as possible: a single scalar value?

    I assume that I'm given a graph, and each node in the graph has a
    value, and no other annotation; I can add annotations, but they have
    to be derived from the values and topology.  Oh, and I assume that no
    revision has more than 2 parents; probably things can be generalized
    to the case of indegree 3 or higher, but it seems like a reasonable
    restriction...

    So, anyway, here's what I came up with.  Perhaps you all can tell me
    if it makes sense.

    User model
    ----------

    Since the goal was to be "really, truly, right", I had to figure out
    what exactly that meant... basically, what I'm calling a "user model"
    -- a formal definition of how the user thinks about merging, to give
    an operational definition of "should conflict" and "should clean
    merge".  My rules are these:
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
    This in itself is not an algorithm, or anything close to it; the hope
    is that it's a good description of what people actually want out of a
    merge algorithm, expressed clearly enough that we can create an
    algorithm that fits these desiderata.

    Algorithm
    ---------

    I'll use slightly novel notation.  Lower case letters represent values
    that scalar the scalar takes.  Upper case letters represent nodes in
    the graph.

    Now, here's an algorithm, that is supposed to just be a transcription
    of the above rules, one step more formal:
      First, we need to know where users actively expressed an intention.
      Intention is defined by (1), above.  We use * to mark where this
      occurred:

        i)      a*     graph roots are always marked

                a
        ii)     |      no mark, value was not set
                a

                a
        iii)    |      b != a, so b node marked
                b*

              a   b
        iv)    \ /
                c*
                       c is totally new, so marked
              a   a
               \ /
                c*

              a   b    we're marking places where users expressed
        v)     \ /     intention; so b should be marked iff this
                b?     was a conflict (!)

              a   a    for now I'm not special-casing the coincidental
        vi)    \ /     clean merge case, so let's consider this to be
                a?     a subclass of (v).

      That's all the cases possible.  So, suppose we go through and
      annotate our graph with *s, using the above rules; we have a graph
      with some *s peppered through it, each * representing one point that
      a user took action.

      Now, a merge algorithm per se: Let's use *(A) to mean the unique
      nearest marked ancestor of node A.  Suppose we want to merge A and
      B.  There are exactly 3 cases:
        - *(A) is an ancestor of B, but not vice versa: B wins.
        - *(B) is an ancestor of A, but not vice versa: A wins.
        - *(A) is _not_ an ancestor of B, and vice versa: conflict,
          escalate to user
      Very intuitive, right?  If B supercedes the intention that led to A,
      then B should win, and vice-versa; if not, the user has expressed
      two conflicting intentions, and that, by definition, is a conflict.

      This lets us clarify what we mean by "was a conflict" in case (v)
      above.  When we have a merge of a and b that gives b, we simple
      calculate *(a); if it is an ancestor of 'b', then we're done, but if
      it isn't, then we mark the merge node.  (Subtle point: this is
      actually not _quite_ the same as detecting whether merging 'a' and
      'b' would have given a conflict; if we somehow managed to get a
      point in the graph that would have clean merged to 'a', but in fact
      was merged to 'b', then this algorithm will still mark the merge
      node.)  For cases where the two parents differ, you have to do this
      using the losing one; for cases where the two parents are the same,
      you should check both, because it could have been a clean merge two
      different ways.  If *(a1) = *(a2), i.e., both sides have the same
      nearest marked ancestor, consider that a clean merge.

      That's all.

    Examples
    --------

    Of course, I haven't shown you this is well-defined or anything, but
    to draw out the suspense a little, have some worked examples (like
    most places in this document, I draw graphs with two leaves and assume
    that those are being merged):

      graph:
           a*
          / \
         a   b*
      result: *(a) is an ancestor of b, but *(b) is not an ancestor of a;
        clean merge with result 'b'.

      graph:
           a*
          / \
         b*  c*
      result: *(b) = b is not an ancestor of c, and *(c) = c is not an
        ancestor of c; conflict.

      graph:
           a*
          / \
         b*  c*  <--- these are both marked, by (iii)
         |\ /|
         | X |
         |/ \|
         b*  c*  <--- which means these were conflicts, and thus marked
      result: the two leaves are both marked, and thus generate a conflict,
        as above.

    Right, enough of that.  Math time.

    Math
    ----

    Theorem: In a graph marked following the above rules, every node N
      will have a unique least marked ancestor M, and the values of M and N
      will be the same.
    Proof: By downwards induction on the graph structure.  The base case
      are graph roots, which by (i) are always marked, so the statement is
      trivially true.  Proceeding by cases, (iii) and (iv) are trivially
      true, since they produce nodes that are themselves marked.  (ii) is
      almost as simple; in a graph 'a' -> 'a', the child obviously
      inherits the parent's unique least marked ancestor, which by
      inductive hypothesis exists.  The interesting case is (v) and (vi):
         a   b
          \ /
           b
      If the child is marked, then again the statement is trivial; so
      suppose it is not.  By definition, this only occurs when *(a) is an
      ancestor of 'b'.  But, by assumption, 'b' has a unique nearest
      ancestor, whose value is 'b'.  Therefore, *(a) is also an ancestor
      of *(b).  If we're in the weird edge case (vi) where a = b, then
      these may be the same ancestor, which is fine.  Otherwise, the fact
      that a != b, and that *(a)'s value = a's value, *(b)'s value = b's
      value, implies that *(a) is a strict ancestor of *(b).  Either way,
      the child has a unique least marked ancestor, and it is the same
      ULMA as its same-valued parent, so the ULMA also has the right
      value.  QED.

    Corollary: *(N) is a well-defined function.

    Corollary: The three cases mentioned in the merge algorithm are the
      only possible cases.  In particular, it cannot be that *(A) is an
      ancestor of B and *(B) is an ancestor of A simultaneously, unless
      the two values being merged are identical (and why are you running
      your merge algorithm then?).  Or in other words: ambiguous clean
      merge does not exist.
    Proof: Suppose *(A) is an ancestor of B, and *(B) is an ancestor of A.
      *(B) is unique, so *(A) must also be an ancestor of *(B).
      Similarly, *(B) must be an ancestor of *(A).  Therefore:
        *(A) = *(B)
      We also have:
        value(*(A)) = value(A)
        value(*(B)) = value(B)
      which implies
        value(A) = value(B).  QED.

    Therefore, the above algorithm is well-defined in all possible cases.

    We can prove another somewhat interesting fact:
    Theorem: If A and B would merge cleanly with A winning, then any
      descendent D of A will also merge cleanly with B, with D winning.
    Proof: *(B) is an ancestor of A, and A is an ancestor of D, so *(B) is
      an ancestor of D.

    I suspect that this is enough to show that clean merges are order
    invariant, but I don't have a proof together ATM.

    Not sure what other properties would be interesting to prove; any
    suggestions?  It'd be nice to have some sort of proof about "once a
    conflict is resolved, you don't have to resolve it again" -- which is
    the problem that makes ambiguous clean merge so bad -- but I'm not
    sure how to state such a property formally.  Something about it being
    possible to fully converge a graph by resolving a finite number of
    conflicts or something, perhaps?

    Funky cases
    -----------

    There are two funky cases I know of.

    Coincidental clean merge:
        |
        a
       / \
      b*  b*

    Two people independently made the same change.  When we're talking
    about textual changes, some people argue this should give a conflict
    (reasoning that perhaps the same line _should_ be inserted twice).  In
    our context that argument doesn't even apply, because these are just
    scalars; so obviously this should be a clean merge.  Currently, the
    only way this algorithm has to handle this is to treat it as an
    "automatically resolved conflict" -- there's a real conflict here, but
    the VCS, acting as an agent for the user, may decide to just go ahead
    and resolve it, because it knows perfectly well what the user will do.
    In this interpretation, everything works fine, all the above stuff
    applies; it's somewhat dissatisfying, though, because it's a violation
    of the user model -- the user has not necessarily looked at this
    merge, but we put the * of user-assertion on the result anyway.  Not a
    show-stopper, I guess...

    It's quite possible that the above stuff could be generalized to allow
    non-unique least marked ancestors, that could only arise in exactly
    this case.

    I'm not actually sure what the right semantics would be, though.  If
    we're merging:
        |
        a
       / \
      b   b
       \ / \
        b   c
    Should that be a clean merge?  'b' was set twice, and only one of
    these settings was overridden; is that good enough?

    Do you still have the same opinion if the graph is:
        |
        a
        |
        b
       / \
      c   b
      |  / \
      b  b  c
      \ /
       b
    ?  Here the reason for the second setting of 'b' was that a change
    away from it was reverted; to make it extra cringe-inducing, I threw
    in that change being reverted was another change to 'c'... (this may
    just be an example of how any merge algorithm has some particular case
    you can construct where it will get something wrong, because it
    doesn't _actually_ know how to read the users's minds).

    Supporting these cases may irresistably lead back to ambiguous clean,
    as well:
         |
         a
        / \
       b*  c*
      / \ / \
     c*  X   b*
      \ / \ /
       c   b

    The other funky case is this thing (any clever name suggestions?):
        a
       / \
      b*  c*
       \ / \
        c*  d*
    Merging here will give a conflict, with my algorithm; 3-way merge
    would resolve it cleanly.  Polling people on #monotone and #revctrl,
    the consensus seems to be that they agree with 3-way merge, but giving
    a conflict is really not _that_ bad.  (It also seems to cause some
    funky effects with darcs-merge; see zooko's comments on #revctrl and
    darcs-users.)

    This is really a problem with the user model, rather than the
    algorithm.  Apparently people do not interpret the act of resolving
    the b/c merge to be "setting" the result; They seem to interpret it as
    "selecting" the result of 'c'; the 'c' in the result is in some sense
    the "same" 'c' as in the parent.  The difference between "setting" and
    "selecting" is the universe of possible options; if you see
       a   b
        \ /
         c
    then you figure that the person doing the merge was picking from all
    possible resolution values; when you see
       a   b
        \ /
         b
    you figure that the user was just picking between the two options
    given by the parents.  My user model is too simple to take this into
    account.  It's not a huge extension to the model to do so; it's quite
    possible that an algorithm could be devised that gave a clean merge
    here, perhaps by separately tracking each node's nearest marked
    ancestor and the original source of its value as two separate things.

    Relation to other work
    ----------------------

    This algorithm is very close to the traditional codeville-merge
    approach to this problem; the primary algorithmic difference is the
    marking of conflict resolutions as being "changes".  The more
    important new stuff here, I think, are the user model and the proofs.

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

    I suspect the benefit of the proofs is obvious to anyone who has spent
    much time banging their head against this problem; until a few days
    ago I was skeptical there _was_ a way to design a merge algorithm that
    didn't run into problems like ambiguous clean merge.

    I'm still skeptical, of course, until people read this; merging is
    like crypto, you can't trust anything until everyone's tried to break
    it... so let's say I'm cautiously optimistic .  If this holds up,
    I'm quite happy; between the user model and the proofs, I'm far more
    confident that this does something sensible in all cases and has no
    lurking edge cases than I have been in any previous algorithm.  The
    few problem cases I know of display a pleasing conservatism -- perhaps
    more cautious than they need to be, but even if they do cause an
    occasional unnecessary conflict, once the conflict is resolved it
    should stay resolved.

    So... do your worst!

    -- Nathaniel

    --
    So let us espouse a less contested notion of truth and falsehood, even
    if it is philosophically debatable (if we listen to philosophers, we
    must debate everything, and there would be no end to the discussion).
      -- Serendipities, Umberto Eco

## <span id="multi-mark-merge"></span> Improvements to *-merge

This appears to be the text of the
`gmane.comp.version-control.revctrl` message numbered 93 referred to
above.

    From: Nathaniel Smith <njs@...>
    Subject: improvements to *-merge
    Newsgroups: gmane.comp.version-control.revctrl, gmane.comp.version-control.monotone.devel
    Date: 2005-08-30 09:21:18 GMT

    This is a revised version of *-merge:
      http://thread.gmane.org/gmane.comp.version-control.monotone.devel/4297
    that properly handles accidental clean merges.  It does not improve
    any of the other parts, just the handling of accidental clean merges.
    It shows a way to relax the uniqueness of the *() operator, while
    still preserving the basic results from the above email.  For clarity,
    I'll say 'unique-*-merge' to refer to the algorithm given above, and
    'multi-*-merge' to refer to this one.

    This work is totally due to Timothy Brownawell <tbrownaw@...>.
    All I did was polish up the proofs and write it up.  He has a more
    complex version at:
      http://article.gmane.org/gmane.comp.version-control.monotone.devel/4496
    that also attempts to avoid the conflict with:
         a
        / \
       b*  c*
        \ / \
         c*  d*
    and has some convergence in it, but the analysis for that is not done.

    So:

    User model
    ----------

    We keep exactly the same user model as unique-*-merge:

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

    The difference is that unique-*-merge does not _quite_ fulfill this
    model, because in real life your algorithm will automatically resolve
    coincidental clean merge cases without asking for user input; but
    unique-* is not smart enough to take this into account when inferring
    user intentions.

    Algorithm
    ---------

    We start by marking the graph of previous revisions.  For each node in
    the graph, we either mark it (denoted by a *), or do not.  A mark
    indicates our inference that a human expressed an intention at this
    node.

        i)      a*     graph roots are always marked

                a1
        ii)     |      no mark, value was not set
                a2

                a
        iii)    |      b != a, so 'b' node marked
                b*

              a   b
        iv)    \ /
                c*
                       'c' is totally new, so marked
              a1  a2
               \ /
                c*

              a   b1   we're marking places where users expressed
        v)     \ /     intention; so 'b' should be marked iff this
                b2?    was a conflict

              a1  a2   'a' matches parents, and so is not marked
        vi)    \ /     (alternatively, we can say this is a special
                a3     case of (v), that is never a conflict)

    Case (vi) is the only one that differs from unique-* merge.  However,
    because of it, we must use a new definition of *():

    Definition: By *(A), we mean we set of minimal marked ancestors of A.
    "Minimal" here is used in the mathematical sense of a node in a graph
    that has no descendents in that graph.

    Algorithm: Given two nodes to merge, A and B, we consider four cases:
       a) value(A) = value(B): return the shared value
       b) *(A) > B: return value(B)
       c) *(B) > A: return value(A)
       d) else: conflict; escalate to user
    Where "*(A) > B" means "all elements of the set *(A) are non-strict
    ancestors of the revision B".  The right way to read this is as "try
    (a) first, and then if that fails try (b), (c), (d) simultaneously".

    Note that except for the addition of rule (a), this is a strict
    generalization of the unique-* algorithm; if *(A) and *(B) are
    single-element sets, then this performs _exactly_ the same
    computations as the unique-* algorithm.

    Now we can say what we mean by "was a conflict" in case (v) above:
    given a -> b2, b1 -> b2, we leave b2 unmarked if and only if
    *(a) > b1.

    Examples
    --------

    1.
        a1*
       / \
      a2  b*

    result: *(a2) = {a1}, a1 > b, so b wins.

    2.
        a*
       / \
      b*  c*

    result: *(b) = {b}, *(c) = {c}, neither *(b) > c nor *(c) > b, so
     conflict.

    3.
        a*
       / \
      b1* b2*
       \ / \
        b3  c1*

    result: *(b3) = {b1, b2}; b2 > c1, but b1 is not > c, so c does not
     win.  *(c1) = {c1}, which is not > b3.  conflict.
    note: this demonstrates that this algorithm does _not_ do convergence.
    Instead, it takes the conservative position that for one node to
    silently beat another, the winning node must pre-empt _all_ the
    intentions that created the losing node.  While it's easy to come up
    with just-so stories where this is the correct thing to do (e.g., b1
    and b2 each contain some other changes that independently require 'a'
    to become 'b'; c1 will have fixed up b2's changes, but not b1's), this
    doesn't actually mean much.  Whether this is good or bad behavior a
    somewhat unresolved question, that may ultimately be answered by which
    merge algorithms turn out to be more tractable...

    4.
        a*
       / \
      b1* b2*
      |\ /|
      | X |
      |/ \|
      b3  c*

    result: *(b3) = {b1, b2} > c.  *(c) = {c}, which is not > b3.  c wins
     cleanly.

    5.
         a*
        / \
       b1* c1*
      / \ / \
     c2* X   b2*
      \ / \ /
       c3  b3

    result: *(c3) = {c1, c2}; c1 > b3 but c2 is not > b3, so b3 does not
     win.  likewise, *(b3) = {b1, b2}; b1 > c3 but b2 is not > c3, so c3
     does not win either.  conflict.

    6.
         a*
        / \
       b1* c1*
      / \ / \
     c2* X   b2*
      \ / \ /
       c3  b3
       |\ /|
       | X |
       |/ \|
       c4* b4*

    (this was my best effort to trigger an ambiguous clean merge with this
    algorithm; it fails pitifully:)
    result: *(c4) = {c4}, *(b4) = {b4}, obvious conflict.

    Math
    ----

    The interesting thing about this algorithm is that all the unique-*
    proofs still go through, in a generalized form.  The key one that
    makes *-merge tractable is:

    Theorem: In a graph marked by the above rules, given a node N, all
     nodes in *(N) will have the same value as N.
    Proof: By induction.  We consider the cases (i)-(vi) above.  (i)
     through (iv) are trivially true.  (v) is interesting.  b2 is marked
     when *(a) not > b1.  b2 being marked makes that case trivial, so
     suppose *(a) > b1.  All elements of *(a) are marked, and are
     ancestors of b1; therefore, by the definition of *() and "minimal",
     they are also all ancestors of things in *(b1).  Thus no element of
     *(a) can be a minimal marked ancestor of b2.
     (vi) is also trivial, because *(a3) = *(a1) union *(a2).  QED.

    We also have to do a bit of extra work because of the sets:

    Corollary 1: If *(A) > B, and any element R of *(B) is R > A, then
     value(A) = value(B).
    Proof: Let such an R be given.  R > A, and R marked, imply that there
     is some element S of *(A) such that R > S.
     On the other hand, *(A) > B implies that S > B.  By similar reasoning
     to the above, this means that there is some element T of *(B) such
     that S > T.  So, recapping, we have:
      nodes:   R  >  S  >  T
       from: *(B)  *(A)  *(B)
     *(B) is a set of minimal nodes, yet we have R > T and R and T both in
     *(B).  This implies that R = T.  R > S > R implies that S = R,
     because we are in a DAG.  Thus
       value(A) = value(S) = value(R) = value(B)
     QED.

    Corollary 2: If *(A) > B and *(B) > A, then not only does value(A) =
     value(B), but *(A) = *(B).
    Proof: By above, each element of *(B) is equal to some element of
     *(A), and vice-versa.

    This is good, because it means our algorithm is well-defined.  The
    only time when options (b) and (c) (in the algorithm) can
    simultaneously be true, is when the two values being merged are
    identical to start with.  I.e., no somewhat anomalous "4th case" of
    ambiguous clean merge.

    Actually, this deserves some more discussion.  With *() returning a
    set, there are some more subtle "partial ambiguous clean" cases to
    think about -- should we be worrying about cases where some, but not
    all, of the marked ancestors are pre-empted?  This is possible, as in
    example 5 above:
         a*
        / \
       b1* c1*
      / \ / \
     c2* X   b2*
      \ / \ /
       c3  b3
    A hypothetical (convergence supporting?) algorithm that said A beats B
    if _any_ elements of *(A) are > B would give an ambiguous clean merge
    on this case.  (Maybe that wouldn't be so bad, so long as we marked
    the result, but I'm in no way prepared to do any sort of sufficient
    analysis right now...)

    The nastiest case of this is where *(A) > B, but some elements of *(B)
    are > A -- so we silently make B win, but it's really not _quite_
    clear that's a good idea, since A also beat B sometimes -- and we're
    ignoring those user's intentions.

    This is the nice thing about Corollary 1 (and why I didn't just
    collapse it into Corollary 2) -- it assures us that the only time this
    _weak_ form of ambiguous clean can happen is when A and B are already
    identical.  This _can_ happen, for what it's worth:
           a*
          /|\
         / | \
        /  |  \
       /   |   \
      b1*  b2*  d*
      |\   /\  /
      | \ /  \/
      |  X   b3*
      | / \ /
      |/   b4
      b5
    Here *(b5) = {b3, b2}, *(b6) = {b2, b4}.  If we ignore for a moment
    that b4 and b5 have the same value, this is a merge that b4 would win
    and b5 would lose, even though one of b4's ancestors, i.e. b1, is
    pre-empted by b5.  However, it can _only_ happen if we ignore that
    they have the same value...

    The one other thing we proved about unique-* merge also still applies;
    the proof goes through word-for-word:
    Theorem: If A and B would merge cleanly with A winning, then any
      descendent D of A will also merge cleanly with B, with D winning.
    Proof: *(B) > A, and A > D, so *(B) > D.

    Discussion
    ----------

    This algorithm resolves one of the two basic problems I observed for
    unique-* merge -- coincidental clean merges are now handled, well,
    cleanly, and the user model is fully implemented.  However, we still
    do not handle the unnamed case (you guys totally let me down when I
    requested names for this case last time):
        a
       / \
      b*  c*
       \ / \
        c*  d*
    which still gives a conflict.  We also, of course, continue to not
    support more exotic features like convergence or implicit rollback.

    Not the most exciting thing in the world.  OTOH, it does strictly
    increase the complexity of algorithms that are tractable to formal
    analysis.

    Comments and feedback appreciated.

    -- Nathaniel

    --
    "The problem...is that sets have a very limited range of
    activities -- they can't carry pianos, for example, nor drink
    beer."

## <span id="more-on-mark-merge"></span> More on "mark-merge"

This appears to be the text of the
`gmane.comp.version-control.revctrl` message numbered 92 referred to
above.

    From: Timothy Brownawell <tbrownaw@...>
    Subject: more on "mark-merge"
    Newsgroups: gmane.comp.version-control.revctrl, gmane.comp.version-control.monotone.devel

    Prerequisite:
    http://thread.gmane.org/gmane.comp.version-control.monotone.devel/4297

    A user can make 2 types of merge decisions:
    (1): One parent is better than the other (represented by *)
    (2): Both parents are wrong (represented by ^)

    Since there are 2 types of merge decisions, it would be bad to treat all
    merge decisions the same. Also, in the case of merge(a, a) = a, it is
    possible for there to be multiple least decision ancestors.

    =====

    Define: ^(A) is the set of ancestors of A that it gets its value from
    (found by setting N=A and iterating N = *(N) until there is no change)
            *(A) is the set of least ancestors of A in which the user made a
    decision

    note that erase_ancestors(^(A)) = ^(A),
    and erase_ancestors(*(A)) = *(A)

    =====

    & is intersection, | is union

    *(A) has the same properties as before, except that it is not a single
    ancestor, but a set. This set can acquire more than one member only in
    the case of
       Aa    Ba
         \  /
          Ca
    , where *(A) and *(B) are different; *(C) will be
    erase_ancestors(*(A) | *(B))

    The ancestory corollary becomes:
    any ancestor C of A with value(C) != value(A) will be an ancestor of at
    least one member of *(A)

    When merging A and B:

    # if one side knows of _all_ places that the other side was chosen, it
    wins
    (1)
    set X = erase_ancestors(*(A) | *(B))
        if X & *(B) = {}, A wins
        if X & *(A) = {}, B wins
    else, X contains members of both *(A) and *(B)

    # if one side knows of _all_ places that the other side originated, it
    wins
    (2)
    set Y = erase_ancestors(*(A) | ^(B))
    set Z = erase_ancestors(*(B) | ^(A))
        if Y & ^(B) = {} and Z & ^(A) = {}, conflict
        if Y & ^(B) = {}, A wins
        if Z & ^(A) = {}, B wins

    # if one side knows of _any_ places that the other side originated, it
    wins
    (3)
        if Y & ^(B) != ^(B) and Z & ^(A) != ^(A), conflict
        if Y & ^(B) != ^(B), A wins
        if Z & ^(A) != ^(A), B wins

    # else, nobody knows anything
    (4) conflict

    (3) is convergence, and can be safely left out if unwanted

    ====

    "Funky cases"

    Coincidental clean does not exist; a mark is only needed when there is
    user intervention.

        |
        a
       / \
      b   b
       \ / \
        b   c
    and the example after it will resolve cleanly iff (3) is included.

         |
         a
        / \
       b*  c*
      / \ / \
     c*  X   b*
      \ / \ /
       c   b
    will be a conflict.

        a
       / \
      b*  c*
       \ / \
        c*  d*
    This ("the other funky case") is handled by (2), and resolves cleanly.

    Tim
