from os.path import dirname, join, basename
import sys
from itertools import cycle


def main(fn):
    with open(fn) as f:
        lines = [l.strip() for l in f]

    print(dec(lines[0],
              "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.,;:?! '()",
              "Roads? Where We're Going, We Don't Need Roads."))


def dec(msg, chars, key):
    d = ""
    for c, k in zip(msg, cycle(key)):
        try:
            i = chars.index(k) + 1
        except ValueError:
            d += c
            continue
        try:
            j = chars.index(c)
        except ValueError:
            d += c
            continue
        j = ((j - i) % len(chars)) + 1
        d += chars[j - 1]
    return d


if __name__ == '__main__':
    print(__file__)
    if len(sys.argv) < 2:
        fn = join(dirname(dirname(dirname(__file__))), "data", basename(__file__)[2:-3].replace("_", "-"))
    else:
        fn = sys.argv[1]
    main(fn)
