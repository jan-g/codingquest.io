from os.path import dirname, join, basename
import sys
from math import sqrt
from itertools import cycle


class Board:
    def __init__(self):
        self.g = [[] for _ in range(7)]

    def __getitem__(self, item):
        (c, r) = item
        if 0 <= c < len(self.g):
            if 0 <= r < len(self.g[c]):
                return self.g[c][r]
        return None

    def play(self, p, col):
        self.g[col - 1].append(p)
        for c in range(7):
            for r in range(7):
                if (v := self[c,r]) is None:
                    continue
                for (dc, dr) in ((0, 1), (1, 0), (1, 1), (1, -1)):
                    for l in range(4):
                        if self[c + dc * l, r + dr * l] != v:
                            break
                    else:
                        return v


def main(fn):
    with open(fn) as f:
        lines = [l.strip() for l in f]

    wins = [0, 0, 0]
    for game in lines:
        b = Board()
        for p, col in zip(cycle([0, 1, 2]), game):
            if b.play(p, int(col)) is not None:
                wins[p] += 1
                break
    print(wins, wins[0] * wins[1] * wins[2])


if __name__ == '__main__':
    print(__file__)
    if len(sys.argv) < 2:
        fn = join(dirname(dirname(dirname(__file__))), "data", basename(__file__)[2:-3].replace("_", "-"))
    else:
        fn = sys.argv[1]
    main(fn)
