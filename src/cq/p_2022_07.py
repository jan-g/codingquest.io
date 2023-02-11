from os.path import dirname, join, basename
import sys
from dataclasses import dataclass


@dataclass
class Rect:
    x0: int
    y0: int
    x1: int
    y1: int

    def __eq__(self, other):
        return self.x0 == other.x0 and self.x1 == other.x1 and self.y0 == other.y0 and self.y1 == other.y1

    def __hash__(self):
        return hash((self.x0, self.y0, self.x1, self.y1))

    @staticmethod
    def filter(rects):
        return {r for r in rects if r.x0 < r.x1 and r.y0 < r.y1}

    def area(self):
        return (self.x1 - self.x0) * (self.y1 - self.y0)

    def contains(self, other):
        return (
            self.x0 <= other.x0 <= other.x1 <= self.x1 and
            self.y0 <= other.y0 <= other.y1 <= self.y1
        )

    def __sub__(self, other):
        if other.x1 <= self.x0 or self.x1 <= other.x0:
            return Rect.filter({self})
        if other.y1 <= self.y0 or self.y1 <= other.y0:
            return Rect.filter({self})

        # Split the pieces out
        rs = {self}

        r2 = set()
        for r in rs:
            if r.x0 <= other.x0 < r.x1:
                r2.add(Rect(x0=r.x0, y0=r.y0, x1=other.x0, y1=r.y1))
                r2.add(Rect(x0=other.x0, y0=r.y0, x1=r.x1, y1=r.y1))
            else:
                r2.add(r)
        rs = r2

        r2 = set()
        for r in rs:
            if r.x0 <= other.x1 < r.x1:
                r2.add(Rect(x0=r.x0, y0=r.y0, x1=other.x1, y1=r.y1))
                r2.add(Rect(x0=other.x1, y0=r.y0, x1=r.x1, y1=r.y1))
            else:
                r2.add(r)
        rs = r2

        r2 = set()
        for r in rs:
            if r.y0 <= other.y0 < r.y1:
                r2.add(Rect(x0=r.x0, y0=r.y0, x1=r.x1, y1=other.y0))
                r2.add(Rect(x0=r.x0, y0=other.y0, x1=r.x1, y1=r.y1))
            else:
                r2.add(r)
        rs = r2

        r2 = set()
        for r in rs:
            if r.y0 <= other.y1 < r.y1:
                r2.add(Rect(x0=r.x0, y0=r.y0, x1=r.x1, y1=other.y1))
                r2.add(Rect(x0=r.x0, y0=other.y1, x1=r.x1, y1=r.y1))
            else:
                r2.add(r)
        rs = r2

        # Strip out anything inside other
        rs = {r for r in Rect.filter(rs)
              if not other.contains(r)}
        return rs


def main(fn):
    with open(fn) as f:
        lines = [parse_line(l) for l in f]
    rs = calc(lines)
    print(len(rs), sum(r.area() for r in rs))


def parse_line(l):
    return (int(c) for c in l.strip().split())


def calc(lines, w=20000, h=100000):
    rs = {Rect(x0=0, y0=0, x1=w, y1=h)}
    for (x, y, w, h) in lines:
        remove = Rect(x0=x, y0=y, x1=x+w, y1=y+h)
        rs = set.union(*(
            r - remove for r in rs
        ))

    return rs


def total(rs):
    return sum(r.area() for r in rs)


if __name__ == '__main__':
    print(__file__)
    if len(sys.argv) < 2:
        fn = join(dirname(dirname(dirname(__file__))), "data", basename(__file__)[2:-3].replace("_", "-"))
    else:
        fn = sys.argv[1]
    main(fn)
