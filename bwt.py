import numpy as np


class bwt():
    def __init__(self, s):
        self.s = np.array(list(s), dtype=np.unicode_)
        self.transformed = []
        self.count_table = []
        self.alpha = {}

    def calc_matrix(self):
        s = np.append(self.s, '$')
        matrix = np.empty([len(s), len(s)], dtype=np.unicode_)
        for i in range(len(s)):
            matrix[i] = np.concatenate([s[i:len(s)], s[0:i]])
        return matrix[matrix[:, 0].argsort()]

    def transform(self):
        self.transformed = self.calc_matrix()[:, -1]
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
        if not self.transformed:
            self.transform()
        p = 0
        s = "$"
        x = 0
        while x != "$":
            x = self.transformed[p]
            s = x + s
            p = self.alpha[self.s[p]] + self.count_table[p]
        return s[1:]


if __name__ == "__main__":
    b = bwt("ACACGACGTTAT")
    b.transform()
    print(b.transformed)
    b.count_alpha()
    print(b.alpha, b.count_table)
    print(b.inverse())
