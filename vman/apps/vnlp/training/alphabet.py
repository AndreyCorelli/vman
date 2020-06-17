import regex as re


class Alphabet:
    reg_word = re.compile(r'[a-z]+')
    prefix_max = 3
    prefix_min = 2
    suffix_max = 4
    suffix_min = 1
    root_min = 3


class EnAlphabet(Alphabet):
    pass
