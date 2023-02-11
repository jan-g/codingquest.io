from cq.p_2022_07 import *


t = """
66 87 34 13
64 67 36 33
40 54 58 46
51 17 49 45
83 15 17 51
46 46 51 54
20 34 52 52
65 21 35 46
32 68 49 32
13 79 43 21
87 81 13 19
65 26 35 55
46 79 51 21
17 53 46 45
77 17 23 41
4 17 54 47
7 28 42 53
9 47 45 41
40 14 45 44
77 61 23 39
"""


def test_eg2():
    lines = [parse_line(l) for l in t.strip().splitlines(keepends=False)]
    rs = calc(lines, w=100, h=100)
    assert total(rs) == 2061
