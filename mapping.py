import time
import timeit
from random import choice

import matplotlib.pyplot as plt
import numpy as np
from memory_profiler import profile

# Burrow-Wheeler Transform


# @profile
def generate_bwt(original_seq):
    seq = original_seq + '$'
    matrix = []
    seq_final = list()
    # matrice permutation circulaire
    for i in range(len(seq)):
        matrix.append(seq[i:len(seq)] + seq[0:i])
    matrix.sort()
    # transformé Burrows Wheeler
    for seq in matrix:
        seq_final.append(seq[-1])
    return ("".join(seq_final))


def count_alpha(bwt_seq):
    count_table = []
    alpha = {}
    for n in bwt_seq:
        if n not in alpha:
            alpha[n] = 0
        count_table.append(alpha[n])
        alpha[n] += 1
    t = 0
    for k in sorted(alpha.keys()):
        tmp = alpha[k]
        alpha[k] = t
        t += tmp
    return count_table, alpha


def generate_position(s):
    count_table, alpha = count_alpha(s)
    pos = []
    L = len(s)
    p = 0
    while len(pos) < len(s):
        pos[p] = L - 2
        p = alpha[s[p]] + count_table[p]
        L -= 1
    return pos


# @profile
def gene_seq(bwt):
    (count, alpha) = count_alpha(bwt)
    p = 0
    seq = "$"
    x = 0
    while x != "$":
        x = bwt[p]
        seq = x + seq
        p = alpha[x] + count[p]
    return seq[1:]


# suffix array variant for Burrows-Wheeler Transform
# SEQUENCE = "^BANANA|"

# sorted_i_suffix_arrray = sorted(
#     range(len(SEQUENCE)), key=lambda i: SEQUENCE[i:])

# last_index = list(map(lambda i: (i + len(SEQUENCE) - 1) %
#                   len(SEQUENCE), sorted_i_suffix_arrray))

# last_column = np.array(list(SEQUENCE))[last_index]


# David A. Scott's bijective Burrows-Wheeler transform

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


# @profile
def bwts(s):
    rotations = lf_conjugates(s)
    sorted_rotations = sorted(rotations)
    return ''.join(map(lambda x: x[-1], sorted(sorted_rotations)))


# @profile
def ibwts(s):
    sorted_keys = [x[0] for x in sorted(enumerate(s), key=lambda p: p[1])]
    cycles = find_cycles(sorted_keys)
    return ''.join(map(lambda i: s[i], sum(cycles, [])))


def generate_seq(length):
    return ''.join(choice('ACGT') for _ in range(length))


if __name__ == "__main__":
    start_time = time.time()
    times_bwt = []
    for _ in range(100):
        gene_seq(generate_bwt(generate_seq(100000)))
        times_bwt.append(time.time() - start_time)
        start_time = time.time()

    times_bwt = list(map(lambda x: x * 1000, times_bwt))

    print(f"median: {np.median(times_bwt)} \t" +
          f"mean: {np.mean(times_bwt)} \t" +
          f"sd: {np.std(times_bwt)}")

    start_time = time.time()
    times_bwts = []
    for _ in range(100):
        ibwts(bwts(generate_seq(100000)))
        times_bwts.append(time.time() - start_time)
        start_time = time.time()

    times_bwts = list(map(lambda x: x * 1000, times_bwts))

    print(f"median: {np.median(times_bwts)} \t" +
          f"mean: {np.mean(times_bwts)} \t" +
          f"sd: {np.std(times_bwts)}")

    mean_mean = (np.mean(times_bwts) + np.mean(times_bwt)) / 2
    max_sd = max(np.std(times_bwts), np.std(times_bwt))
    myrange = [mean_mean - 4 * max_sd, mean_mean + 4 * max_sd]

    plt.hist(times_bwt, bins=100, range=myrange,
             alpha=0.5, label='bwt', edgecolor='black')
    plt.hist(times_bwts, bins=100, range=myrange,
             alpha=0.5, label='bwts', edgecolor='black')
    plt.legend(loc='upper right')

    plt.show()

    # gene_seq(generate_bwt(generate_seq(100000)))

    # ibwts(bwts(generate_seq(100000)))

    # time_res_bwt = timeit.timeit("gene_seq(generate_bwt(generate_seq(1000)))",
    #                              globals=globals(), number=100)

    # print(time_res_bwt)
    # print(
    #     f"median: {np.median(time_res_bwt)} \t mean: {np.mean(time_res_bwt)} \t sd: {np.std(time_res_bwt)}")
    # np.histogram(time_res_bwt, bins=100)

    # time_res_bwts = timeit.timeit("ibwts(bwts(generate_seq(1000)))",
    #                               globals=globals(), number=100)

    # print(time_res_bwts)
    # print(
    #     f"median: {np.median(time_res_bwts)} \t mean: {np.mean(time_res_bwts)} \t sd: {np.std(time_res_bwts)}")
    # np.histogram(time_res_bwt, bins=100)

    # bwts("banana")
    # bwts("abacabab")

    # ibwts(bwts("banana"))
    # ibwts(bwts("abacabab"))
