import numpy as np

SEQUENCE = "^BANANA|"

# suffix array solution

sorted_i_suffix_arrray = sorted(
    range(len(SEQUENCE)), key=lambda i: SEQUENCE[i:])

last_index = list(map(lambda i: (i + len(SEQUENCE) - 1) %
                  len(SEQUENCE), sorted_i_suffix_arrray))

last_column = np.array(list(SEQUENCE))[last_index]


# Bijective variant

# allisons.org/ll/AlgDS/Strings/Factors/
# wikiwand.com/en/Lyndon_word#Duval_algorithm
def lf_duval(s):
    i = 0
    factors = []
    while (i < len(s)):
        j = i + 1
        k = i
        while j < len(s) and s[k] <= s[j]:
            if s[k] < s[j]:
                k = i
            else:
                k += 1
            j += 1
        while i <= k:
            factors.append(s[i:(i + j - k)])
            i += j - k
    return factors


def lf_conjugates(s):
    factors = lf_duval(s)
    ret = []
    for factor in factors:
        for idx in range(len(factor)):
            ret.append(factor[-idx:] + factor[:-idx])
    return ret


# use infinite lexicographic order to sort the conjugates
def expend_words(w, l):
    while len(w) < l:
        w = w * 2
        if len(w) > l:
            w = w[0:l]
    return w


def find_cycles(p):
    visited = set()
    cycles = []
    for i in p:
        if i in visited:
            continue
        path = [i]
        j = p[i]
        while i != j:
            path.append(j)
            j = p[j]
        else:
            cycles.append(path)
            visited |= set(path)
    return cycles[::-1]


def bwts(s):
    rotations = lf_conjugates(s)
    sorted_rotations = sorted(rotations, key=lambda w: expend_words(w, len(s)))
    return ''.join(map(lambda x: x[-1], sorted(sorted_rotations)))


def ibwts(s):
    sorted_keys = [x[0] for x in sorted(enumerate(s), key=lambda p: p[1])]
    cycles = find_cycles(sorted_keys)
    print(cycles)
    return ''.join([''.join(map(lambda i: s[i], cycle)) for cycle in cycles])


output = bwts("banana")
output = bwts("abacabab")
