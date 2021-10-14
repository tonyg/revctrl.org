from sets import Set as set
from bisect import bisect

def unique_lcs(a, b):
    # set index[line in a] = position of line in a unless
    # unless a is a duplicate, in which case it's set to None
    index = {}
    for i in xrange(len(a)):
        line = a[i]
        if line in index:
            index[line] = None
        else:
            index[line]= i
    # make btoa[i] = position of line i in a, unless
    # that line doesn't occur exactly once in both, 
    # in which case it's set to None
    btoa = [None] * len(b)
    index2 = {}
    for pos, line in enumerate(b):
        next = index.get(line)
        if next is not None:
            if line in index2:
                # unset the previous mapping, which we now know to
                # be invalid because the line isn't unique
                btoa[index2[line]] = None
                del index[line]
            else:
                index2[line] = pos
                btoa[pos] = next
    # this is the Patience sorting algorithm
    # see http://en.wikipedia.org/wiki/Patience_sorting
    backpointers = [None] * len(b)
    stacks = []
    lasts = []
    k = 0
    for bpos, apos in enumerate(btoa):
        if apos is None:
            continue
        # as an optimization, check if the next line comes at the end,
        # because it usually does
        if stacks and stacks[-1] < apos:
            k = len(stacks)
        # as an optimization, check if the next line comes right after
        # the previous line, because usually it does
        elif stacks and stacks[k] < apos and (k == len(stacks) - 1 or stacks[k+1] > apos):
            k += 1
        else:
            k = bisect(stacks, apos)
        if k > 0:
            backpointers[bpos] = lasts[k-1]
        if k < len(stacks):
            stacks[k] = apos
            lasts[k] = bpos
        else:
            stacks.append(apos)
            lasts.append(bpos)
    if len(lasts) == 0:
        return []
    result = []
    k = lasts[-1]
    while k is not None:
        result.append((btoa[k], k))
        k = backpointers[k]
    result.reverse()
    return result

assert unique_lcs('', '') == []
assert unique_lcs('a', 'a') == [(0, 0)]
assert unique_lcs('a', 'b') == []
assert unique_lcs('ab', 'ab') == [(0, 0), (1, 1)]
assert unique_lcs('abcde', 'cdeab') == [(2, 0), (3, 1), (4, 2)]
assert unique_lcs('cdeab', 'abcde') == [(0, 2), (1, 3), (2, 4)]
assert unique_lcs('abXde', 'abYde') == [(0, 0), (1, 1), (3, 3), (4, 4)]
assert unique_lcs('acbac', 'abc') == [(2, 1)]

def recurse_matches(a, b, ahi, bhi, answer, maxrecursion):
    oldlen = len(answer)
    if maxrecursion < 0:
        # this will never happen normally, this check is to prevent DOS attacks
        return
    oldlength = len(answer)
    if len(answer) == 0:
        alo, blo = 0, 0
    else:
        alo, blo = answer[-1]
        alo += 1
        blo += 1
    if alo == ahi or blo == bhi:
        return
    for apos, bpos in unique_lcs(a[alo:ahi], b[blo:bhi]):
        # recurse between lines which are unique in each file and match
        apos += alo
        bpos += blo
        recurse_matches(a, b, apos, bpos, answer, maxrecursion - 1)
        answer.append((apos, bpos))
    if len(answer) > oldlength:
        # find matches between the last match and the end
        recurse_matches(a, b, ahi, bhi, answer, maxrecursion - 1)
    elif a[alo] == b[blo]:
        # find matching lines at the very beginning
        while alo < ahi and blo < bhi and a[alo] == b[blo]:
            answer.append((alo, blo))
            alo += 1
            blo += 1
        recurse_matches(a, b, ahi, bhi, answer, maxrecursion - 1)
    elif a[ahi - 1] == b[bhi - 1]:
        # find matching lines at the very end
        nahi = ahi - 1
        nbhi = bhi - 1
        while nahi > alo and nbhi > blo and a[nahi - 1] == b[nbhi - 1]:
            nahi -= 1
            nbhi -= 1
        recurse_matches(a, b, nahi, nbhi, answer, maxrecursion - 1)
        for i in xrange(ahi - nahi):
            answer.append((nahi + i, nbhi + i))

