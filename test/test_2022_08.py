from cq.p_2022_08 import *


def test_decode():
    key ="With great power comes great responsibility"
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.,;:?! '()"
    ct = "lfwwrsvbvMbmIEnK:wDjutpzoxfwowypDDHxB(rzfwKXBMd"
    d = dec(ct, chars, key)

    assert d == "I could use this to pass secret notes in class!"
