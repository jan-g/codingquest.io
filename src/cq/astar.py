import heapq
from functools import cmp_to_key
from .item import Pair

__all__ = ['AStarFailure', 'astar', 'const', 'fill', 'backtrack',
           'minimum_set', 'minimum_on', 'minimum_by', 'cmp', 'maximum_by',
           'arb_minimum_by', 'arb_maximum_by']


class AStarFailure(Exception):
    def __init__(self, *args, visited=None, inspected=None):
        super().__init__(*args)
        self.visited = visited
        self.inspected = inspected


def const(v):
    return lambda _: v


def astar(
        start,
        finished=const(False),
        cost=len,
        estimate=const(0),
        next=const(set()),
        summarise=lambda x: x,
):
    q = []
    visited = {}
    inspected = []

    heapq.heappush(q, (cost(start), start))

    while len(q) > 0:
        (c, item) = heapq.heappop(q)
        summary = summarise(item)
        if summary in visited:
            continue
        inspected.append(item)
        if finished(item):
            return item

        visited[summary] = c
        for step in next(item):
            heapq.heappush(q, (cost(step) + estimate(step), step))

    raise AStarFailure(visited=visited, inspected=inspected)


# Fill from a starting element, by increasing cost.
# Return a map of summary -> cost for all elements reached.
def fill(
        start,
        cost=len,
        next=const(set()),
        summarise=lambda x: x,
):
    q = []
    visited = {}

    heapq.heappush(q, Pair(cost(start), start))

    while len(q) > 0:
        c, item = heapq.heappop(q)
        summary = summarise(item)
        if summary in visited:
            continue
        visited[summary] = c

        for step in next(item):
            heapq.heappush(q, Pair(cost(step), step))

    return visited


def backtrack(
    starts=set(),
    next=const(set()),
    cost=const(0),
):
    visited = set()
    path = [set(starts)]

    while True:
        frontier = path[-1]
        visited = visited | frontier

        steps = {}
        for cell in frontier:
            current_cost = cost(cell)
            for step in next(cell):
                if step not in visited:
                    new_cost = cost(step)
                    if new_cost is not None and new_cost < current_cost:
                        if step not in steps or new_cost < steps[step]:
                            steps[step] = new_cost
        if len(steps) == 0:
            # No precursors
            return path[::-1]

        target = min(steps.values())
        frontier = set(c for c in steps if steps[c] == target)
        path.append(frontier)


def minimum_set(c):
    if len(c) == 0:
        return set()
    target = min(c.values())
    return {x for x in c if c[x] == target}


def minimum_on(cs, on=None):
    if on is None:
        on = lambda x: cs[x]
    return minimum_set({c: on(c) for c in cs})


def minimum_by(cs, by=lambda a, b: 0):
    if len(cs) == 0:
        return set()
    cs = sorted(cs, key=cmp_to_key(by))
    return {c for c in cs if by(cs[0], c) == 0}


def arb_minimum_by(cs, by=lambda a, b: 0):
    if len(cs) == 0:
        return None
    return sorted(cs, key=cmp_to_key(by))[0]


def maximum_by(cs, by=lambda a, b: 0):
    if len(cs) == 0:
        return set()
    cs = sorted(cs, key=cmp_to_key(by), reverse=True)
    return {c for c in cs if by(cs[0], c) == 0}


def arb_maximum_by(cs, by=lambda a, b: 0):
    if len(cs) == 0:
        return None
    return sorted(cs, key=cmp_to_key(by))[-1]


def cmp(a, b):
    return 0 if a == b else -1 if a < b else 1