a1 = []
recurse_matches(['a', None, 'b', None, 'c'], ['a', 'a', 'b', 'c', 'c'], 5, 5, a1, 10)
assert a1 == [(0, 0), (2, 2), (4, 4)]
a2 = []
recurse_matches(['a', 'c', 'b', 'a', 'c'], ['a', 'b', 'c'], 5, 3, a2, 10)
assert  a2 == [(0, 0), (2, 1), (4, 2)]

class Weave:
    def __init__(self):
        # [(lineid, line)]
        self.weave = []
        # {revid: [parent]}
        self.parents = {}
        # {revid: [((lineid1, lineid2), state)]}
        # states are integers
        # each edge's state starts at 0, then goes to 1, 2, etc.
        # odd states are when both lines are present and no lines are
        # between them, even otherwise
        # edges at the beginning and end are denoted by (None, lineid) and
        # (lineid, None) respectively. If the file is empty then (None, None)
        # is used
        # the merge between two states is the greater of the two values
        self.newedgestates = {}

    def add_revision(self, revid, lines, parents):
        assert revid not in self.parents
        for p in parents:
            assert p in self.parents
        self.parents[revid] = [i for i in parents]

        # match against living lines
        living = self._lineids(self._make_vals(revid))
        mapping = []
        livinglines = []
        for (pos, (lineid, line)) in enumerate(self.weave):
            if lineid in living:
                mapping.append(pos)
                livinglines.append(line)
        matches2 = []
        recurse_matches(lines, livinglines, len(lines), len(livinglines), matches2, 10)

        # match against the whole weave
        matches = []
        lines2 = [line for (lineid, line) in self.weave]
        for p, q in matches2:
            recurse_matches(lines, lines2, p, mapping[q], matches, 10)
            matches.append((p, mapping[q]))
        recurse_matches(lines, lines2, len(lines), len(lines2), matches, 10)
    
        # build a new weave
        newweave = []
        revpos = -1
        weavepos = -1
        matches.append((len(lines), len(lines2)))
        currentlines = []
        for a, b in matches:
            if b > weavepos + 1:
                # add current weave lines to the new weave
                newweave.extend(self.weave[weavepos + 1:b])
            if a > revpos + 1:
                # add lines which have never appeared before to the weave
                for i in xrange(revpos + 1, a):
                    lineid = (revid, i)
                    currentlines.append(lineid)
                    newweave.append((lineid, lines[i]))
            if b != len(lines2):
                newweave.append(self.weave[b])
                currentlines.append(self.weave[b][0])
            revpos = a
            weavepos = b
        self.weave = newweave
        # calculate which lines had their states changed in this revision
        currentedges = set()
        if len(currentlines) > 0:
            for i in xrange(len(currentlines) - 1):
                currentedges.add((currentlines[i], currentlines[i+1]))
            currentedges.add((None, currentlines[0]))
            currentedges.add((currentlines[-1], None))
        else:
            currentedges.add((None, None))
        newedgevals = []
        vals = self._make_vals(revid)
        for edge in currentedges:
            if edge not in vals:
                newedgevals.append((edge, 1))
        for edge, state in vals.items():
            if (state & 1 == 1) != (edge in currentedges):
                newedgevals.append((edge, state + 1))
        if len(newedgevals) > 0:
            self.newedgestates[revid] = newedgevals

    def _make_vals(self, revid):
        # return {lineid: state} for the given revision
        unused = [revid]
        s = set()
        while unused:
            next = unused.pop()
            if next not in s:
                unused.extend(self.parents[next])
                s.add(next)
        v = {}
        for n in s:
            for p, q in self.newedgestates.get(n, []):
                v[p] = max(v.get(p, 0), q)
        return v

    def _lineids(self, vals):
        # return set of lineids of lines alive in output of _make_vals
        lineids = set()
        for (ida, idb), state in vals.items():
            if state & 1 == 1:
                if ida is not None:
                    lineids.add(ida)
                if idb is not None:
                    lineids.add(idb)
        return lineids

    def retrieve_revision(self, revid):
        # returns a list of strings
        ids = self._lineids(self._make_vals(revid))
        return [line for (lineid, line) in self.weave if lineid in ids]

    def merge(self, reva, revb):
        # returns [line]
        # non-conflict lines are strings, conflict sections are
        # ([linesa], [linesb])
        edgesa = self._make_vals(reva)
        alines = self._lineids(edgesa)
        edgesb = self._make_vals(revb)
        blines = self._lineids(edgesb)
        lastalineid = None
        lastblineid = None
        awins = False
        bwins = False
        apartial = []
        bpartial = []
        result = []
        for (lineid, line) in (self.weave + [(None, None)]):
            if lineid is None or lineid in alines:
                edge = (lastalineid, lineid)
                aval = edgesa.get(edge, 0)
                bval = edgesb.get(edge, 0)
                if aval > bval:
                    awins = True
                if bval > aval:
                    bwins = True
                lastalineid = lineid
            if lineid is None or lineid in blines:
                edge = (lastblineid, lineid)
                aval = edgesa.get(edge, 0)
                bval = edgesb.get(edge, 0)
                if aval > bval:
                    awins = True
                if bval > aval:
                    bwins = True
                lastblineid = lineid
            if lineid is None or (lineid in alines and lineid in blines):
                if awins and bwins:
                    result.append((apartial, bpartial))
                elif awins:
                    result.extend(apartial)
                elif bwins:
                    result.extend(bpartial)
                awins = False
                bwins = False
                apartial = []
                bpartial = []
                if line is not None:
                    result.append(line)
            else:
                if lineid in alines:
                    apartial.append(line)
                if lineid in blines:
                    bpartial.append(line)
        return result
