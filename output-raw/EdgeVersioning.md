# Edge Versioning

BramCohen said:

  the basic idea is that if you have XY -> XAY and XY -> XBY and XAY, XBY -> XABY and XAY -> XCY and XCY, XBY -> XCY, then XABY, XCY -> X<AB=C>Y on the grounds that AB never appeared next to each other in the history of the other side

Or, to put it graphically:

attachment:edge-versioning.png

In this case, the user has indicated that C beats A and that C beats B, but never that C beats AB, so presenting the conflict "AB" vs. "C" makes more sense than silently picking C.

The motivating case for edge versioning is when there's a conflict between A and B which one user resolves as XABY and another resolves as XBAY. When their resolutions are merged together, SimpleWeaveMerge will arbitrarily pick either XABY or XBAY, without a conflict, depending on the weave ordering. With edge versioning, a conflict such as X<A=>BAY will be given, which while arguably not the best conflict to give in this situation is at least a conflict rather than an arbitrary erroneous clean merge.

The word "edge" in the name refers to a boundary between sections of text.  For example, if "ABC" and "DEF" are merged to create "ABCDEF", then something '''new''' has happened because "CD" was created.  "CD" is an ''edge'' between two regions of text which were not previously adjacent.  With edge versioning, "CD" would be versioned just as lines are in CodevilleMerge.

Another simpler case that illustrates this is ABC -> AC being merged with ABC -> AXC (i.e. deleting a line vs. editing the same line).  Without edge versioning the result would be a clean merge to AXC, as "B" was deleted on both sides.  With edge versioning the result would be  A<=X>C (i.e. a conflict between an empty region and the inserted "X").
