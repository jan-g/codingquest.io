from os.path import dirname, join, basename
import sys


def main(fn):
    with open(fn) as f:
        lines = [int(l.strip()) for l in f]

    sums = []
    s = 0
    for n in lines:
        s += n
        sums.append(s)
    diffs = [b - a for (a, b) in zip(sums, sums[60:])]
    avgs = [d / 60 for d in diffs]
    outsides = [a < 1500 or a > 1600 for a in avgs]
    print(sum(outsides))


if __name__ == '__main__':
    print(__file__)
    if len(sys.argv) < 2:
        fn = join(dirname(dirname(dirname(__file__))), "data", basename(__file__)[2:-3].replace("_", "-"))
    else:
        fn = sys.argv[1]
    main(fn)