w = Weave()
w.add_revision(1, ['a', 'b'], [])
assert w.retrieve_revision(1) == ['a', 'b']
w.add_revision(2, ['a', 'x', 'b'], [1])
assert w.retrieve_revision(2) == ['a', 'x', 'b']
w.add_revision(3, ['a', 'y', 'b'], [1])
assert w.retrieve_revision(3) == ['a', 'y', 'b']
assert w.merge(2, 3) == ['a', (['x'], ['y']), 'b']
w.add_revision(4, ['a', 'x', 'b'], [1])
w.add_revision(5, ['a', 'z', 'b'], [4])
assert w.merge(2, 5) == ['a', 'z', 'b']
w = Weave()
w.add_revision(1, ['b'], [])
assert w.retrieve_revision(1) == ['b']
w.add_revision(2, ['x', 'b'], [1])
assert w.retrieve_revision(2) == ['x', 'b']
w.add_revision(3, ['y', 'b'], [1])
assert w.retrieve_revision(3) == ['y', 'b']
assert w.merge(2, 3) == [(['x'], ['y']), 'b']
w.add_revision(4, ['x', 'b'], [1])
w.add_revision(5, ['z', 'b'], [4])
assert w.merge(2, 5) == ['z', 'b']
w = Weave()
w.add_revision(1, ['a'], [])
assert w.retrieve_revision(1) == ['a']
w.add_revision(2, ['a', 'x'], [1])
assert w.retrieve_revision(2) == ['a', 'x']
w.add_revision(3, ['a', 'y'], [1])
assert w.retrieve_revision(3) == ['a', 'y']
assert w.merge(2, 3) == ['a', (['x'], ['y'])]
w.add_revision(4, ['a', 'x'], [1])
w.add_revision(5, ['a', 'z'], [4])
assert w.merge(2, 5) == ['a', 'z']
w = Weave()
w.add_revision(1, [], [])
assert w.retrieve_revision(1) == []
w.add_revision(2, ['x'], [1])
assert w.retrieve_revision(2) == ['x']
w.add_revision(3, ['y'], [1])
assert w.retrieve_revision(3) == ['y']
assert w.merge(2, 3) == [(['x'], ['y'])]
w.add_revision(4, ['x'], [1])
w.add_revision(5, ['z'], [4])
assert w.merge(2, 5) == ['z']

