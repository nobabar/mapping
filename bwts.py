class bwts:
    """
    Scottification of the Burrows-Wheeler transform.

    Parameters
    ----------
    s : str
        string to transform

    Attributes
    ----------
    s : str
        string to transform
    transformed : str
        transformed string

    Methods
    -------
    lf_duval()
        calculate the Lyndon factorization using Duval's algorithm
    lf_conjugates()
        calculate the conjugates of the Lyndon factors
    transform()
        transform the string
    sorted_keys()
        sorted indices of the transformed string
    find_cycles()
        find the cycles of the sorted indices
    inverse()
        inverse the transform
    """

    def __init__(self, s):
        self.s = s
        self.transformed = ""

    def lf_duval(self):
        """
        Calculate the Lyndon factorization using Duval's algorithm

        Returns
        -------
        list
            Lyndon factorization
        """
        i = 0
        factors = []
        while i < len(self.s):
            j = i + 1
            k = i
            while j < len(self.s) and self.s[k] <= self.s[j]:
                if self.s[k] < self.s[j]:
                    k = i
                else:
                    k += 1
                j += 1
            while i <= k:
                factors.append(self.s[i : (i + j - k)])
                i += j - k
        return factors

    def lf_conjugates(self):
        """
        Calculate the conjugates of the Lyndon factors

        Returns
        -------
        list
            Lyndon factorization with conjugates
        """
        factors = self.lf_duval()
        ret = []
        for factor in factors:
            for idx in range(len(factor)):
                ret.append(factor[-idx:] + factor[:-idx])
        return ret

    def transform(self):
        """
        Transform the string

        Returns
        -------
        str
            transformed string
        """
        transformed = "".join(map(lambda x: x[-1], sorted(self.lf_conjugates())))
        self.transformed = transformed
        return transformed

    def sorted_keys(self):
        """
        Calculate the sorted indices of the transformed string

        Returns
        -------
        list
            sorted indices
        """
        transformed = self.transform()
        return [x for x in sorted(range(len(transformed)), key=transformed.__getitem__)]

    # def map(self):
    #     sorted_transformed = np.sort(self.transformed)
    #     start = np.searchsorted(
    #         sorted_transformed, self.transformed, side='left')
    #     cum_sum = cum_sum = np.cumsum(
    #         self.transformed == self.transformed.reshape(-1, 1), axis=1)
    #     count_occ = np.diagonal(cum_sum) - 1
    #     summed = start + count_occ
    #     sorter = summed.argsort()
    #     i = np.arange(len(self.transformed))
    #     return sorter[np.searchsorted(summed, i, sorter=sorter)]

    def find_cycles(self):
        """
        Find the cycles of the sorted indices

        Returns
        -------
        list
            cycles
        """
        sorted_keys = self.sorted_keys()
        visited = set()
        cycles = []
        for i in sorted_keys:
            if i in visited:
                continue
            path = [i]
            j = sorted_keys[i]
            while i != j:
                path.append(j)
                j = sorted_keys[j]
            else:
                cycles.append(path)
                visited |= set(path)
        return cycles[::-1]

    def inverse(self):
        """
        Inverse the transform using the cycles

        Returns
        -------
        str
            inverse transform
        """
        cycles = self.find_cycles()
        return "".join(map(lambda i: self.s[i], sum(cycles, [])))
