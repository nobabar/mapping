import numpy as np


class bwt():
    def __init__(self, s):
        self.s = np.array(list(s), dtype=np.unicode_)
        self.matrix = self.calc_matrix()
        self.transformed = self.transform()
        self.count_table, self.alpha = self.count_alpha()

    def calc_matrix(self):
        s = np.append(self.s, '$')
        matrix = np.empty([len(s), len(s)], dtype=np.unicode_)
        for i in range(len(s)):
            matrix[i] = np.concatenate([s[i:len(s)], s[0:i]])
        return matrix[matrix[:, 0].argsort()]

    def transform(self):
        return self.matrix[:, -1]

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
            p = self.alpha[self.s[p]] + self.count_table[p]
        return s[1:]


if __name__ == "__main__":
    b = bwt("ACACGACGTTAT")
    print(b.transformed)
    print(b.alpha, b.count_table)
    print(b.inverse())
