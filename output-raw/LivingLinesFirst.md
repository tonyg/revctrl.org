# Living Lines First

LivingLinesFirst is a refinement of having ["Convergence"] in a ["Weave"]. It involves ignoring lines which aren't alive in ancestors (or aren't alive in the combination of ancestors, as per GenerationCounting) and then having a second pass which does include non-living lines and looks for matches of lines between matches which were found in the last pass.

For example, let's say we start with this:

```
         ACB
        /   \
    ACPQB   AXCB
```

and then add a new version like so:

```
         ACB
        /   \
    ACPQB   AXCB
             |
            APQXB
```

Now we wish to perform resolution on APQXB on the right. The weave looks like AXCPQB, so if we did a longest common substring against the weave the commonality would be APQB and a new X would be added to the weave, resulting in a weave of AXCPQXB. But with living lines first, we first match against the living lines, which are AXCB, for a common substring in the first pass of AXB, so the PQ is regarded as new and we have a weave of APQXCPQB.

If in contrast we add the same version in a different place we get a different answer:

```
         ACB
        /   \
    ACPQB   AXCB
       |
    APQXB
```

In this case the PQ is alive and the X isn't, so we have matching lines of APQB and a new weave of AXCPQXB.