w = Weave()
w.add_revision(1, ['a', 'b'], [])
w.add_revision(2, ['a', 'c', 'b'], [1])
w.add_revision(3, ['a', 'b'], [2])
w.add_revision(4, ['a', 'd', 'b'], [1])
assert w.merge(2, 4) == ['a', (['c'], ['d']), 'b']
assert w.merge(3, 4) == ['a', ([], ['d']), 'b']
w.add_revision(5, ['a', 'b'], [4])
assert w.merge(4, 5) == ['a', 'b']
w = Weave()
w.add_revision(1, ['b'], [])
w.add_revision(2, ['c', 'b'], [1])
w.add_revision(3, ['b'], [2])
w.add_revision(4, ['d', 'b'], [1])
assert w.merge(2, 4) == [(['c'], ['d']), 'b']
assert w.merge(3, 4) == [([], ['d']), 'b']
w.add_revision(5, ['b'], [4])
assert w.merge(4, 5) == ['b']
w = Weave()
w.add_revision(1, ['a'], [])
w.add_revision(2, ['a', 'c'], [1])
w.add_revision(3, ['a'], [2])
w.add_revision(4, ['a', 'd'], [1])
assert w.merge(2, 4) == ['a', (['c'], ['d'])]
assert w.merge(3, 4) == ['a', ([], ['d'])]
w.add_revision(5, ['a'], [4])
assert w.merge(4, 5) == ['a']
w = Weave()
w.add_revision(1, [], [])
w.add_revision(2, ['c'], [1])
w.add_revision(3, [], [2])
w.add_revision(4, ['d'], [1])
assert w.merge(2, 4) == [(['c'], ['d'])]
assert w.merge(3, 4) == [([], ['d'])]
w.add_revision(5, [], [4])
assert w.merge(4, 5) == []

w = Weave()
w.add_revision(1, ['a', 'b', 'c', 'd', 'e'], [])
w.add_revision(2, ['a', 'x', 'c', 'd', 'e'], [1])
w.add_revision(3, ['a', 'e'], [1])
w.add_revision(4, ['a', 'b', 'c', 'd', 'e'], [3])
assert w.merge(2, 4) == ['a', (['x'], ['b']), 'c', 'd', 'e']
w = Weave()
w.add_revision(1, ['b', 'c', 'd', 'e'], [])
w.add_revision(2, ['x', 'c', 'd', 'e'], [1])
w.add_revision(3, ['e'], [1])
w.add_revision(4, ['b', 'c', 'd', 'e'], [3])
assert w.merge(2, 4) == [(['x'], ['b']), 'c', 'd', 'e']
w = Weave()
w.add_revision(1, ['a', 'b', 'c', 'd'], [])
w.add_revision(2, ['a', 'x', 'c', 'd'], [1])
w.add_revision(3, ['a'], [1])
w.add_revision(4, ['a', 'b', 'c', 'd'], [3])
assert w.merge(2, 4) == ['a', (['x'], ['b']), 'c', 'd']
w = Weave()
w.add_revision(1, ['b', 'c', 'd'], [])
w.add_revision(2, ['x', 'c', 'd'], [1])
w.add_revision(3, [], [1])
w.add_revision(4, ['b', 'c', 'd'], [3])
assert w.merge(2, 4) == [(['x'], ['b']), 'c', 'd']

