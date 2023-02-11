from os.path import dirname, join, basename
import sys
from hashlib import sha256


def main(fn):
    with open(fn) as f:
        lines = [l.strip().split() for l in f]

    vars = {v: 0 for v in "ABCDEFGHIJKL"}
    vars["cond"] = False
    pc = 0

    def val(s):
        try:
            return int(s)
        except ValueError:
            return vars[s]

    while pc < len(lines):
        match (instr := lines[pc])[0]:
            case "ADD":
                vars[instr[1]] += val(instr[2])
                pc += 1
            case "MOD":
                vars[instr[1]] %= val(instr[2])
                pc += 1
            case "DIV":
                vars[instr[1]] //= val(instr[2])
                pc += 1
            case "MOV":
                vars[instr[1]] = val(instr[2])
                pc += 1
            case "JMP":
                pc += val(instr[1])
            case "JIF":
                if vars["cond"]:
                    pc += val(instr[1])
                else:
                    pc += 1
            case "CEQ":
                vars["cond"] = val(instr[1]) == val(instr[2])
                pc += 1
            case "CGE":
                vars["cond"] = val(instr[1]) >= val(instr[2])
                pc += 1
            case "OUT":
                print(val(instr[1]))
                pc += 1
            case "END":
                break
    else:
        print("ran off end of program")


if __name__ == '__main__':
    print(__file__)
    if len(sys.argv) < 2:
        fn = join(dirname(dirname(dirname(__file__))), "data", basename(__file__)[2:-3].replace("_", "-"))
    else:
        fn = sys.argv[1]
    main(fn)
