from os.path import dirname, join, basename
import sys
from cq.astar import astar


def main(fn):
    with open(fn) as f:
        lines = [l.strip() for l in f]

    (x0, y0) = lines[0].index(' '), 0
    (x1, y1) = lines[-1].index(' '), len(lines) - 1

    def neighbours(xy):
        (x, y) = xy
        s = {
            (x2, y2)
            for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1))
            if 0 <= (y2 := y + dy) < len(lines)
            and 0 <= (x2 := x + dx) < len(lines[y2])
            and lines[y2][x2] == ' '
        }
        return s

    def manh(xy1, xy2):
        (x1, y1) = xy1
        (x2, y2) = xy2
        return abs(x1 - x2) + abs(y1 - y2)

    ans = astar(
        start=[(x0, y0)],
        finished=lambda p: p[-1] == (x1, y1),
        summarise=lambda p: p[-1],
        next=lambda p: [p + [s] for s in neighbours(p[-1])],
        estimate=lambda p: manh((x1, y1), p[-1]),
    )

    print(len(ans))


if __name__ == '__main__':
    print(__file__)
    if len(sys.argv) < 2:
        fn = join(dirname(dirname(dirname(__file__))), "data", basename(__file__)[2:-3].replace("_", "-"))
    else:
        fn = sys.argv[1]
    main(fn)
