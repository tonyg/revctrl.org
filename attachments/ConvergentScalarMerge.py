from sets import Set as set
from copy import copy

class Weave:
    def __init__(self):
        # {revid: [parent]}
        self.parents = {}
        # {revid: [(value, state)]}
        # states are integers
        # each value's state starts at 0, then goes to 1, 2, etc.
        # odd states are when the value is present, even are when it is not
        # the merge between two states is the greater of the two values
        self.newstates = {}

    def add_revision(self, revid, value, parents):
        assert revid not in self.parents
        for p in parents:
            assert p in self.parents
        self.parents[revid] = copy(parents)
        newvals = []
        vals = self._make_vals(revid)
        for oldvalue, state in vals.items():
            if oldvalue != value and (state & 1 == 1):
                newvals.append((oldvalue, state + 1))
        if vals.get(value, 0) & 1 != 1:
            newvals.append((value, vals.get(value, 0) + 1))
        if len(newvals) > 0:
            self.newstates[revid] = newvals

    def _parents(self, revid):
        unused = [revid]
        result = set()
        while unused:
            next = unused.pop()
            if next not in result:
                unused.extend(self.parents[next])
                result.add(next)
        return result

    def _make_vals(self, revid):
        # return {lineid: state} for the given revision
        v = {}
        for n in self._parents(revid):
            for p, q in self.newstates.get(n, []):
                v[p] = max(v.get(p, 0), q)
        return v

    def _winner(self, vals):
        for (value, state) in vals.items():
            if state & 1 == 1:
                # Niklaus Wirth can bite me
                return value, state
        assert False

    def retrieve_revision(self, revid):
        return self._winner(self._make_vals(revid))[0]

    def annotate(self, revid):
        # returns (value, [perpetrator])
        winpair = self._winner(self._make_vals(revid))
        perps = []
        for parent in self._parents(revid):
            for i in self.newstates.get(parent, []):
                if i == winpair:
                    perps.append(parent)
        return (winpair[0], perps)

    def merge(self, reva, revb):
        # returns either a single value or a conflicting pair of values
        va = self._make_vals(reva)
        vb = self._make_vals(revb)
        awinner, awinnerstate = self._winner(va)
        bwinner, bwinnerstate = self._winner(vb)
        if awinner == bwinner:
            return awinner
        awins = awinnerstate > vb.get(awinner, 0)
        bwins = bwinnerstate > va.get(bwinner, 0)
        if awins and not bwins:
            return awinner
        if bwins and not awins:
            return bwinner
        return (awinner, bwinner)

w = Weave()
w.add_revision(1, 'a', [])
assert w.retrieve_revision(1) == 'a'
assert w.annotate(1) == ('a', [1])
w.add_revision(2, 'b', [1])
assert w.annotate(2) == ('b', [2])
assert w.merge(1, 2) == 'b'
w.add_revision(3, 'a', [1])
assert w.annotate(3) == ('a', [1])
assert w.merge(1, 3) == 'a'
w.add_revision(4, 'c', [1])
assert w.merge(2, 4) == ('b', 'c')
assert w.merge(3, 4) == 'c'
w.add_revision(5, 'b', [1])
w.add_revision(6, 'b', [2, 5])
assert w.annotate(6) == ('b', [2, 5])
w.add_revision(7, 'd', [5])
assert w.annotate(7) == ('d', [7])
assert w.merge(2, 7) == 'd'
w.add_revision(8, 'b', [7])
assert w.annotate(8) == ('b', [8])
w.add_revision(9, 'b', [8, 2])
assert w.annotate(9) == ('b', [8])
