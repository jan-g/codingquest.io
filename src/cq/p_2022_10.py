from os.path import dirname, join, basename
import sys
from PIL import Image


def main(fn):
    with open(fn + ".png", "rb") as f:
        img = Image.open(f)
        img.load()

    w, h = img.size
    x, y = (-1, 0)
    b = ""
    by = 0
    bits = 0
    while True:
        x += 1
        if x >= w:
            x = 0
            y += 1
            if y >= h:
                break
        (r, *_) = img.getpixel((x, y))
        by = by * 2 + (r & 1)
        bits += 1
        if bits == 8:
            if by == 0:
                break
            bits = 0
            b += chr(by)
            by = 0

    print(b)


if __name__ == '__main__':
    print(__file__)
    if len(sys.argv) < 2:
        fn = join(dirname(dirname(dirname(__file__))), "data", basename(__file__)[2:-3].replace("_", "-"))
    else:
        fn = sys.argv[1]
    main(fn)
