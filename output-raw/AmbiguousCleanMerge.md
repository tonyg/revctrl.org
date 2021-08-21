# Ambiguous Clean Merge

A case which causes considerable problems for many merge algorithms. Specificaly:

{{{
    a
   / \
  b   c
  |\ /|
  | X |
  |/ \|
  b   c
}}}

While everyone agrees that this case should be a conflict, it can be difficult to implement because b and c both beat each other. b wins because of the following path:

{{{
    a
     \
      c
     /
    /
   /
  b
}}}

While c wins because of the following path:

{{{
    a
   /
  b
   \
    \
     \
      c
}}}

See CrissCrossMerge for more discussion.
