# Generation Counting

GenerationCounting is a the technique for supporting ["Convergence"] used by ConvergentScalarMerge and PreciseCodevilleMerge. It involves keeping a 'generation count' for every possible value. Generation counts start out at 0 for everything, then go to 1 when the thing appears, then 2 when it's deleted again, then 3 when it's re-added, etc. When two different versions are merged together, the higher number wins.

GenerationCounting clearly has the definitional property of ["Convergence"] that when one side of a merge has the other one as a subset of its history, then the superset wins. It also somewhat controversially clean merges in other cases, for example the following:

{{{
  a
  |\
  | \
  b  c
  |  |
  c  b
  |
  z
}}}

GenerationCounting will make z win cleanly in this case, as discussed on the ConvergentScalarMerge page.
  Do I understand GenerationCounting correctly in the following two cases:
{{{
  (Case II)
  a
  |\
  b c
  | |
  c b
  | |
  z c

  (Case III)
  a
  |\
  b c
  | |
  c b
  | |
  z c
    |
    b
}}}
   Do both case II and case III result in a conflict? If so, then regardless of the judgement as to whether the first example case should merge to z, GenerationCounting seems counterintuitive to me.  Both of these cases should be at least as likely or more likely to clean merge to z than the first example case. In case II, after all, both sides seem to have agreed that c beats b, i.e. converged on c, and then one side offers z as a further change on c.  In case III, the right hand side has simply dithered longer about which of b or c is better -- why does that make it harder to merge with z, which the left-hand side implicitly thinks is better than both b and c?  Generally speaking, in two long-sundered branches, why is it relevant how many times a branch has considered and dropped a value?  Perhaps it would make more sense to cap the count at 2, and return to 1 upon a further reappearance?  Then all three cases would cleanly merge to z. This would roughly say that a node's value wins over everything considered in its history, which seemed to be the consensus on the Convergence page. Thanks for any thoughts. -- GlenWhitney
