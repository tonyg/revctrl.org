# Operational Transformation

Operational Transformation is a theory very similar to the Darcs Theory of Patches (see [DarcsMerge](DarcsMerge.md)).  It has been developed by the collaborative editing community.

In collaborative editing, much less emphasis is placed on conflict marking (they don't bother with it).  Conflicts occur at a much more fine-grained level than in revision control (e.g. keypresses) and at the place that both users are currently working in real time.  This means that each user should see the other making changes in the same area, and use a mechanism other than the editing system to coordinate.  Conflict resolution just has to ensure consistency, and can otherwise do pretty much anything, as long as it is automatic.

A document starts empty.  Each user then begins transforming it.  Those transformations are concurrently sent to other users.  However, with multiple machines, these messages might be received in different orders by different users.  Ressel et. al. (in Proceedings of the ACM Conference on Computer Supported Cooperative Work 1996) proved some properties that must apply so that when all messages are eventually received and processed, all copies of the document are identical.  From these two properties, you can show correctness (for their definition of correctness).

## Definitions

An _operation_ is a modification of a document.  e.g. the addition of a character at a particular position in the document because of a keypress.

A _transformation function_ is a function, `T`, that merges two parallel operations by serialising them.  This is similar to the `||`-merge operation in Darcs, or the exact [ThreeWayTextMergeImplementation](ThreeWayTextMergeImplementation.md).  `T(op1, op2)` returns an operation that is the 'same' as op1 but changed so that it can be applied after op2.

Composition is expressed as `.`: `op1 . op2` means to apply `op1`, and then apply `op2` to the result.  We also define `T(opx, opy . opz) = T(T(opx, opy), opz)`.  This says that to transform `opx` through a pair of operations, `opy.opz`, you first transform `opx` through `opy`, and then you transform the result of that through `opz`.

### example

A standard merge looks as below.  We have one initial context, `a`, and two changes, `op1` and `op2` that both apply to `a`.  Each of `op1` and `op2` can be passed through the transformation function `T` to get `op1' = T(op1, op2)` and `op2' = T(op2, op1)`.

```
      a
     / \
op1 /   \ op2
   /     \
  b       c
   \     /
op2'\   / op1'
     \ /
      d
```

## Requirements

TP1: For every two concurrent operations, `op1` and `op2`, defined on the same state, the transformation function `T` must satisfy:

```
op1 . T(op2, op1) == op2 . T(op1, op2)
```

In the above example, this is requirement that `op1 . op2' == op2 . op1'`.  `d` is consistent regardless of which way around the merge is performed.  This is what the above example shows.

TP2: For every three concurrent operations, `op1`, `op2` and `op3`, defined on the same state, the transformation function `T` must satisfy:

```
T(op3, op1 . T(op2, op1)) == T(op3, op2 . T(op1, op2))
```

or equivalently:

```
T(T(op3,op1),T(op2,op1)) == T(T(op3,op2),T(op1,op2))
```

### example

Start with the previous example where there are two parallel operations, `op1` and `op2`.  Property TP1 says that which op you choose to transform to serialise them doesn't matter.  This gives us the _abcd_ diamond of states which again appears below.  Property TP2 goes one step further and says that the way you serialise a third operation, `op3`, through the other two doesn't matter either.  We could transform `op3` through `op1` and then `op2'`, or we could transform `op3` through `op2` and then `op1'`.  The result should be the same.

```
op1' = T(op1, op2)
op2' = T(op2, op1)
op3'a = T(op3, op1)
op3'b = T(op3, op2)
op3''a = T(op3'a, op2')
op3''b = T(op3'b, op1')

                    a--------
                   / \       \
              op1 /   \ op2   \ op3
                 /     \       \
            ----b       c----   e
           /     \     /     \
    op3'a /  op2' \   / op1'  \ op3'b
         /         \ /         \
        g           d           h
                   / \
            op3''a | | op3''b
                   \ /
                    f
```

## Ressel's Transformation Functions

These are some proposed operators for collaborative editing, and a proposed transformation function.  I mention them here because they are similar to exact three-way-merge, and yet can be shown NOT to satisfy the above properties.

In this formalism, priorities are fixed attributes of the user than makes the change.  They are used to resolve conflicts (it allows both changes to be made in the order defined by the priorities).

There are two operations:

`Ins(p, c, pr)` inserts character `c` at position `p` with priority `pr`.  `Del(p, pr)` deletes the character at location `p` with priority `pr`.

And the definition of the transformation function is relatively straight forward:

```
T(Ins(p1, c1, u1), Ins(p2, c2, u2)) :-
   if (p1 < p2) or (p1 == p2 and u1 < u2) return Ins(p1, c1, u1)
   else return Ins(p1 + 1, c1, u1)

T(Ins(p1, c1, u1), Del(p2, u2)) :-
   if (p1 <= p2) return Ins(p1, c1, u1)
   else return Ins(p1 - 1, c1, u1)

T(Del(p1, u1), Ins(p2, c2, u2)) :-
   if (p1 < p2) return Del(p1, u1)
   else return Del(p1 + 1, u1)

T(Del(p1, u1), Del(p2, u2)) :-
   if (p1 < p2) return Del(p1, u1)
   else if (p1 > p2) return Del(p1 - 1, u1)
   else return Id()
```

The counter example of TP2 (from [http://hal.inria.fr/inria-00071213 Proving correctness of transformation functions in collaborative editing systems] by Oster et. al., but with typesetting errors corrected):

```

   Site 1              Site 2              Site 3

   "abc"               "abc"               "abc"

op1 = ins(3,x)     op2 = del(2)        op3 = ins(2,y)

  "abxc"               "ac"                "aybc"

                   op3' = ins(2,y)     op2' = del(3)

                       "ayc"               "ayc"

                   op1' = ins(2,x)     op1'' = ins(3,x)

                       "axyc"              "ayxc"

```

## Tombstone Transformation Functions

Having shown other systems incorrect, Oster et. al. then go on to describe the Tombstone Transformation Functions, or TTF.  In version control parlance, this is a weave (see [SimpleWeaveMerge](SimpleWeaveMerge.md)).  No characters are ever deleted, but rather they are marked invisible (these invisible characters are the 'tombstones').  Ordering ties are broken by user-ID.  They show that this system satisfies TP2 when many other systems do not.

## Strengths

Can provably merge correctly.

## Weaknesses

Does not mark conflicts at all.

## Used by

 * A good summary paper is available from INRIA: http://hal.inria.fr/inria-00071213
 * The [http://dev.libresource.org/home/doc/so6-user-manual so6 revision control system] (pronounced saucisse)

## Related

Operational Transformation theory is related to Darcs theory of patches.  Darcs is based on commuting patches:

```
op1.op2 <-> op2'.op1'
```

As described in [http://www.abridgegame.org/pipermail/darcs-users/2003/000221.html this thread], this effect can be achieved using the OT transformation operator as long as you can invert an operation.  We'll define `Inv(op)` to be another operation that has the opposite effect of `op`.  This means that `Inv(op).op` is the identity.  `Inv(op)` is both a left and a right inverse, so `op.Inv(op)` is also the identity.

We can then define the commuted op1 and op2, those being op1' and op2', as:

```
op2' = T(op2, Inv(op1))
op1' = T(op1, op2')
```

Rather than inverting operators, it is also possible to view this as having an inverse Transformation function, `T⁻¹`.  Imagine `opA` and `opB` are parallel ops that need to be merged; then we get `opB' = T(opB, opA)`.  And then `opB = T⁻¹(opB', opA)`.  The commutation of `op1` and `op2` then becomes:

```
op2' = T-1(op2, op1)
op1' = T(op1, op2')
```

[This paper](http://hal.inria.fr/inria-00109039/en/) describes partial `T⁻¹` functions for the tombstone transformation operators.

----

[CategoryMergeAlgorithm](CategoryMergeAlgorithm.md)
