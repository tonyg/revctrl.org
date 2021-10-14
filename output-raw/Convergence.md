# Convergence

Convergence is the behavior where an identical change is made in two different branches, like this:

{{{
    a
   / \
  b   b
}}}

Version control systems are said to support convergence if they view both b's in the above example as being the same change. In practice this means that if one of the b's is modified and then the two are merged, the modification wins.

So the following example:

{{{
    a
   / \
  b   b
  |
  c
}}}

Should cleanly merge to c, assuming the standard interpretation of AccidentalCleanMerge.

Currently hardly any version control system properly supports convergence.

Convergence is sometimes referred to as 'implicit cherry-picking' because it allows cherry-picking to be done offline using diff and patch, and the system figures out what happened. This is in contrast to explicit cherry-picking, which requires the user give semantic input describing the cherry-pick to the system, which is the style supported by Darcs.

Properly supporting convergence leads to extraordinarily powerful support of cherry-picking. It allows cherry-picks to simply be done, possibly even via offline distribution of patches, and the system implicitly realizes what happened, even with a simple snapshot-based history.

There are some inherent limitations to what convergence can do. Specifically, in cases like the following:

{{{
  a
  |
  b
  |
  a
  |
  b
}}}

If a user does an offline cherry-pick from the first state to the last state and applies it elsewhere, then the system will have no idea that the intermediary states happened, and that branch will tend to lose or conflict in some cases which it should outright win.

One way to handle these limitations is to do cherry-picking within the version control system, and have cherry-picks of multiple sequential changes create revisions for all of the intervening values.

The following case involves some subtlety:

{{{
  a
  |\
  | \
  x  y
  |  |
  b  |
  |  |
  z  b
}}}

In this case, y appeared on the right but doesn't any longer, creating a 'phantom' conflict. The most compelling argument about whether to support phantom conflicts is that they cause StaircaseMerge to become a conflict, which indicates that they should be ignored.

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

In this case, if we assume setting to b to mean 'b defeats x' then we have a conflict, but if we assume it to mean 'b wins' then we have a convergent case and z wins. Using the 'b defeats x' definition is more complicated, and particularly difficult for line-based data where there is no one-to-one mapping between old lines and new lines. The general feeling seems to be that 'b wins' is a better approach.

Contrast the above with the following case, which is a clean merge regardless of whether a change means 'b defeats a' or 'b wins'. One could also interpret it to mean 'b defeats this exact history', which would result in this case being a conflict.


{{{
  a
  |\
  | \
  b  c
  |  |
  a  a
  |  |
  c  b
  |  |
  a  a
  |
  z
}}}

See the ImplicitUndo page for a discussion of interactions with convergence.
