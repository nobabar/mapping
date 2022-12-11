import numpy as np


class bwt:
    """
    Burrows-Wheeler Transform

    Parameters
    ----------
    s : str
        string to transform

    Attributes
    ----------
    s : np.array
        string to transform
    transformed : np.array
        transformed string
    count_table : list
        count table
    alpha : dict
        alphabet

    Methods
    -------
    calc_matrix()
        calculate the matrix
    transform()
        transform the string
    count_alpha()
        count the alphabet
    generate_position()
        generate the position
    inverse()
        inverse the transform
    """

    def __init__(self, s):
        self.s = np.array(list(s), dtype=np.unicode_)
        self.transformed = []
        self.count_table = []
        self.alpha = {}

    def calc_matrix(self):
        """
        Calculate the BWT matrix

        Returns
        -------
        np.array
            BWT matrix
        """
        s = np.append(self.s, "$")
        matrix = np.empty([len(s), len(s)], dtype=np.unicode_)
        for i in range(len(s)):
            matrix[i] = np.concatenate([s[i: len(s)], s[0:i]])
        return matrix[matrix[:, 0].argsort()]

    def transform(self):
        """
        Extract the last column of the BWT matrix, which is the transformed string

        Returns
        -------
        np.array
            transformed string
        """
        self.transformed = self.calc_matrix()[:, -1]
        return self.transformed

    def count_alpha(self):
        """
        Index the string and count the number of occurrences

        Returns
        -------
        list
            count table
        dict
            alphabet
        """
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
        """
        Generate the position of the first character in the original sequence

        Returns
        -------
        list
            position in the original sequence
        """
        pos = []
        L = len(self.s)
        p = 0

        while len(pos) < len(self.s):
            pos[p] = L - 2
            p = self.alpha[self.s[p]] + self.count_table[p]
            L -= 1
        return pos

    def inverse(self):
        """
        Inverse the transform

        Returns
        -------
        str
            original string
        """
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
