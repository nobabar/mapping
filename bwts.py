class bwts():
    def __init__(self, s):
        self.s = s
        self.transformed = ''.join(map(lambda x: x[-1],
                                       sorted(self.lf_conjugates())))
        self.sorted_keys = [x for x in sorted(range(len(self.transformed)),
                                              key=self.transformed.__getitem__)]

    def lf_duval(self):
        i = 0
        factors = []
        while (i < len(self.s)):
            j = i + 1
            k = i
            while j < len(self.s) and self.s[k] <= self.s[j]:
                if self.s[k] < self.s[j]:
                    k = i
                else:
                    k += 1
                j += 1
            while i <= k:
                factors.append(self.s[i:(i + j - k)])
                i += j - k
        return factors

    def lf_conjugates(self):
        factors = self.lf_duval()
        ret = []
        for factor in factors:
            for idx in range(len(factor)):
                ret.append(factor[-idx:] + factor[:-idx])
        return ret

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
        visited = set()
        cycles = []
        for i in self.sorted_keys:
            if i in visited:
                continue
            path = [i]
            j = self.sorted_keys[i]
            while i != j:
                path.append(j)
                j = self.sorted_keys[j]
            else:
                cycles.append(path)
                visited |= set(path)
        return cycles[::-1]

    def inverse(self):
        cycles = self.find_cycles()
        return ''.join(map(lambda i: self.s[i], sum(cycles, [])))
