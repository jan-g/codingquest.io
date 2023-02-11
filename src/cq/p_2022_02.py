from os.path import dirname, join, basename
import sys
from collections import Counter


def main(fn):
    win = set("12 48 30 95 15 55 97".split())
    with open(fn) as f:
        lines = [Counter(l.strip().split()) for l in f]

    won = 0
    for l in lines:
        match = sum(l[c] for c in win)
        won += {
            0: 0,
            1: 0,
            2: 0,
            3: 1,
            4: 10,
            5: 100,
            6: 1000,
            7: 0+1j
        }[match]
    print(won)


if __name__ == '__main__':
    print(__file__)
    if len(sys.argv) < 2:
        fn = join(dirname(dirname(dirname(__file__))), "data", basename(__file__)[2:-3].replace("_", "-"))
    else:
        fn = sys.argv[1]
    main(fn)
