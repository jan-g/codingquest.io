from os.path import dirname, join, basename
import sys
from hashlib import sha256


def main(fn):
    with open(fn) as f:
        lines = [l.strip() for l in f]

    last_hash = "0" * 64
    ok = True
    for l in lines:
        d, m, ph, h = l.split("|")
        if ok:
            if ph != last_hash:
                print("problem with last hash")
                break
            new_hash = sha256(f"{d}|{m}|{last_hash}".encode()).hexdigest()
            if new_hash != h:
                print("bad hash", l, "should be", new_hash)
                ok = False
            else:
                last_hash = h
        if not ok:
            m = 0
            while True:
                new_hash = sha256(f"{d}|{m}|{last_hash}".encode()).hexdigest()
                if new_hash.startswith("000000"):
                    break
                m += 1
            print(f"{d}|{m}|{last_hash}|{new_hash}")
            last_hash = new_hash


if __name__ == '__main__':
    print(__file__)
    if len(sys.argv) < 2:
        fn = join(dirname(dirname(dirname(__file__))), "data", basename(__file__)[2:-3].replace("_", "-"))
    else:
        fn = sys.argv[1]
    main(fn)