w = Weave()
w.add_revision(1, ['a', 'b'], [])
w.add_revision(2, ['a', 'c', 'b'], [1])
w.add_revision(3, ['a', 'd', 'b'], [1])
w.add_revision(4, ['a', 'c', 'd', 'b'], [2, 3])
w.add_revision(5, ['a', 'd', 'c', 'b'], [2, 3])
assert w.merge(4, 5) == ['a', (['c'], []), 'd', 'c', 'b']
w = Weave()
w.add_revision(1, ['b'], [])
w.add_revision(2, ['c', 'b'], [1])
w.add_revision(3, ['d', 'b'], [1])
w.add_revision(4, ['c', 'd', 'b'], [2, 3])
w.add_revision(5, ['d', 'c', 'b'], [2, 3])
assert w.merge(4, 5) == [(['c'], []), 'd', 'c', 'b']
w = Weave()
w.add_revision(1, ['a'], [])
w.add_revision(2, ['a', 'c'], [1])
w.add_revision(3, ['a', 'd'], [1])
w.add_revision(4, ['a', 'c', 'd'], [2, 3])
w.add_revision(5, ['a', 'd', 'c'], [2, 3])
assert w.merge(4, 5) == ['a', (['c'], []), 'd', 'c']
w = Weave()
w.add_revision(1, [], [])
w.add_revision(2, ['c'], [1])
w.add_revision(3, ['d'], [1])
w.add_revision(4, ['c', 'd'], [2, 3])
w.add_revision(5, ['d', 'c'], [2, 3])
assert w.merge(4, 5) == [(['c'], []), 'd', 'c']

w = Weave()
w.add_revision(1, ['a', 'b'], [])
w.add_revision(2, ['a', 'f', 'y', 'y', 'f', 'b'], [1])
w.add_revision(3, ['a', 'y', 'b'], [1])
w.add_revision(4, ['a', 'p', 'y', 'p', 'b'], [3])
w.add_revision(5, ['a', 'q', 'y', 'q', 'b'], [3])
assert w.merge(4, 5) == ['a', (['p'], ['q']), 'y', (['p'], ['q']), 'b']
w = Weave()
w.add_revision(1, [], [])
w.add_revision(2, ['f', 'y', 'y', 'f'], [1])
w.add_revision(3, ['y'], [1])
w.add_revision(4, ['p', 'y', 'p'], [3])
w.add_revision(5, ['q', 'y', 'q'], [3])
assert w.merge(4, 5) == [(['p'], ['q']), 'y', (['p'], ['q'])]
w = Weave()
w.add_revision(1, ['a'], [])
w.add_revision(2, ['a', 'f', 'y', 'y', 'f'], [1])
w.add_revision(3, ['a', 'y'], [1])
w.add_revision(4, ['a', 'p', 'y', 'p'], [3])
w.add_revision(5, ['a', 'q', 'y', 'q'], [3])
assert w.merge(4, 5) == ['a', (['p'], ['q']), 'y', (['p'], ['q'])]
w = Weave()
w.add_revision(1, ['a', 'b'], [])
w.add_revision(2, ['a', 'f', 'y', 'y', 'f', 'b'], [1])
w.add_revision(3, ['a', 'y', 'b'], [1])
w.add_revision(4, ['a', 'p', 'z', 'z', 'y', 'z', 'z', 'p', 'b'], [3])
w.add_revision(5, ['a', 'q', 'z', 'z', 'y', 'z', 'z', 'q', 'b'], [3])
assert w.merge(4, 5) == ['a', (['p'], ['q']), 'z', 'z', 'y', 'z', 'z', (['p'], ['q']), 'b']
w = Weave()
w.add_revision(1, ['a', 'b'], [])
w.add_revision(2, ['a', 'f', 'y', 'y', 'f', 'b'], [1])
w.add_revision(3, ['a', 'y', 'b'], [1])
w.add_revision(4, ['a', 'p', 'z', 'm', 'y', 'm', 'z', 'p', 'b'], [3])
w.add_revision(5, ['a', 'q', 'z', 'n', 'y', 'n', 'z', 'q', 'b'], [3])
assert w.merge(4, 5) == ['a', (['p'], ['q']), 'z', (['m'], ['n']), 'y', (['m'], ['n']), 'z', (['p'], ['q']), 'b']


