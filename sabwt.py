import numpy as np


class sabwt:
    def __init__(self, s):
        self.s = s
        self.transformed = []
        self.count_table = []
        self.alpha = {}

    def calc_suffix_array(self):
        return sorted(range(len(self.s)), key=lambda i: self.s[i:])

    def transform(self):
        sa = self.calc_suffix_array()
        last_index = list(
            map(lambda i: (i + len(self.s) - 1) % len(self.s), sa))
        self.transformed = np.array(list(self.s))[last_index]
        return self.transformed

    def count_alpha(self):
        for n in self.transformed:
            if n not in self.alpha:
                self.alpha[n] = 0
            self.count_table.append(self.alpha[n])
            self.alpha[n] += 1
        t = 0
        for k in sorted(self.alpha.keys()):
            tmp = self.alpha[k]
            self.alpha[k] = t
            t += tmp
        return self.count_table, self.alpha

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


if __name__ == "__main__":
    s = "mmiissiissiippii$"
    b = sabwt(s)
    print(b.transformed)
