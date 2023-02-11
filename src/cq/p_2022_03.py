from os.path import dirname, join, basename
import sys
from math import sqrt


def main(fn):
    with open(fn) as f:
        lines = [tuple(int(i) for i in l.strip().split()) for l in f]

    d = 0
    for (x1, y1, z1), (x2, y2, z2) in zip(lines, lines[1:]):
        d += int(sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2))
    print(d)


if __name__ == '__main__':
    print(__file__)
    if len(sys.argv) < 2:
        fn = join(dirname(dirname(dirname(__file__))), "data", basename(__file__)[2:-3].replace("_", "-"))
    else:
        fn = sys.argv[1]
    main(fn)
