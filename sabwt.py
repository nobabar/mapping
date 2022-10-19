import numpy as np


class sabwt():
    def __init__(self, s):
        self.s = s
        self.sa = self.calc_suffix_array()
        self.transformed = self.transform()
        self.count_table, self.alpha = self.count_alpha()

    def calc_suffix_array(self):
        return sorted(range(len(self.s)), key=lambda i: self.s[i:])

    def transform(self):
        last_index = list(map(lambda i: (i + len(self.s) - 1) %
                          len(self.s), self.sa))
        return np.array(list(self.s))[last_index]

    def count_alpha(self):
        count_table = []
        alpha = {}
        for n in self.transformed:
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

    def generate_position(self):
        pos = []
        L = len(self.s)
        p = 0
        while len(pos) < len(self.s):
            pos[p] = L - 2
            p = self.alpha[self.s[p]] + self.count_table[p]
            L -= 1
        return pos

    def inverse(self):
        p = 0
        s = "$"
        x = 0
        while x != "$":
            x = self.transformed[p]
            s = x + s
            p = self.alpha[x] + self.count_table[p]
        return s[1:]
